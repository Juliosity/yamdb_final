import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filter import TitleFilter
from .mixins import WorkingWithListViewSet
from .permissions import (
    AdminOnly, IsAdminOrReadOnly, IsModeratorAuthorOrReadOnly
)
from .serializers import (
    AdminSerializer, TokenSerializer, UserSerializer,
    SignUpSerializer, CategorySerializer,
    CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer,
    TitlePostSerializer
)
from reviews.models import Category, Genre, Title, User, Review


SIGNUP_ERROR = '{value} уже занят. Используйте другой {field}.'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    ordering = ['id']
    lookup_field = 'username'
    permission_classes = (AdminOnly,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
        detail=False
    )
    def get_your_info(self, request):
       # serializer = UserSerializer(instance=request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                instance=request.user,
                data=request.data,
                partial=True

            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        serializer = UserSerializer(instance=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserSignupViewSet(views.APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, created = User.objects.get_or_create(
                username=username, email=email
            )
        except IntegrityError:
            field = 'username' if User.objects.filter(username=username).exists() else 'email'
            return Response(
                SIGNUP_ERROR.format(value=serializer.validated_data.get(field), field=field),
                status=status.HTTP_400_BAD_REQUEST
            )
            # if User.objects.filter(username=username).exists():
            #     return Response(
            #         SIGNUP_ERROR.format(value=username, field='username'),
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            # return Response(
            #     SIGNUP_ERROR.format(value=email, field='email'),
            #     status=status.HTTP_400_BAD_REQUEST
            # ) # Лишнее дублирование в строках 72..75 и 76..79.
        user.confirmattion_code = uuid.uuid4()
        user.save()
        email_text = (
            f'''
            Добрый день, {user.username}!
            Спасибо что зарегистрировались в нашем приложении.
            Ваш код доступа - {user.confirmation_code}.
            '''
        )
        email = EmailMessage(
            to=[user.email],
            subject='Регистрация на YAMDB',
            body=email_text,
            from_email=settings.MAIN_EMAIL
        )
        email.send()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username'))
        if (
            user.confirmation_code
            == serializer.validated_data['confirmation_code']
        ):
            access_token = str(AccessToken.for_user(user))
            return Response(
                data={'token': access_token},
                status=status.HTTP_200_OK)
        return Response(
            data={'token': 'Не верный токен'},
            #А как код инвалидировать? Где он задаётся?
            status=status.HTTP_400_BAD_REQUEST
        )
# Дыра в безопасности!
# Так как сервер отвечает "мимо" при любом числе попыток, можно устроить перебор до угадывания.
# Да, сейчас угадать uuid() не реально. 
# Но! Этот контроллер не знает какая сложность у пин-кода.
# Есть вероятность, что сложность будет сокращена, например, чтобы пересылать не почтой, а СМСками (как от банков).
# Лучше сделать пин-код одноразовым.

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostSerializer


class GenreViewSet(WorkingWithListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(WorkingWithListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

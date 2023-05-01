# from django.contrib.auth.tokens import default_token_generator
# from django.shortcuts import get_object_or_404
# from api_yamdb.comments.models import Review, Comment
# from api_yamdb.reviews.models import Title
# from api_yamdb.comments.serializers import(
#     ReviewSerializer,
#     CommentSerializer,
#     )
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from api_yamb.api.permissions import IsAdminOrSuperUser, IsAuthorOrAdminOrReadOnly
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import AccessToken



# class ReviewViews(viewsets.ModelViewSet):
#     """"Работа с отзывами.
#         Получить, добавить,
#         отредактировать, удалить отзыв.
#     """
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = (IsAuthorOrAdminOrReadOnly,)

#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         return title.reviews.all()

#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         serializer.save(author=self.request.user, title=title)


# class CommentViewSet(viewsets.ModelViewSet):
#     """"Работа с отзывами к комментариям.
#         Получить, добавить,
#         отредактировать, удалить
#         комментарий к отзыву.
#     """
#     # queryset = Review.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (IsAuthorOrAdminOrReadOnly,)

#     def get_queryset(self):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id)
#         return review.comments.all()

#     def perform_create(self, serializer):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id)
#         serializer.save(author=self.request.user, review=review)

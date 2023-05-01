# from django.shortcuts import get_object_or_404
# from api_yamdb.comments.models import Comment, Review
# from api_yamdb.reviews.models import Title
# from rest_framework import serializers


# class ReviewSerializer(serializers.ModelSerializer):
#     """Сериализатор для работы с отзывами."""
#     author = SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         # unique=True,
#     )
#     title = SlugRelatedField(
#         slug_field='name',
#         read_only=True
#     )

#     def validate(self, data):
#         request = self.context.get('request')
#         author = request.user
#         title_id = self.context.get('view').kwargs.get('title_id')
#         title = get_object_or_404(Title, pk=title_id)
#         if request.method == 'POST':
#             review = Review.objects.filter(
#                 title=title,
#                 author=author,
#             )
#             if review.exists():
#                 raise 'Вы уже оставляли отзыв.'
#         return data

#     class Meta:
#         fields = ('id', 'text', 'author', 'score', 'pub_date')
#         model = Review


# class CommentSerializer(serializers.ModelSerializer):
#     author = SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         # unique=True,
#     )

#     class Meta:
#         fields = ('id', 'review', 'text', 'author', 'pub_date')
#         model = Comment

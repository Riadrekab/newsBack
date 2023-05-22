from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile, Category, Topic, Result,historyResult


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        return response


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'title', 'url', 'image', 'body', 'created_at']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = historyResult
        fields = ['id','input']


class ProfileSerializer(serializers.ModelSerializer):
    preferred_topics = TopicSerializer(many=True)
    savedResults = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_savedResults(self, obj):
        results = obj.result_set.all()
        serializer = ResultSerializer(results, many=True)
        return serializer.data

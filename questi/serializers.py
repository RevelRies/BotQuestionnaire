from rest_framework import serializers

class ThemeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=999)


class QuestionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=999)
    theme = serializers.CharField(max_length=999)


class AnswerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=999)
    question = serializers.CharField(max_length=999)
    correct = serializers.BooleanField()
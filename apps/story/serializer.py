from rest_framework import serializers
from apps.story.models import Story, StoryQuestion, QuestionOption, StorySurveyResponse, SurveyAnswer


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'text', 'order']


class StoryQuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = StoryQuestion
        fields = ['id', 'title', 'description', 'question_type', 'order', 'is_required', 'options']


class StoryQuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryQuestion
        fields = ['title', 'description', 'question_type', 'order', 'is_required']


class StoryDetailSerializer(serializers.ModelSerializer):
    questions = StoryQuestionSerializer(many=True, read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'title', 'description', 'image', 'link', 'product', 'product_title',
                  'is_active', 'start_date', 'end_date', 'questions']


class StoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title', 'image', 'is_active']


class StoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'description', 'image', 'link', 'product', 'is_active',
                  'start_date', 'end_date']


class SurveyAnswerSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question.title', read_only=True)
    selected_options_text = serializers.SerializerMethodField()

    class Meta:
        model = SurveyAnswer
        fields = ['id', 'question', 'question_title', 'selected_options',
                  'selected_options_text', 'text_answer']
        read_only_fields = ['question_title', 'selected_options_text']

    def get_selected_options_text(self, obj):
        return [option.text for option in obj.selected_options.all()]


class StorySurveyResponseSerializer(serializers.ModelSerializer):
    answers = SurveyAnswerSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    story_title = serializers.CharField(source='story.title', read_only=True)

    class Meta:
        model = StorySurveyResponse
        fields = ['id', 'story', 'story_title', 'user', 'is_completed', 'answers', 'created_at', 'updated_at']
        read_only_fields = ['user', 'is_completed', 'created_at', 'updated_at']


class StorySurveyResponseCreateSerializer(serializers.Serializer):
    """So'rovnomaga javoblar jo'natish"""
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField()
        ),
        help_text='[{"question_id": 1, "selected_option_ids": [1,2], "text_answer": ""}, ...]'
    )

    def create(self, validated_data):
        story = self.context['story']
        user = self.context['request'].user
        answers_data = validated_data['answers']

        # So'rovnoma javoblarini yaratish
        response_obj, created = StorySurveyResponse.objects.get_or_create(
            story=story,
            user=user
        )

        # Har bir savol uchun javob saqlash
        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            selected_option_ids = answer_data.get('selected_option_ids', [])
            text_answer = answer_data.get('text_answer', '')

            try:
                question = StoryQuestion.objects.get(id=question_id, story=story)
            except StoryQuestion.DoesNotExist:
                continue

            survey_answer, _ = SurveyAnswer.objects.get_or_create(
                response=response_obj,
                question=question
            )

            if selected_option_ids:
                options = QuestionOption.objects.filter(id__in=selected_option_ids, question=question)
                survey_answer.selected_options.set(options)

            if text_answer:
                survey_answer.text_answer = text_answer
                survey_answer.save()

        response_obj.is_completed = True
        response_obj.save()

        return response_obj

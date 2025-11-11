from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.story.models import Story, StoryQuestion, QuestionOption, StorySurveyResponse
from apps.story.serializer import (
    StoryListSerializer, StoryDetailSerializer, StoryCreateUpdateSerializer,
    StoryQuestionSerializer, StoryQuestionCreateUpdateSerializer,
    QuestionOptionSerializer, StorySurveyResponseSerializer,
    StorySurveyResponseCreateSerializer
)
from apps.story.permissions import IsAdminOrReadOnly, CanSubmitSurvey


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(is_active=True)
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return StoryListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StoryCreateUpdateSerializer
        return StoryDetailSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Story.objects.all()
        return Story.objects.filter(is_active=True)

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAdminUser])
    def questions(self, request, pk=None):
        """So'rovnoma savollarini boshqarish"""
        story = self.get_object()

        if request.method == 'POST':
            serializer = StoryQuestionCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(story=story)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            questions = story.questions.all()
            serializer = StoryQuestionSerializer(questions, many=True)
            return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def add_option(self, request, pk=None):
        """Savolga javob varianti qo'shish"""
        story = self.get_object()
        question_id = request.data.get('question_id')
        text = request.data.get('text')
        order = request.data.get('order', 1)

        try:
            question = StoryQuestion.objects.get(id=question_id, story=story)
        except StoryQuestion.DoesNotExist:
            return Response(
                {'error': 'Savol topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )

        option = QuestionOption.objects.create(
            question=question,
            text=text,
            order=order
        )
        return Response(
            QuestionOptionSerializer(option).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[CanSubmitSurvey])
    def submit_survey(self, request, pk=None):
        """So'rovnomani to'ldirib jo'natish"""
        story = self.get_object()
        serializer = StorySurveyResponseCreateSerializer(
            data=request.data,
            context={'story': story, 'request': request}
        )
        if serializer.is_valid():
            response_obj = serializer.save()
            response_serializer = StorySurveyResponseSerializer(response_obj)
            return Response(
                {
                    'message': "So'rovnoma saqlandi",
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def my_survey(self, request, pk=None):
        """O'z so'rovnoma javoblarini ko'rish"""
        story = self.get_object()
        try:
            response_obj = StorySurveyResponse.objects.get(story=story, user=request.user)
            serializer = StorySurveyResponseSerializer(response_obj)
            return Response(serializer.data)
        except StorySurveyResponse.DoesNotExist:
            return Response(
                {'message': "Siz bu so'rovnomani to'dirmagansiz"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def survey_responses(self, request, pk=None):
        """Barcha foydalanuvchilarning so'rovnoma javoblarini ko'rish (Admin)"""
        story = self.get_object()
        responses = StorySurveyResponse.objects.filter(story=story)
        serializer = StorySurveyResponseSerializer(responses, many=True)
        return Response(serializer.data)

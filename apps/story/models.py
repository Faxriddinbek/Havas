from django.db import models
from apps.user.model.users import User
from apps.product.models import Product
from apps.shared.models import BaseModel


class Story(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='stories/', verbose_name="Rasm")
    link = models.URLField(blank=True, verbose_name="Havolasi")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Mahsulot"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Boshlanish vaqti")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Tugash vaqti")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"


class StoryQuestion(models.Model):
    """Story ichidagi so'rovnoma savollar"""
    QUESTION_TYPE_CHOICES = [
        ('radio', 'Bitta javob tanlash (Radio)'),
        ('checkbox', 'Bir nechta javob tanlash (Checkbox)'),
        ('text', 'Matn kiritish'),
    ]

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255, verbose_name="Savol")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPE_CHOICES,
        default='radio',# agar modelyaratilayotganda foydalanuvhi shu fieldni tanlamsa avtomatik defoltni tanlab beradi
        verbose_name="Savol turi"# bu faqat admin panelda ko'rinadi
    )
    order = models.IntegerField(default=1, verbose_name="Tartib raqami")
    is_required = models.BooleanField(default=True, verbose_name="Majburiy")

    def __str__(self):
        return f"{self.story.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ('story', 'order')


class QuestionOption(models.Model):
    """So'rovnoma javob variantlari"""
    question = models.ForeignKey(StoryQuestion, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255, verbose_name="Javob varianti")
    order = models.IntegerField(default=1, verbose_name="Tartib raqami")

    def __str__(self):
        return f"{self.question.title} → {self.text}"

    class Meta:
        ordering = ['order']


class StorySurveyResponse(models.Model):
    """Foydalanuvchining so'rovnomaga javoblarini saqlash"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='survey_responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Foydalanuvchi')
    is_completed = models.BooleanField(default=False, verbose_name="To'ldirildi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.story.title}"

    class Meta:
        unique_together = ('story', 'user')
        verbose_name = "So'rovnoma javoblar"
        verbose_name_plural = "So'rovnoma javoblar"


class SurveyAnswer(models.Model):
    """Har bir savolga foydalanuvchining javobi"""
    response = models.ForeignKey(StorySurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(StoryQuestion, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(QuestionOption, blank=True, verbose_name="Tanlangan variantlar")
    text_answer = models.TextField(blank=True, verbose_name="Matn javob")

    def __str__(self):
        return f"{self.response.user.username} - {self.question.title}"
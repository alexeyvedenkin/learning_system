from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='courses/previews', blank=True, null=True)
    description = models.TextField(verbose_name='Содержание курса', blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    theme = models.ForeignKey(Course, related_name='lessons',
                              on_delete=models.SET_NULL,
                              verbose_name='Из курса', blank=True, null=True
                              )
    description = models.TextField(verbose_name='Содержание урока', blank=True, null=True)
    preview = models.ImageField(upload_to='lessons/previews', blank=True, null=True)
    video_file = models.FileField(upload_to='lessons/videos', blank=True, null=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

from datetime import timezone

from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(upload_to="courses/previews", blank=True, null=True)
    description = models.TextField(verbose_name="Содержание курса", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор курса")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена курса")
    last_update = models.DateTimeField(auto_now=True)  # Автоматически обновляем поле при изменении объекта

    def save(self, *args, **kwargs):
        if not self.last_update:  # Если это новый объект (last_update пустое)
            self.last_update = timezone.now()  # Устанавливаем текущее время
        super().save(*args, **kwargs)  # Вызываем метод родителя для сохранения

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название урока")
    theme = models.ForeignKey(
        Course, related_name="lessons", on_delete=models.PROTECT, verbose_name="Из курса", blank=True, null=True
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор урока")
    description = models.TextField(verbose_name="Содержание урока", blank=True, null=True)
    preview = models.ImageField(upload_to="lessons/previews", blank=True, null=True)
    video_file = models.FileField(upload_to="lessons/videos", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена урока")
    last_update = models.DateTimeField(auto_now=True)  # Автоматически обновляем поле при изменении объекта

    def save(self, *args, **kwargs):
        if not self.last_update:  # Если это новый объект (last_update пустое)
            self.last_update = timezone.now()  # Устанавливаем текущее время
        super().save(*args, **kwargs)  # Вызываем метод родителя для сохранения

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title

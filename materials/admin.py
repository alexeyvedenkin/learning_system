from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "preview", "description")
    list_filter = ("name",)
    search_fields = ("name", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "theme", "owner", "description", "preview", "video_file")
    search_fields = ("theme", "title")

    # def get_theme(self, obj):
    #     # Lesson.objects.get(id=obj.id).theme.name
    #     print(type(obj.theme[0].name))
    #     return Course.objects.filter(lessons__id=obj.id).name

    @admin.display(description='Курс', ordering='theme__name')
    def get_theme(self, obj):
        return obj.theme.name
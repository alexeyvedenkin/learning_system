from django.contrib import admin

from users.models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "phone", "city", "get_groups")
    list_filter = ("last_name",)
    search_fields = ("last_name",)

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = "Groups"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_date", "course", "lesson", "amount", "payment_method")
    list_filter = ("user", "payment_date", "course", "lesson", "amount", "payment_method")
    search_fields = ("payment_method",)
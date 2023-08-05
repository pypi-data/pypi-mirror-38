from django.contrib import admin
from .models import Machine, Operator


class OperatorInline(admin.TabularInline):
    model = Operator
    extra = 0


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('key',)
    inlines = [OperatorInline]

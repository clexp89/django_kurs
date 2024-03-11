from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Category, Event 


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "number_events"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "sub_title"]
    

    @admin.display(description="Anzahl Events")
    def number_events(self, obj: Category):
        return obj.events.count()
    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "is_active"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "sub_title"]
    list_filter = ["category"]
    actions = ["make_inactive", "make_active"]
    readonly_fields = ["created_at", "updated_at"]
    
    fieldsets = (
        ("Standard Info", {"fields": ("author", "name", "date", "category")}),
        ("Detail Info", {
                        "fields": (
                            "description", 
                            "min_group", 
                            "sub_title", 
                            "is_active", 
                            "created_at",
                            "updated_at")}),
    )

    def get_readonly_fields(self, request, obj):
        """Setze author auf readonly, wenn der Event schon angelegt wurde."""
        if obj and obj.pk:
            readonly = super().get_readonly_fields(request, obj)
            readonly.append("author")
            return readonly
        else:
            return []

    @admin.display(description="Setze Einträge aktiv")
    def make_active(self, request, queryset):
        """Setze alle aktivierten Events auf aktiv.
        
        queryset = die Menge aller markierten Einträge
        """
        queryset.update(is_active=True)

    @admin.display(description="Setze Einträge inaktiv")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
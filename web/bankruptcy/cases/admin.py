from django.contrib import admin
from .models import Case, DocketEntry, Document

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ["name", "recap_id", "date_filed", "jurisdiction", "chapter"]
    search_fields = ["name", "chapter", "jurisdiction", "recap_id"]

@admin.register(DocketEntry)
class DocketEntryAdmin(admin.ModelAdmin):
    list_display = ["recap_id", "case", "date_filed"]
    search_fields = ["recap_id", "description"]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["recap_id", "pacer_id", "doc_type", "is_available"]
    search_fields = ["description", "text"]

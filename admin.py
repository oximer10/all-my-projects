from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','content','author','pub_date','is_deleted')
    search_fields=('title',)
    list_filter=('pub_date',)
    list_editable=('is_deleted',)
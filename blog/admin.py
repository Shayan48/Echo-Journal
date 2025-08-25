from django.contrib import admin
from .models import Blog, Category

admin.site.register(Category)
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')

    actions = ['approve_blogs']

    def approve_blogs(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} blog(s) approved successfully.')
    approve_blogs.short_description = "Approve selected blogs"

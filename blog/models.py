from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blogs:category', args=[self.slug])


# BLOG MODEL
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True, unique=True)  # Add unique=True
    excerpt = models.TextField(max_length=300, blank=True, help_text="Optional short summary for list view")
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # Approval system
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="blogs")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if not self.excerpt:
            self.excerpt = " ".join(self.content.split()[:30]) + "..."

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:detail', args=[self.slug])

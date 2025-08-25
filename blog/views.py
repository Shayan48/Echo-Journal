from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Blog, Category
from .forms import BlogForm


# HOME PAGE
def homepage(request):
    latest_blogs = Blog.objects.select_related('category').order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'latest_blogs': latest_blogs,
        'categories': categories,
    })

# BLOG LIST VIEW (with category filter + search + pagination)
def blog_list(request, category_slug=None):
    categories = Category.objects.all()
    active_category = None
    blogs = Blog.objects.select_related('category', 'author').order_by('-created_at')

    # Category filter
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        blogs = blogs.filter(category=active_category)

    # Search filter
    query = request.GET.get('q')
    if query:
        blogs = blogs.filter(title__icontains=query)

    # Pagination
    paginator = Paginator(blogs, 6)  # 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogs/blog_list.html', {
        'categories': categories,
        'active_category': active_category,
        'page_obj': page_obj,
    })

# def blogs_by_category(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     posts = Blog.objects.filter(category=category)
#     return render(request, "blogs/blog_list.html", {
#         "categories": Category.objects.all(),
#         "active_category": category,
#         "page_obj": posts
#     })

# BLOG DETAIL VIEW
from django.shortcuts import render, get_object_or_404
from .models import Blog

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blogs/blog_details.html', {'post': blog})


# ADD BLOG VIEW (Only for logged-in users)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BlogForm

@login_required
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)  # Don't save yet
            blog.author = request.user      # Assign current logged-in user as author
            blog.save()                     # Now save
            return redirect('blogs:blog_list')
    else:
        form = BlogForm()
    return render(request, 'blogs/add_blog.html', {'form': form})



# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms

# Custom Signup Form
class SignupForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Split full name into first_name and last_name
            name_parts = full_name.strip().split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            # Authenticate and login user
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Account created and logged in successfully!")
                return redirect('blogs:blog_list')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



# STATIC PAGES
def aboutPage(request):
    return render(request, 'about.html')

def teamPage(request):
    return render(request, 'team.html')

def ContactPage(request):
    return render(request, 'contact.html')

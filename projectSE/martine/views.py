
# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse


def home(request):
    return render(request, 'home.html')

def about(request):
    # Redirect any click to the reclamation create page
    return redirect(reverse('reclamations:new'))

def packages(request):
    return render(request, 'feedback:new')


def packages_feedback(request):
    """
    A lightweight page accessible from /packages/feedback/ that links to the feedback form.
    """
    # If you want to auto-redirect to feedback/new, use:
    # return redirect(reverse('feedback:new'))
    # But here we render a small page with a CTA.
    return render(request, 'packages_feedback.html')


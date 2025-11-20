# feedback/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

def feedback_list(request):
    """
    If user is staff: show all feedbacks; otherwise show own feedbacks (or all public).
    """
    if request.user.is_authenticated and request.user.is_staff:
        feedbacks = Feedback.objects.select_related('user', 'offer').order_by('-date_soumission')
    else:
        feedbacks = Feedback.objects.filter(user=request.user).select_related('offer').order_by('-date_soumission') if request.user.is_authenticated else Feedback.objects.none()
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

def feedback_detail(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    # Simple permission: only staff or owner can view
    if not request.user.is_authenticated or (not request.user.is_staff and fb.user != request.user):
        messages.error(request, "You don't have permission to view that feedback.")
        return redirect('feedback:list')
    return render(request, 'feedback/feedback_detail.html', {'feedback': fb})

@login_required  # require login to submit (optional - remove decorator to allow anonymous)
def feedback_create(request, offer_id=None):
    """
    Show form (GET) and create Feedback (POST).
    If offer_id provided, pre-fill the offer.
    """
    initial = {}
    if offer_id:
        initial['offer'] = offer_id

    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user
            fb.save()
            messages.success(request, "Thank you — your feedback has been received.")
            return redirect('feedback:thanks')
    else:
        form = FeedbackForm(initial=initial)
    return render(request, 'feedback/feedback_form.html', {'form': form})

def feedback_thanks(request):
    return render(request, 'feedback/feedback_thanks.html')

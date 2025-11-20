# reclamations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Reclamation, ReclamationComment
from .forms import ReclamationForm, ReclamationCommentForm

@login_required
def reclamation_list(request):
    """
    Show the current user's reclamations.
    Admin/staff can see all reclamations (optional).
    """
    if request.user.is_staff or request.user.is_superuser:
        reclamations = Reclamation.objects.select_related('client', 'reservation').order_by('-date_creation')
    else:
        reclamations = Reclamation.objects.filter(client=request.user).select_related('reservation').order_by('-date_creation')

    return render(request, 'reclamations/reclamation_list.html', {'reclamations': reclamations})


@login_required
def reclamation_create(request):
    """
    Create a new reclamation. The 'client' is assigned automatically from request.user.
    The ReclamationForm will narrow the reservation choices to those belonging to the user.
    """
    if request.method == 'POST':
        form = ReclamationForm(request.POST, user=request.user)
        comment_form = ReclamationCommentForm(request.POST)  # optional immediate comment
        if form.is_valid():
            rec = form.save(commit=False)
            rec.client = request.user
            rec.save()
            # if user added a comment in the same form (optional), create it
            if comment_form.is_valid() and comment_form.cleaned_data.get('description'):
                cc = comment_form.save(commit=False)
                cc.reclamation = rec
                cc.user = request.user
                cc.save()

            messages.success(request, "Votre réclamation a été soumise.")
            return redirect('reclamations:list')
    else:
        form = ReclamationForm(user=request.user)
        comment_form = ReclamationCommentForm()

    # Also show recent reservations to help the user choose reservation if needed (form handles reservation queryset)
    return render(request, 'reclamations/reclamation_form.html', {'form': form, 'comment_form': comment_form})


@login_required
def reclamation_detail(request, pk):
    rec = get_object_or_404(Reclamation, pk=pk)
    # permission: only owner or staff can view
    if not (request.user.is_staff or rec.client == request.user):
        messages.error(request, "Vous n'avez pas la permission de voir cette réclamation.")
        return redirect('reclamations:list')

    comment_form = ReclamationCommentForm()
    return render(request, 'reclamations/reclamation_detail.html', {'reclamation': rec, 'comment_form': comment_form})


@login_required
def reclamation_add_comment(request, pk):
    rec = get_object_or_404(Reclamation, pk=pk)
    # Only allow comment if user is owner or staff
    if not (request.user.is_staff or rec.client == request.user):
        messages.error(request, "Permission refusée.")
        return redirect('reclamations:list')

    if request.method == 'POST':
        form = ReclamationCommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.reclamation = rec
            c.user = request.user
            c.save()
            messages.success(request, "Commentaire ajouté.")
        else:
            messages.error(request, "Erreur dans le commentaire.")

    return redirect('reclamations:detail', pk=pk)

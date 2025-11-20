# example view snippet
from django.shortcuts import redirect, get_object_or_404
from .models import Feedback
from offers.models import Offer

def submit_feedback(request):
    if request.method == 'POST':
        offer = None
        offer_id = request.POST.get('offer_id')
        if offer_id:
            offer = get_object_or_404(Offer, id=offer_id)

        fb = Feedback.objects.create(
            user = request.user if request.user.is_authenticated else None,
            offer = offer,
            note = request.POST.get('note') or None,
            description = request.POST.get('description', ''),
            attachement = request.FILES.get('attachement')
        )
        # redirect or render success
        return redirect('some_where')

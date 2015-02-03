from django.shortcuts import render

# Create your views here.

from .models import Transaction, Membership
from .signals import membership_dates_update

import random

def upgrade(request):
	if request.user.is_authenticated():
		trans = Transaction.objects.create_new(request.user,\
				 "aslkdfjasdf%s"%(random.randint(0,100)),\
				  25.00, "visa")
		if trans.success:
			membership_instance, created = Membership.objects.get_or_create(user=request.user)
			membership_dates_update.send(membership_instance, new_date_start=trans.timestamp)
	return render(request, "billing/upgrade.html", {})



def billing_history(request):
	history = Transaction.objects.filter(user=request.user).filter(success=True)
	return render(request, "billing/history.html", {"queryset": history})
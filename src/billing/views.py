from django.shortcuts import render

# Create your views here.

from .models import  Membership, Transaction, UserMerchantId
from .signals import membership_dates_update

import random

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="3j27nwdw8mbvk68y",
                                  public_key="nj79pbd2hs4fvg8y",
                                  private_key="ed237abab42d8d181a6b735c9f155782")


PLAN_ID = "monthly_plan"

def billing_history(request):
	history = Transaction.objects.filter(user=request.user).filter(success=True)
	return render(request, "billing/history.html", {"queryset": history})


def upgrade(request):
	if request.user.is_authenticated():
		try:
			#something to get the current customer id stored somewhere 
			merchant_customer_id = UserMerchantId.objects.get(user=request.user).customer_id
		except UserMerchantId.DoesNotExist:
			new_customer_result = braintree.Customer.create({})
			if new_customer_result.is_success:
				merchant_customer_id = UserMerchantId.objects.create(user=request.user)
				merchant_customer_id.customer_id = new_customer_result.customer.id
				merchant_customer_id.save()
				print """Customer created with id = {0}""".format(new_customer_result.customer.id)
			else:
				print "Error: {0}".format(new_customer_result.message)
				#redirect somewhere??
		except:
			#some error occured
			#redirect somewhere
			pass

		trans = Transaction.objects.create_new(request.user,\
				 "aslkdfjasdf%s"%(random.randint(0,100)),\
				  25.00, "visa")
		if trans.success:
			membership_instance, created = Membership.objects.get_or_create(user=request.user)
			membership_dates_update.send(membership_instance, new_date_start=trans.timestamp)
	return render(request, "billing/upgrade.html", {})




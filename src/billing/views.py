from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.

from .models import  Membership, Transaction, UserMerchantId
from .signals import membership_dates_update

import random

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="3j27nwdw8mbvk68y",
                                  public_key="64zrsxstnhykn4v2",
                                  private_key="5507587264ea632357cad014f69ed78f")


PLAN_ID = "monthly_plan"

def billing_history(request):
	history = Transaction.objects.filter(user=request.user).filter(success=True)
	return render(request, "billing/history.html", {"queryset": history})


def upgrade(request):
	client_token = braintree.ClientToken.generate()
	if request.user.is_authenticated():
		try:
			#something to get the current customer id stored somewhere 
			merchant_obj = UserMerchantId.objects.get(user=request.user)
		except UserMerchantId.DoesNotExist:
			new_customer_result = braintree.Customer.create({})
			if new_customer_result.is_success:
				merchant_obj, created = UserMerchantId.objects.get_or_create(user=request.user)
				merchant_obj.customer_id = new_customer_result.customer.id
				merchant_obj.save()
				print """Customer created with id = {0}""".format(new_customer_result.customer.id)
			else:
				print "Error: {0}".format(new_customer_result.message)
				messages.error(request, "There was an error with your account. Please contact us.")
				return redirect("contact_us")
		except:
			messages.error(request, "There was an error with the server. Please try agin or contact us if the problem persists.")
			return redirect("contact_us")

		merchant_customer_id = merchant_obj.customer_id
		if request.method == "POST":
			nonce = request.POST.get("payment_method_nonce", None)
			if nonce is not None:
				payment_method_result = braintree.PaymentMethod.create({
						"customer_id": merchant_customer_id,
						"payment_method_nonce": nonce,
						"options": {
							"make_default": True
						}
					})
				if not payment_method_result.is_success:
					messages.error(request, "An error occured: %s" %(payment_method_result.message))
					return redirect("upgrade")
				the_token = payment_method_result.payment_method.token
				subscription_result = braintree.Subscription.create({
					"payment_method_token": the_token,
					"plan_id": PLAN_ID
				})
				if subscription_result.is_success:
					payment_type = subscription_result.subscription.transactions[0].payment_instrument_type
					trans_id = subscription_result.subscription.transactions[0].id
					sub_id = subscription_result.subscription.id
					sub_amount = subscription_result.subscription.price
					if payment_type == braintree.PaymentInstrumentType.PayPalAccount:
						trans = Transaction.objects.create_new(request.user, trans_id, sub_amount, "PayPal")
						trans_success = trans.success
					elif payment_type ==braintree.PaymentInstrumentType.CreditCard:
						credit_card_details = subscription_result.subscription.transactions[0].credit_card_details
						card_type = credit_card_details.card_type
						last_4 = credit_card_details.last_4
						trans = Transaction.objects.create_new(request.user,trans_id, sub_amount, card_type, last_four=last_4)
						trans_success = trans.success
					else:
						trans_success = False

					if trans_success:
						membership_instance, created = Membership.objects.get_or_create(user=request.user)
						membership_dates_update.send(membership_instance, new_date_start=trans.timestamp)
						messages.success(request, "Welcome to Srvup. Your membership has been activated.")
						return redirect("billing_history")

					else:
						messages.error(request, "There was an error with your transaction, please contact us.")
						return redirect("contact_us")
				else:
					messages.error(request, "An error occured: %s" %(subscription_result.message))
					return redirect("upgrade")
			
	context =  {"client_token":client_token}

	return render(request, "billing/upgrade.html",context)




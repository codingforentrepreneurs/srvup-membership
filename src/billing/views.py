from django.shortcuts import render

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
				#redirect somewhere??
		except:
			#some error occured
			#redirect somewhere
			pass

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
					if payment_type == "paypal_acccount":
						trans = Transaction.objects.create_new(request.user,trans_id, sub_amount, "PayPal")
						trans_success = trans.success
					elif payment_type == "credit_card":
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
				else:
					print subscription.message

				# customer_update_result = braintree.Customer.update(merchant_customer_id, {
				# 	"payment_method_nonce": nonce
				# 	})

				# credit_card_token = customer_update_result.customer.credit_cards[0].token
				# subscription_result = braintree.Subscription.create({
				# 		"payment_method_token": credit_card_token,
				# 		"plan_id": PLAN_ID
				# 	})
				# if subscription_result.is_success:
				# 	trans_id = subscription_result.subscription.id
				# 	trans = Transaction.objects.create_new(request.user,trans_id,25.00, "visa")
				# 	if trans.success:
				# 		membership_instance, created = Membership.objects.get_or_create(user=request.user)
				# 		membership_dates_update.send(membership_instance, new_date_start=trans.timestamp)
				# else:
				# 	print "failed"
					
				# customer_card = braintree.Customer.find(merchant_customer_id).credit_cards[0].token

			
	context =  {"client_token":client_token}

	return render(request, "billing/upgrade.html",context)




from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)




from billing.models import Membership, UserMerchantId
from notifications.signals import notify

class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
        	raise ValueError('Must include username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
        	username = username,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password):
        """
        Creates and saves a superuser with the given username, email and password.
        """

        user = self.create_user(
			username=username,
			email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
	username = models.CharField(
	    max_length=255,
	    unique=True,
	)
	email = models.EmailField(
	    verbose_name='email address',
	    max_length=255,
	    unique=True,
	)
	first_name = models.CharField(
			max_length=120,
			null=True,
			blank=True,
			)
	last_name = models.CharField(
			max_length=120,
			null=True,
			blank=True,
			)
	is_member = models.BooleanField(default=False, 
					verbose_name='Is Paid Member')
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_full_name(self):
	    # The user is identified by their email address
	    return "%s %s" %(self.first_name, self.last_name)

	def get_short_name(self):
	    # The user is identified by their email address
	    return self.first_name

	def __unicode__(self):
	    return self.username

	def has_perm(self, perm, obj=None):
	    "Does the user have a specific permission?"
	    # Simplest possible answer: Yes, always
	    return True

	def has_module_perms(self, app_label):
	    "Does the user have permissions to view the app `app_label`?"
	    # Simplest possible answer: Yes, always
	    return True

	@property
	def is_staff(self):
	    "Is the user a member of staff?"
	    # Simplest possible answer: All admins are staff
	    return self.is_admin





def user_logged_in_signal(sender, signal, request, user, **kwargs):
	request.session.set_expiry(60000)
	membership_obj, created = Membership.objects.get_or_create(user=user)
	if created:
		membership_obj.date_start = timezone.now()
		membership_obj.save()
		user.is_member = True
		user.save()
	user.membership.update_status()


user_logged_in.connect(user_logged_in_signal)




class UserProfile(models.Model):
	user = models.OneToOneField(MyUser)
	bio = models.TextField(null=True, blank=True)
	facebook_link = models.CharField(max_length=320, 
		null=True, 
		blank=True, 
		verbose_name='Facebook profile url')
	twitter_handle = models.CharField(max_length=320, 
		null=True, 
		blank=True, 
		verbose_name='Twitter handle')		


	def __unicode__(self):
		return self.user.username



def new_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
		new_profile, is_created = UserProfile.objects.get_or_create(user=instance)
		#print new_profile, is_created
		notify.send(instance, 
					recipient=MyUser.objects.get(username='jmitchel3'), #admin user
					verb='New user created.')
		# merchant account customer id -- stripe vs braintree
	try:
		merchant_obj = UserMerchantId.objects.get(user=instance)
	except:
		new_customer_result = braintree.Customer.create({
				"email": instance.email
			})
		if new_customer_result.is_success:
			merchant_obj, created = UserMerchantId.objects.get_or_create(user=instance)
			merchant_obj.customer_id = new_customer_result.customer.id
			merchant_obj.save()
			print """Customer created with id = {0}""".format(new_customer_result.customer.id)
		else:
			print "Error: {0}".format(new_customer_result.message)
			messages.error(request, "There was an error with your account. Please contact us.")

		
		# send email for verifying user email

post_save.connect(new_user_receiver, sender=MyUser)



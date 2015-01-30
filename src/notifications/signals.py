from django.dispatch import Signal


notify = Signal(providing_args=['recipient', 'verb', 'action', 'target', 'affected_users'])


"""

sender_content_type = models.ForeignKey(ContentType, related_name='nofity_sender')
sender_object_id = models.PositiveIntegerField()
sender_object = GenericForeignKey("sender_content_type", "sender_object_id")

verb = models.CharField(max_length=255)

action_content_type = models.ForeignKey(ContentType, related_name='notify_action', 
	null=True, blank=True)
action_object_id = models.PositiveIntegerField()
action_object = GenericForeignKey("action_content_type", "action_object_id")

target_content_type = models.ForeignKey(ContentType, related_name='notify_target', 
	null=True, blank=True)
target_object_id = models.PositiveIntegerField()
target_object = GenericForeignKey("target_content_type", "target_object_id")

recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')

#read
#unread
timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
"""


def get_vid_for_direction(instance, direction):
	''' get next video instance based on direction and current video instance'''
	category = instance.category
	video_qs = category.video_set.all()
	if direction == "next":
		new_qs = video_qs.filter(order__gt=instance.order)
	else:
		new_qs = video_qs.filter(order__lt=instance.order).reverse()
	next_vid = None
	if len(new_qs) >= 1:
		try:
			next_vid = new_qs[0]
		except IndexError:
			next_vid = None
	return next_vid

	
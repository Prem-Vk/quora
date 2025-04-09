from django.db.models.signals import post_save
from django.dispatch import receiver
from webapp.models import UserPreference, Answer
from django.db import transaction


@receiver(post_save, sender=UserPreference)
def update_preference_count(sender, instance: UserPreference, created, **kwargs):
    user_preference = UserPreference.objects.filter(answer=instance.answer)
    updated_fields = ['updated_at']
    if created:
        print("skjdcbkjshckjsh")
        with transaction.atomic():
            answer = Answer.objects.select_for_update().get(pk=instance.answer_id)
            if instance.like:
                answer.like_count += 1
                updated_fields.append("like_count")
            elif instance.dislike:
                answer.dislike_count += 1
                updated_fields.append("dislike_count")
            answer.save(update_fields=updated_fields)
    else:
        print("Yaha tak aaya")
        with transaction.atomic():
            answer = Answer.objects.select_for_update().get(pk=instance.answer_id)
            answer.like_count = user_preference.filter(like=True).count()
            answer.dislike_count = user_preference.filter(dislike=True).count()
            updated_fields += ["like_count", "dislike_count"]
            answer.save(update_fields=updated_fields)

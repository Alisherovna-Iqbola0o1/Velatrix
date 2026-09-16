from django.utils import timezone

from .models import DailyProgress, XPTransaction


def get_or_create_today_progress(user):
    today = timezone.now().date()
    progress, _ = DailyProgress.objects.get_or_create(user=user, date=today)
    return progress


def award_xp(user, amount, reason="", related_lesson=None, related_test=None):
    # 1. Tranzaksiyani bazaga yozamiz
    XPTransaction.objects.create(
        user=user,
        amount=amount,
        reason=reason,
        related_lesson=related_lesson,
        related_test=related_test,
    )

    # 2. User modelida xp maydoni bo'lsa, uni yangilaymiz
    if hasattr(user, "xp"):
        user.xp = (user.xp or 0) + amount
        user.save(update_fields=["xp"])

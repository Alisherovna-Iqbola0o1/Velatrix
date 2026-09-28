from .utils import award_xp, get_or_create_today_progress

from django.core import signing
from django.utils import timezone

from courses.models import Question
from .models import (
    ExtremalTestAttempt,
    LessonAttempt,
    LessonProgress,
    QuestionAttempt,
)


def start_lesson_attempt(user, lesson):
    progress, _ = LessonProgress.objects.get_or_create(
        user=user, lesson=lesson, defaults={"status": "unlocked"}
    )
    progress.status = "in_progress"
    if not progress.unlocked_at:
        progress.unlocked_at = timezone.now()
    progress.save(update_fields=["status", "unlocked_at"])

    attempt_count = LessonAttempt.objects.filter(user=user, lesson=lesson).count()
    return LessonAttempt.objects.create(
        user=user,
        lesson=lesson,
        attempt_number=attempt_count + 1,
        result="in_progress",
    )


def submit_answer(user, attempt, question, given_answer):
    is_correct = _check_answer(question, given_answer)

    QuestionAttempt.objects.create(
        lesson_attempt=attempt,
        question=question,
        given_answer=given_answer,
        is_correct=is_correct,
    )

    progress = LessonProgress.objects.get(user=user, lesson=attempt.lesson)

    if not is_correct:
        progress.current_wrong_streak += 1
        progress.save(update_fields=["current_wrong_streak"])
        return {"is_correct": False, "needs_help": progress.current_wrong_streak >= 3}

    progress.current_wrong_streak = 0
    progress.save(update_fields=["current_wrong_streak"])

    total_questions = attempt.lesson.questions.count()
    correct_so_far = (
        attempt.question_attempts.filter(is_correct=True)
        .values_list("question_id", flat=True)
        .distinct()
        .count()
    )

    if correct_so_far >= total_questions:
        attempt.result = "passed"
        attempt.finished_at = timezone.now()
        attempt.save(update_fields=["result", "finished_at"])

        progress.status = "completed"
        progress.completed_at = timezone.now()
        progress.save(update_fields=["status", "completed_at"])

        award_xp(
            user,
            attempt.lesson.xp_reward,
            f"Dars tugallandi: {attempt.lesson}",
            related_lesson=attempt.lesson,
        )

        today = get_or_create_today_progress(user)
        today.lessons_completed_today += 1
        today.save(update_fields=["lessons_completed_today"])

        return {"is_correct": True, "lesson_completed": True}

    return {"is_correct": True, "lesson_completed": False}


def _check_answer(question, given_answer):
    if question.question_type in ("open_answer", "code_challenge", "true_false"):
        return (question.correct_answer or "").strip().lower() == (
            given_answer or ""
        ).strip().lower()
    if question.question_type == "multiple_choice":
        correct_choice = question.choices.filter(is_correct=True).first()
        return correct_choice is not None and str(correct_choice.id) == str(
            given_answer
        )
    return False


def check_daily_lesson_limit(user):
    today_progress = get_or_create_today_progress(user)

    if today_progress.lessons_completed_today < 2:
        return True, None
    if today_progress.lessons_completed_today >= 4:
        return False, "daily_limit_reached"

    passed_today = ExtremalTestAttempt.objects.filter(
        user=user, taken_at__date=today_progress.date, passed=True
    ).exists()

    return (True, None) if passed_today else (False, "extremal_test_required")


EXTREMAL_TOKEN_SALT = "extremal-test"
EXTREMAL_TOKEN_MAX_AGE = 2100  # 35 daqiqa


def start_extremal_test(user):
    today_progress = get_or_create_today_progress(user)

    if today_progress.lessons_completed_today < 2:
        return None, "not_eligible"
    if today_progress.extremal_test_used_today:
        return None, "already_used_today"

    completed_lesson_ids = LessonProgress.objects.filter(
        user=user, status="completed"
    ).values_list("lesson_id", flat=True)

    questions = list(
        Question.objects.filter(lesson_id__in=completed_lesson_ids).order_by("?")[:50]
    )
    if not questions:
        return None, "no_questions_available"

    question_ids = [str(q.id) for q in questions]
    token = signing.dumps(
        {"user_id": str(user.id), "question_ids": question_ids},
        salt=EXTREMAL_TOKEN_SALT,
    )
    return {"token": token, "questions": questions}, None


def submit_extremal_test(user, token, answers):
    try:
        data = signing.loads(
            token, salt=EXTREMAL_TOKEN_SALT, max_age=EXTREMAL_TOKEN_MAX_AGE
        )
    except signing.BadSignature:
        return None, "token_expired_or_invalid"

    if data["user_id"] != str(user.id):
        return None, "token_expired_or_invalid"

    question_ids = set(data["question_ids"])
    valid_answers = [a for a in answers if str(a["question_id"]) in question_ids]

    # N+1 muammosi tuzatildi: 50 marta emas, BITTA so'rov bilan barcha savollarni olamiz
    questions_map = Question.objects.in_bulk([a["question_id"] for a in valid_answers])

    wrong_count = sum(
        1
        for item in valid_answers
        if not questions_map.get(item["question_id"])
        or not _check_answer(questions_map[item["question_id"]], item["answer"])
    )
    passed = wrong_count <= 3

    ExtremalTestAttempt.objects.create(
        user=user,
        score=len(valid_answers) - wrong_count,
        wrong_count=wrong_count,
        passed=passed,
    )

    today_progress = get_or_create_today_progress(user)
    today_progress.extremal_test_used_today = True
    today_progress.save(update_fields=["extremal_test_used_today"])

    return {"passed": passed, "wrong_count": wrong_count}, None

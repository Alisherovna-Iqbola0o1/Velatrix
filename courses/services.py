
def is_course_unlocked(user, course):
    """
    Kursning prerequisite_course'i borligini va u tugallanganligini tekshiradi.
    To'liq mantiq 'progress' ilovasi yaratilgach yoziladi (LessonProgress kerak).
    """
    if course.prerequisite_course is None:
        return True
    # TODO: progress ilovasi tayyor bo'lgach, haqiqiy tekshiruv yoziladi
    return False

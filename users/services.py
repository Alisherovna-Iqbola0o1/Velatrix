from django.contrib.auth.hashers import check_password
from django.core import signing

RESET_TOKEN_SALT = 'password-reset'
RESET_TOKEN_MAX_AGE = 600  # soniyada — 10 daqiqa


def verify_security_answer(user, given_answer):
    return check_password(given_answer, user.security_answer_hash)


def generate_reset_token(user):
    return signing.dumps({'user_id': str(user.id)}, salt=RESET_TOKEN_SALT)


def verify_reset_token(token):
    try:
        data = signing.loads(token, salt=RESET_TOKEN_SALT, max_age=RESET_TOKEN_MAX_AGE)
        return data['user_id']
    except signing.BadSignature:
        return None
        
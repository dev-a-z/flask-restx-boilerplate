import time

from functools import wraps
from typing import Callable
from flask import request

from service.auth_service import Auth


def func_elapsed_time(original_func) -> Callable:
    """
    함수가 실행되는데까지의 총 소요 시간을 체크해주는 데코레이터
    """

    @wraps(original_func)
    def wrapper(*args, **kwargs):  # *args, **kwargs 입력인수 추가
        start = time.time()
        # pylint: disable=not-callable
        original_func(*args, **kwargs)  # 전달받은 *args, **kwargs를 입력파라미터로 기존함수 수행
        end = time.time()
        print("함수 수행시간: %f 초" % (end - start))

    return wrapper


def token_required(original_func) -> Callable:
    """
    사용자 토큰 확인 데코레이터
    """

    @wraps(original_func)
    def wrapper(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get("data")

        if not token:
            return data, status

        return original_func(*args, **kwargs)

    return wrapper


def admin_token_required(original_func: Callable) -> Callable:
    """
    관리자 토큰 확인 데코레이터
    """

    @wraps(original_func)
    def wrapper(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get("data")

        if not token:
            return data, status

        admin = token.get("admin")
        if not admin:
            response_object = {
                "status": 403,
                "message": "admin token required",
            }
            return response_object, 403

        return original_func(*args, **kwargs)

    return wrapper

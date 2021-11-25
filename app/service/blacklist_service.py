from typing import Dict, Tuple

from flask import abort
from database.models import BlacklistToken
from database.factory import DatabaseFactory


def create_blacklist_token(token: str) -> Tuple[Dict[str, str], int]:
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        session = DatabaseFactory.create_session()
        session.add(blacklist_token)
        session.commit()
        response_object = {
            "status": 200,
            "message": "Successfully logged out.",
        }
        return response_object, 200
    except Exception as ex:
        session.rollback()

        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = "Blacklist 토큰 생성 중 오류가 발생하였습니다."
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, message, details=details)
    finally:
        session.close()

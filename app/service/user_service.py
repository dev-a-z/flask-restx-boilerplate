from typing import Dict, Tuple

from flask_restx import abort
from database.factory import DatabaseFactory
from database.models import User


def create_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    try:
        session = DatabaseFactory.create_session()
        # 사용자 등록
        new_user = User(
            id=data["id"],
            password=data["password"],
            admin=data["admin"],
            active_account=data["activeAccount"],
            locale=data["locale"],
        )
        session.add(new_user)
        # 5. 변경 사항 커밋
        session.commit()
        response_object = {
            "status": 201,
            "message": "Successfully registered.",
        }
        # 리턴 값이 여러 개인 경우 Tuple 형태로 반환 된다.
        return response_object, 201
    except Exception as ex:
        session.rollback()

        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = "사용자 등록 처리 중 오류가 발생하였습니다."
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, message, details=details)
    finally:
        session.close()


def get_all_users():
    """
    전체 사용자 목록 조회(관리자)
    """
    try:
        session = DatabaseFactory.create_session()
        return session.query(User).all()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = "전체 사용자 목록 조회 중 오류가 발생하였습니다."
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, message, details=details)
    finally:
        session.close()


def get_a_user(user_id):
    """
    특정 사용자 목록 조회(관리자)
    """
    try:
        session = DatabaseFactory.create_session()
        return session.query(User).filter(User.id == user_id).first()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = "특정 사용자 목록 조회 중 오류가 발생하였습니다."
        details = template.format(type(ex).__name__, ex.args)
        return abort(500, message, details=details)
    finally:
        session.close()

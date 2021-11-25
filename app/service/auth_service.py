import datetime

from typing import Dict, Tuple, Union

import re
import jwt

from werkzeug.exceptions import BadRequest
from flask_restx import abort
from database.models import User, BlacklistToken, Policy
from database.factory import DatabaseFactory
from service.blacklist_service import create_blacklist_token
from util.constants import Constants

from config.config import Config


class Auth:
    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        """
        User log-in bussiness logic
        """
        try:
            session = DatabaseFactory.create_session()
            # fetch the user data
            user = session.query(User).filter(User.id == data.get("id")).first()
            if user and user.check_password(data.get("password")):
                access_token = Auth.encode_auth_token(user.id)
                result = (
                    session.query(
                        User.id.label("user_id"),
                        User.admin.label("admin"),
                        User.active_account,
                        User.locale,
                    )
                    .filter(User.id == user.id)
                    .first()
                )
                user_info = {}
                if result:
                    user_info = result._asdict()
                response_object = {
                    "status": 200,
                    "message": "Successfully logged in",
                    "access_token": access_token,
                    "admin": user_info["admin"],
                    "active_account": user_info["active_account"],
                    "locale": user_info["locale"],
                }
                return response_object, 200
            else:
                response_object = {
                    "status": 401,
                    "message": "id or password does not match",
                }
                return response_object, 401

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = "사용자 로그인 처리 중 오류가 발생하였습니다."
            details = template.format(type(ex).__name__, ex.args)
            return abort(500, message, details=details)
        finally:
            session.close()

    @staticmethod
    def logout_user(data: str) -> Tuple[Dict[str, str], int]:
        """
        User log-out bussiness logic
        """
        auth_token = data.split(" ")[1]
        return create_blacklist_token(token=auth_token)

    @staticmethod
    def get_logged_in_user(new_request):
        """
        토큰 확인하여 로그인한 사용자의 정보를 조회하는 비지니스 로직
        """
        try:
            session = DatabaseFactory.create_session()
            # get the auth token
            auth_token = new_request.headers.get("Authorization")
            if auth_token:
                auth_token = auth_token.split(" ")[1]
                resp = Auth.decode_auth_token(auth_token)
                user = session.query(User).filter(User.id == resp).first()
                if user:
                    response_object = {
                        "status": 200,
                        "data": {
                            "user_id": user.id,
                            "admin": user.admin,
                        },
                    }
                    return response_object, 200
                else:
                    response_object = {
                        "status": 401,
                        "message": "Invalid token. Please check again.",
                    }
                    return response_object, 401
            else:
                response_object = {
                    "status": 401,
                    "message": "Provide a valid auth token.",
                }
                return response_object, 401
        except IndexError:
            return {
                "status": 401,
                "message": "Bad Request: `Bearer ` prefix to Authorization(header)",
            }, 400
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = "로그인한 사용자 정보 조회 중 오류가 발생하였습니다."
            details = template.format(type(ex).__name__, ex.args)
            return abort(500, message, details=details)
        finally:
            session.close()

    @staticmethod
    def check_blacklist(auth_token: str) -> bool:
        # check whether auth token has been blacklisted
        session = DatabaseFactory.create_session()
        res = (
            session.query(BlacklistToken)
            .filter(BlacklistToken.token == str(auth_token))
            .first()
        )
        bool(res)  # 하기 python built-in 함수로 아래 로직을 대신 할 수 있음.
        # if res:
        #     return True
        # else:
        #     return False

    @staticmethod
    def encode_auth_token(user_id: str) -> bytes:
        """
        Generates the Auth Token

        인코딩 과정에서의 payload type:
        --------------------------
            iss: 토큰 발급자(issuer)
            sub: 토큰 제목(subject)
            aud: 토큰 대상자(audience)
            exp: 토큰 만료 시간(expiration),
                NumericDate 형식으로 되어 있어야 함
                ex) 1480849147370
            nbf: 토큰 활성 날짜(not before),
                이 날이 지나기 전의 토큰은 활성화되지 않음
            iat: 토큰 발급 시간(issued at), 토큰 발급 이후의 경과 시간을 알 수 있음
            jti: JWT 토큰 식별자(JWT ID),
                중복 방지를 위해 사용하며, 일회용 토큰(Access Token) 등에 사용
        Returns
        --------
        `string`

        """
        try:
            #
            payload = {
                "exp": Config.JWT_TOKEN_EXP,  # 토큰 유효기간 설정
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, "secret", algorithm="HS256")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = "토큰 인코딩 처리 중 오류가 발생하였습니다."
            details = template.format(type(ex).__name__, ex.args)
            return abort(500, message, details=details)

    @staticmethod
    def decode_auth_token(auth_token: str) -> Union[str, int]:
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, "secret", algorithms="HS256")
            is_blacklisted_token = Auth.check_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            else:
                return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = "토큰 디코딩 처리 중 오류가 발생하였습니다."
            details = template.format(type(ex).__name__, ex.args)
            return abort(500, message, details=details)

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        비밀번호 유효성 검사
            @param password
            @return bool
        """
        try:
            session = DatabaseFactory.create_session()
            policies = (
                session.query(Policy)
                .filter(Policy.policy_type == "PASSWORD")
                .all()
            )
            password_length = None
            for policy in policies:
                if policy.policy_key == "PASSWORD_LENGTH":
                    password_length = int(policy.policy_value)
            if len(password) < password_length:
                raise BadRequest("비밀번호는 최소 8자리 이상이어야 합니다.")
            if (
                re.search("[a-z]+", password) is None
                or re.search("[A-Z]+", password) is None
            ):
                raise BadRequest("비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 합니다.")
            if re.search("[0-9]+", password) is None:
                raise BadRequest("비밀번호는 최소 1개 이상의 숫자가 포함되어야 합니다.")
            if not any(sc in Constants.SPECIAL_CHARACTERS for sc in password):
                raise BadRequest("비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다.")
            return True
        except BadRequest as ex:
            abort(400, ex)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = "비밀번호 유효성 검사 중 오류가 발생하였습니다."
            details = template.format(type(ex).__name__, ex.args)
            return abort(500, message, details=details)

    @staticmethod
    def change_password(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        """
        비밀번호 변경
        """
        try:
            response_object = {}
            session = DatabaseFactory.create_session()
            user = session.query(User).filter(User.id == data.get("id")).first()
            # 1. 기존 비밀번호와 일치하는지 체크
            if user and user.check_password(
                data.get("before_changed_password")
            ):
                # 2. 변경될 비밀번호가 정책에 맞게 입력됐는지 체크
                if Auth.validate_password(data.get("after_changed_password")):
                    # 3. 비밀번호 변경
                    user.password = data.get("after_changed_password")
                    session.commit()
                    response_object = {
                        "status": 200,
                        "message": "Successfully changed password.",
                    }
            else:
                response_object = {
                    "status": 401,
                    "message": "id or password does not match",
                }
                return response_object, 401

            return response_object, 200
        except BadRequest as ex:
            return {"status": 400, "message": ex.data["message"]}, 400
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = "비밀번호 변경 중 오류가 발생하였습니다."
            details = template.format(type(ex).__name__, ex.args)
            return abort(500, message, details=details)

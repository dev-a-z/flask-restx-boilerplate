from typing import Dict, Tuple
from flask import request
from flask_restx import Resource

from service.auth_service import Auth
from dto.auth_dto import AuthDto
from util.constants import Constants
from util.decorator import token_required

api = AuthDto.api

_parser = api.parser()
_parser.add_argument("Authorization", location="headers", required=True)


@api.route("auth/login")
class Login(Resource):
    @api.expect(AuthDto.input_login, validate=True)
    @api.marshal_with(AuthDto.output_login)
    @api.doc(responses=Constants.RESPONSES)
    def post(self) -> Tuple[Dict[str, str], int]:
        """
        사용자 로그인
        """
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route("auth/logout")
class Logout(Resource):
    @token_required
    @api.expect(_parser, validate=True)
    @api.doc(responses=Constants.RESPONSES)
    def post(self) -> Tuple[Dict[str, str], int]:
        """
        사용자 로그아웃
        """
        # get auth token
        auth_header = request.headers.get("Authorization")
        return Auth.logout_user(data=auth_header)


@api.route("auth/change-password")
class ChangePassword(Resource):
    @token_required
    @api.expect(AuthDto.change_password, validate=True)
    @api.doc(responses=Constants.RESPONSES)
    def post(self) -> Tuple[Dict[str, str], int]:
        """
        비밀번호 변경
        """
        # get the post data
        post_data = request.json
        return Auth.change_password(data=post_data)

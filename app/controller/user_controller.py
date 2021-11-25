from typing import Dict, Tuple
from flask import request
from flask_restx import Resource

from dto.user_dto import UserDto
from util.constants import Constants

from util.decorator import admin_token_required
from service.user_service import create_user, get_all_users, get_a_user


api = UserDto.api
_user_info = UserDto.user_info

_parser = api.parser()
_parser.add_argument("Authorization", location="headers", required=True)


@api.route("users")
class UserManagement(Resource):
    @admin_token_required
    @api.expect(_parser, validate=True)
    @api.marshal_list_with(_user_info, envelope="data")
    @api.doc(responses=Constants.RESPONSES)
    def get(self):
        """ 전체 사용자 목록 조회(관리자) """
        return get_all_users()

    @api.expect(UserDto.add_user, validate=True)
    @api.doc(responses=Constants.RESPONSES)
    def post(self) -> Tuple[Dict[str, str], int]:
        """ 신규 사용자 등록(관리자) """
        data = request.json
        return create_user(data=data)


@api.route("users/<string:user_id>/information")
class UserRUD(Resource):
    @admin_token_required
    @api.expect(_parser, validate=True)
    @api.marshal_list_with(_user_info, envelope="data")
    @api.doc(responses=Constants.RESPONSES)
    def get(self, user_id):
        """ 특정 사용자 목록 조회(관리자) """
        return get_a_user(user_id)

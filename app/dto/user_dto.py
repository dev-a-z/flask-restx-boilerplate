from flask_restx import Namespace, fields


class UserDto:
    """
    사용자 관리 DTO

    flask_restx -> Namespace 및 Swagger Document의 Model을 정의한다.
    """

    api = Namespace("user", description="사용자 관리")
    # 첫번째 파라미터 모델 명
    # 두번째 파라미터 모델 스키마
    user_info = api.model(
        "user_info",
        {
            "id": fields.String(required=True, description="사용자 아이디"),
            "registerDate": fields.Date(
                required=True,
                description="등록일자",
                example="2021-01-01",
                attribute="register_date",
            ),
            "admin": fields.Boolean(default=False, description="관리자 여부"),
            "activeAccount": fields.Boolean(
                default=True,
                description="계정 활성화 여부",
                attribute="active_account",
            ),
            "locale": fields.String(
                example="kor",
                description="다국어",
                attribute="locale",
            ),
        },
    )
    # 첫번째 파라미터 모델 명
    # 두번째 파라미터 모델 스키마
    # 세번째 파라미터 Parent 모델 스키마
    add_user = api.inherit(
        "add_user",
        user_info,
        {
            "password": fields.String(required=True, description="사용자 비밀번호"),
        },
    )

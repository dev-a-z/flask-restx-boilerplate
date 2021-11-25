from flask_restx import Namespace, fields


class AuthDto:
    """
    인증 관리 DTO

    flask_restx -> Namespace 및 Swagger Document의 Model을 정의한다.
    """

    api = Namespace("auth", description="인증 관리")
    input_login = api.model(
        "input_login",
        {
            "id": fields.String(required=True, description="사용자 아이디"),
            "password": fields.String(required=True, description="사용자 비밀번호"),
        },
    )

    output_login = api.model(
        "output_login",
        {
            "status": fields.Integer(
                description="HTTP Status Code", example=200
            ),
            "message": fields.String(
                description="메시지", example="Successfully logged in"
            ),
            "accessToken": fields.String(
                description="인증 토큰", example="eyJ0...", attribute="access_token"
            ),
            "admin": fields.Boolean(description="관리자 여부", example=False),
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

    change_password = api.model(
        "change_password",
        {
            "id": fields.String(required=True, description="사용자 아이디"),
            "before_changed_password": fields.String(
                required=True, description="변경 전 비밀번호"
            ),
            "after_changed_password": fields.String(
                required=True, description="변경 후 비밀번호"
            ),
        },
    )

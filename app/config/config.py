import os
import datetime


class DBConfig:
    @classmethod
    def _get_env(cls):
        # dev
        cls.db_type = os.environ.get("DB_TYPE", "postgresql")
        cls.db_user = os.environ.get("DB_USER", "onepredict")
        cls.db_password = os.environ.get("DB_PASSWORD", "Init1234")
        cls.db_hostname = os.environ.get(
            "DB_HOSTNAME",
            "10.10.30.15",
        )
        cls.db_port = os.environ.get("DB_PORT", 5432)
        cls.db_name = os.environ.get("DB_NAME", "flask_demo")

        # test
        # prod

    @classmethod
    def db_uri(cls):
        cls._get_env()
        # pylint: disable=line-too-long
        db_uri = f"{cls.db_type}://{cls.db_user}:{cls.db_password}@{cls.db_hostname}:{cls.db_port}/{cls.db_name}"
        return db_uri


class Config:
    SQLALCHEMY_DATABASE_URI = DBConfig.db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    JWT_TOKEN_EXP = datetime.datetime.utcnow() + datetime.timedelta(
        days=1, minutes=1, seconds=5
    )


if __name__ == "__main__":
    url = DBConfig.db_uri()

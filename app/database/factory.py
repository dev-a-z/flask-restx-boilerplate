import os

from sqlalchemy import create_engine, event, exc
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from database.models import Base, User, Policy
from config.config import DBConfig


class DatabaseFactory:
    database_engine = create_engine(
        DBConfig.db_uri(),
        encoding="UTF-8",
        echo=True,
        pool_size=20,
        max_overflow=0,
    )

    @classmethod
    def initialize(cls, app):
        """
        초기화
        """
        app.config["SQLALCHEMY_DATABASE_URI"] = DBConfig.db_uri()
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        cls._create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

        if not database_exists(cls.database_engine.url):
            create_database(cls.database_engine.url)

        # 스키마 삭제(데이터 삭제 및 컬럼 신규 추가 시 주석 해제)
        # if cls._has_schema("flask_demo"):
        #     cls._drop_schema("flask_demo", True)

        if not cls.database_engine.dialect.has_schema(
            cls.database_engine, "flask_demo"
        ):
            cls.database_engine.execute(CreateSchema("flask_demo"))
            Base.metadata.create_all(cls.database_engine, checkfirst=False)

        # 관리자 계정 생성
        session = cls.create_session()
        admin_user = session.query(User).filter(User.id == "admin").first()
        if admin_user is None:
            session.add(
                User(
                    id="admin",
                    password="onepredict@@",
                    admin=True,
                    active_account=True,
                    locale="kor",
                )
            )
            session.commit()
            session.close()
        else:
            session.close()

        # Default security settings
        session = cls.create_session()
        security_list = session.query(Policy).all()
        if len(security_list) == 0:
            session.add(
                Policy(
                    policy_key="PASSWORD_LENGTH",
                    policy_value="8",
                    policy_type="PASSWORD",
                )
            )
            session.add(
                Policy(
                    policy_key="FAILURE_LOGIN_COUNT",
                    policy_value="10",
                    policy_type="LOGIN",
                )
            )
            session.commit()
            session.close()
        else:
            session.close()

    @classmethod
    def _create_engine(cls, uri):
        cls.database_engine = create_engine(
            uri, encoding="UTF-8", echo=True, pool_size=20, max_overflow=0
        )

    @classmethod
    def create_session(cls):
        # 멀티프로세스 수행 전 engine dispose
        # engine dispose함수는 병렬처리 용도로 멀티프로세스 함수에 추가했었으나,
        # 멀티 프로세스 수행 후 임의의 다음 번 API 호출에서 session을 생성하지 못하는 문제로 인해,
        # 세션 생성 시 dispose하도록 로직에 추가
        cls.database_engine.dispose()
        with cls.database_engine.connect():
            session = scoped_session(
                sessionmaker(autocommit=False, bind=cls.database_engine)
            )
        return session

    @classmethod
    @event.listens_for(database_engine, "connect")
    def connect(cls, connection_record):
        print("connect!")
        connection_record.info["pid"] = os.getpid()

    @classmethod
    @event.listens_for(database_engine, "checkout")
    def checkout(cls, connection_record, connection_proxy):
        print("checkout!")
        pid = os.getpid()
        if connection_record.info["pid"] != pid:
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s"
                % (connection_record.info["pid"], pid)
            )

    @classmethod
    def _has_schema(cls, name):
        return cls.database_engine.dialect.has_schema(cls.database_engine, name)

    @classmethod
    def _create_schema(cls, name):
        cls.database_engine.execute(CreateSchema(name))

    @classmethod
    def _drop_schema(cls, name, cascade=False):
        cls.database_engine.execute(DropSchema(name, cascade=cascade))

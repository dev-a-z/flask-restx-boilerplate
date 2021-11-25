import datetime
import random
import bcrypt

from flask_sqlalchemy import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    # Text,
    ForeignKey,
    DateTime,
    Numeric,
    # KeyConstraint,
    # ForeignKeyConstraint,
    Index,
    ARRAY,
    # LargeBinary,
    Boolean,
    # UniqueConstraint,
)
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    """
    사용자 테이블
    -----------------
        사용자 정보들을 저장한다.
    """

    __tablename__ = "user"
    __table_args__ = {"schema": "flask_demo"}

    id = Column("id", String(50), primary_key=True, autoincrement=False)
    password_hash = Column("password_hash", String(100), nullable=False)
    register_date = Column("register_date", DateTime(timezone=False))
    admin = Column("admin", Boolean, default=False)
    active_account = Column("active_account", Boolean, default=True)
    locale = Column("locale", String(50))

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        """
        비밀번호 설정(setter 함수)
        """
        # hashpw 함수의 첫번째 파라미터로 byte객체가 필요하여 str 객체 내의 encode() 메소드 활용하여 utf-8로 인코딩
        # 두번째 파라미터로 salt를 사용하여 암호화
        encrypted_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        )
        # 데이터 베이스 저장을 위해 bytes 객체를 utf-8로 디코딩하여 str 객체로 변환
        self.password_hash = encrypted_password.decode("utf-8")

    def check_password(self, password: str) -> bool:
        """
        비밀번호 체크 함수
        """
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def __init__(
        self,
        id,  # pylint: disable=redefined-builtin
        password,
        admin,
        active_account,
        locale,
    ):
        self.id = id
        self.password = password
        self.register_date = datetime.datetime.now()
        self.admin = admin
        self.active_account = active_account
        self.locale = locale


class Policy(Base):
    """
    정책 테이블
    -----------------
        정책과 관련된 정보들을 저장한다.
        ex) 비밀번호 정책, 연속적인 비밀번호 불일치 시 계정 잠금 횟수 등등..
    """

    __tablename__ = "policy"
    __table_args__ = {"schema": "flask_demo"}

    # Columns
    id = Column("id", Integer, primary_key=True)
    policy_key = Column("policy_key", String(255))
    policy_value = Column("policy_value", String(255))
    policy_type = Column("policy_type", String(255))

    def __init__(
        self,
        policy_key,
        policy_value,
        policy_type,
    ):
        self.policy_key = policy_key
        self.policy_value = policy_value
        self.policy_type = policy_type


class BlacklistToken(Base):
    """
    블랙리스트 관리 테이블
    -----------------
        로그아웃 시 사용중인 토큰을 해당 테이블에 저장한다.
    """

    __tablename__ = "blacklist_token"
    __table_args__ = {"schema": "flask_demo"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(255), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return "<id: token: {}".format(self.token)


class DemoData(Base):
    """
    데모 데이터 테이블
    -----------------
        데모 데이터를 저장한다
    """

    __tablename__ = "demo_data"
    __table_args__ = {"schema": "flask_demo"}

    # Columns
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        "user_id",
        ForeignKey("flask_demo.user.id", ondelete="CASCADE"),
    )
    acquisition_date = Column("acquisition_date", DateTime())
    demo_data = Column("demo_data", ARRAY(Numeric()))

    # Relations(one to one)
    relationship("DemoAi", uselist=False)

    def __init__(
        self,
        user_id,
        acquisition_date,
        demo_data,
    ):
        self.id = id
        self.user_id = user_id
        self.acquisition_date = acquisition_date
        self.demo_data = demo_data


Index(
    "DemoData_index",
    DemoData.user_id,
    DemoData.acquisition_date,
    unique=True,
)

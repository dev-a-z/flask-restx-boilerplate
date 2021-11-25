# flask-restx-bolierplate
본 어플리케이션은 flask, flask-restx, SQLAlchemy, PostgreSQL 활용하여
빠르게 REST API 서비스를 개발하기 위한 boilerplate입니다.

(Build a REST API with Flask, flask-restx, SQLAlchemy and PostgreSQL)
>모든 개발 및 디버깅은 VSCode 내에서 진행되어 관련 설정 파일이 포함되어 있습니다.  
>__Note__: 다른 IDE(ex.`Pycharm`) or Editor에서 개발하시는 경우,  
>_`.vscode 폴더`_ 및 _`flask-restx-boilerplate.code-workspace`_ 파일 등을 삭제하시면 됩니다.

----------------------------
## Directory layout

    flask-bolierplate
    ├── .vscode/
    │   ├── launch.json             # vscode 실행 관련 설정
    │   └── settings.json           # vscode 내 format, lint, test 등 설정
    ├── app/                        # Application root
    │   ├── config/                 
    │   │   └── config.py           # DB, App envirionment
    │   ├── controller/             # Route, Entry point
    │   ├── database/               
    │   │   ├── factory.py          # DB Factory(Create Schema)
    │   │   └── models.py           # DB Schema
    │   ├── dto/                    # DTO, Swagger model
    │   ├── service/                # Bussiness, Data Access Logic
    │   └── util/                   # Utilities
    │   │   ├── constants.py        # 상수 정의
    │   │   ├── custom_fields.py    # flask_restx fields Implements
    │   │   └── decorator.py        # @Decorator
    ├── build/                      # build 설정 파일(docker)
    ├── local/                      # local test 환경 구축을 위한 docker 기반 설정(ex. postgresql)
    ├── scripts/                    # Scripts
    ├── tests/                      # Tests(pytest)
    ├── .env                        # python-dotenv 설정(환경변수)
    ├── .gitignore                  # git 반영 제외 설정 파일
    ├── .pylintrc                   # pylint 설정 파일
    ├── .python-version             # 프로젝트 진입 시 바로 설정한 가상환경으로 접속 할 수 있도록 하는 설정 파일
    ├── flask-restx-boilerplate.code-workspace # vscode 내 workspace 설정 파일
    ├── Makefile                    # Custum CLI 생성
    ├── README.md
    └── requirements.txt            # Python package management

---
## VSCode 개발 환경 설정
VSCode를 사용하는 경우 기본적인 설정에 대해서 설명합니다.
### [launch.json](https://code.visualstudio.com/docs/editor/debugging#_launch-configurations "launch.json 설정 관련 Document")
실행 모드, 환경변수 및 args 등 실행과 관련된 부분을 설정합니다.


### [settings.json](https://code.visualstudio.com/docs/getstarted/settings "settings.json 설정 관련 Document")

`Python Path` 및 VSCode 내에서 사용할 `testing`, `formatting`, `linting` 등을 설정합니다.    
>__Note__: 처음 저장소를 clone 및 fork 시 `python.pythonPath` 부분을 사용자 환경에 맞게 변경해야 합니다.

---
## How to use?
>__Note__: 사내 Python 개발 환경은 `pyenv`, `pyenv-virtaulenv`를 사용하고 있습니다.  
>또한, 모든 실행 및 빌드는 `Makefile`에서 작성 및 관리합니다.
### PYTHON PATH & RUNTIME 환경 설정
개발하기 전 Python path 및 런타임 환경변수 설정이 필요합니다.
* `settings.json` 파일 내 _python.pythonPath_ 를 사용자 환경에 맞게 변경합니다
* `.env` 파일 내 _PYTHONPATH_ 를 사용자 환경에 맞게 변경합니다
### 가상환경 구성
#### 1. 파이썬 및 가상환경 설치
    $ pyenv install 3.8.5
    $ pyenv virtualenv 3.8.5 flask-restx-boilerplate

#### 2. 가상환경 활성화
    $ pyenv activate flask-restx-boilerplate
> __Note__: 작업 환경(Workspace) 진입 시, `.python-version` 설정으로 인하여 자동으로 가상환경이 활성화 됩니다

### 설치
파이썬 모듈 설치

    $ make install

### 실행
flask app 실행

    $ make run

### Swagger url
* http://localhost:5000/v1

### 테스트
test(pytest) 파일 실행

    $ make tests

### Get API List
API 전체 목록 가져오기

    $ make routes

### Docker
#### docker build

    $ make docker-build

#### docker run

    $ make docker-run

#### docker stop

    $ make docker-stop

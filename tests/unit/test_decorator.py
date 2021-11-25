import os
import sys
import pytest

sys.path.append(os.path.join(os.getcwd(), "app"))
from util.decorator import func_elapsed_time


@pytest.fixture
def get_func_name():
    return "test"


@func_elapsed_time
# pylint: disable=redefined-outer-name
def test_func_elapsed_time(get_func_name):
    """ 함수가 실행되는데까지의 총 소요 시간을 체크해주는 데코레이터 테스트 """
    print("'%s'을 출력합니다." % get_func_name)
    return "테스트"

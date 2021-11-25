from flask_restx import fields


class MtrStatusItem(fields.Raw):
    """
    주 변압기 진단 결과에 따른 결과 값 매핑 함수
    """

    def format(self, value):
        rtn = None
        if value == 0:
            rtn = "정상"
        elif value == 1:
            rtn = "관심"
        elif value == 2:
            rtn = "주의"
        elif value == 3:
            rtn = "이상"
        elif value == 4:
            rtn = "심각"

        return rtn

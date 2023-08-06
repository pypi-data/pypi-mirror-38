class ParameterTypeError(Exception):

    def __init__(self, error_lineno=0, error_code=-1, error_type="", error_msg=""):
        super().__init__(self)  # 初始化父类
        self.error_lineno = error_lineno
        self.error_code = error_code
        self.error_type = error_type
        self.error_msg = error_msg

    def __str__(self):
        return str(self.error_lineno) + ' ' + str(self.error_code) + ' ' + self.error_type + ' ' + self.error_msg


class ParameterValueError(Exception):

    def __init__(self, error_lineno=0, error_code=-2, error_type="", error_msg=""):
        super().__init__(self)  # 初始化父类
        self.error_lineno = error_lineno
        self.error_code = error_code
        self.error_type = error_type
        self.error_msg = error_msg

    def __str__(self):
        return str(self.error_lineno) + ' ' + str(self.error_code) + ' ' + self.error_type + ' ' + self.error_msg


if __name__ == '__main__':
    try:
        raise ParameterTypeError(0, -1, "ParameterTypeError", '参数异常')
    except ParameterTypeError as e:
        print(e)

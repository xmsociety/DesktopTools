from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QPixmap

import re
import datetime
from logger import logger


def replace_spaces(s1, s2):
    # s1 is the first string; # s2 is the second string
    # use re module to replace consecutive spaces with s2
    # create a regular expression pattern that matches one or more spaces
    # pattern = re.compile(r"\s+") # 替换特殊字符和空格
    pattern = re.compile(r" +")
    # use sub method to replace the matched spaces with s2
    result = pattern.sub(s2, s1)
    # return the result
    return result


def safe_eval(expr):
    """
    - 只允许使用以下内置函数和变量
    - 如果出现异常，说明表达式不合法
    """
    # allowed_globals = {'__builtins__': None, 'abs': abs, 'round': round}
    allowed_globals = {'__builtins__': None}
    allowed_locals = {}
    # 执行表达式
    result = eval(expr, allowed_globals, allowed_locals)
    return result


def data2json(str_data: str) -> str:
    """
    - data 字符串转json字符串(包含格式化)
    - 不做异常处理, 同一在使用处捕获
    """
    import json
    data = safe_eval(str_data)
    if data:
        str_data = json.dumps(data, ensure_ascii=False, indent=4)
    return str_data


def extract_numbers(string):
    pattern = r'\d+'
    numbers = re.findall(pattern, string)
    numbers = ''.join(numbers)
    return numbers


def unixtime_to_datetime_str(unixtime_str):
    unixtime_str = extract_numbers(unixtime_str)
    if not unixtime_str or not unixtime_str.isdigit():
        return ""
    unixtime = int(unixtime_str)
    dt = datetime.datetime.fromtimestamp(unixtime)
    dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt_str


class ClipFuncs:
    SplitSign: str = ": "

    def __init__(self, clipboard: QClipboard) -> None:
        self.clipboard = clipboard
        self.dict_registered: dict = {
            f"clip-连续空格替换为指定符号{self.SplitSign}": self.replace_spaces,
            "clip-data转为JSON字符串": self.data2json,
            "clip-unixtime转datetime": self.unixtime_to_datetime_str,
        }

    def get_clipboard_text(self):
        originalText = self.clipboard.text()
        if originalText:
            return originalText
        return ""

    def unixtime_to_datetime_str(self):
        content = unixtime_to_datetime_str(self.get_clipboard_text() or 0)
        if not content:
            return False, "非unix时间"
        self.clipboard.setText(content)
        return True, ""

    def data2json(self):
        """
        将data转为json字符串
        """
        originalText = self.clipboard.text()
        if originalText:
            try:
                content = data2json(originalText)
                self.clipboard.setText(content)
            except Exception as err:
                logger.error(f"data2json: {err}")
                return False, str(err)
        return True, ''

    def replace_spaces(self, target_symbol: str):
        """
        将连续空格替换为|
        多为复制表格数据转Markdown使用
        """
        originalText = self.clipboard.text()
        if originalText:
            content = replace_spaces(originalText, target_symbol)
            logger.debug(f"{originalText} chg2(by: {target_symbol}) {content}")
            self.clipboard.setText(content)
        return True, ''

if __name__ == "__main__":
    # rst = replace_spaces(
    #     "Hello   world  nihao haha  liuliuliu  niubi \n 1 2 3 4  5", "|"
    # )
    # print(rst)
    print(extract_numbers("jas123asdkh123"))
    print(extract_numbers("213"))

from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QPixmap

from logger import logger


def replace_spaces(s1, s2):
    # s1 is the first string; # s2 is the second string
    # use re module to replace consecutive spaces with s2
    import re

    # create a regular expression pattern that matches one or more spaces
    # pattern = re.compile(r"\s+") # 替换特殊字符和空格
    pattern = re.compile(r" +")
    # use sub method to replace the matched spaces with s2
    result = pattern.sub(s2, s1)
    # return the result
    return result


class ClipFuncs:
    SplitSign: str = ": "

    def __init__(self, clipboard: QClipboard) -> None:
        self.clipboard = clipboard
        self.dict_registered: dict = {
            f"clip-连续空格替换为指定符号{self.SplitSign}": self.replace_spaces,
        }

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


if __name__ == "__main__":
    rst = replace_spaces(
        "Hello   world  nihao haha  liuliuliu  niubi \n 1 2 3 4  5", "|"
    )
    print(rst)

from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QStyledItemDelegate


class CustomItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # 绘制默认项
        super().paint(painter, option, index)

        # 获取当前项的文本
        item = self.parent().item(index.row())
        text = item.text()

        # 设置半透明的颜色
        painter.setPen(QColor(150, 150, 150, 150))  # 半透明的灰色
        painter.setFont(QFont("Helvetica Neue", 12))

        # 计算并绘制快捷键提示，确保其右对齐
        shortcut_text = f" (Ctrl+{index.row() + 1})"
        text_width = painter.fontMetrics().horizontalAdvance(shortcut_text)

        # 绘制文本
        painter.drawText(
            option.rect.right() - text_width - 10, option.rect.top() + 15, shortcut_text
        )

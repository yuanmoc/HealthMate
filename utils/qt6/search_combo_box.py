from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QStandardItemModel
from PyQt6.QtWidgets import QCompleter, QComboBox


class SearchComboBox(QComboBox):
    # 自定义信号
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lineEdit().setPlaceholderText('搜索...')
        self.lineEdit().textChanged.connect(self.filterItems)
        self.setModel(QStandardItemModel(self))

    def filterItems(self, text):
        completer = QCompleter(self.model(), self)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setCompleter(completer)
        self.completer().setCompletionPrefix(text)
        self.completer().complete()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        重写鼠标按下事件
        :param event:
        :return:
        """
        super(SearchComboBox, self).mousePressEvent(event)
        if self.count() > 0:
            return
        # 当鼠标左键单击时
        if event.button() == Qt.MouseButton.LeftButton:
            # 发射信号
            self.clicked.emit()
            # 弹出下拉框
            QComboBox.showPopup(self)


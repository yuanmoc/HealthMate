from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel
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

        # 添加筛选器模型来筛选匹配项
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)  # 大小写不敏感
        self.pFilterModel.setSourceModel(self.model())

        # 添加一个使用筛选器模型的QCompleter
        self.completer = QCompleter(self.pFilterModel, self)
        # 始终显示所有(过滤后的)补全结果
        self.completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)  # 不区分大小写
        self.setCompleter(self.completer)

        # Qcombobox编辑栏文本变化时对应的槽函数
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

        # 当在Qcompleter列表选中候，下拉框项目列表选择相应的子项目

    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

    # 在模型更改时，更新过滤器和补全器的模型
    def setModel(self, model):
        super(SearchComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # 在模型列更改时，更新过滤器和补全器的模型列
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(SearchComboBox, self).setModelColumn(column)

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


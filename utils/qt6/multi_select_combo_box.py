import typing

from PyQt6 import sip
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QComboBox, QListWidget, QLineEdit, QCheckBox, QListWidgetItem, QCompleter


class MultiSelectComboBox(QComboBox):
    # 有item被选择时，发出信号
    itemChecked = pyqtSignal(list)
    clicked = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super(MultiSelectComboBox, self).__init__(parent)
        self.list_wgt = QListWidget(self)
        self.setView(self.list_wgt)
        self.setModel(self.list_wgt.model())
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # 保存QCheckBox控件
        self.items = []
        self.addItem('全选', None)

    def addItem(self, text: str, userData: typing.Any = ...):
        #   在这里给每个CheckBox都绑定了信号，目的是每次Check都能作出响应。
        check = QCheckBox(text, self.view())
        check.stateChanged.connect(self.on_state_changed)
        self.items.append((check, userData))
        item = QListWidgetItem(self.view())
        self.view().addItem(item)
        self.view().setItemWidget(item, check)


    def addItems(self, items):
        for item in items:
            self.addItem(*item)

    def clear(self):
        self.view().clear()
        self.items.clear()
        self.addItem('全选', None)

    def get_selected(self):
        sel_item = []
        for item in self.items:
            check_box = item[0]
            if self.items[0] == item:
                continue
            if not sip.isdeleted(check_box) and check_box.checkState() == Qt.CheckState.Checked:
                sel_item.append(item)
        return sel_item

    def set_all_state(self, state):
        for item in self.items:
            check_box = item[0]
            check_box.blockSignals(True)
            check_box.setCheckState(Qt.CheckState(state))
            check_box.blockSignals(False)

    def check_ok(self, value):
        for item in self.items:
            check_box = item[0]
            if value in check_box.text():
                check_box.blockSignals(True)
                check_box.setCheckState(Qt.CheckState.Checked)
                check_box.blockSignals(False)
        sel_item = self.get_selected()
        self.lineEdit().setText(';'.join([item[0].text() for item in sel_item]))

    def on_state_changed(self, state):
        if self.sender() == self.items[0][0]:
            self.set_all_state(state)
        sel_item = self.get_selected()
        self.itemChecked[list].emit(sel_item)
        self.lineEdit().setText(';'.join([item[0].text() for item in sel_item]))


    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        重写鼠标按下事件
        :param event:
        :return:
        """
        super(MultiSelectComboBox, self).mousePressEvent(event)
        if self.items is not None and len(self.items) > 1:
            return
        # 当鼠标左键单击时
        if event.button() == Qt.MouseButton.LeftButton:
            # 发射信号
            self.clicked.emit()
            # 弹出下拉框
            QComboBox.showPopup(self)


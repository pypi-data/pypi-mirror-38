"""
Based on `Stackoverflow <https://stackoverflow.com/a/17788371>`_.
"""
from PyQt5.QtCore import QEvent, QPoint, QRect, Qt
from PyQt5.QtWidgets import QApplication, QStyle, QStyleOptionButton, QStyledItemDelegate


class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CheckBoxDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        checked = index.model().data(index, Qt.DisplayRole)
        style_option = QStyleOptionButton()

        if index.flags() & Qt.ItemIsEnabled:
            style_option.state |= QStyle.State_Enabled
        else:
            style_option.state |= QStyle.State_ReadOnly

        if checked:
            style_option.state |= QStyle.State_On
        else:
            style_option.state |= QStyle.State_Off

        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        style_option.rect = self.get_check_box_rect(option)
        QApplication.style().drawControl(QStyle.CE_CheckBox, style_option, painter)
        painter.restore()

    def get_check_box_rect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint(option.rect.x() + option.rect.width() / 2 - check_box_rect.width() / 2,
                                 option.rect.y() + option.rect.height() / 2 - check_box_rect.height() / 2)

        return QRect(check_box_point, check_box_rect.size())

    def editorEvent(self, event, model, option, index):
        """
        Change the data in the model and the state of the checkbox if the user presses the left mouse button or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        """
        if not index.flags() & Qt.ItemIsEnabled:
            return False

        # Change only state if left clicked released and inside the check box
        if event.button() != Qt.LeftButton or event.type() != QEvent.MouseButtonRelease or not self.get_check_box_rect(
                option).contains(event.pos()):
            return False

        # Change the checkbox-state
        self.setModelData(None, model, index)

        return True

    def setModelData(self, editor, model, index):
        """
        The user wanted to change the old state in the opposite.
        """
        new_data = not index.model().data(index, Qt.EditRole)
        model.setData(index, new_data, Qt.EditRole)

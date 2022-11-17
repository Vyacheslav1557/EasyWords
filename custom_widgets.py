from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt


class ObjectWithIdAndLinkAndValue:
    def __init__(self, id_=None, link=None, value=None):
        self.id_ = id_
        self.link = link
        self.value = value

    def get_id(self):
        return self.id_

    def get_link(self):
        return self.link

    def get_value(self):
        return self.value

    def set_id(self, id_):
        self.id_ = id_


class TurningObject:
    def __init__(self):
        self.side = 0

    def turn(self):
        self.side ^= 1
        return self.side


class ListWidgetItemWithId(QListWidgetItem, ObjectWithIdAndLinkAndValue):
    def __init__(self, text, id_=None):
        QListWidgetItem.__init__(self, text)
        ObjectWithIdAndLinkAndValue.__init__(self, id_=id_)


class ListWidgetItemWithLinkAndValue(QListWidgetItem, ObjectWithIdAndLinkAndValue):
    def __init__(self, text, link=None, value=None):
        QListWidgetItem.__init__(self, text)
        ObjectWithIdAndLinkAndValue.__init__(self, link=link, value=value)


class PushButtonWithId(QPushButton, ObjectWithIdAndLinkAndValue, TurningObject):
    def __init__(self, *args, id_=None, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        ObjectWithIdAndLinkAndValue.__init__(self, id_=id_)
        TurningObject.__init__(self)


class LabelWithId(QLabel, ObjectWithIdAndLinkAndValue, TurningObject):
    def __init__(self, *args, id_=None, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        ObjectWithIdAndLinkAndValue.__init__(self, id_=id_)
        TurningObject.__init__(self)


class HorizontalTabBar(QTabBar):
    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(self.tabRect(index),
                             Qt.AlignCenter | Qt.TextDontClip,
                             self.tabText(index))

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        if size.width() < size.height():
            size.transpose()
        return size


class TabWidget(QTabWidget):
    def __init__(self, parent=None, **kwargs):
        QTabWidget.__init__(self, parent, **kwargs)
        self.setTabBar(HorizontalTabBar())

import json
from datetime import datetime

import qtawesome
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QWidget, QTableWidgetItem, QAbstractItemView, QDateTimeEdit, \
    QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCalendarWidget
from docker import DockerClient
from signal_dispatcher.signal_dispatcher import SignalDispatcher

from events_dock.mappers import EventMapper
from events_dock.models import Event
from events_dock.utils import Config


class QVboLayout(object):
    pass


class Events(QWidget):
    stream_events = True

    def __init__(self, client: DockerClient, flags=None, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.__client = client
        self.__layout = QVBoxLayout()
        self.__events_table = EventsTable()
        self.__config = Config()
        self.__start_date = DateTimePicker()
        self.__end_date = DateTimePicker()
        self.__filter = QPushButton('Filter')
        self.__clear = QPushButton('Clear')
        title = self.__config.get('app.name') + ' v.' + self.__config.get('app.version')
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(self.__config.get('app.icon')))

    def show(self):
        # Filter form
        self.setLayout(self.__layout)
        row = QHBoxLayout()
        row.addWidget(QLabel('From:'), 0, Qt.AlignLeft)
        row.addWidget(self.__start_date, 0, Qt.AlignLeft)
        row.addWidget(QLabel('To:'), 0, Qt.AlignLeft)
        row.addWidget(self.__end_date, 0, Qt.AlignLeft)
        self.__filter.setIcon(QIcon(qtawesome.icon('fa.filter')))
        row.addWidget(self.__filter, 1, Qt.AlignLeft)
        self.__clear.setIcon(qtawesome.icon('fa.remove'))
        row.addWidget(self.__clear, 2, Qt.AlignLeft)
        self.__start_date.setDateTime(QDateTime().currentDateTime().addDays(-1))
        self.__end_date.setDateTime(QDateTime().currentDateTime())
        self.__end_date.setMinimumDateTime(self.__start_date.dateTime())

        # Filter events
        SignalDispatcher.register_signal('events_dock.start_date_changed', self.__start_date.dateChanged)
        SignalDispatcher.register_handler('events_dock.start_date_changed', self.on_start_date_changed)
        SignalDispatcher.register_signal('events_dock.clear_filter', self.__clear.clicked)
        SignalDispatcher.register_handler('events_dock.clear_filter', self.on_clear)
        SignalDispatcher.register_signal('events_dock.filter', self.__filter.clicked)
        SignalDispatcher.register_handler('events_dock.filter', self.on_filter)

        self.__layout.addLayout(row)
        self.__layout.addWidget(self.__events_table)
        self.__events_table.show()
        width = self.__events_table.width()
        self.setMinimumWidth(width)

        return super().show()

    @pyqtSlot(Event, name='docker_event')
    def on_event(self, event):
        if Events.stream_events:
            self.__events_table.on_event(event)

    @pyqtSlot(name="clear_filter")
    def on_clear(self):
        self.__events_table.setRowCount(0)
        self.__start_date.setDateTime(QDateTime().currentDateTime().addDays(-1))
        self.__end_date.setDateTime(QDateTime().currentDateTime())
        Events.stream_events = True

    @pyqtSlot(name='start_date_changed')
    def on_start_date_changed(self):
        date_time = self.__start_date.dateTime()
        self.__end_date.setMinimumDateTime(date_time)

    @pyqtSlot(Event, name='docker_event')
    def on_filter_event(self, event: Event):
        self.__events_table.on_event(event)

    @pyqtSlot(name='filter')
    def on_filter(self):
        Events.stream_events = False
        self.__events_table.setRowCount(0)
        since = self.__start_date.dateTime().toSecsSinceEpoch()
        until = self.__end_date.dateTime().toSecsSinceEpoch()
        data = self.__client.events(until=until, since=since)

        for event in data:
            event = json.loads(event.decode('utf-8'))
            event = EventMapper.map(event)
            self.__events_table.on_event(event)

        data.close()


class EventsTable(QTableWidget):
    def __init__(self, *__args):
        self.__config = Config()
        super().__init__(*__args)

    def show(self):
        self.setColumnCount(self.__config.section('table').__len__())
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        columns = []

        for column in self.__config.section('table'):
            columns.append(self.__config.get('table.' + column))

        self.setHorizontalHeaderLabels(columns)

        return super().show()

    def on_event(self, event: Event):
        position = self.rowCount()
        time = datetime.fromtimestamp(event.time / 1000000000)
        self.insertRow(position)
        self.setItem(position, 0, QTableWidgetItem(time.__str__()))
        self.setItem(position, 1, QTableWidgetItem(event.action))
        self.setItem(position, 2, QTableWidgetItem(event.type))
        self.setItem(position, 3, QTableWidgetItem(event.actor))
        self.resizeColumnToContents(0)
        self.scrollToBottom()


class DateTimePicker(QDateTimeEdit):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCalendarPopup(True)
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setFirstDayOfWeek(Qt.Monday)
        self.setCalendarWidget(calendar)
        self.setDisplayFormat('d MMM yyyy - hh:mm:ss')


class ClearButton(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setIcon(qtawesome.icon('fa.remove'))
        self.setText('Clear')
        self.setToolTip('Clear filter')

    def show(self):
        super().show()


class FilterButton(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setIcon(qtawesome.icon('fa.filter'))
        self.setToolTip('Filter events results.')
        self.setText('Filter')

    def show(self):
        super().show()

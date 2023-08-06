import json

from PyQt5.QtCore import pyqtSignal

from events_dock.mappers import EventMapper
from events_dock.models import Event


class EventStreamHandler:
    docker_event = pyqtSignal(Event, name='docker_event')

    def handle(self, event_stream):
        for event in event_stream:
            event = json.loads(event.decode('utf-8'))
            event = EventMapper.map(event)
            self.docker_event.emit(event)

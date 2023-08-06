import json

from PyQt5.QtCore import QThread, pyqtSignal
from docker import DockerClient

from events_dock.mappers import EventMapper
from events_dock.models import Event


class EventsThread(QThread):
    """
    EventsThread is used to emit events on containers operations detected. This keeps the interface up to date with
    the changes behind.

    Attributes:
        :client (DockerClient): Docker client
        :docker_event (pyqtSignal): Signal that is emitted
    """
    docker_event = pyqtSignal(Event, name='docker_event')

    def __init__(self, client: DockerClient):
        """
        :param client (DockerClient):
        """
        super().__init__()
        self.client = client

    def run(self):
        events = self.client.events()

        for event in events:
            event = json.loads(event.decode('utf-8'))
            docker_event = EventMapper.map(event)
            self.docker_event.emit(docker_event)



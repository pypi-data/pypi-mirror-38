"""
Main application classes. Used to initialize the application.
"""
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from docker import DockerClient

from events_dock.components import Events
from events_dock.threads import EventsThread
from events_dock.utils import Config


class App:
    def __init__(self, client: DockerClient):
        self.__config = Config()
        self.__app = QApplication(sys.argv)
        self.__client = client
        self.__main_widget = Events(client)

    def run(self):
        self.__main_widget.show()

        events_thread = EventsThread(self.__client)
        events_thread.start(priority=1)
        events_thread.docker_event.connect(self.__main_widget.on_event)

        self.__app.exec()

    @property
    def client(self):
        return self.__client

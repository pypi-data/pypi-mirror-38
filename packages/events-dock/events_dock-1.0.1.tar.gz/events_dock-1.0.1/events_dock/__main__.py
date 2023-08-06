import sys

import docker
from events_dock.app import App


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    app = App(docker.from_env())
    app.run()


if __name__ == "__main__":
    main()

from events_dock.models import Event


class EventMapper:
    @staticmethod
    def map(event_data: dict):
        """
        :param event_data: Event data from event stream.
        :return Event: Returns Event object.
        """
        event = Event(
            time_str=event_data.get('timeNano'),
            type_name=event_data.get('Type'),
            actor_id=event_data.get('Actor').get('ID'),
            action_name=event_data.get('Action')
        )

        return event

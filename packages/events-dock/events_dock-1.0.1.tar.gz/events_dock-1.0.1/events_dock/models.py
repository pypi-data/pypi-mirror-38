class Event:
    def __init__(self, time_str='', type_name='', actor_id='', action_name=''):
        self.__time = time_str
        self.__type = type_name
        self.__actor = actor_id
        self.__action = action_name

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time_string: str):
        self.__time = time_string

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type_name: str):
        self.__type = type_name

    @property
    def actor(self):
        return self.__actor

    @actor.setter
    def actor(self, actor_id: str):
        self.__actor = actor_id

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action_name):
        self.__action = action_name

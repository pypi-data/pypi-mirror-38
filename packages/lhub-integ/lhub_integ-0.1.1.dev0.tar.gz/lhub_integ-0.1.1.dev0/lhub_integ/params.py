from abc import ABCMeta
from collections import defaultdict

from lhub_integ.env import __EnvVar

from enum import Enum

# pulled from forms.model.DataType
class DataType(Enum):
    STRING = "string"
    COLUMN = "column"
    NUMBER = "number"
    # no node datatype because integrations can only pull from one node


# pulled from forms.model.InputType
class InputType(Enum):
    TEXT = "text"
    TEXT_AREA = "textarea"
    EMAIL = "email"
    PASSWORD = "password"
    SELECT = "select"
    COLUMN_SELECT = "columnSelect"


class __Param(__EnvVar, metaclass=ABCMeta):
    def __init__(
        self,
        name,
        description=None,
        default=None,
        optional=False,
        options=None,
        data_type=DataType.STRING,
        input_type=InputType.TEXT,
    ):
        super().__init__(name, default, optional)
        self.description = description
        self.default = default
        self.data_type = data_type
        self.options = options
        if data_type == DataType.COLUMN:
            self.input_type = InputType.InputType.COLUMN_SELECT
        elif options is not None and len(options) > 1:
            self.input_type = InputType.SELECT
        else:
            self.input_type = input_type


"""
We take most of the param information from our Form.Input case class. 
We don't enable a dependsOn field because if the dataType is a column then it will auto depends on its parent. 
"""


class ConnectionParam(__Param, metaclass=ABCMeta):
    """
    ConnectionParam provides a parameter specified by the connection

    Example usage:

    API_KEY = ConnectionParam('api_key')
    def process_row(url):
      requests.get(url, params={api_key: API_KEY.get()})
    """

    _all = set()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._all.add(self)

    @classmethod
    def all(cls):
        return sorted(cls._all, key=lambda var: var.name)


class ActionParam(__Param, metaclass=ABCMeta):
    """
    ActionParam provides a parameter specified by the action

    Example usage:

    API_KEY = ConnectionParam('api_key', action='process_row')

    import requests
    def process_row(url):
      requests.get(url, params={api_key: API_KEY.get()})
    """

    action_map = defaultdict(set)

    def __init__(self, *args, action: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_map[action].add(self)

    @classmethod
    def for_action(cls, action):
        return sorted(cls.action_map[action], key=lambda var: var.name)


"""
JSON I/O Handlers

This module contains the various built-in handlers. Such as:

    * date/datetime
    * dataclass
"""

import abc
import collections
import datetime
import dateutil.parser
import json
import logging
import six

try:
    import dataclasses
except ImportError:
    dataclasses = None


logger = logging.getLogger(__name__)

REGISTRY = {}
HANDLERS = {}


def register(name=None):
    """
    Register handler.
    """
    global REGISTRY

    def register_handler(cls):
        key = name or cls.__name__.replace('Handler', '').lower()
        REGISTRY[key] = cls
        logger.debug('Registered JSON handler: {}'.format(key))
        return cls

    return register_handler


def _init_handlers():
    global HANDLERS
    if not HANDLERS:
        for name, handler in REGISTRY.items():
            HANDLERS[name] = handler(name=name)


def get_handlers():
    """
    Get all registered handlers.

    Returns:
        list[Handler]: Handlers
    """
    _init_handlers()
    return list(HANDLERS.values())


def get_handler(name):
    """
    Get handler with the given name.

    Args:
        name (str): Handler name.

    Returns:
        Handler or None: JSON handler
    """
    _init_handlers()
    return HANDLERS.get(name)


def activate(name):
    """
    Turn on the given handler.

    Args:
        name (str): Handler name.

    Returns:
        Handler or None: JSON handler
    """
    handler = get_handler(name)
    handler.active = True
    return handler


def deactivate(name):
    """
    Turn off the given handler.

    Args:
        name (str): Handler name.

    Returns:
        Handler or None: JSON handler
    """
    handler = get_handler(name)
    handler.active = False
    return handler


@six.add_metaclass(abc.ABCMeta)
class Handler(object):
    """
    JSON Handler

    This is an abstract class. It defines the required interface
    for a JSON handler. All subclasses must implement any abstract
    methods and/or properties.
    """

    def __init__(self, name=None):
        """
        Initialize handler.

        Args:
            name (str, optional): Handler name.
        """
        self._name = name
        self._active = True

    @property
    def name(self):
        """
        Get/set handler name.

        str: Handler name.
        """
        if not self._name:
            cls_name = self.__class__.__name__
            self._name = cls_name.replace('Handler', '').lower()

        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def active(self):
        """
        Get/set active state.

        bool: True if active, fales otherwise.
        """
        return self._active

    @active.setter
    def active(self, active):
        self._active = bool(active)

    @abc.abstractmethod
    def match(self, obj):
        """
        Match the given object.

        This method is used to determine whether this
        handler is used for the given object.

        Args:
            obj: Object to be encoded

        Returns:
            bool: True if this is a matching handler, false otherwise.
        """
        pass

    @abc.abstractmethod
    def encode(self, obj):
        """
        Encode the given object.

        Args:
            obj: Object to be encoded

        Returns:
            object: Encoded data object.
        """
        pass

    @abc.abstractmethod
    def decode(self, obj):
        """
        Decode the given object.

        Args:
            obj: Object to be decoded

        Returns:
            object: Decoded data object.
        """
        pass


@register('datetime')
class DateTimeHandler(Handler):
    """
    DateTime JSON Handler.

    This class is used to handle the encoding/decoding
    of date/datetime objects.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize datetiime handler.
        """
        super(DateTimeHandler, self).__init__(*args, **kwargs)
        self._fmt = None

    @property
    def fmt(self):
        """
        Get/set datetime format.
        """
        return self._fmt

    @fmt.setter
    def fmt(self, fmt):
        self._fmt = str(fmt) if fmt else None

    def match(self, obj):
        """
        Check if the given object is a datetime object.

        Args:
            obj: Object to be encoded

        Returns:
            bool: True if this is a matching handler, false otherwise.
        """
        return isinstance(obj, (datetime.date, datetime.datetime))

    def encode(self, obj):
        """
        Encode the given datetime object.

        Args:
            datetime.datetime: datetime object

        Returns:
            dict: Encoded datetime object.
        """
        if not self.fmt:
            data = obj.isoformat()
        else:
            data = obj.strftime(self.fmt)

        return {
            'type': type(obj).__name__,
            'data': data
        }

    def decode(self, obj):
        """
        Decode the given datetime object.

        Args:
            dict: Encoded datetime object.

        Returns:
            datetime.date or datetime.datetime: Decoded datetime object.
        """
        date_type = obj['type']
        valid_types = ['date', 'datetime']
        if date_type not in valid_types:
            msg = (
                'Invalid datetime encoding.'
                'Expected type key with one of {}'
            )
            msg = msg.format(valid_types)
            raise ValueError(msg)

        if date_type == 'date':
            return dateutil.parser.parse(obj['data']).date()
        else:
            return dateutil.parser.parse(obj['data'])


@register('dataclass')
class DataclassHandler(Handler):
    """
    Dataclass Tuple JSON Handler.

    This class is used to handle the encoding/decoding
    of `dataclass` objects.
    """

    def match(self, obj):
        """
        Check if the given object is a dataclass object.

        Args:
            obj: Object to be encoded

        Returns:
            bool: True if this is a matching handler, false otherwise.
        """
        if dataclasses:
            return dataclasses.is_dataclass(obj)

        return False

    def encode(self, obj):
        """
        Encode the given dataclass object.

        Args:
            dataclass: dataclass object

        Returns:
            dict: Encoded dataclass object.
        """
        return {
            'class_name': obj.__class__.__name__,
            'data': obj.__dict__
        }

    def decode(self, obj):
        """
        Decode the given dataclass object.

        Args:
            dict: Encoded dataclass object.

        Returns:
            dataclass: Decoded dataclass object.
        """
        name = obj['class_name']
        items = obj['data']
        cls = dataclasses.make_dataclass(name, items.keys())
        return cls(**items)

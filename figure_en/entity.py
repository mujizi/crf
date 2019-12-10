# -*- coding: UTF-8 -*-
import json
from .utils.constant import DEFAULT_TYPE


class Entity(object):
    def __init__(self, text, start, end, entity_type=DEFAULT_TYPE):
        self.__text = text
        self.__start = start
        self.__end = end
        self.__entity_type = entity_type

    @property
    def entity(self):
        return self.__text

    @entity.setter
    def entity(self, value):
        self.__check_text(value)
        self.__text = value

    @staticmethod
    def __check_text(value):
        if not isinstance(value, str):
            raise TypeError('entity text is not string.')
        if not value:
            raise ValueError('entity text is empty')

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__check_index(value)
        self.__start = value

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value):
        self.__check_index(value)
        self.__end = value

    @staticmethod
    def __check_index(value):
        if not isinstance(value, int):
            raise TypeError('entity end index is not integer.')
        if value < 0:
            raise ValueError('entity end index is less than zero.')

    @property
    def type(self):
        return self.__entity_type

    @type.setter
    def type(self, value):
        self.__check_entity_type(value)
        self.__entity_type = value

    @staticmethod
    def __check_entity_type(value):
        if not isinstance(value, str):
            raise TypeError('entity type is not string.')
        if not value:
            raise ValueError('entity type is empty.')

    def __str__(self):
        fmt = 'Entity(text="{entity}", start={start}, end={end}, type={type})'
        return fmt.format(entity=self.__text, start=self.__start, end=self.__end, type=self.__entity_type)

    def to_json(self):
        entity = {'entity': self.__text, 'start': self.__start,
                  'end': self.__end, 'type': self.__entity_type}
        return entity

    def from_json(self, object):
        if not isinstance(object, dict):
            raise TypeError('entity type is not dictionary')
        if 'entity' not in object:
            raise ValueError('key entity doesn\'t exist')
        if 'start' not in object:
            raise ValueError('key start doesn\'t exist')
        if 'end' not in object:
            raise ValueError('key end doesn\'t exist')
        if 'type' not in object:
            raise ValueError('key type doesn\'t exist')

        self.__check_text(object['entity'])
        self.__check_index(object['start'])
        self.__check_index(object['end'])
        self.__check_entity_type(object['type'])

        entity = Entity(object['entity'], object['start'], object['end'], object['type'])
        return entity

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise TypeError('item value must be string')
        if item not in {'entity', 'start', 'end', 'type'}:
            raise ValueError('item value must be in entity, start, end and type')

        if item == 'entity':
            value = self.__text
        elif item == 'start':
            value = self.__start
        elif item == 'end':
            value = self.__end
        else:
            value = self.__entity_type

        return value

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('key must be string')
        if key not in {'entity', 'start', 'end', 'type'}:
            raise ValueError('key not in entity, start, end and type')

        if key == 'entity':
            self.__check_text(value)
            self.__text = value
        elif key == 'start':
            self.__check_index(value)
            self.__start = value
        elif key == 'end':
            self.__check_index(value)
            self.__end = value
        else:
            self.__check_entity_type(value)
            self.__entity_type = value

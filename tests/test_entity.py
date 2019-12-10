# -*- coding: UTF-8 -*-
import json
from unittest import TestCase
from figure_en.entity import *


class TestEntity(TestCase):
    def test_init(self):
        entity = Entity('Google', 0, 6, 'COMPANY')
        self.assertEqual(entity.start, 0)
        self.assertEqual(entity['start'], 0)
        self.assertEqual(entity.end, 6)
        self.assertEqual(entity.entity, 'Google')
        self.assertEqual(entity.type, 'COMPANY')
        entity['start'] = 10
        self.assertEqual(entity.start, 10)
        self.assertEqual(entity['start'], 10)
        print(json.dumps([entity], default=Entity.to_json))

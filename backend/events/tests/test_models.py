import inspect
from typing import List, Dict, Tuple

from django.test import TestCase
from django.core.validators import ValidationError

# Do not use relative paths for import. This tests if the module name is correctly maintained.
from events.models import Event
from tests.generic.models_tests import model_basic_tests


class TestEventModel(TestCase):
    def test_basics(self):
        expected_field_names: List[str] = [
            'title',
            'slug',
            'location',
            'event_start_datetime',
            'event_end_datetime',
            'registration_start_datetime',
            'registration_end_datetime',
            'max_occupancy',
            'current_occupancy',
            'participants',
            'important_message',
            'description',
            'descr_truncate_num',
            'image',
            'image_height',
            'image_width',
        ]
        default_val_attrs: List[Tuple[str]] = [
            ('default_location', 'TBA'),
            ('min_descr_truncate_num', 50),
            ('default_image_size', 260),
        ]
        fields_len_dict: Dict[str, int] = {
            'title': 50,
            'slug': 60,
            'location': 100,
        }

        model_basic_tests(Event, expected_field_names, default_val_attrs, fields_len_dict)

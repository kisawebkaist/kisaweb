import pytest
import inspect
from typing import (
    Optional,
    NoReturn,
    Dict,
    List,
    Tuple,
    Union,
    Any,
)

from django.db.models import Model  # type: ignore
from django.core.validators import ValidationError  # type: ignore


def field_names_test(model, expected_field_names):
    field_names = [f.name for f in model._meta.get_fields()]
    for name in expected_field_names:
        assert name in field_names, f'"{name}" is not a field in {model}.'


def default_val_attrs_test(model, default_val_attrs):
    class_members = inspect.getmembers(model)
    for tup in default_val_attrs:
        assert tup in class_members, f'Either the name or the value of the attribute {tup} does not exist in {model}.'


@pytest.mark.django_db
def max_length_test(model, fields_len_dict: Dict[str, int]) -> Optional[NoReturn]:
    for key, val in fields_len_dict.items():
        string = 'x' * val
        data = { key: string }
        event = model(**data)
        try:
            event.full_clean()
        except ValidationError as e:
            assert key not in e.message_dict, f'Max length for {key} field in {model} is not at least {val}.'


def model_basic_tests(
    model,
    expected_field_names: List[str],
    default_val_attrs: List[Tuple[str, Any]],
    fields_len_dict: Dict[str, int],
) -> None:
    if not issubclass(model, Model):
        raise TypeError(f'{model} is not a Django model class')

    field_names_test(model, expected_field_names)
    default_val_attrs_test(model, default_val_attrs)
    max_length_test(model, fields_len_dict)

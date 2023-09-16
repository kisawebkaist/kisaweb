from importlib import import_module
import inspect

from django.test import TestCase
from django.urls import reverse, resolve


def test_events_urls():
    # Order of elements in tuples of urls:
    #   0: url name
    #   1: url route
    #   2: view function/class name
    #  -1: args/kwargs

    # for kwargs, integers have to written as string -> some issue with how resolve() works
    urls = [
        ('events', '/events/', 'EventList'),
        ('event_create', '/events/create-event/', 'EventCreate'),
        ('event_detail', '/events/some-slug/', 'EventDetail', {'slug': 'some-slug'}),
        ('modify_event_registration', '/events/modify-registration/10/', 'modify_registration', {'pk': '10'}),
        ('event_update', '/events/modify-event/some-slug/', 'EventUpdate', {'slug': 'some-slug'}),
        ('event_delete', '/events/delete-event/some-slug/', 'delete_event', {'slug': 'some-slug'}),
        (
            'modify_event_descr_truncate_num',
            '/events/modify-event-truncate-num/10/',
            'modify_descr_truncate_num',
            {'pk': '10'},
        ),
        (
            'modify_event_truncated_descr',
            '/events/modify-event-truncated-descr/10/',
            'modify_truncated_descr',
            {'pk': '10'},
        ),
    ]
    with_args_len = max([len(t) for t in urls])

    for tup in urls:
        resolver = resolve(tup[1])
        assert resolver.url_name == tup[0], f'URL name error'
        assert resolver.func.__name__ == tup[2], f'View class/function name error'

        if len(tup) == with_args_len:
            # assert resolver.kwargs == tup[-1], f'URL kwargs error'

            module_name = resolver.func.__module__
            object_name = resolver.func.__name__
            imported_object = getattr(import_module(module_name), object_name)

            if inspect.isclass(imported_object):
                bases = imported_object.__bases__
                if len(bases) == 1 and bases[0].__name__ == 'DetailView':
                    assert imported_object.slug_url_kwarg in tup[-1].keys(), (
                            f'slug_url_kwarg in {object_name} does not match url kwarg in urls.py')
            elif inspect.isfunction(imported_object):
                # inspect.signature used instead of inspect.getfullargspec because the latter does not show parameters after 'request' -> reason unknown
                for key in tup[-1].keys():
                    try:
                        args = inspect.signature(imported_object).parameters[key]
                    except KeyError:
                        raise KeyError(f'{object_name} does not have a parameter named {key}')


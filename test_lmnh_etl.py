import pytest
from lmnh_etl import key_validator, message_formatter, key_values, value_validator


def test_key_values_missing_keys():
    assert key_values({}) == {"at": "at", "val": "val", "site": "site",
                              "incident_type": "incident_type"}


def test_key_values():
    assert key_values({'at': '2025-03-11T12:30:56.967864+00:00',
                       'site': '4'}) == {'at': '2025-03-11T12:30:56.967864+00:00',
                                         'site': '4', "val": "val",
                                         "incident_type": "incident_type"}


def test_key_validator():
    input = {'at': '2025-03-11T12:30:56.967864+00:00',
             'site': '4', 'val': 1, 'incident_type': 'incident_type'}
    assert key_validator(input) == ''


def test_key_validator_no_keys():
    input = {"at": "at", "val": "val", "site": "site",
             "incident_type": "incident_type"}
    assert key_validator(input) == 'at, val, site'


def test_key_validator_no_site_keys():
    input = {"at": "at", "val": "val", "site": '4',
             "incident_type": "incident_type"}
    assert key_validator(input) == 'at, val'


def test_key_validator_no_type_keys():
    input = {"at": "at", "val": -1, "site": '4',
             "incident_type": "incident_type"}
    assert key_validator(input) == 'at, incident_type'


def test_message_formatter():
    input = {'at': '2025-03-11T12:30:56.967864+00:00',
             'site': '4', 'val': 1, 'incident_type': 'incident_type'}
    assert message_formatter(input) == {'at': '2025-03-11T12:30:56.967864+00:00',
                                        'site': 4, 'val': 1}


def test_message_formatter_zeros():
    input = {'at': '2025-03-11T12:30:56.967864+00:00',
             'site': '0', 'val': 0, 'incident_type': 'incident_type'}
    assert message_formatter(input) == {'at': '2025-03-11T12:30:56.967864+00:00',
                                        'site': 6, 'val': 5}


def test_message_formatter_zeros_incident():
    input = {'at': '2025-03-11T12:30:56.967864+00:00',
             'site': '0', 'val': -1, 'incident_type': 0}
    assert message_formatter(input) == {'at': '2025-03-11T12:30:56.967864+00:00',
                                        'site': 6, 'val': -1, 'type': 2}


def test_value_validator_type():
    input = {'at': '2025-03-11T12:30:56.967864+00:00',
             'site': '0', 'val': -1, 'incident_type': -1}
    assert value_validator(input) == 'type:-1'


def test_value_validator_all():
    input = {'at': '2025-03-11T12:30:56.967864+00:00',
             'site': '-1', 'val': -2}
    assert value_validator(input) == 'site:-1, val:-2'


def test_message_formatter():
    input = {'at': '2025-03-11T12:30:56.967864+00:00',
             'site': '0', 'val': 0, 'incident_type': 'incident_type'}
    message_formatter(input) == {'at': '2025-03-11T12:30:56.967864+00:00',
                                 'site': 6, 'val': 5}

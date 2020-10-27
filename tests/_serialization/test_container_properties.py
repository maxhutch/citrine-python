import pytest
import unittest

from citrine._serialization import properties

from ._data import VALID_SERIALIZATIONS
from ._utils import make_class_with_property


@pytest.mark.parametrize('sub_prop,sub_value,sub_serialized', VALID_SERIALIZATIONS)
def test_list_property_serde(sub_prop, sub_value, sub_serialized):
    prop = properties.List(sub_prop)
    value = [sub_value for _ in range(5)]
    serialized = [sub_serialized for _ in range(5)]
    assert prop.deserialize(serialized) == value
    assert prop.serialize(value) == serialized


@pytest.mark.parametrize('sub_prop,sub_value,sub_serialized', VALID_SERIALIZATIONS)
def test_object_property_serde(sub_prop, sub_value, sub_serialized):
    klass = make_class_with_property(sub_prop, 'some_property_name')
    prop = properties.Object(klass)
    instance = klass(sub_value)
    serialized = {'some_property_name': sub_serialized}
    assert prop.deserialize(serialized) == instance
    assert prop.serialize(instance) == serialized


@pytest.mark.parametrize('sub_prop,sub_value,sub_serialized', VALID_SERIALIZATIONS)
def test_optional_property(sub_prop, sub_value, sub_serialized):
    prop = properties.Optional(sub_prop)
    assert prop.deserialize(sub_serialized) == sub_value
    assert prop.serialize(sub_value) == sub_serialized
    assert prop.deserialize(None) is None
    assert prop.serialize(None) is None


@pytest.mark.parametrize('key_type,key_value,key_serialized', VALID_SERIALIZATIONS)
@pytest.mark.parametrize('value_type,value_value,value_serialized', VALID_SERIALIZATIONS)
def test_mapping_property(key_type, value_type, key_value, value_value, key_serialized, value_serialized):
    prop = properties.Mapping(key_type, value_type)
    value = {key_value: value_value}
    serialized = {key_serialized: value_serialized}
    assert prop.deserialize(serialized) == value
    assert prop.serialize(value) == serialized


@pytest.mark.parametrize('key_type,key_value,key_serialized', VALID_SERIALIZATIONS)
@pytest.mark.parametrize('value_type,value_value,value_serialized', VALID_SERIALIZATIONS)
def test_mapping_property_list_of_pairs(key_type, value_type, key_value, value_value, key_serialized, value_serialized):
    prop = properties.Mapping(key_type, value_type, ser_as_list_of_pairs = True)
    value = {key_value: value_value}
    serialized = [(key_serialized, value_serialized),]
    assert prop.deserialize(serialized) == value
    unittest.TestCase().assertCountEqual(prop.serialize(value), serialized)


def test_mapping_property_list_of_pairs_multiple():
    prop = properties.Mapping(properties.String, properties.Integer, ser_as_list_of_pairs = True)
    value = {'foo': 1, 'bar': 2}
    serialized = [('foo', 1), ('bar', 2)]
    assert prop.deserialize(serialized) == value
    unittest.TestCase().assertCountEqual(prop.serialize(value), serialized)

class dummyDescriptor(object):
    """docstring for dummyDescriptor"""
    dummy_map = properties.Mapping(properties.Float, properties.String)
    dummy_set = properties.Set(properties.Float)


def test_collection_setters():
    dummy_descriptor = dummyDescriptor()
    dummy_descriptor.dummy_map = {1: "1"}
    dummy_descriptor.dummy_set = {1}
    assert 1.0 in dummy_descriptor.dummy_map
    assert 1.0 in dummy_descriptor.dummy_set


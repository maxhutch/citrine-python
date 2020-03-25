"""Tools for working with Descriptors."""
from abc import abstractmethod
from typing import Type, List, Mapping  # noqa: F401
from uuid import UUID

from citrine._serialization.serializable import Serializable
from citrine._serialization.polymorphic_serializable import PolymorphicSerializable
from citrine._serialization import properties
from citrine.informatics.descriptors import Descriptor
from citrine.resources.file_link import FileLink


class DataSource(PolymorphicSerializable['DataSource']):
    """[ALPHA] A source of data for the AI engine.

    Data source provides a polymorphic interface for specifying different kinds of data as the
    training data for predictors and the input data for some design spaces.

    """

    @abstractmethod
    def _attrs(self) -> List[str]:
        pass  # pragma: no cover

    def __eq__(self, other):
        try:
            return all([
                self.__getattribute__(key) == other.__getattribute__(key) for key in self._attrs()
            ])
        except AttributeError:
            return False

    @classmethod
    def get_type(cls, data) -> Type[Serializable]:
        """Return the subtype."""
        if "type" not in data:
            raise ValueError("Can only get types from dicts with a 'type' key")
        types: List[Type[Serializable]] = [
            CSVDataSource, AraTableDataSource
        ]
        res = next((x for x in types if x.typ == data["type"]), None)
        if res is None:
            raise ValueError("Unrecognized type: {}".format(data["type"]))
        return res


class CSVDataSource(Serializable['CSVDataSource'], DataSource):
    """[ALPHA] A data source based on a CSV file stored on the data platform.

    Parameters
    ----------
    file_link: FileLink
        link to the CSV file to read the data from
    column_definitions: Mapping[str, Descriptor]
        Map the column headers to the descriptors that will be used to interpret the cell contents

    """

    typ = properties.String('type', default='csv_data_source', deserializable=False)
    file_link = properties.Object(FileLink, "file_link")
    column_definitions = properties.Mapping(
        properties.String, properties.Object(Descriptor), "column_definitions")

    def _attrs(self) -> List[str]:
        return ["file_link", "column_definitions", "typ"]

    def __init__(self,
                 file_link: FileLink,
                 column_definitions: Mapping[str, Descriptor]):
        self.file_link = file_link
        self.column_definitions = column_definitions


class AraTableDataSource(Serializable['AraTableDataSource'], DataSource):
    """[ALPHA] A data source based on an Ara table hosted on the data platform.

    TODO: replace "Ara" with whatever non-codename we pick for that component of the platform

    Parameters
    ----------
    table_id: UUID
        Unique identifier for the table
    table_version: int
        Version number for the table

    """

    typ = properties.String('type', default='hosted_table_data_source', deserializable=False)
    table_id = properties.UUID("table_id")
    table_version = properties.Integer("table_version")

    def _attrs(self) -> List[str]:
        return ["table_id", "table_version", "typ"]

    def __init__(self,
                 table_id: UUID,
                 table_version: int):
        self.table_id = table_id
        self.table_version = table_version

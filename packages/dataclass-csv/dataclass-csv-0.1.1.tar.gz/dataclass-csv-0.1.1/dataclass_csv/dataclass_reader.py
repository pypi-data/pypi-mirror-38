import dataclasses

from csv import DictReader

from .field_mapper import FieldMapper


class DataclassReader:
    def __init__(
        self,
        f,
        cls_mapper,
        fieldnames=None,
        restkey=None,
        restval=None,
        dialect='excel',
        *args,
        **kwds
    ):

        if not f:
            raise ValueError('The f argument is required')

        if cls_mapper is None or not dataclasses.is_dataclass(cls_mapper):
            raise ValueError('cls_mapper argument needs to be a dataclass')

        self.cls_mapper = cls_mapper
        self.optional_fields = self._get_optional_fields()
        self.field_mapping = {}

        self.reader = DictReader(
            f,
            fieldnames,
            restkey,
            restval,
            dialect,
            *args,
            **kwds,
        )

    def _get_optional_fields(self):
        return [
            field.name
            for field in dataclasses.fields(self.cls_mapper)
            if not isinstance(field.default, dataclasses._MISSING_TYPE)
        ]

    def _add_to_mapping(self, property_name, csv_fieldname):
        self.field_mapping[property_name] = csv_fieldname

    def _get_value(self, row, field):
        try:
            key = (
                field.name
                if field.name not in self.field_mapping.keys()
                else self.field_mapping.get(field.name)
            )
            value = row[key]
        except KeyError:
            if field.name in self.optional_fields:
                return field.default
            else:
                raise KeyError(
                    f'The value {field.name} is missing in the CSV file.'
                )
        else:
            if not value and field.name in self.optional_fields:
                return field.default
            elif not value and field.name not in self.optional_fields:
                raise ValueError(
                    (
                        f'The field {field.name} is required. Verify if any '
                        'row in the CSV file is missing this data.'
                    )
                )
            else:
                return value

    def _process_row(self, row):
        mapped_user = self.cls_mapper()

        for field in dataclasses.fields(self.cls_mapper):

            value = self._get_value(row, field)

            try:
                transformed_value = field.type(value)
            except ValueError:
                raise ValueError(
                    (
                        f'The field {field.name} is defined as {field.type} '
                        f'but received a value of type {type(value)}.'
                    )
                )
            else:
                setattr(mapped_user, field.name, transformed_value)

        return mapped_user

    def __next__(self):
        row = next(self.reader)
        return self._process_row(row)

    def __iter__(self):
        return self

    def map(self, csv_fieldname):
        return FieldMapper(
            lambda property_name: self._add_to_mapping(
                property_name, csv_fieldname
            )
        )

from dataclasses import dataclass


@dataclass
class Field:
    number: int
    name: str
    string: bool
    size: int


class RecordType:
    def __init__(self, name="", fields=[]):
        self.name = name
        self.fields = fields

    def field_widths(self):
        return tuple(x.size for x in self.fields)

    def field_names(self):
        return [x.name for x in self.fields if x.size > 0]

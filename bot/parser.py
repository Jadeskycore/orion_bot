from parse import *


class Parser:

    def __init__(self, header):
        self._commands = []
        self.header = header

    def parse(self, source):
        for command in self._commands:
            command.parse_source(source)

    def add_command(self, name, kind, destination=None):
        if kind == bool:
            self._commands.append(
                BoolCommand(self, name, destination)
            )
        elif kind == str:
            self._commands.append(
                ValueCommand(self, name, destination)
            )
        elif kind == tuple:
            self._commands.append(
                KeyValueCommand(self, name, destination)
            )
        else:
            return

    def get_help(self):
        help_strings = []
        for cmd in self._commands:
            help_strings.append(f"-*{cmd.name}*")
        return '\n'.join(help_strings)


class Command:
    def __init__(self, parser_cls, name, destination_field=None):
        self.parser = parser_cls
        self.name = name
        self.destination = (
            destination_field if destination_field
            else self.name
        )

    def parse_source(self, source):
        pass


class BoolCommand(Command):
    def parse_source(self, source):
        parse_result = parse(
            f"{self.parser.header} {{}}",
            source
        )
        if parse_result and parse_result[0] == self.destination:
            setattr(self.parser, self.destination, True)


class ValueCommand(Command):
    def parse_source(self, source):
        parse_result = parse(
            f"{self.parser.header} {self.destination} {{}}",
            source
        )
        if parse_result and parse_result[0]:
            setattr(self.parser, self.destination, parse_result[0])


class KeyValueCommand(Command):
    def parse_source(self, source):
        parse_result = parse(
            f"{self.parser.header} {self.destination} {{}} {{}}",
            source
        )
        if parse_result and parse_result[0] and parse_result[1]:
            setattr(self.parser, self.destination, (parse_result[0], parse_result[1]))

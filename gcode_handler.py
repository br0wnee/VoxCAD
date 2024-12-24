from settings import *
import re


class GCodeHandler:
    def __init__(self):
        self.commands = []

    def parse(self, gcode_file):
        with open(gcode_file, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith(";"):  # Ignore empty or comment lines
                    continue

                parsed_line = self.parse_line(line)
                if parsed_line:
                    self.commands.append(parsed_line)

    def parse_line(self, line):
        pattern = r"([G,M]\d+|\w)\s*([-+]?\d*\.\d+|\d+)"
        matches = re.findall(pattern, line)

        if not matches:
            return None

        command = {}
        for match in matches:
            key, value = match
            if value.isdigit() or "." in value:
                value = float(value)
            command[key] = value

        return command

    def get_commands(self):
        return self.commands


# Usage:
gcode_parser = GCodeHandler()
gcode_parser.parse("test.gcode")

for command in gcode_parser.get_commands():
    print(command)

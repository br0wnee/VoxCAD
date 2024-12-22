from settings import *
import re


class GCodeHandler:
    def __init__(self, gcode_file):
        self.gcode_file = gcode_file
        self.commands = []

    def parse(self):
        with open(self.gcode_file, "r") as file:
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
gcode_parser = GCodeHandler("test.gcode")
gcode_parser.parse()

for command in gcode_parser.get_commands():
    print(command)

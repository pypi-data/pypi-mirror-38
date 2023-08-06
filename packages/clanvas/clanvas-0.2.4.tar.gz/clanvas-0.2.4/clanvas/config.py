import io
from typing import Union, Dict


def parse_clanvas_config(input: io.TextIOBase) -> ((str, Dict[str, Dict[str, str]]), str):
    config = dict()
    default = None
    for line_number, line in enumerate(input):
        tokens = line.split()
        if len(tokens) == 0:
            continue
        elif len(tokens) == 1:
            return None, f"Key {tokens} has no value (line {line_number})"
        elif tokens[0].lower() == 'host' or tokens[1].lower() == 'host':
            if current_host is not None:
                config[current_host] = current_host_dict

            if len(tokens) == 2:
                current_host = tokens[1]
            elif len(tokens) == 3:
                if tokens[0].lower() == 'default':
                    current_host = tokens[2]
                    default = current_host
                else:
                    return None, f'Invalid modifier on host "{tokens[0]} (line {line_number})'

            current_host_dict = dict()


def main():
    pass


if __name__ == "__main__":
    main()

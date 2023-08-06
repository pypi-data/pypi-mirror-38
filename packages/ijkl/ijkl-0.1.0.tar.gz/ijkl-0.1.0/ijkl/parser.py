import os
import re

def parse(template):
    """
    Parses template and remove comments.
    """
    config = template.splitlines(True)
    parsed = []
    for line in config:
        if re.match(r'(^#|^\s$)', line):
            continue
        elif re.match(r'^include*', line):
            if re.match(r'^include \S+$', line):
                parsed.append(include(line.split()[1]))
            else:
                raise WrongSyntax("""
                    Error: include command takes exactly onefile as argument.
                """)
        else:
            parsed.append(line)

    return ''.join(parsed)


def include(name, folder='~/.config/i3'):
    """
    Include external file
    """
    name = os.path.expanduser(name)

    if os.path.exists(name):
        include_file = open(name)
    elif os.path.exists(os.path.join(folder, name)):
        include_file = open(os.path.join(folder, name))
    else:
        raise OSError('Error: ' + name + ' file not found!')

    contents = include_file.read()
    include_file.close()

    return parse(contents)


class WrongSyntax(Exception):
    """
    Exception for wrong syntax
    """
    pass

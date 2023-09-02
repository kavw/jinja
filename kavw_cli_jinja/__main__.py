import os
import sys
import json
from dataclasses import dataclass
import jinja2
import kavw_cli_jinja.errors as errors


def main_help():
    cmd = 'poetry run py -m ' + __package__
    return """\
Usage:
    {cmd} [PATH] [JSON] > output_file

Example:
    {cmd} /path/to/template '{{\"username\":\"John\"}}' > output.txt
    """.format(cmd=cmd)


@dataclass
class ArgFile:
    dir: str
    name: str


def resolve_file(path: str) -> ArgFile:
    dirname = resolve_dir(os.path.dirname(path))
    name = os.path.basename(path)
    return ArgFile(dirname, name)


def resolve_dir(name: str) -> str:
    if os.path.isabs(name):
        if os.path.isdir(name):
            return name
        raise errors.InvalidDir(f"Given path '{name}' is not a directory")

    if name.startswith('~'):
        return os.path.abspath(os.path.expanduser(os.path.expandvars(name)))

    return os.path.abspath(name)


def resolve_args(path: str, data: str) -> tuple[ArgFile, dict]:
    file = resolve_file(path)
    full_path = file.dir + '/' + file.name
    if not os.path.isfile(full_path):
        raise errors.InvalidPath(f"Given path {path} is not a file")

    data = json.loads(data)
    if not isinstance(data, dict):
        raise errors.InvalidJson("Given JSON is supposed to be converted into a dict")

    return file, data


def main(params):
    if len(params) < 3:
        raise errors.TooFewArguments("Missing required arguments")

    if len(params) > 3:
        raise errors.TooMuchArguments("Too much arguments")

    args = resolve_args(params[1], params[2])
    loader = jinja2.FileSystemLoader(searchpath=args[0].dir)
    env = jinja2.Environment(loader=loader)
    tpl = env.get_template(args[0].name)
    print(tpl.render(**args[1]))


if __name__ == '__main__':
    try:
        main(sys.argv)
    except errors.ValidationError as e:
        print(e)
        print(main_help())
        sys.exit(1)


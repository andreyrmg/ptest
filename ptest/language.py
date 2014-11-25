from configparser import ConfigParser
import os
from subprocess import check_output, CalledProcessError, STDOUT


class CompilationError(Exception):
    def __init__(self, cmd, status, output):
        self.cmd = cmd
        self.status = status
        self.output = output

    def __str__(self):
        return "{}\nexit code: {}, output: {}".format(self.cmd, self.status, self.output)


class Compiler(object):

    def __init__(self, name, build, build_args, build_output_arg):
        super().__init__()
        self._name = name
        self._build = build
        self._build_args = build_args.split(',')
        self._build_output_arg = build_output_arg

    def prepare(self, working_dir, source):
        args = [self._build]
        args.extend(self._build_args)
        args.append(self._build_output_arg + working_dir)
        args.append(source)
        try:
            check_output(args, stderr=STDOUT, cwd=working_dir, universal_newlines=True)
            _, filename = os.path.split(source)
            filename, _ = os.path.splitext(filename)
            return [os.path.join(working_dir, filename)]
        except CalledProcessError as e:
            raise CompilationError(e.cmd, e.returncode, e.output)

    @property
    def name(self):
        return self._name


def load_from_config(config):
    return dict((section, Compiler(section, **config[section])) for section in config.sections())


def load_from_file(filename):
    config = ConfigParser()
    config.read(filename)
    return load_from_config(config)


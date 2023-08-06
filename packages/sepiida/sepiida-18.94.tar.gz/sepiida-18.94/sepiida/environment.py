import os
import sys
from pathlib import Path

import attrdict


class Undefined():
    pass

class UndefinedError(Exception):
    "Raised when a required setting is not provided"
    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

class ParseError(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

class Specification():
    '''Contains Key/Value pairs of 'VARIABLE_STRING : seppida.Variable
    objects for enviroment variables and secrets. '''


    def __init__(self, **kwargs):
        self.kwargs = kwargs


    def parse(self):
        "Parse the variables that are defined in the given spec from the environment"
        results = attrdict.AttrDict()
        errors = set()
        for k, v in self.kwargs.items():
            try:
                results[k] = v.parse(os.environ.get(k))
            except ValueError as e:
                errors.add(ValueError("The value for {} was invalid: {}".format(k, e)))
            except UndefinedError:
                errors.add(UndefinedError("The variable {} was undefined and has no default value".format(k)))
        if errors:
            raise ParseError(errors)
        return results


    def load_secrets(self):
        '''Tries to match and load docker secrets based on expected
        environment variables. Load them if match and possible. See design/ENV_FROM_SECRETES.md'''
        results = attrdict.AttrDict()
        errors = set()
        for k, v in self.kwargs.items():
            try:
                filepath = Path(f"/run/secrets/{k}")
                if filepath.is_file():
                    with filepath.open('r') as fh:
                        data = fh.read()
                        results[k] = v.parse(data)
            except ValueError as e:
                errors.add(ValueError("The value for {} was invalid: {}".format(k, e)))
        if errors:
            raise ParseError(errors)
        return results


class Variable():
    "A single environment variable"
    def __init__(self, default=Undefined, parser=None, docs=None):
        self.default = default
        self.docs    = docs
        self.parser  = parser

    def parse(self, value):
        "Parse the given value or raise ValueError"
        if value is None:
            if self.default is Undefined:
                raise UndefinedError
            value = self.default
        return self.parser(value) if self.parser else value


class VariableInteger(Variable):
    def parse(self, value):
        return int(super().parse(value))


class VariableBoolean(Variable):
    def parse(self, value):
        value = super().parse(value)
        try:
            return int(value) != 0
        except ValueError:
            if value not in ('t', 'f', 'T', 'F', 'True', 'False', 'true', 'false'):
                raise ValueError("The value should be either '1' or '0'")
            return value[0] in ('t', 'T')


class VariableFloat(Variable):
    def parse(self, value):
        return float(super().parse(value))


class VariableList(Variable):
    def parse(self, value):
        val = super().parse(value)
        return val.split(';')

#common specification used for all sepiida services
DEFAULT_SPEC = Specification(
    API_TOKEN       = Variable('some api token'),
    ENVIRONMENT     = Variable('testing'),
    SECRET_KEY      = Variable('keep it secret, keep it safe'),
    SEPIIDA_JWT_AUD = Variable(''),
    SEPIIDA_JWT_KEY = Variable(''),
    SERVER_NAME     = Variable('sepiida.service'),
    STORAGE_SERVICE = Variable('https://woodhouse.service/'),
    TRUSTED_DOMAINS = VariableList('service;example.com;another-example.com'),
    USER_SERVICE    = Variable('https://users.service/'),
    SSL             = VariableBoolean(1), #defaults to ON
)

def parse(spec):
    '''
    @param spec: Specification object from a sub-class
    @return Specification object , mix-in of base specification and passed specification
    '''
    default_settings = {}
    try:
        default_settings = DEFAULT_SPEC.parse()
        settings = spec.parse()
        default_settings.update(settings)
        parse.settings = default_settings
    except ParseError as parse_error:
        message = (
            "The program cannot start because there were errors parsing the "
            "settings from environment variables: \n\t{}"
        ).format('\n\t'.join([str(e) for e in parse_error.errors]))
        sys.exit(message)
    try :
        # secrets  from docker secrets system
        secrets = DEFAULT_SPEC.load_secrets()
        spec_secrets = spec.load_secrets()
        secrets.update(spec_secrets)
        if default_settings is not None:
            default_settings.update(secrets)
    except ParseError as parse_error:
        message = (
            "The program cannot start because there were errors parsing the "
            "settings from docker secrets: \n\t{}"
        ).format('\n\t'.join([str(e) for e in parse_error.errors]))
        sys.exit(message)
    return default_settings

# global singleton, not an indent mistake
parse.settings = None

def get():
    if not parse.settings:
        raise Exception((
            "You have attempted to access the environment settings without having "
            "first parsed them from a specification. Please first call parse(spec) "
            "with a valid environment specification before calling the get() function"
        ))
    return parse.settings

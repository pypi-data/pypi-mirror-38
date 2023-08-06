from struct import calcsize, pack, unpack
from time import sleep
from types import MethodType

from serial import Serial
from serial.serialutil import SerialException


_version = '2.0.1'

_list_req = 0xff
_end_of_string = '\0'


def _cast(c_type):
    """Select the appropriate casting function given a C type.

    :arg str c_type: C type.

    :returns obj: Casting function.
    """
    if c_type[0] in ['c', 's']:
        return str
    if c_type[-1] in ['f', 'd']:
        return float
    return int


def _type_name(c_type):
    """Python type name of a C type.

    :arg str c_type: C type.

    :returns str: Python type name.
    """
    if not c_type:
        return ''
    return _cast(c_type).__name__


def _strip_split(string, delimiter):
    return list(map(lambda x: x.strip(), string.split(delimiter)))


def _parse_signature(index, signature):
    """Parse a C function signature string.

    :arg int index: Function index.
    :arg str signature: Function signature.

    :returns dict: Method object.
    """
    method = {
        'doc': '',
        'index': index,
        'name': 'method{}'.format(index),
        'parameters': [],
        'return': {'doc': ''}}

    method['return']['fmt'], parameters = signature.split(':')
    method['return']['typename'] = _type_name(method['return']['fmt'])

    for i, type_ in enumerate(parameters.split()):
        method['parameters'].append({
            'doc': '',
            'name': 'arg{}'.format(i),
            'fmt': type_,
            'typename': _type_name(type_)})

    return method


def _add_doc(method, doc):
    """Add documentation to a method object.

    :arg dict method: Method object.
    :arg str doc: Method documentation.
    """
    parts = list(map(lambda x: _strip_split(x, ':'), doc.split('@')))

    if list(map(lambda x: len(x), parts)) != [2] * len(parts):
        return

    method['name'], method['doc'] = parts[0]

    index = 0
    for part in parts[1:]:
        name, description = part

        if name != 'return':
            if index < len(method['parameters']):
                method['parameters'][index]['name'] = name
                method['parameters'][index]['doc'] = description
            index += 1
        else:
            method['return']['doc'] = description


def _parse_line(index, line):
    """Parse a method definition line.

    :arg int index: Line number.
    :arg str line: Method definition.

    :returns dict: Method object.
    """
    signature, description = line.strip(_end_of_string).split(';', 1)

    method = _parse_signature(index, signature)
    _add_doc(method, description)

    return method


def _make_docstring(method):
    """Make a docstring for a function.

    :arg dict method: Method object.

    :returns str: Function docstring.
    """
    help_text = ''

    if method['doc']:
        help_text += method['doc']

    if method['parameters']:
        help_text += '\n'

    for parameter in method['parameters']:
        help_text += '\n:arg {} {}:'.format(
            parameter['typename'], parameter['name'])
        if parameter['doc']:
            help_text += ' {}'.format(parameter['doc'])

    if method['return']['fmt']:
        help_text += '\n\n:returns {}:'.format(method['return']['typename'])
        if method['return']['doc']:
            help_text += ' {}'.format(method['return']['doc'])

    return help_text


class Interface(object):
    def __init__(self, device, baudrate=9600):
        """Initialise the class.

        :arg str device: Serial device name.
        :arg int baudrate: Baud rate.
        """
        try:
            self._connection = Serial(device, baudrate)
        except SerialException as error:
            raise IOError(error.strerror.split(':')[0])
        sleep(1)

        self.methods = self._get_methods()
        for method in self.methods.values():
            setattr(self, method['name'], MethodType(self._call(method), self))

        device_version = self.call_method('version')
        if device_version != _version:
            raise ValueError(
                'version mismatch (device: {}, client: {})'.format(
                    device_version, _version))

    def _read_str(self):
        """Read a delimited string from serial.

        :returns str: String.
        """
        data = ''

        while True:
            char = self._connection.read().decode('utf-8')
            if char == _end_of_string:
                break
            data += char

        return data

    def _select(self, index):
        """Initiate a remote procedure call, select the method.

        :arg int index: Method index.
        """
        self._connection.write(pack('B', index))

    def _write_parameter(self, param_type, param_value):
        """Provide parameters for a remote procedure call.

        :arg str param_type: Type of the parameter.
        :arg str param_value: Value of the parameter.
        """
        if param_type == 's':
            self._connection.write(
                (param_value + _end_of_string).encode('utf-8'))
            return
        self._connection.write(
            pack(param_type, _cast(param_type)(param_value)))

    def _read_value(self, return_type):
        """Read a return value from a remote procedure call.

        :arg str return_type: Return type.

        :returns any: Return value.
        """
        if return_type == 's':
            return self._read_str()
        return unpack(
            return_type, self._connection.read(calcsize(return_type)))[0]

    def _get_methods(self):
        """Get remote procedure call methods.

        :returns dict: Method objects indexed by name.
        """
        self._select(_list_req)

        methods = {}
        index = 0
        while True:
            line = self._read_str()
            if not line:
                break
            method = _parse_line(index, line)
            methods[method['name']] = method
            index += 1

        return methods

    def _call(self, method, *args):
        """Make a member function for a method.

        :arg dict method: Method object.
        :arg any *args: Parameters for the method.

        :returns function: New member function.
        """
        def call(self, *args):
            return self.call_method(method['name'], *args)

        call.__name__ = method['name']
        call.__doc__ = _make_docstring(method)

        return call

    def call_method(self, name, *args):
        """Execute a method.

        :arg str name: Method name.
        :arg list *args: Method parameters.

        :returns any: Return value of the method.
        """
        if name not in self.methods:
            raise ValueError('invalid method name: {}'.format(name))
        method = self.methods[name]

        parameters = method['parameters']
        if len(args) != len(parameters):
            raise TypeError(
                '{} expected {} arguments, got {}'.format(
                    name, len(parameters), len(args)))

        # Call the method.
        self._select(method['index'])

        # Provide parameters (if any).
        if method['parameters']:
            for index, parameter in enumerate(method['parameters']):
                self._write_parameter(parameter['fmt'], args[index])

        # Read return value (if any).
        if method['return']['fmt']:
            return self._read_value(method['return']['fmt'])
        return None

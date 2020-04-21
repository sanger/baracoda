import re
from baracoda.exceptions import WrongPrefixError

class HeronFormatter:

    def __init__(self, params):
        if self.validate_params(params):
            self.prefix = params['prefix']
        else:
            raise WrongPrefixError()
            
    def validate_params(self, params):
        if params is None:
            return False
        if not 'prefix' in params:
            return False
        if not type(params['prefix']) == str:
            return False
        expr = re.compile("^[A-Z0-9]{1,10}$")
        return bool(expr.match(params['prefix']))

    def hex_to_int(self, val: str):
        return int(val, 16)

    def checksum(self, hex_str: str):
        pos = 0
        even = odd = 0
        for char in reversed(hex_str):
            if (pos % 2) == 0:
                even += self.hex_to_int(char)
            else:
                odd += self.hex_to_int(char)
            pos += 1
        val = ((odd * 3) + even) % 16
        
        if (val != 0):
            return format((16 - val), 'X')
        else:
            return format(val, 'X')

    def barcode(self, value: str):
        return "".join([self.prefix, "-", value, self.checksum(value)])


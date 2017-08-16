from ..simple import MungSubstitutor


class MungSubstitutorCommon(MungSubstitutor):

    substitution_table_common = {
        'a': '@',
        'b': '8',
        'd': '6',
        'e': '3',
        'g': '9',
        'i': '1',
        'l': '1',
        'o': '0',
        'q': '9',
        's': '$',
        '0': 'O',
        '1': 'I',
        '3': 'E',
        'A': '@',
        'E': '3',
        'I': '1',
        'O': '0',
        'S': '2'
    }

    def substitute(self, pwd):
        return self.munger(pwd, self.substitution_table_common.iteritems())



class MungSubstitutor():

    substitution_table_simple = {
        'a': '@',
        'b': '8',
        'c': '(',
        'd': '6',
        'e': '3',
        'f': '#',
        'g': '9',
        'h': '#',
        'i': '1',
        'j': '!',
        'k': '<',
        'l': '1',
        'o': '0',
        'q': '9',
        's': '$',
        't': '+',
        'v': '>',
        'w': 'uu',
        'x': '%',
        '/': '-',
        '-': '/',
        '0': 'O',
        '1': 'I',
        '3': 'E',
        'A': '@',
        'B': '8',
        'C': '(',
        'E': '3',
        'I': '1',
        'O': '0',
        'S': '2'
    }

    def substitute(self, pwd):
        return self.munger(pwd, self.substitution_table_simple.iteritems())

    def munger(self, pwd, table):
        """
        Function for munging a
        password string
        """
        munged_pwd = pwd
        for letter, replacement in table:
            munged_pwd = munged_pwd.replace(letter, replacement)

        return munged_pwd

import random
from ..simple import MungSubstitutor


class MungSubstitutorRandom(MungSubstitutor):
    """
    SubClasses MungSubstituor to give
    us random values from the simple
    munger
    """

    def substitute(self, pwd):
        """
        Random samples 3 items
        from parent class simple
        substitution table
        """

        random_simple_table = random.sample(
            self.substitution_table_simple.items(), 3)
        return self.munger(pwd, random_simple_table)

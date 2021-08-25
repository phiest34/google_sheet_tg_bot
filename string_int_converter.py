class String_int_converter:
    def __init__(self):
        self.data = {}

    def set_string(self, string):
        self.data[string] = self.__generate_int(string)

    def get_int(self, string):
        value = self.data[string]
        return value if value is not None else -1

    def get_string(self, int_value):
        for key, value in self.data.items():
            if value == int_value:
                return key
        return ''

    def __generate_int(self, string):
        return hash(string)

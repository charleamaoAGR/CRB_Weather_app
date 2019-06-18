class GroupedArray:

    def __init__(self, identifiers, is_scalar=False):
        self.data_dict = {}

        for each_identifier in identifiers:
            self.data_dict[each_identifier] = []

        self.size = len(identifiers)
        self.is_scalar = is_scalar

    def add_identifier(self, identifier):

        if identifier not in self.data_dict.keys():
            self.data_dict[identifier] = []

    def insert_data(self, identifier, data):

        if self.is_scalar:
            self.data_dict[identifier].append(data)
            self.size += 1
        else:
            if isinstance(data, list):
                self.data_dict[identifier].append(data)
                self.size += 1
            else:
                raise Exception('Expected data of Type: List.')

    def get_data(self, identifier):
        return self.data_dict[identifier]


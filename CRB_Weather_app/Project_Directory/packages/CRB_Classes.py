from subprocess import call


class GroupedArray:

    def __init__(self, identifiers=[], is_scalar=False):
        self.data_dict = {}
        self.identifiers = identifiers

        for each_identifier in identifiers:
            self.data_dict[each_identifier] = []

        self.size = len(identifiers)
        self.is_scalar = is_scalar

    def add_identifier(self, identifier):

        if identifier not in self.data_dict.keys():
            self.identifiers.append(identifier)
            self.data_dict[identifier] = []

    def insert_data(self, identifier, data):

        self.add_identifier(identifier)
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

    def get_identifiers(self):
        return self.identifiers


class BatchFile:

    def __init__(self, working_directory):
        self.working_directory = working_directory
        self.batch_contents = "cd %s\n" % working_directory
        self.file_path = None

    def insert_command(self, command):
        self.batch_contents = self.batch_contents + command + '\n'

    def export(self, file_name, folder_path="SELF"):
        if folder_path == 'SELF':
            self.file_path = self.working_directory + '\\' + file_name
        else:
            self.file_path = folder_path + '\\' + file_name
        with open(self.file_path, 'w+') as output_batch:
            output_batch.write(self.batch_contents)

    def run(self):
        if self.file_path is not None:
            call(self.file_path)
        else:
            raise Exception("BatchFile object was not exported prior to run command.")

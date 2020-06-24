import configparser


def read_data(data_file):

    def process_data(line):
        start, end, length = line.split(',')
        return int(start), int(end), float(length)

    with open(data_file, 'r') as file:
        return [process_data(line) for line in file]

def parse_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config
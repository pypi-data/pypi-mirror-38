# Create a namespace to be passed
from main import main


class cust_args():
    # Class to imitate a args

    def __init__(self, SONG):
        self.SONG_NAME = SONG['name']
        self.batch = SONG['batch']
        self.nolocal = SONG['nolocal']
        self.quiet = SONG['quiet']
        self.setup = SONG['setup']
        self.url = SONG['url']


def make_cust_args(song_name):
    # Function to make custom args
    song_dict = {'name': song_name,
                'batch': None,
                'nolocal': False,
                'quiet': False,
                'setup': False,
                'url': None}
    new_args = cust_args(song_dict)
    return new_args


def call_main(song):
    # Call main
    main(make_cust_args(song))


def read_and_call(filename):
    # Open the file
    READ_STREAM = open(filename, 'r')
    while True:
        line = READ_STREAM.readline()
        if not line:
            break
        call_main(line)
    # Not really necessary but srill
    READ_STREAM.close()


if __name__ == '__main__':
    read_and_call('nana.txt')

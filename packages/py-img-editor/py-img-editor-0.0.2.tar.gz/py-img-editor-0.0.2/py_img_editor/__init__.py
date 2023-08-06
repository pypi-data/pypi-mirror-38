from subprocess import check_call
from argparse import ArgumentParser
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def start():
    with open(os.devnull, 'w') as f:
        check_call('/tmp/uwsgi --ini {}'.format(os.path.join(PROJECT_DIR, 'uwsgi.ini')).split(), stdout=f)
    print('Running py-img-editor at http://127.0.0.1:8000/')


def stop():
    with open(os.devnull, 'w') as f:
        check_call('/tmp/uwsgi --stop /tmp/py-img-editor.pid'.split(), stdout=f)
        os.remove(os.path.join(PROJECT_DIR, 'temp.png'))
    print('py-img-editor stopped.')


def main():
    parser = ArgumentParser()
    parser.add_argument('--start', action='store_true')
    parser.add_argument('--stop', action='store_true')

    args = parser.parse_args()
    if args.start:
        start()
    if args.stop:
        stop()


if __name__ == '__main__':
    main()

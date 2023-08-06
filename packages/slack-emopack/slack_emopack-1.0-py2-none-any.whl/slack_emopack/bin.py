from slack_emopack.Importer import Importer
from slack_emopack.IconFetcher import IconFetcher
from getpass import getpass
import sys
import os
import string
import argparse


inp = raw_input  # noqa F821

parser = argparse.ArgumentParser()
args = parser.parse_args()


def status(added, emojis):
    sys.stdout.write('uploading to slack.. {}/{}\r'.format(
        len(added),
        len(emojis)
    ))
    sys.stdout.flush()


def run():
    importer = Importer(
        os.environ.get('SLACK_URL') or inp('Slack url: '),
        os.environ.get('SLACK_EMAIL') or inp('Email: '),
        getpass('Password: ')
    )

    importer.status = status

    iconfetcher = IconFetcher()
    icons = []

    for char in string.ascii_lowercase:
        icons += iconfetcher.get_icons(char)
        print('Found: {} icons for: {}'.format(len(icons), char))

    icons = list(set(icons))

    print('Will import: {} icons.'.format(len(icons)))
    importer.login()
    importer.upload_emojis(icons)

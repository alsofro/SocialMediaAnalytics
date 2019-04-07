from argparse import FileType
from sys import stdin
import time

from django.core.management.base import BaseCommand
from dataqueryapp.utils import sanitize_user_input


file_name = 'popular_groups'


class Command(BaseCommand):
    help = 'This command will download vk_groups data'

    def handle(self, *args, **options):
        file_name = options['input']
        groups = file_name.read().split()
        print(">>>>", repr(groups))
        for group in groups:
            print(group)
            try:
                sanitize_user_input(group)
            except:
                time.sleep(1)
                sanitize_user_input(group)

    def add_arguments(self, parser):
        parser.add_argument('input', nargs='?', type=FileType('r'),
                            default=stdin)


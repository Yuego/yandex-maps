#!/usr/bin/env python
#import os
import sys
from django.core.management import execute_from_command_line

sys.argv.insert(1, 'test')

if len(sys.argv) == 2:
    sys.argv.append('yandex_maps')
    sys.argv.append('test_app')

if __name__ == "__main__":
    execute_from_command_line()


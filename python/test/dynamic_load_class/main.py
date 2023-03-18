#!/usr/bin/env python3

import sys
import utils.test_classes as test_module

try:
    class_name = sys.argv[1]
    if class_name not in ('A', 'B', 'D'):
        raise ValueError
except Exception as e:
    print('Run with 1 argument that must be A or B')
    print(e)
    sys.exit(1)

selected_class = getattr(test_module, class_name)
c = selected_class()

print(c.value)

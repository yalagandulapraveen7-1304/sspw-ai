import os
import sys
import runpy

if __name__ == '__main__':
    src_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'app.py')
    runpy.run_path(src_file, run_name='__main__')

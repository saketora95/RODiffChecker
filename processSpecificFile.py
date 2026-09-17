import os
import sys
import datetime

import function.file_process as fp
import function.iteminfo_effect_replace as iteminfo_replace

ENCODING = 'utf-8'
DATETIME_TEXT = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
EXECUTE_PATH = os.path.abspath(os.path.dirname(__file__)) + '\\'
if getattr(sys, 'frozen', False):
    EXECUTE_PATH = os.path.dirname(sys.executable) + '\\'
OUTPUT_PATH = EXECUTE_PATH + 'output\\'

fp.create_dir(OUTPUT_PATH)

iteminfo_replace.replace_file(f'{EXECUTE_PATH}kr_info.txt', f'{OUTPUT_PATH}TargetResult.txt', ENCODING)
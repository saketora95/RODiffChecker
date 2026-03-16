import os
import shutil
import glob

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def is_file_exist(file_path, file_name):
    return os.path.exists(file_path + file_name)

def copy_to(input_file, target_file):
    shutil.copy(input_file, target_file)
    print(f'  複製檔案: {target_file}')

def get_file_list(dir_path, prefix, file_ext_name='*'):
    search_pattern = os.path.join(dir_path, f"{prefix} *.{file_ext_name}")
    file_list = glob.glob(search_pattern)
    return file_list

def maintain_file_limit(dir_path, prefix, max_count, file_ext_name='*'):
    file_list = get_file_list(dir_path, prefix, file_ext_name)
    while len(file_list) > max_count:
        remove_target = file_list[0]
        os.remove(file_list[0])
        del file_list[0]
        print(f'  刪除檔案: {remove_target}')

def get_newest_file(dir_path, prefix, file_ext_name='*'):
    file_list = get_file_list(dir_path, prefix, file_ext_name)
    return file_list[-1]

def parse_lub_to_lua(parser_path, lub_file_path):
    parse_command = f'{parser_path} "{lub_file_path}" > "{lub_file_path[:-4]}.lua"'
    os.system(parse_command)
    print(f'  生成檔案: {lub_file_path[:-4]}.lua')

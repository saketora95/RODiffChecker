import difflib

def read_file(input_file_path, encoding='utf-8'):
    prop_file_lines = open(input_file_path, 'r', encoding=encoding).readlines()

    data_dict = {}
    item_id = ''
    in_target_area = False
    for i in range(0, len(prop_file_lines)):
        if prop_file_lines[i] == 'Item = {\n':
            in_target_area = True
            continue
        
        if not in_target_area:
            continue

        if prop_file_lines[i].startswith('SkillGroup'):
            break

        front_brackets_index = prop_file_lines[i].find('[')
        if front_brackets_index != -1:
            item_id = prop_file_lines[i][front_brackets_index + 1:prop_file_lines[i].find(']')]
            if item_id not in data_dict:
                data_dict[item_id] = ''
    
        data_dict[item_id] += prop_file_lines[i]
    return data_dict

def compare_dict(old_data_dict, new_data_dict, result_path):
    write_file = open(result_path, 'w', encoding='utf-8')

    for old_key in old_data_dict:
        if old_key not in new_data_dict:
            write_file.write(f'# {old_key} (資料移除)\n{old_data_dict[old_key]["raw_text"]}\n\n----- ----- -----\n\n')
            print(f'    - 發現 [ 資料移除 ]: {old_key}')

    for new_key in new_data_dict:
        if new_key in old_data_dict and old_data_dict[new_key] != new_data_dict[new_key]:
            differ = difflib.Differ()
            diff = differ.compare(old_data_dict[new_key].splitlines(), new_data_dict[new_key].splitlines())

            write_file.write('# {} (內容變更)\n{}\n\n----- ----- -----\n\n'.format(
                new_key,
                '\n'.join([line for line in diff if not line.startswith('? ')])
            ))
            print(f'    - 發現 [ 內容變更 ]: {new_key}')
            continue

        if new_key not in old_data_dict:
            write_file.write(f'# {new_key} (新增資料)\n{new_data_dict[new_key]["raw_text"]}\n\n----- ----- -----\n\n')
            print(f'    - 發現 [ 新增資料 ]: {new_key}')
            continue
    
    write_file.write('文件到此結束。')
    print(f'  生成比對結果: {result_path}')

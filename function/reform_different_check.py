import difflib

def read_file(input_file_path, encoding='utf-8'):
    reform_file_lines = open(input_file_path, 'r', encoding=encoding).readlines()

    data_dict = {}
    temp_dict = {
        'id': '',
        'base': '',
        'result': '',
        'raw_text': ''
    }

    for line in reform_file_lines:
        new_info_index = line.find('	[')
        if new_info_index >= 0:
            if temp_dict['id'] != '':
                data_dict[temp_dict['id']] = temp_dict.copy()

            temp_dict['id'] = line[line.find('[') + 1 : line.find(']')]
            temp_dict['base'] = ''
            temp_dict['target'] = ''
            temp_dict['raw_text'] = line
            continue

        if temp_dict['id'] == '':
            continue

        base_index = line.find('BaseItem')
        if base_index >= 0:
            temp_dict['base'] = line.split('"')[1]

        result_index = line.find('ResultItem')
        if result_index >= 0:
            temp_dict['result'] = line.split('"')[1]
        
        temp_dict['raw_text'] += line

    data_dict[temp_dict['id']] = temp_dict.copy()
    return data_dict

def compare_dict(old_data_dict, new_data_dict, result_path, encoding='utf-8'):
    write_file = open(result_path, 'w', encoding=encoding)

    for old_key in old_data_dict:
        if old_key not in new_data_dict:
            relation_equips = f'{old_data_dict[old_key]["base"]} → {old_data_dict[old_key]["result"]}'
            write_file.write('# {} (資料移除)\n關聯裝備: {}\n{}\n\n----- ----- -----\n\n'.format(
                old_key, 
                relation_equips,
                old_data_dict[old_key]
            ))
            write_file.write(f'# {old_key} (資料移除)\n{old_data_dict[old_key]}\n\n----- ----- -----\n\n')
            print(f'    發現 資料移除: {old_key} ({relation_equips})')

    for new_key in new_data_dict:
        if new_key in old_data_dict and old_data_dict[new_key] != new_data_dict[new_key]:
            old_relation = f'{old_data_dict[new_key]["base"]} → { old_data_dict[new_key]["result"]}'
            new_relation = f'{new_data_dict[new_key]["base"]} → { new_data_dict[new_key]["result"]}'
            relation_equips = old_relation if old_relation == new_relation else f'({old_relation}) 與 ({new_relation})'
            differ = difflib.Differ()
            diff = differ.compare(old_data_dict[new_key]['raw_text'].splitlines(), new_data_dict[new_key]['raw_text'].splitlines())

            write_file.write('# {} (內容調整)\n關聯裝備: {}\n{}\n\n----- ----- -----\n\n'.format(
                new_key,
                relation_equips,
                '\n'.join([line for line in diff if not line.startswith('? ')])
            ))
            
            print(f'    發現 內容調整: {new_key} ({relation_equips})')
            continue

        if new_key not in old_data_dict:
            relation_equips = f'{new_data_dict[new_key]["base"]} → { new_data_dict[new_key]["result"]}'
            write_file.write('# {} (新增資料)\n關聯裝備: {}\n{}\n\n----- ----- -----\n\n'.format(
                new_key, 
                relation_equips,
                new_data_dict[new_key]
            ))
            print(f'    發現 新增資料: {new_key} ({relation_equips})')
            continue
    
    write_file.write('文件到此結束。')
    print(f'  生成比對結果: {result_path}')

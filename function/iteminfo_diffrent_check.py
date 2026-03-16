import difflib

def read_lua_file(input_file_path, encoding):
    raw_data = []
    for line in open(input_file_path, 'r', encoding=encoding):
        if line[0] in ['[', 'u', 'i']:
            raw_data.append(line.strip('\n'))

    item_dict = {}
    id = '0'
    for line in raw_data:
        # 1st line, get item id
        if line[0] == '[':
            id = line[1:line.find(']')]
            item_dict[id] = {}

        # 2nd line, get item name
        if line[0] == 'u':
            tc_index = line.find('identifiedDisplayName')
            kr_index = line.find('identifiedResourceName')

            item_dict[id]['Name_TC'] = line[
                (tc_index + 25) : (kr_index - 3)
            ]

        # 3rd line, get item descript
        if line[0] == 'i':
            raw_descript = line[30 : line.find('}')]
            item_dict[id]['Descript'] = raw_descript.replace('\", \"', '\n').replace('\"', '')

            # Remove color code
            while True:
                code_index = item_dict[id]['Descript'].find('^')
                if code_index == -1:
                    break
                else:
                    item_dict[id]['Descript'] = item_dict[id]['Descript'][:code_index] + item_dict[id]['Descript'][code_index + 7:]
            
            # Slot number
            slot_index = line.find('slotCount')
            item_dict[id]['Slot'] = line[slot_index + 12:slot_index + 13]

    return item_dict

def compare_dict(old_dict, new_dict, result_path, encoding='utf-8'):

    write_file = open(result_path, 'w', encoding=encoding)

    for item_id in new_dict:
        # Both dict exist
        if item_id in old_dict:

            # But diffrent
            if old_dict[item_id] != new_dict[item_id]:

                print('    - 發現 [ 內容變更 ]: {0} - {1}'.format(item_id, new_dict[item_id]['Name_TC']))
                differ = difflib.Differ()
                diff = differ.compare(old_dict[item_id]['Descript'].splitlines(), new_dict[item_id]['Descript'].splitlines())

                temp_text = ''
                if old_dict[item_id]['Name_TC'] != new_dict[item_id]['Name_TC'] or old_dict[item_id]['Slot'] != new_dict[item_id]['Slot']:
                    temp_text += '- [ID: {0}] {1}{2}\n+ '.format(
                        item_id,
                        old_dict[item_id]['Name_TC'],
                        ' [{0}]'.format(old_dict[item_id]['Slot']) if old_dict[item_id]['Slot'] != '0' else ''
                    )

                temp_text += '[ID: {0}] {1}{2} (內容變更)\n{3}\n\n----- ----- -----\n\n'.format(
                    item_id,
                    new_dict[item_id]['Name_TC'],
                    ' [{0}]'.format(new_dict[item_id]['Slot']) if new_dict[item_id]['Slot'] != '0' else '',
                    '\n'.join([line for line in diff if not line.startswith('? ')]),
                )

                write_file.write(temp_text)

        # New item
        else:
            print('    - 發現 [ 新增道具 ]: {0} - {1}'.format(item_id, new_dict[item_id]['Name_TC']))
            if new_dict[item_id]['Slot'] == '0':
                write_file.write(
                    '[ID: {0}] {1} (新增道具)\n{2}\n\n----- ----- -----\n\n'.format(
                        item_id,
                        new_dict[item_id]['Name_TC'],
                        new_dict[item_id]['Descript'],
                    )
                )
            else:
                write_file.write(
                    '[ID: {0}] {1} [{2}] (新增道具)\n{3}\n\n----- ----- -----\n\n'.format(
                        item_id,
                        new_dict[item_id]['Name_TC'],
                        new_dict[item_id]['Slot'],
                        new_dict[item_id]['Descript'],
                    )
                )

    write_file.write('文件到此結束。')
    print(f'  生成比對結果: {result_path}')
import os
import sys
import datetime

import function.config_reader as config_reader
import function.file_process as fp
import function.iteminfo_diffrent_check as iteminfo_diff
import function.iteminfo_effect_replace as iteminfo_replace
import function.enchantlist_different_check as enchantlist_diff
import function.equipprop_different_check as equipprop_diff
import function.equipprop_effect_explain as equipprop_explain
import function.reform_different_check as reform_diff

#region Initial
ENCODING = 'utf-8'
OTHER_ENCODING = 'cp950'
ITEM_FILE_NAME = 'iteminfo_new.lub'
ENCHANT_FILE_NAME = 'enchantlist.txt'
PROPERTY_FILE_NAME = 'equipmentproperties.txt'
REFORM_FILE_NAME = 'itemreformsystem.txt'
KR_ITEM_FILE_NAME = 'itemInfo_true.lub'

DATETIME_TEXT = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

EXECUTE_PATH = os.path.abspath(os.path.dirname(__file__)) + '\\'
if getattr(sys, 'frozen', False):
    EXECUTE_PATH = os.path.dirname(sys.executable) + '\\'
INPUT_PATH = EXECUTE_PATH + 'input\\'
TEMP_PATH = EXECUTE_PATH + 'temp\\'
PARSER_PATH = EXECUTE_PATH + 'parser\\luadec.exe'
OUTPUT_PATH = EXECUTE_PATH + 'output\\'

process_flag_dict = {
    ITEM_FILE_NAME: False,
    ENCHANT_FILE_NAME: False,
    PROPERTY_FILE_NAME: False,
    REFORM_FILE_NAME: False,
    KR_ITEM_FILE_NAME: False
}

#endregion

#region Title
print('''
 _______  _______  ___   _  _______  _______  _______  ______    _______  _______  _______ 
|       ||   _   ||   | | ||       ||       ||       ||    _ |  |   _   ||  _    ||       |
|  _____||  |_|  ||   |_| ||    ___||_     _||   _   ||   | ||  |  |_|  || | |   ||   ____|
| |_____ |       ||      _||   |___   |   |  |  | |  ||   |_||_ |       || |_|   ||  |____ 
|_____  ||       ||     |_ |    ___|  |   |  |  |_|  ||    __  ||       ||___    ||_____  |
 _____| ||   _   ||    _  ||   |___   |   |  |       ||   |  | ||   _   |    |   | _____| |
|_______||__| |__||___| |_||_______|  |___|  |_______||___|  |_||__| |__|    |___||_______|

# 提醒
1. 這是一個自製的小程式，用於一次性檢查 iteminfo_new.lub, enchantlist.lub, equipmentproperties.lub 與 itemreformsystem.lub 檔案。
2. 主要目的為比對這些檔案舊版本與新版本的不同，因此如果是第一次執行或僅有一份檔案，程式僅會進行初步的初始化，或者比對結果為空（因為沒有不同的檔案，無論怎麼比較都是相同的）。
3. 部分步驟需要使用者自行將 .lub 檔案轉換為 .lua 或 .txt 檔案，若沒有這部分的能力，部分流程將無法執行。
4. 此程式正確執行時，不會自動關閉；倘若執行後程式自行消失，表示中途遭遇了什麼錯誤或 bug 而導致程式執行失敗。
''')

input(f'上述提醒已經閱讀過了嗎？如果沒問題的話，按下 Enter 就會開始執行了。\n')

print('# 程式開始執行\n')

#endregion

#region File Copy

fp.create_dir(INPUT_PATH)
fp.create_dir(TEMP_PATH)
fp.create_dir(OUTPUT_PATH)

for file_name in process_flag_dict:
    if fp.is_file_exist(INPUT_PATH, file_name):
        process_flag_dict[file_name] = True

        pure_file_name = file_name[:-4]
        file_ext_name = file_name[-3:]
        
        fp.copy_to(
            f'{INPUT_PATH}{file_name}',
            f'{TEMP_PATH}{pure_file_name} {DATETIME_TEXT}.{file_name[-3:]}'
        )
        fp.maintain_file_limit(TEMP_PATH, pure_file_name, 5, file_ext_name)
print('第 1 步驟: 搬移檔案完成\n')

#endregion

#region Item Info

if process_flag_dict[ITEM_FILE_NAME]:
    pure_file_name = ITEM_FILE_NAME[:-4]
    newest_file = fp.get_newest_file(TEMP_PATH, pure_file_name)
    fp.parse_lub_to_lua(PARSER_PATH, newest_file)
    fp.maintain_file_limit(TEMP_PATH, pure_file_name, 5, 'lua')

    lua_file_list = fp.get_file_list(TEMP_PATH, pure_file_name, 'lua')
    if len(lua_file_list) >= 2:
        old_info = iteminfo_diff.read_lua_file(lua_file_list[-2], ENCODING)
        new_info = iteminfo_diff.read_lua_file(lua_file_list[-1], ENCODING)

        iteminfo_diff.compare_dict(old_info, new_info, f'{OUTPUT_PATH}ItemInfoCompareResult.txt', ENCODING)
        print(f'  結束 {pure_file_name} 的比對處理。')
    else:
        print(f'  由於檔案數量不足，略過 {pure_file_name} 的比對處理。')
print(f'第 2 步驟: 比對 {ITEM_FILE_NAME} 檔案完成\n')

#endregion

#region Enchant List

if process_flag_dict[ENCHANT_FILE_NAME]:
    pure_file_name = ENCHANT_FILE_NAME[:-4]
    newest_file = fp.get_newest_file(TEMP_PATH, pure_file_name)

    enchant_file_list = fp.get_file_list(TEMP_PATH, pure_file_name)
    if len(enchant_file_list) >= 2:
        old_info = enchantlist_diff.read_file(enchant_file_list[-2], OTHER_ENCODING)
        new_info = enchantlist_diff.read_file(enchant_file_list[-1], OTHER_ENCODING)

        enchantlist_diff.compare_dict(old_info, new_info, f'{OUTPUT_PATH}EnchantListCompareResult.txt', ENCODING)
        print(f'  結束 {pure_file_name} 的比對處理。')
    else:
        print(f'  由於檔案數量不足，略過 {ENCHANT_FILE_NAME} 的比對處理。')
print(f'第 3 步驟: 比對 {ENCHANT_FILE_NAME} 檔案完成\n')

#endregion

#region Equipment Properties

if process_flag_dict[PROPERTY_FILE_NAME]:
    pure_file_name = PROPERTY_FILE_NAME[:-4]
    newest_file = fp.get_newest_file(TEMP_PATH, pure_file_name)

    prop_file_list = fp.get_file_list(TEMP_PATH, pure_file_name)
    if len(prop_file_list) >= 2:
        old_info = equipprop_diff.read_file(prop_file_list[-2], ENCODING)
        new_info = equipprop_diff.read_file(prop_file_list[-1], ENCODING)

        equipprop_diff.compare_dict(old_info, new_info, f'{OUTPUT_PATH}EquipmentPropertiesCompareResult.txt')
        print(f'  結束 {pure_file_name} 的比對處理。')

        equipprop_explain.explain_file(
            f'{OUTPUT_PATH}EquipmentPropertiesCompareResult.txt',
            f'{OUTPUT_PATH}EquipmentPropertiesExplainResult.txt'
        )
    else:
        print(f'  由於檔案數量不足，略過 {pure_file_name} 的比對處理。')
print(f'第 4 步驟: 比對 {PROPERTY_FILE_NAME} 檔案完成\n')

#endregion

#region Item Reform System

if process_flag_dict[REFORM_FILE_NAME]:
    pure_file_name = REFORM_FILE_NAME[:-4]
    newest_file = fp.get_newest_file(TEMP_PATH, pure_file_name)

    reform_file_list = fp.get_file_list(TEMP_PATH, pure_file_name)
    if len(reform_file_list) >= 2:
        old_info = reform_diff.read_file(reform_file_list[-2], OTHER_ENCODING)
        new_info = reform_diff.read_file(reform_file_list[-1], OTHER_ENCODING)

        reform_diff.compare_dict(old_info, new_info, f'{OUTPUT_PATH}ItemReformCompareResult.txt', ENCODING)
        print(f'  結束 {pure_file_name} 的比對處理。')
    else:
        print(f'  由於檔案數量不足，略過 {REFORM_FILE_NAME} 的比對處理。')
print(f'第 5 步驟: 比對 {REFORM_FILE_NAME} 檔案完成\n')

#endregion

#region KR Item Info

if process_flag_dict[KR_ITEM_FILE_NAME]:
    pure_file_name = KR_ITEM_FILE_NAME[:-4]
    newest_file = fp.get_newest_file(TEMP_PATH, pure_file_name)
    fp.parse_lub_to_lua(PARSER_PATH, newest_file)
    fp.maintain_file_limit(TEMP_PATH, pure_file_name, 5, 'lua')

    lua_file_list = fp.get_file_list(TEMP_PATH, pure_file_name, 'lua')
    if len(lua_file_list) >= 2:
        old_info = iteminfo_diff.read_lua_file(lua_file_list[-2], 'cp949')
        new_info = iteminfo_diff.read_lua_file(lua_file_list[-1], 'cp949')

        iteminfo_diff.compare_dict(old_info, new_info, f'{OUTPUT_PATH}ItemInfoCompareResult_KR.txt', ENCODING)
        print(f'  結束 {pure_file_name} 的比對處理。')

        iteminfo_replace.replace_file(f'{OUTPUT_PATH}ItemInfoCompareResult_KR.txt', f'{OUTPUT_PATH}ItemInfoReplaceResult_KR.txt', ENCODING)
    else:
        print(f'  由於檔案數量不足，略過 {pure_file_name} 的比對處理。')
print(f'第 6 步驟: 比對 {KR_ITEM_FILE_NAME} 檔案完成\n')

#endregion

print(f'執行結束，按下任意按鍵退出。')
os.system('pause')
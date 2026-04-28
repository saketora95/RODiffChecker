from function.iteminfo_diffrent_check import read_lua_file

target_file = 'temp/iteminfo_new 20260421131417.lua'
data_dict = read_lua_file(target_file, 'utf-8')

for id in data_dict:
    data_dict[id]['len'] = len(data_dict[id]['Descript'])

sorted_items = sorted(
    data_dict.items(),
    key=lambda item: item[1].get('len', 0),
    reverse=True
)

for item_id, item_data in sorted_items[:10]:
    print(f"id={item_id}, len={item_data['len']}")
    print(f"{item_data['Name_TC']}")
    # print(f"{item_data['Descript']}")


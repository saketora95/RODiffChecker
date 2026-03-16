import function.equipprop_explain_table as ex_table
import re

CALL_PATTERN = re.compile(r'^(\s*)(?:[-+?]\s)?([A-Za-z_]\w*)\((.*)\)\s*$', re.DOTALL)

def split_args(args_str: str) -> list[str]:
    """
    按頂層逗號分割參數字串，正確處理巢狀括號。
    e.g. "0, 5 + (temp - 5)" → ["0", "5 + (temp - 5)"]
    """
    args, current, depth = [], [], 0
    for ch in args_str:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ',' and depth == 0:
            args.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        args.append(''.join(current).strip())
    return args

def parse_function_call(line: str):
    """正確辨識一行函式呼叫，回傳 (indent, func_name, args) 或 None"""
    m = CALL_PATTERN.match(line.rstrip())
    if not m:
        return None
    indent, name, args_raw = m.group(1), m.group(2), m.group(3)
    return indent, name, split_args(args_raw)

def explain_line(line: str):
    result = parse_function_call(line)
    if result:
        indent, name, args = result
        handler = ex_table.function_handlers.get(name)
        if handler:
            raw = handler(indent, args)
            return replace_key_word(raw) + '\n', True

    return replace_key_word(line), False

def replace_key_word(input_line: str):
    for key in ex_table.ext_param_table:
        input_line = input_line.replace(key, ex_table.ext_param_table[key])
        
    for key in ex_table.keep_word_table:
        print(key)
        input_line = input_line.replace(key, ex_table.keep_word_table[key])

    for key in ex_table.get_table:
        input_line = input_line.replace(key, ex_table.get_table[key])

    for key in ex_table.class_table:
        input_line = input_line.replace(key, ex_table.class_table[key])

    for key in ex_table.size_table:
        input_line = input_line.replace(key, ex_table.size_table[key])

    for key in ex_table.element_table:
        input_line = input_line.replace(key, ex_table.element_table[key])

    for key in ex_table.race_table:
        input_line = input_line.replace(key, ex_table.race_table[key])
    
    return input_line

def explain_file(input_file_name, output_file_name):
    output_file = open(output_file_name, 'w', encoding='utf-8')
    output_file.write('此為實驗性功能，極度容易出錯，尤其是 體型/屬性/種族/階級 傷害部分，請斟酌參考。\n\n')

    for line in open(input_file_name, 'r', encoding='utf-8').readlines():
        explained_line, existPattern = explain_line(line)

        # if existPattern:
        #     output_file.write(explained_line)

        # else:
        #     output_file.write(line)

        output_file.write(explained_line)
    output_file.close()
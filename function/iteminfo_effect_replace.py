import re
from typing import Iterable

import function.iteminfo_effect_table as effect_table


def _build_regex_rules():
    first_layer_compiled_rules = []
    for rule in effect_table.FIRST_LAYER_REGEX_REPLACE_RULES:
        pattern = rule.get('pattern', '')
        replacement = rule.get('replacement', '')
        flags = rule.get('flags', 0)

        if not pattern:
            continue

        first_layer_compiled_rules.append(
            {
                'pattern': pattern,
                'compiled': re.compile(pattern, flags),
                'replacement': replacement,
            }
        )

    second_layer_compiled_rules = []
    for rule in effect_table.SECOND_LAYER_REGEX_REPLACE_RULES:
        pattern = rule.get('pattern', '')
        replacement = rule.get('replacement', '')
        flags = rule.get('flags', 0)

        if not pattern:
            continue

        second_layer_compiled_rules.append(
            {
                'pattern': pattern,
                'compiled': re.compile(pattern, flags),
                'replacement': replacement,
            }
        )
    
    first_layer_compiled_rules = sorted(
        first_layer_compiled_rules,
        key=lambda x: len(x['pattern']),
        reverse=True
    )

    second_layer_compiled_rules = sorted(
        second_layer_compiled_rules,
        key=lambda x: len(x['pattern']),
        reverse=True
    )

    return first_layer_compiled_rules, second_layer_compiled_rules

FIRST_LAYER_COMPILED_REGEX_RULES, SECOND_LAYER_COMPILED_REGEX_RULES = _build_regex_rules()


def _format_with_match(template: str, match: re.Match) -> str:
    values = dict(match.groupdict())
    for index, group_value in enumerate(match.groups(), start=1):
        values[f'g{index}'] = group_value

    try:
        return template.format(**values)
    except KeyError:
        return match.group(0)


def apply_replace_rules(text: str) -> str:
    replaced_text = text

    for rule in FIRST_LAYER_COMPILED_REGEX_RULES:
        compiled = rule['compiled']
        replacement = rule['replacement']

        if callable(replacement):
            replaced_text = compiled.sub(replacement, replaced_text)
        else:
            replaced_text = compiled.sub(
                lambda m, tpl=replacement: _format_with_match(tpl, m),
                replaced_text,
            )

    for rule in SECOND_LAYER_COMPILED_REGEX_RULES:
        compiled = rule['compiled']
        replacement = rule['replacement']

        if callable(replacement):
            replaced_text = compiled.sub(replacement, replaced_text)
        else:
            replaced_text = compiled.sub(
                lambda m, tpl=replacement: _format_with_match(tpl, m),
                replaced_text,
            )

    for source, target in effect_table.LITERAL_REPLACE_TABLE.items():
        replaced_text = replaced_text.replace(source, target)

    return replaced_text


def apply_replace_rules_to_lines(lines: Iterable[str]) -> list[str]:
    return [apply_replace_rules(line) for line in lines]


def replace_file(input_file_path: str, output_file_path: str, encoding: str = 'utf-8'):
    output_file = open(output_file_path, 'w', encoding=encoding)

    for line in open(input_file_path, 'r', encoding=encoding).readlines():
        replaced_text = apply_replace_rules(line)

        if replaced_text[-1] == '\n':
            output_file.write(replaced_text)
        else:
            output_file.write(replaced_text + '\n')

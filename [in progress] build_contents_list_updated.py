import pandas as pd
import re, os
from utilities import read_text_file_to_dataset, write_resultset_to_excel_file
from build_contents_list import find_regex_patterns, find_keywords_and_common_words, find_remaining


def organize_data_into_dict(dataset):
    result = {}

    for lst in dataset:
        key1, key2 = int(lst[0]), lst[1]

        if key1 not in result.keys():
            result[key1] = {}

        if len(result[key1].keys()) <= 1:
            if key2 not in result[key1].keys():
                result[key1][key2] = []

            result[key1][key2].append(lst[3])

    return result


def flatten(x):
    values = []
    for l in x.values():
        for j in l:
            values.append(j)
    return values


def create_contents_list(data_in_dict):
    contents_lists = []

    for i in range(len(data_in_dict.keys())):
        contents_lists.append([])
        values = flatten(list(data_in_dict.values())[i])

        regex_patterns, remaining = find_regex_patterns(values)  # pass in all values in that group
        keywords, common_words = find_keywords_and_common_words(remaining)
        contents_lists[i] = [common_words, keywords, regex_patterns]

    return contents_lists


def find_remaining(data_in_dict, contents_list):

    def remove_words(value, pat):

        if not any([special in pat for special in ['箱半周长']]):
            pat = '(?<![\u4e00-\u9fff])(?<!\d)' + pat + '(?![\u4e00-\u9fff])(?!\d)'

        return re.sub(pat, '', value)

    remaining = dict()

    for i in range(len(data_in_dict.keys())):
        values = flatten(list(data_in_dict.values())[i])

        for v in values:

            common_words, keywords, regex_patterns = contents_list[i][j + 1][0], contents_list[i][j + 1][1], contents_list[i][j + 1][2]

            value = v

            for rg in regex_patterns:
                value = remove_words(value, patterns[rg])

            for word in common_words + keywords:
                value = remove_words(value, word)

            value = value.split(':')[1]
            for special_character in ['(', ')', ' ', '、', '（', '）']:
                value = value.replace(special_character, '')

            if value:
                key = dataset[i][0]
                if key in remaining.keys():
                    if value not in remaining[key]:
                        remaining[key].append(value)
                else:
                    remaining[key] = [value]


def main():
    datasets = ['/Users/tonytuzki/Desktop/Glodon_USA/9./output/GANSU_0304_category_name_value_cleaned_spec_all.txt']

    for d in datasets:
        dataset = read_text_file_to_dataset(d, '§', True)
        data_in_dict = organize_data_into_dict(dataset)
        contents_list = create_contents_list(data_in_dict)
        write_resultset_to_excel_file(contents_list, 'contents_GANSU_0304_category_name_value_cleaned_spec_all.xlsx', [1, 2, 3])
        remaining = find_remaining(data_in_dict, contents_list)
        # print('GANSU_0304_category_name_value_cleaned_spec_all.xlsx :', len(remaining.keys()), 'remaining', remaining)


if __name__ == "__main__":
    main()

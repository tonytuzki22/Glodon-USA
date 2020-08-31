from utilities import read_excel_file_to_list, write_resultset_to_excel_file
import re
from regex_patterns import patterns


def organize_row_into_dict(data_in_row):
    """ Organizes a row of data into a dictionary.
    :param data_in_row: a row of data
    :return: a dictionary where
        - each key is a title sub-row
        - each value is list of content sub-rows for that title sub-row
    """

    split_data = data_in_row.split('\n')
    result, temp_key = {}, ''

    for d in split_data:
        if '      ' not in d:  # a title sub-row
            temp_key = d
            result[temp_key] = []
        else:  # a content sub-row
            result[temp_key].append(d.split('      ')[1])
    return result


def find_regex_patterns(values_in_group):
    """ Finds the regex patterns for the group.
    :param values_in_group: a list of content sub-rows for a particular title sub-row,
                            which is part of the result of calling organize_row_into_dict
    :return: a tuple whose
        - first element is a list of all patterns that are matched by any content sub-row
        - second element is a list of remaining phrases in all content sub-rows that does not match any patterns
    """

    found_patterns = []
    grouped_remaining = []

    for v in values_in_group:

        remaining = v.replace('（', '(').replace('）', ')')

        if ':' in v:
            remaining = remaining.split(':')[1]

        for name, pat in patterns.items():
            match = re.search(pat, v)

            if match:
                matched_string = match.group(0)
                remaining = remaining.replace(matched_string, '')  # remove the matched string from remaining

                if name not in found_patterns:
                    found_patterns.append(name)

        grouped_remaining.append(remaining)
    return found_patterns, grouped_remaining


def find_keywords_and_common_words(remaining_in_group):
    """ Find the keywords and common words among the remaining phrases in the group.
    :param remaining_in_group: a list of remaining phrases, which is the result of find_regex_patterns
    :return: a tuple whose
        - first element is a list of keywords, which are not shared by the remaining phrases
        - second element is a list of common words, which are shared by the remaining phrases
    """

    keywords, common_words = [], []
    unique_tokens = []

    for r in remaining_in_group:
        tokens = re.split('\s+|\(|\)|、', r)
        unique_tokens.extend([t for t in tokens if t not in unique_tokens and t != ''])

    for t in unique_tokens:

        if not any(char.isdigit() for char in t) or any(special in t for special in ['SF', 'kV', '380V']):

            if_in_all = all([t in r for r in remaining_in_group])

            if if_in_all and t not in common_words:
                common_words.append(t)
            elif not if_in_all and t not in keywords:
                keywords.append(t)

    return keywords, common_words


def build_contents_list(dataset):
    """ Creates a contents list for a dataset.
    :param dataset: a list containing a dataset
    :return: a nested list, with a list for every row of the dataset, whose
        - first element is the itemcode for that row
        - other elements are the content lists for each group of that row, whose
            - first element is a list of common words
            - second element is a list of keywords
            - third element is a list of patterns
    """
    contents_lists = []

    for i in range(len(dataset)):  # for every row
        data_in_row = dataset[i][4]
        row_in_dict = organize_row_into_dict(data_in_row)
        contents_lists.append([dataset[i][0]])  # one list for every row

        for j in range(len(row_in_dict.keys())):  # for every group in row
            contents_lists[i].append([])  # one list for every group in row
            regex_patterns, remaining = find_regex_patterns(
                list(row_in_dict.values())[j])  # pass in all values in that group
            keywords, common_words = find_keywords_and_common_words(remaining)
            contents_lists[i][j + 1] = [common_words, keywords, regex_patterns]
    return contents_lists


def find_remaining(dataset, contents_list):
    """ Find the phrases that are not contained in the contents list.
    :param dataset: a list containing the dataset
    :param contents_list: a list containing the contents of the dataset, which is the result of create_contents_list
    :return: a dictionary, whose
        - each key is the itemcode of the row
        - each value is a list of phrases that are not contained in the contents list
    """

    def remove_words(value, pat):

        if not any([special in pat for special in ['箱半周长']]):
            pat = '(?<![\u4e00-\u9fff])(?<!\d)' + pat + '(?![\u4e00-\u9fff])(?!\d)'

        return re.sub(pat, '', value)

    remaining = {}

    if len(dataset) == len(contents_list):

        for i in range(len(dataset)):  # for every row

            if dataset[i][0] == contents_list[i][0]:

                data_in_row = dataset[i][4]
                row_in_dict = organize_row_into_dict(data_in_row)

                for j in range(len(row_in_dict.keys())):  # for every group in row

                    common_words, keywords, regex_patterns = contents_list[i][j + 1][0], contents_list[i][j + 1][1], \
                                                             contents_list[i][j + 1][2]

                    for v in (list(row_in_dict.values())[j]):  # for every value in group

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

    return remaining


def main():
    datasets = {'清单编码_清单指引特征项_工作内容及定额_0309.xlsx': ['itemcode', '1', '2', '3', '4', '5'],
                '清单编码_清单指引特征项_工作内容及定额_0310.xlsx': ['itemcode', '1', '2', '3', '4', '5', '6'],
                '清单编码_清单指引特征项_工作内容及定额_0304.xlsx': ['itemcode', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']}

    for file_name, column_names in datasets.items():
        print('\n** now running program for', file_name, '**')
        dataset = read_excel_file_to_list(file_name)

        contents_list = build_contents_list(dataset)
        output_file_name = 'contents_' + file_name
        write_resultset_to_excel_file(contents_list, output_file_name, column_names)
        print('built contents file as', output_file_name)

        remaining = find_remaining(dataset, contents_list)
        print('diagnostics:')
        print('  # of remaining rows:', len(remaining.keys()))
        print('  remaining rows:', remaining)
        if len(remaining.keys()) == 0:
            print('  success!')


if __name__ == "__main__":
    main()

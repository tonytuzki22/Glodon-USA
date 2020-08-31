from utilities import read_excel_file_to_list, write_resultset_to_excel_file


def check_status(correct_value, incorrect_value):
    """ Checks the status of the correct value and the incorrect value.
    :param correct_value: the correct value
    :param incorrect_value: the incorrect value
    :return: D if the status is deletion, A if the status is addition, and M if the status is modification.
    """
    if correct_value == '':
        return 'D'
    elif incorrect_value == '':
        return 'A'
    return 'M'


def build_wrong_results_list(dataset):
    """ Builds a list for wrong results in the dataset.
    :param dataset: a list containing the dataset
    :return: a list of list, with one for each row in the dataset, each containing
            DBIS, 清单编码, name, valuetype, extractor, incorrect_result, correct_result, check_status, original status
    """
    result = []
    for i in range(len(dataset)):

        row = dataset[i]
        predicted, actual = row[7].split('\n'), row[8].split('\n')

        for a in actual:

            split_a = a.split('፨')
            a_name, a_value_type, a_value, a_status = split_a[0], split_a[1], split_a[2], split_a[3].split('(')[1].split(')')[0]

            for p in predicted:

                if ':{' in p:
                    split_p = p.split(':{')
                    p_name, p_value_type, = split_p[0], split_p[1].split('(')[0]

                    if '(' in p:
                        p_extractor = p.split('(')[1].split(')')[0]
                    else:
                        p_extractor = ''

                    if ':' in split_p[1]:
                        p_value = split_p[1].split(':')[1].split('}')[0]
                    else:
                        p_value = ''

                    if a_name == p_name and a_value_type == p_value_type and a_value != p_value:
                        checked_status = check_status(a_value, p_value)
                        r = [row[1], row[2], a_name, a_value_type, p_extractor, p_value, a_value, checked_status, a_status]

                        if r not in result:
                            result.append(r)
    print(result)
    return result


def main():

    file_name = '031001001_parser_results.xlsx'
    print('\n** now running tests for', file_name, '**')

    dataset = read_excel_file_to_list(file_name)
    wrong_results_list = build_wrong_results_list(dataset)

    output_file_name = '031001001_parser_results3.xlsx'
    write_resultset_to_excel_file(wrong_results_list, output_file_name,
                                  ['DBID', '清单编码', 'name', 'valuetype', 'extractor', 'incorrect_result',
                                   'correct_result', 'check_status', 'original_status'])
    print('built wrong results sheet as', output_file_name)


if __name__ == "__main__":
    main()
from utilities import read_excel_file_to_list, write_resultset_to_excel_file


def check(x1, x2):
    """ Checks if the written data is correct, compared to the actual data.
    :param x1: the written data for a particular row
    :param x2: the actual data for a particular row
    :return: True if there is a sub-row in x1 that matches x2, in terms of name, value type, and value.
    """
    written, actual = x1.split('\n'), x2.split('\n')

    for a in actual:

        split_a = a.split('፨')
        a_name, a_value_type, a_value = split_a[0], split_a[1], split_a[2]

        found = False

        for p in written:

            if ':{' in p:
                split_p = p.split(':{')
                p_name, p_value_type = split_p[0], split_p[1].split('(')[0]

                if ':' in split_p[1]:
                    p_value = split_p[1].split(':')[1].split('}')[0]

                    if a_name == p_name and a_value == p_value and a_value_type == p_value_type:
                        found = True

        if not found:
            return False

    return True


def main():

    file_name = '031001001_parser_results.xlsx'
    print('\n** now running program for', file_name, '**')
    dataset = read_excel_file_to_list(file_name)

    result = []
    for i in range(len(dataset)):
        row = dataset[i]

        if not check(row[7], row[8]):
            row[0] = 0
        result.append(row)

        """
        if check(row[7], row[8]):
            result.append(1)
        else:
            result.append(0)

    print(result)
        """

    output_file_name = '031001001_parser_results2.xlsx'
    write_resultset_to_excel_file(result, output_file_name,
                                  ['正确与否？1-正确;0-有错', 'DBID', '清单编码', 'RESULT_DETAIL_ID',
                                   'SPECID', '清单名称', '清单描述', '解析结果', '校验结果'])
    print('built checked results file as', output_file_name)


if __name__ == "__main__":
    main()


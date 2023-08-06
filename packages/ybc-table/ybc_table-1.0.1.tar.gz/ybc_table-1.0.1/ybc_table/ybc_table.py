import terminaltables as tt


def table(data, table_type='ascii'):
    """
    返回Ascii Table
    :param data: 要转换的数据（二维列表）
    :param table_type: 可以指定的转换类型 ['ascii', 'single', 'double', 'github']
    :return: 表格形式的字符串
    """
    type_list = ['ascii', 'single', 'double', 'github']

    if table_type not in type_list:
        table_type = 'ascii'

    if table_type == 'ascii':
        t = tt.AsciiTable(data)
    elif table_type == 'single':
        t = tt.SingleTable(data)
    elif table_type == 'double':
        t = tt.DoubleTable(data)
    elif table_type == 'github':
        t = tt.GithubFlavoredMarkdownTable(data)

    return t.table


def main():
    data = [[1, 2, 3], [4, 5, 6]]

    print(table(data, 'ascii'))
    print(table(data, 'single'))
    print(table(data, 'double'))
    print(table(data, 'github'))


if __name__ == '__main__':
    main()

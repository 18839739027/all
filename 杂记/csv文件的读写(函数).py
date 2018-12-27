# -*- coding: utf-8 -*-
# @Time    : 2018/12/27  16:16
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2018/12/27  11:22
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm

"""
CSV(Comma-Separated Values)即逗号分隔值，可以用Excel打开查看。由于是纯文本，任何编辑器也都可打开。与Excel文件不同，CSV文件中：
    值没有类型，所有值都是字符串
    不能指定字体颜色等样式
    不能指定单元格的宽高，不能合并单元格
    没有多个工作表
    不能嵌入图像图表
在CSV文件中，以,作为分隔符，分隔两个单元格。像这样a,,c表示单元格a和单元格c之间有个空白的单元格。依此类推。
不是每个逗号都表示单元格之间的分界。所以即使CSV是纯文本文件，也坚持使用专门的模块进行处理。Python内置了csv模块。
"""
import csv


def reader_writer():
    # 文件的读取
    filename = r'test.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        # 不能直接打印出想看到的内容, 最外层是list
        # eg: print(reader) = <_csv.reader object at 0x000001FEA7A66C78>
        # print(list(reader))
        for row in reader:
            print(reader.line_num, row)
    #     f.close()

    # 数据的写入
    # 可以写入一行或多行
    datas = [['你是谁', '我是小爱'] , ['你在哪', '你在干什么']]
    with open('test.csv', 'a', newline='') as f:
        # 默认打开当前项目文件夹下， 若无则创建， 可指定路径
        writer = csv.writer(f)
        for row in datas:
            writer.writerow(row)
        # 写入多行数据
        # writer.writerows(datas)


def Dict_reader_writer():
    """DictReader和DictWriter对象"""
    filename = 'test2.csv'
    headers = ['name', 'age']
    datas = [{'name': 'Bob', 'age': 23},
             {'name': 'Jerry', 'age': 44},
             {'name': 'Tom', 'age': 15}
             ]
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in datas:
            writer.writerow(row)


    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name']
            age = row['age']
            print(name, age)


if __name__ == '__main__':
    Dict_reader_writer()





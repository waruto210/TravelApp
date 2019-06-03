import json


class Label:
    """生成一个地名与序号对应的字典对象"""
    def __init__(self, label_filepath: str):
        """Label类生成函数

        :param label_filepath:label文件路径，json格式
        """
        self.label = self.load_label(label_filepath)

    @staticmethod
    def load_label(label_filepath: str):
        """导入label

        :param label_filepath: label文件路径，json格式
        :return: label字典
        """
        label_list_file = open(label_filepath, 'r', encoding='utf-8')
        label_list = label_list_file.read()
        label_list_file.close()
        label_list = json.loads(label_list)
        return label_list


label1 = Label('./label.json')
label = label1.label[0]
# print(label)


# b = [bool] * 10
# for i in range(10):
#     b[i] = False
# print(b)

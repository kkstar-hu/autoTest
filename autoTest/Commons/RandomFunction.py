
import datetime
import random
import string


class CommonGenerator(object):

    @staticmethod
    def generate_verify_code(code_length):
        """
        生成指定长度的数字字符串
        :param code_length: 指定长度
        :return:
        """
        return "".join(random.sample([x for x in string.digits], code_length))

    @staticmethod
    def generate_spec_uuid(spec_name, str_length):
        """
        :param spec_name: 前缀名称
        :param str_length: 指定长度数字或字母
        :return:
        """
        return '{}_{}'.format(spec_name,
                              "".join(random.sample([x for x in string.hexdigits + string.digits], str_length)))

    @staticmethod
    def generate_spec(spec_name, str_length):
        """
        :param spec_name: 前缀名称
        :param str_length: 指定长度数字
        :return:
        """
        return '{}{}'.format(spec_name,
                              "".join(random.sample([x for x in string.digits], str_length)))

    @staticmethod
    def generate_spec_password(pw_str_length):
        """
        :param pw_str_length: 指定长度
        :return:
        """
        return "".join(random.sample(string.ascii_letters, pw_str_length))

    @staticmethod
    def random_number(length=1, fmt="%Y%m%d%H%M"):
        """
        随机生成一组数字
        :param length: 默认生成1个数字，其他以时间格式生成
        :param fmt: 年月日时分格式生成就诊号
        :return:
        """
        if length == 1:
            return random.randint(0, 9)

        else:
            return datetime.datetime.now().strftime(fmt)

    def GBK2312(self):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
        val = f'{head:x}{body:x}'
        st = bytes.fromhex(val).decode('gb2312')
        return st

    def first_name(self):  # 随机取姓氏字典
        first_name_list = [
            '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
            '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
            '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
            '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
            '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
            '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
            '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
        n = random.randint(0, len(first_name_list) - 1)
        f_name = first_name_list[n]
        return f_name

    def second_name(self):
        # 随机取数组中字符，取到空字符则没有second_name
        second_name_list = [self.GBK2312(), '']
        n = random.randint(0, 1)
        s_name = second_name_list[n]
        return s_name

    def last_name(self):
        return self.GBK2312()

    def create_name(self):
        name = self.first_name() + self.second_name() + self.last_name()
        return name


cg = CommonGenerator()
if __name__ == '__main__':
    # common_generator = CommonGenerator()
    # new_str = common_generator.generate_spec_uuid('urc', 12)
    # verify_code = common_generator.generate_verify_code(6)
    # password_str = common_generator.generate_spec_password(8)
    # print(new_str, verify_code, password_str)
    print(cg.create_name())

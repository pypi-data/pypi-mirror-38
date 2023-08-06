# coding: utf-8
import random


class Student:
    def __init__(self, no=None):
        if not no:
            no = "{}{}1{:04}".format(random.randint(2008, 2019), random.randint(0, 4), random.randint(1, 2000))
        self.no = no
        self.ability = 100

    def work_hard(self):
        print("我用功学习，努力工作！")

    def succeed(self):
        print("完成理想，走向人生巅峰!")

    def celebrate(self):
        print("祝信息与通信工程学院十周年生日快乐!\n")

    def who_am_i(self):
        print('我是『{}』, 我是北邮人，也是信通人！'.format(self.no))

    @staticmethod
    def who_will_i_be(ideal=None, *args, **kwargs):
        print('我会成为什么样的人？')
        if callable(ideal):
            ideal(*args, **kwargs)
        else:
            print("成为自己的理想！")
        print()


class SICE:
    establish_year = 2008
    everyone = [Student() for i in range(100)]
    leaders = {
        'dean': '刘韵洁',
        'executive_dean': '张琳',
        'party_committee_secretary': '杨洁',
        'associate_dean': ['冯春燕', '尹长川', '苏菲'],
        'vice_secretary': ['罗梅娟', '王文华']
    }
    centers = [{
        '信息理论与技术教研中心': {
            '林家儒教授团队': {
                '主要科研方向': '通信中的信息处理、信息理论与通信网技术'
            },
            '张琳教授团队': {
                '主要科研方向': '通信中的信息处理、信息理论与通信网技术'
            },
        },
        '无线通信教研中心': {
            '王文博教授团队': {
                '主要科研方向': '无线通信信号处理理论'
            },
            '杨鸿文教授团队': {
                '主要科研方向': '无线理论与技术'
            },
        },
        '多媒体技术教研中心': {
            '门爱东教授团队': {
                '主要科研方向': '多媒体通信和数字图像处理数字内容处理技术、数字媒体创意与制作'
            },
            '景晓军教授团队': {
                '主要科研方向': '军事通信学、图像处理、信息安全、多媒体通信'
            },
        },
        '通信网技术教研中心': {
            '尹长川教授团队': {
                '主要科研方向': '通信网关键理论和技术'
            },
            '纪越峰教授团队': {
                '主要科研方向': '宽带通信系统与网络技术'
            },
            '温向明教授团队': {
                '主要科研方向': '信息通信网络理论、技术与应用'
            },
            '纪红教授团队 ': {
                '主要科研方向': '宽带信息网络及无线网络'
            },
        },
        '泛网无线教研中心': {
            '张平教授团队': {
                '主要科研方向': '新一代无线通信基础理论与网络技术'
            },
            '陶小峰教授团队': {
                '主要科研方向': '新一代无线通信基础理论与网络技术'
            },
            '蒋挺教授团队': {
                '主要科研方向': '短距离无线通信新技术'
            },
        },
        '网络搜索教研中心': {
            '郭军教授团队': {
                '主要科研方向': 'Web搜索理论与技术'
            },
        },
        '宽带网络监控教研中心': {
            '杨洁教授团队': {
                '主要科研方向': '网络数据科学与技术'
            },
        },
        '实验中心': '''
            实验中心总面积约2000平方米, 拥有各类仪器设备2500余件，设备固定资产达1600余万元。
            设有电路与电子技术创新实践基地、通信原理实验室、电磁场与微波实验室、计算机实验室、
            通信专业实验室、信息网络工程实验室及数字媒体艺术实验室。担负着全院本科生及部分研究生的
            专业基础实验、专业实验、课程设计、创新实践和各类相关竞赛等任务。
            在实验教学中着重体现“重视实践、培养能力、激励创新、发展个性、讲究综合、提高素质”的教育思想，
            培养了一批具有创新意识和创新能力的人才，是学校培养学生综合素质和实践能力的重要基地。
            2007年被评为国家级“电子信息”实验教学示范中心建设单位和北京市级“计算机与信息网络”实验教学示范中心建设单位。
            '''
    }]
    merger = ['电信工程学院', '信息工程学院']

    def __str__(self):
        return '北京邮电大学信息与通信工程学院'

    class Decennial:
        def __init__(self):
            self.current_year = 2018

        def __str__(self):
            return '北京邮电大学信息与通信工程学院十周年'

        @staticmethod
        def arriving():
            print(str(Decennial()) + "到来之际")

    @staticmethod
    def cultivate(student):
        print("接受信通院的培养，上课授予知识，实验授予能力")
        student.ability += random.randint(50, 1000)


class Decennial:
    def __init__(self):
        self.current_year = 2018

    def __str__(self):
        return '北京邮电大学信息与通信工程学院十周年'

    @staticmethod
    def arriving():
        print(str(Decennial()) + "到来之际")


if __name__ == '__main__':
    for sicer in SICE.everyone:
        sicer.who_am_i()
        SICE.cultivate(sicer)
        sicer.work_hard()
        sicer.succeed()
        Decennial.arriving()
        sicer.celebrate()

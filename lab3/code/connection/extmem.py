'''
本代码的功能为“模拟磁盘存储和缓冲区管理的简单实现”, 主要包括以下功能:
1. Buffer类: 实现缓冲区的基本功能, 包括空闲磁盘块、释放磁盘块、加载磁盘块到缓冲区、缓冲区写入磁盘块操作
2. drop_blk函数: 删除磁盘上的特定块
3. drop_blk_in_dir函数: 删除整个目录中的所有块
4. gene_data函数: 生成关系R和S的随机数据, 这些数据包括元组和元组中的属性值, 范围由预定义的参数确定。
5. write_disk函数: 将生成的关系实例写入模拟磁盘, 每个关系的数据被划分为多个磁盘块, 每个磁盘块保存一定数量的元组。
代码来源于https://github.com/RookieJunChen/HIT-Database/blob/master/%E5%AE%9E%E9%AA%8C/%E5%AE%9E%E9%AA%8C2/DBS_lab2/part1/extmem.py, 我仅为其添加了易于理解的注释

关系R具有两个属性A和B, 其中A和B的属性值均为int型(4个字节), A的值域为[1, 40], B的值域为[1, 1000]
关系S具有两个属性C和D, 其中C和D的属性值均为int型(4个字节)。C的值域为[20, 60], D的值域为[1, 1000]
'''

import os
from random import randint

disk_dir = './emulate_disk/raw_data/'  # 模拟磁盘所在的目录
tuple_num, blk_num1, blk_num2 = 7, 16, 32  # 每个磁盘块可以保存的元组数目，关系R的磁盘块数，关系S的磁盘块数
end_blk = -1 # 结束块编号

class Buffer:
    def __init__(self, blk_num: int = 8):
        self.io_num = 0  # 磁盘IO次数
        self.blk_num = blk_num  # 缓冲区块总数
        self.free_blk_num = self.blk_num  # 缓冲区空闲块数目
        self.data_occupy = [False] * self.blk_num  # 缓冲区占用情况，False表示未被占用
        self.data = [[]] * self.blk_num  # 缓冲区数据，数据为str类型

    # 获取一个空闲的缓冲区块索引，如果没有则返回-1
    def get_free_blk(self) -> int:
        for idx, flag in enumerate(self.data_occupy):
            if not flag:
                self.data_occupy[idx] = True
                self.free_blk_num -= 1
                return idx
        return -1

    # 指定释放一个已占用的缓冲区块，如果成功释放则返回True
    def free_blk(self, index) -> bool:  # 释放缓冲区的一个磁盘块
        flag = self.data_occupy[index]
        if flag:
            self.free_blk_num += 1
            self.data_occupy[index] = False
        return flag

    # 将指定地址的磁盘块加载到空闲的缓冲区块中，并返回缓冲区块索引
    def load_blk(self, addr: str) -> int:  # 加载磁盘块到缓冲区中，输入参数形如'./disk/relation/r15.blk'
        index = self.get_free_blk()
        if index != -1:
            with open(addr) as f:
                self.data_occupy[index] = True
                self.data[index] = f.read().split('\n')
                self.io_num += 1
        return index

    # 将缓冲区块数据写入指定地址的磁盘块，同时释放该缓冲区块
    def write_blk(self, addr, index):  # 将缓冲区中数据写入磁盘块
        with open(addr, 'w') as f:
            self.io_num += 1
            self.free_blk_num += 1
            self.data_occupy[index] = False
            f.write('\n'.join(self.data[index]))
            return True

    def write_buffer(self, data_lst: list, addr):  # 将CPU处理后的数据暂存入缓冲区，再存入磁盘
        index = self.get_free_blk()
        if index != -1:
            self.data[index] = data_lst
            self.write_blk(addr, index)
        return index != -1

# 给定磁盘块地址，如果存在则删除并返回True，如果不存在则返回False
def drop_blk(addr: str) -> bool:  # 存在返回真，不存在返回假
    blk_path = disk_dir + addr + '.blk'
    blk_exists = os.path.exists(blk_path)
    if blk_exists:
        os.remove(blk_path)
    return blk_exists

# 删除给定目录下的所有文件
def drop_blk_in_dir(file_dir: str):
    for file in os.listdir(file_dir):
        os.remove(file_dir + file)

# 生成R和S的随机数据，R和S均为列表，元素为二维元组，元组的第二个为连接属性，范围为1到1000
def gene_data():
    drop_blk_in_dir(disk_dir)
    # all_data是一个元组列表，包含两个元组（第一个元组代表关系S，第二个代表关系R），每个元组都包含五个元素，分别代表：关系（列表形式）、、关系的元组数目、属性的下界、属性的上界
    all_data, item = [([], set(), blk_num1 * tuple_num, 1, 40), ([], set(), blk_num2 * tuple_num, 20, 60)], None
    for data in all_data:
        for idx in range(data[2]):  # data[2]保存的是关系的元组数目
            while True:
                item = (randint(data[3], data[4]), randint(1, 1000))  # data[3]和data[4]保存属性A和C的值域上下界
                if item not in data[1]:  # data[1]是一个集合，用于生成唯一的元组
                    break
            data[0].append(item)  # data[0]用于保存最终结果
            data[1].add(item)
    return all_data[0][0], all_data[1][0]

# 将生成的关系实例写入磁盘块中
def write_disk(r_lst: list, s_lst: list):
    all_data = [('R', blk_num1, r_lst), ('S', blk_num2, s_lst)]
    for data in all_data:  # 将关系实例写入模拟磁盘
        for idx in range(data[1]):
            with open('%s%s%d.blk' % (disk_dir, data[0], idx+1), 'w') as f:
                blk_data = ['%d %d' % item for item in data[2][idx * tuple_num:(idx + 1) * tuple_num]]
                if idx+1 != data[1]:
                    blk_data.append('%s' % (idx+2))
                else:
                    blk_data.append('%s' % end_blk)
                f.write('\n'.join(blk_data))


if __name__ == '__main__':
    R, S = gene_data()  # 生成关系R和S的随机数据
    write_disk(R, S)  # 将数据写入模拟磁盘
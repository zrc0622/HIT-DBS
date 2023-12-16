from extmem import *

buffer_size = 8 # 缓冲区大小
emulate_disk_dir = "./emulate_disk/"
data_dir = emulate_disk_dir + "raw_data/"
select_dir = emulate_disk_dir + "output/select/"
project_dir = emulate_disk_dir + "output/project/"

# 基于扫描的选择算法, 只使用一块缓冲区（不包括输出缓冲区）
def select(buffer: Buffer, relationship, attribute, value): # 缓冲区、关系名、属性名、值
    # drop_blk_in_dir(select_dir) # 清空磁盘

    if buffer_size < 1:
        print("缓冲区大小不够")

    result = []
    result_num = 1 # 当前输出块数
    now_blk = 1 # 第一块磁盘

    if relationship == "R" and attribute == "A":
        attribute_index = 0
    elif relationship == "S" and attribute == "C":
        attribute_index = 0
    elif relationship == "R" and attribute == "B":
        attribute_index = 1
    elif relationship == "S" and attribute == "D":
        attribute_index = 1
    else:
        print(f"不存在关系{relationship}, 或关系{relationship}不存在属性{attribute}")
    
    item = (relationship, attribute_index, value)
    
    while now_blk != end_blk:
        index = buffer.load_blk('%s%s%d.blk' % (data_dir, item[0], now_blk)) # 加载磁盘块到缓冲区
        for data in buffer.data[index]:
            relationship_tuple = data.split()
            if len(relationship_tuple) == 2: # 如果不是下一块的索引
                if int(relationship_tuple[item[1]]) == item[2]:
                    result.append(data)
                    if len(result) == tuple_num: # 输出缓冲区满（假设输出缓冲区只有一块，不算在输入缓冲区里）
                        result.append('%s' % (result_num + 1))
                        buffer.write_buffer(result, '%s%s%d.blk' % (select_dir, item[0], result_num))
                        result_num += 1
                        result = []
            else:
                now_blk = int(relationship_tuple[0])
        buffer.free_blk(index)
    
    result.append('%s' % end_blk)
    buffer.write_buffer(result, '%s%s%d.blk' % (select_dir, item[0], result_num))

# 不带去重的投影算法
def project(buffer:Buffer, relationship, attribute): # TODO: 基于排序（外排序）的去重算法
    # drop_blk_in_dir(project_dir) # 清空磁盘
    
    result = []
    result_num = 1 # 当前输出块数
    now_blk = 1 # 第一块磁盘

    if relationship == "R" and attribute == "A":
        attribute_index = 0
    elif relationship == "S" and attribute == "C":
        attribute_index = 0
    elif relationship == "R" and attribute == "B":
        attribute_index = 1
    elif relationship == "S" and attribute == "D":
        attribute_index = 1
    else:
        print(f"不存在关系{relationship}, 或关系{relationship}不存在属性{attribute}")

    item = (relationship, attribute_index)
    
    while now_blk != end_blk:
        index = buffer.load_blk('%s%s%d.blk' % (data_dir, item[0], now_blk)) # 加载磁盘块到缓冲区
        for data in buffer.data[index]:
            relationship_tuple = data.split()
            if len(relationship_tuple) == 2: # 如果不是下一块的索引
                result.append('%s' % relationship_tuple[item[1]])
                if len(result) == tuple_num*2: # 输出缓冲区满（假设输出缓冲区只有一块，不算在输入缓冲区里）
                    result.append('%s' % (result_num + 1))
                    buffer.write_buffer(result, '%s%s%d.blk' % (project_dir, item[0], result_num))
                    result_num += 1
                    result = []
            else:
                now_blk = int(relationship_tuple[0])
        buffer.free_blk(index)
    
    result.append('%s' % end_blk)
    buffer.write_buffer(result, '%s%s%d.blk' % (project_dir, item[0], result_num))

    

# 清空缓冲区
def clear_buffer(buffer:Buffer):
    for index in range(buffer_size):
        buffer.free_blk(index)

def main():
    buffer = Buffer(buffer_size) # 创建缓冲区  
    select(buffer, 'R', 'A', 40)
    select(buffer, 'S', 'C', 60)

    clear_buffer(buffer)
    project(buffer, 'R', 'A')



if __name__ == "__main__":
    main()
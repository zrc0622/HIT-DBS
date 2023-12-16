from extmem import *

# TODO: 缓冲区大小检查

buffer_size = 8 # 缓冲区大小
emulate_disk_dir = "./emulate_disk/"
data_dir = emulate_disk_dir + "raw_data/"
select_dir = emulate_disk_dir + "output/select/"
project_dir = emulate_disk_dir + "output/project/"
nested_loop_join_dir = emulate_disk_dir + "output/join/nested_loop/"
sort_merge_join_dir = emulate_disk_dir + "output/join/sort_merge/"
sort_dir = emulate_disk_dir + "output/sort/"

# 基于扫描的选择算法, 只使用1个缓冲块，另外输出使用1个
def select(buffer: Buffer, relationship, attribute, value): # 缓冲区、关系名、属性名、值
    if buffer_size < 2:
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

# 不带去重的投影算法, 只使用1个缓冲块，另外输出使用1个
def project(buffer:Buffer, relationship, attribute): # TODO: 基于排序（外排序）的去重算法
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

def join(type, buffer, relationship1, attribute1, relationship2, attribute2):
    if relationship1 == "R" and attribute1 == "A":
        attribute_index1 = 0
    elif relationship1 == "R" and attribute1 == "B":
        attribute_index1 = 1
    else:
        print(f"不存在关系{relationship1}, 或关系{relationship1}不存在属性{attribute1}")
    
    if relationship2 == "S" and attribute2 == "C":
        attribute_index2 = 0
    elif relationship2 == "S" and attribute2 == "D":
        attribute_index2 = 1
    else:
        print(f"不存在关系{relationship2}, 或关系{relationship2}不存在属性{attribute2}")
    
    if type == 'nested loop':
        nested_loop_join(buffer, relationship1, attribute_index1, relationship2, attribute_index2)
    if type == 'sort merge':
        sort_merge_join(buffer, relationship1, attribute_index1, relationship2, attribute_index2)

# 基于块的嵌套循环连接算法（外层使用6个缓冲块，内层使用1个，输出使用1个）
def nested_loop_join(buffer:Buffer, relationship1, index1, relationship2, index2):
    result = []
    result_num = 1 # 当前输出块数
    now_blk1 = 1 # 关系R第一块磁盘，当前正在读的块
    now_blk2 = 1 # 关系S第一块磁盘

    while now_blk1 != end_blk: # 外层循环
        outer_index_list = [] # 外层缓冲区索引
        for _ in range(buffer_size - 2): # 载入R的6个块，留一块输出，留一块给S
            outer_index = buffer.load_blk('%s%s%d.blk' % (data_dir, relationship1, now_blk1))
            outer_index_list.append(outer_index)
            now_blk1 = int(((buffer.data[outer_index_list[-1]])[-1].split())[0]) # 取出下一块的地址
            if now_blk1 == -1:
                break
        while now_blk2 != end_blk: # 内层循环
            inner_index = buffer.load_blk('%s%s%d.blk' % (data_dir, relationship2, now_blk2))
            now_blk2 = int(((buffer.data[inner_index])[-1].split())[0])
            
            for outer_index in outer_index_list: # 缓冲区排序
                for outer_data in buffer.data[outer_index]:
                    outer_tuple = outer_data.split()
                    if len(outer_tuple) == 2: # 如果不是下一块的索引
                        for inner_data in buffer.data[inner_index]:
                            inner_tuple = inner_data.split()
                            if len(inner_tuple) == 2:
                                if outer_tuple[index1] == inner_tuple[index2]:
                                    result.append('%s %s %s' % (outer_tuple[abs(index1-1)], inner_tuple[abs(index2-1)], outer_tuple[index1]))
                                    if len(result) == 5: # 输出缓冲区满（假设输出缓冲区只有一块，不算在输入缓冲区里，一块64字节能存(64-4)/(4*3)=5个元组）
                                        result.append('%s' % (result_num + 1))
                                        buffer.write_buffer(result, '%s%s%s%d.blk' % (nested_loop_join_dir, relationship1, relationship2, result_num))
                                        result_num += 1
                                        result = []
            
            buffer.free_blk(inner_index) # 释放内层占用缓冲区
        
        for outer_index in outer_index_list: # 释放外层占用缓冲区
            buffer.free_blk(outer_index)

    result.append('%s' % end_blk)
    buffer.write_buffer(result, '%s%s%s%d.blk' % (nested_loop_join_dir, relationship1, relationship2, result_num))

# 外排序算法(多路外存归并排序，每个归并段7页，即使用7个缓冲块，另外输出使用1个)
def sort(buffer:Buffer, relationship, attribute_index):
    now_blk = 1
    segment_num = 1
    
    # 创建归并段
    while now_blk != -1:
        result = []
        result_num = 1
        index_list = [] # 占用缓冲区索引
        sort_list = [] # 缓冲区中需要排序的键值列表
        for _ in range(buffer_size - 1): # 载入7个块，留一块作为输出
            index = buffer.load_blk('%s%s%d.blk' % (data_dir, relationship, now_blk))
            index_list.append(index)
            now_blk = int(((buffer.data[index_list[-1]])[-1].split())[0]) # 取出下一块地址
            if now_blk == -1:
                break
        for index in index_list:
            for data in buffer.data[index]:
                relationship_tuple = data.split()
                if len(relationship_tuple) == 2: # 如果不是下一块的索引
                    sort_list.append(int(relationship_tuple[attribute_index]))
        sorted_indices = sorted(range(len(sort_list)), key=lambda k: sort_list[k]) # 对缓冲区的元组进行排序，并获取结果索引
        for sort_index in sorted_indices:
            index1, index2 = divmod(sort_index, 7) 
            buffer_index = index_list[index1] # 块索引
            result.append((buffer.data[buffer_index])[index2])
            if len(result) == 7: # 输出缓冲区满
                result.append('%s' % (result_num + 1))
                buffer.write_buffer(result, '%s%d%s%d.blk' % (sort_dir, segment_num, relationship, result_num))
                result_num += 1
                result = []

        result.append('%s' % end_blk)
        buffer.write_buffer(result, '%s%d%s%d.blk' % (sort_dir, segment_num, relationship, result_num)) # 段名+关系名+块序号

        for index in index_list: # 释放外层占用缓冲区
            buffer.free_blk(index)
        
        segment_num += 1

    return segment_num

# 排序归并连接
def sort_merge_join(buffer:Buffer, relationship1, index1, relationship2, index2):
    # 归并排序
    segment_num1 = sort(buffer, relationship1, index1)
    # sort_data_dir2 = sort(buffer, relationship2, index2)

# 清空所有缓冲区
def clear_buffer(buffer:Buffer):
    for index in range(buffer_size):
        buffer.free_blk(index)

def main():
    buffer = Buffer(buffer_size) # 创建缓冲区
    # # drop_blk_in_dir(select_dir) # 清空磁盘
    # select(buffer, 'R', 'A', 40)
    # select(buffer, 'S', 'C', 60)

    # clear_buffer(buffer)
    # # drop_blk_in_dir(project_dir) # 清空磁盘
    # project(buffer, 'R', 'A')

    # clear_buffer(buffer)
    # # drop_blk_in_dir(nested_loop_join_dir) # 清空磁盘
    # join('nested loop', buffer, 'R', 'A', 'S', 'C')

    clear_buffer(buffer)
    # drop_blk_in_dir(sort_merge_join_dir) # 清空磁盘
    join('sort merge', buffer, 'R', 'A', 'S', 'C')


if __name__ == "__main__":
    main()
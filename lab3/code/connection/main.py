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

    if result: 
        result.append('%s' % end_blk)
        buffer.write_buffer(result, '%s%s%d.blk' % (select_dir, item[0], result_num))
    else:
        index = buffer.load_blk('%s%s%d.blk' % (select_dir, item[0], result_num-1))
        x = buffer.data[index]
        buffer.free_blk(index)
        x[-1]= '-1'
        buffer.write_buffer(x, '%s%s%d.blk' % (select_dir, item[0], result_num-1))

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
    
    if result: 
        result.append('%s' % end_blk)
        buffer.write_buffer(result, '%s%s%d.blk' % (project_dir, item[0], result_num))
    else:
        index = buffer.load_blk('%s%s%d.blk' % (project_dir, item[0], result_num-1))
        x = buffer.data[index]
        buffer.free_blk(index)
        x[-1]= '-1'
        buffer.write_buffer(x, '%s%s%d.blk' % (project_dir, item[0], result_num-1))

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
        now_blk2 = 1
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

    if result: 
        result.append('%s' % end_blk)
        buffer.write_buffer(result, '%s%s%s%d.blk' % (nested_loop_join_dir, relationship1, relationship2, result_num))
    else:
        index = buffer.load_blk('%s%s%s%d.blk' % (nested_loop_join_dir, relationship1, relationship2, result_num - 1))
        x = buffer.data[index]
        buffer.free_blk(index)
        x[-1]= '-1'
        buffer.write_buffer(x, '%s%s%s%d.blk' % (nested_loop_join_dir, relationship1, relationship2, result_num - 1))

# 外排序算法(多路外存归并排序，每个归并段7页，即使用7个缓冲块，另外输出使用1个)
def sort(buffer:Buffer, relationship, attribute_index):
    now_blk = 1
    segment_num = 0
    
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
            index1, index2 = divmod(sort_index, 7) # TODO: 此处假设所有的块都被填满7个
            buffer_index = index_list[index1] # 块索引
            result.append((buffer.data[buffer_index])[index2])
            if len(result) == 7: # 输出缓冲区满
                result.append('%s' % (result_num + 1))
                buffer.write_buffer(result, '%s%d%s%d.blk' % (sort_dir, segment_num + 1, relationship, result_num))
                result_num += 1
                result = []
        
        if result: 
            result.append('%s' % end_blk)
            buffer.write_buffer(result, '%s%d%s%d.blk' % (sort_dir, segment_num + 1, relationship, result_num)) # 段名+关系名+块序号
        else:
            index = buffer.load_blk('%s%d%s%d.blk' % (sort_dir, segment_num + 1, relationship, result_num - 1))
            x = buffer.data[index]
            buffer.free_blk(index)
            x[-1] = '-1'
            buffer.write_buffer(x, '%s%d%s%d.blk' % (sort_dir, segment_num + 1, relationship, result_num - 1))


        for index in index_list: # 释放外层占用缓冲区
            buffer.free_blk(index)
        
        segment_num += 1

    # 多路归并
    count = 0
    threshold = 0
    result = []
    result_num = 1
    now_blk_list = [1]*segment_num # 每段存储块索引+1（即名称中的段数）
    now_tuple_list = [0]*segment_num # 当前每段的元组索引
    index_list = []
    for segment in range(segment_num): # 读入每段第一块
        index = buffer.load_blk('%s%d%s%d.blk' % (sort_dir, segment + 1, relationship, 1))
        index_list.append(index)
    while any(now_blk !=-1 for now_blk in now_blk_list) or any(now_index != 7 for now_index in now_tuple_list):
        # 从缓冲区中选最小的
        sort_list = []
        for index in index_list: # 取出所有需要比较的属性
            for data in buffer.data[index]:
                relationship_tuple = data.split()
                if len(relationship_tuple) == 2: # 如果不是下一块的索引
                    sort_list.append(int(relationship_tuple[attribute_index]))
        if count == 0:
            min_value = min([value for value in sort_list if value > threshold])
        if count == 1:
            min_value = min([value for value in sort_list if value == threshold])
            count = 0
        threshold = min_value
        min_indices = [index for index, value in enumerate(sort_list) if value == min_value] # 返回最小值索引
        # 放入result中并修改元组索引; 当元组长度为1时更换块，并更新存储块索引
        for min_index in min_indices:
            index1, index2 = divmod(min_index, 7) # TODO: 此处假设每块都被填满7个
            if index2 >= now_tuple_list[index1]:
                buffer_index = index_list[index1]
                result.append((buffer.data[buffer_index])[index2])
                now_tuple_list[index1] += 1 # 更新元组索引
            x = ((buffer.data[buffer_index])[index2+1]).split()
            if len(x) == 1:
                if x[0] == '-1':
                    now_blk_list[index1] = -1
                else:
                    count = 1
                    buffer.free_blk(buffer_index)
                    index = buffer.load_blk('%s%d%s%d.blk' % (sort_dir, index1 + 1, relationship, int(x[0]))) # 载入新的块
                    now_blk_list[index1] = int(x[0]) # 更新存储块索引
                    now_tuple_list[index1] = 0
            
            if len(result) == 7: # 输出缓冲区满
                result.append('%s' % (result_num + 1))
                buffer.write_buffer(result, '%s%s%d.blk' % (sort_dir, relationship, result_num))
                result_num += 1
                result = []
    

    for index in index_list: # 释放占用缓冲区
        buffer.free_blk(index)

    if result: 
        result.append('%s' % end_blk)
        buffer.write_buffer(result, '%s%s%d.blk' % (sort_dir, relationship, result_num)) # 段名+关系名+块序号
    else:
        index = buffer.load_blk('%s%s%d.blk' % (sort_dir, relationship, result_num - 1))
        x = buffer.data[index]
        buffer.free_blk(index)
        x[-1] = '-1'
        buffer.write_buffer(x, '%s%s%d.blk' % (sort_dir, relationship, result_num - 1))

    return segment_num

# 排序归并连接，无法直接进行排序归并连接，先分段排序，再对各段排序，最后对排序结果进行连接
def sort_merge_join(buffer:Buffer, relationship1, index1, relationship2, index2):
    # # 归并排序
    # segment_num1 = sort(buffer, relationship1, index1)
    # segment_num2 = sort(buffer, relationship2, index2)
    done1 = False
    done2 = False

    buffer_index1 = -1 # 关系R占用的缓冲块索引
    buffer_index2 = -1

    now_read1 = 0 # 关系R当前读到的元组索引
    now_read2 = 0

    now_blk1 = 1 # 关系R当前读到的磁盘块索引
    now_blk2 = 1

    join_index1 = [] # 关系R用于连接的元组值
    join_index2 = []

    now_value = 0 # 当前连接键值
    find = False # 是否找到连接键值

    buffer_index1 = buffer.load_blk('%s%s%d.blk' % (sort_dir, relationship1, now_blk1))
    read1 = ((buffer.data[buffer_index1])[now_read1]).split()
    buffer_index2 = buffer.load_blk('%s%s%d.blk' % (sort_dir, relationship2, now_blk2))
    read2 = ((buffer.data[buffer_index2])[now_read2]).split()

    result = []
    result_num = 1

    # 1找R和S大于now_value最小的
        # 2如果不等 小者清除所有缓存块 并读取一个新的块 返回1
        # 3如果相等 
            # 4取出相等的索引，放入join_index1中
                #如果最后一个是7，则读入新的块，放回1
    
    while (not done1) and (not done2): # TODO: 假设每块都满
        last_read1 = read1
        read1 = ((buffer.data[buffer_index1])[now_read1]).split()
        last_read2 = read2
        read2 = ((buffer.data[buffer_index2])[now_read2]).split()
        
        # 如果缺块则换下一块
        if len(read1) == 1 and read1[0] != '-1':
            buffer.free_blk(buffer_index1)
            now_blk1 = int(read1[0])
            buffer_index1 = buffer.load_blk('%s%s%d.blk' % (sort_dir, relationship1, now_blk1))
            now_read1 = 0
            read1 = ((buffer.data[buffer_index1])[now_read1]).split()
        if read1[0] == '-1':
            read1 = last_read1
            done1 = True
        if len(read2) == 1 and read2[0] != '-1':
            buffer.free_blk(buffer_index2)
            now_blk2 = int(read2[0])
            buffer_index2 = buffer.load_blk('%s%s%d.blk' % (sort_dir, relationship2, now_blk2))
            now_read2 = 0
            read2 = ((buffer.data[buffer_index2])[now_read2]).split()
        if read2[0] == '-1':
            read2 = last_read2
            done2 = False

        if not find:
            if int(read1[index1]) == int(read2[index2]):
                find = True
                now_value = int(read1[index1])
            else:
                if int(read1[index1]) > int(read2[index2]):
                    now_read2 += 1
                else:
                    now_read1 += 1
        
        if find:
            while int(read1[index1]) == now_value:
                join_index1.append(read1)
                now_read1 += 1
                read1 = ((buffer.data[buffer_index1])[now_read1]).split()
                if len(read1) == 1 and read1[0] != '-1':
                    buffer.free_blk(buffer_index1)
                    now_blk1 = int(read1[0])
                    buffer_index1 = buffer.load_blk('%s%s%d.blk' % (sort_dir, relationship1, now_blk1))
                    now_read1 = 0
                    read1 = ((buffer.data[buffer_index1])[now_read1]).split()
            while int(read2[index2]) == now_value:
                join_index2.append(read2)
                now_read2 += 1
                read2 = ((buffer.data[buffer_index2])[now_read2]).split()
                if len(read2) == 1 and read2[0] != '-1':
                    buffer.free_blk(buffer_index2)
                    now_blk2 = int(read2[0])
                    buffer_index2 = buffer.load_blk('%s%s%d.blk' % (sort_dir, relationship2, now_blk2))
                    now_read2 = 0
                    read2 = ((buffer.data[buffer_index2])[now_read2]).split()
            for data1 in join_index1:
                for data2 in join_index2:
                    result.append('%s %s %s' % (data1[abs(index1-1)], data2[abs(index2-1)], data1[index1]))
                    if len(result) == 5: # 输出缓冲区满（假设输出缓冲区只有一块，不算在输入缓冲区里，一块64字节能存(64-4)/(4*3)=5个元组）
                        result.append('%s' % (result_num + 1))
                        buffer.write_buffer(result, '%s%s%s%d.blk' % (sort_merge_join_dir, relationship1, relationship2, result_num))
                        result_num += 1
                        result = []
            join_index1 = []
            join_index2 = []
            find = False

    if result: 
        result.append('%s' % end_blk)
        buffer.write_buffer(result, '%s%s%s%d.blk' % (sort_merge_join_dir, relationship1, relationship2, result_num))
    else:
        index = buffer.load_blk('%s%s%s%d.blk' % (sort_merge_join_dir, relationship1, relationship2, result_num - 1))
        x = buffer.data[index]
        buffer.free_blk(index)
        x[-1]= '-1'
        buffer.write_buffer(x, '%s%s%s%d.blk' % (sort_merge_join_dir, relationship1, relationship2, result_num - 1))
    
    buffer.free_blk(buffer_index1)
    buffer.free_blk(buffer_index2)

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

    clear_buffer(buffer)
    drop_blk_in_dir(nested_loop_join_dir) # 清空磁盘
    join('nested loop', buffer, 'R', 'A', 'S', 'C')

    # clear_buffer(buffer)
    # # drop_blk_in_dir(sort_merge_join_dir) # 清空磁盘
    # join('sort merge', buffer, 'R', 'A', 'S', 'C')


if __name__ == "__main__":
    main()
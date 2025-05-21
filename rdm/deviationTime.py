import openpyxl

# 统计任务偏离度
# 定义全局变量存储偏离数据
deviation_data = {
    "产品": {"positive": {}, "positive_time": {}, "negative": {}, "negative_time": {}},
    "项目": {"positive": {}, "positive_time": {}, "negative": {}, "negative_time": {}},
    "日常": {"positive": {}, "positive_time": {}, "negative": {}, "negative_time": {}}
}

# 读取 Excel 文件
def read_excel(file_path):
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        sheet = wb.active

        # 遍历每一行数据
        for row in sheet.iter_rows(min_row=2, values_only=True):  # 从第二行开始
            degree_type = row[15]
            if degree_type == "否":
                continue

            create_user = row[13]
            actual_time = float(row[10])
            deviation_type = "positive" if time_diff >= 0 else "negative"
            time_diff = abs(time_diff)

            update_deviation_data(task_type, create_user, time_diff, deviation_type)
    except openpyxl.utils.exceptions.InvalidFileException:
        print(f"无效的文件格式: {file_path}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    finally:
        wb.close()

def update_deviation_data(task_type, user, time_diff, deviation_type):
    count_map = deviation_data[task_type][deviation_type]
    time_map = deviation_data[task_type][f"{deviation_type}_time"]
    
    if user in count_map:
        count_map[user] += 1
        time_map[user] += time_diff
    else:
        count_map[user] = 1
        time_map[user] = time_diff

def print_results():
    for task_type, data in deviation_data.items():
        print(f"{task_type}+++++++++++++++++++++++++++++++++++++++++++++++")

# 打印结果
def print_results():
    for task_type, data in deviation_data.items():
        print(f"{task_type}+++++++++++++++++++++++++++++++++++++++++++++++")
        compare_and_print(data["positive"], data["negative"], data["positive_time"], data["negative_time"])

# 比较并打印结果
def compare_and_print(pos_map, neg_map, pos_time_map, neg_time_map):
    for user, count in pos_map.items():
        if user in neg_map:
            print(f"{user} {count} {neg_map[user]} {pos_time_map[user]} {neg_time_map[user]}")
            neg_map.pop(user)

    print("-----------------------------------------------")
    for user, count in neg_map.items():
        print(f"{user} {count} {neg_time_map[user]}")

if __name__ == "__main__":
    # 调用函数读取文件和打印结果
    read_excel("D:\明朝万达\研发管理\任务管理\任务审计-202410.xlsx")
    print_results()

import openpyxl

# 统计不同技术技术人员在不同难度任务的任务数量以及工时数据

# 全局字典，用于存储任务数据
product_high_task_map = {}
product_middle_task_map = {}
product_low_task_map = {}
project_high_task_map = {}
project_middle_task_map = {}
project_low_task_map = {}
daily_high_task_map = {}
daily_middle_task_map = {}
daily_low_task_map = {}

# 定义任务优先级类别
task_clt_high = "高"
task_clt_middle = "中"
task_clt_low = "低"

def read_excel(file_path):
    """
    读取Excel文件并根据分类处理任务数据。

    :param file_path: Excel文件路径
    """
    try:
        # 打开Excel工作簿
        workbook = openpyxl.load_workbook(file_path, read_only=True)
        sheet = workbook.active  # 默认读取第一个工作表

        for row_idx, row in enumerate(sheet.iter_rows()):
            if row_idx == 0:
                # 跳过表头行
                continue

            # 获取相关单元格的值
            task_type = str(row[14].value).strip()  
            clt = str(row[3].value).strip()  
            actual_time = float(row[10].value or 0) 

            # 将任务数据分类到对应的字典中
            categorize_task(task_type, clt, actual_time)

        # 打印每个分类的统计信息
        print_map_statistics("高级-高", product_high_task_map)
        print_map_statistics("中级-高", project_high_task_map)
        print_map_statistics("低级-高", daily_high_task_map)

        print_map_statistics("高级-中", product_middle_task_map)
        print_map_statistics("中级-中", project_middle_task_map)
        print_map_statistics("低级-中", daily_middle_task_map)

        print_map_statistics("高级-低", product_low_task_map)
        print_map_statistics("中级-低", project_low_task_map)
        print_map_statistics("初级-低", daily_low_task_map)

    except Exception as e:
        print(f"发生错误: {e}")

def categorize_task(task_type, clt, actual_time):
    """
    根据任务类型和优先级将任务分类到对应的字典中。

    :param task_type: 任务类型
    :param clt: 任务优先级 (高、中、低)
    :param actual_time: 实际耗时
    """
    if task_type in ["T10", "T19", "T8"]:
        update_task_map(product_high_task_map, product_middle_task_map, product_low_task_map, clt, actual_time)
    elif task_type in ["T7", "T6", "T5"]:
        update_task_map(project_high_task_map, project_middle_task_map, project_low_task_map, clt, actual_time)
    elif task_type in ["T4", "T3", "T2", "T1"]:
        update_task_map(daily_high_task_map, daily_middle_task_map, daily_low_task_map, clt, actual_time)

def update_task_map(high_map, middle_map, low_map, clt, actual_time):
    """
    根据任务优先级更新对应的任务字典。

    :param high_map: 高优先级任务字典
    :param middle_map: 中优先级任务字典
    :param low_map: 低优先级任务字典
    :param clt: 任务优先级 (高、中、低)
    :param actual_time: 实际耗时
    """
    if clt == task_clt_high:
        high_map[len(high_map)] = high_map.get(len(high_map), 0) + actual_time
    elif clt == task_clt_middle:
        middle_map[len(middle_map)] = middle_map.get(len(middle_map), 0) + actual_time
    elif clt == task_clt_low:
        low_map[len(low_map)] = low_map.get(len(low_map), 0) + actual_time

def print_map_statistics(map_name, task_map):
    """
    打印任务字典的统计信息。

    :param map_name: 任务字典名称
    :param task_map: 任务字典
    """
    count = len(task_map)
    total_time = sum(task_map.values())
    print(f"{map_name}: {count} 个任务，总耗时: {total_time}")

# 示例调用
read_excel("D:\明朝万达\研发管理\任务管理\任务审计-202410.xlsx")

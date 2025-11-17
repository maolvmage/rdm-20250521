#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
nginx日志分析工具

该脚本用于分析nginx访问日志，统计不同员工在指定时间段内的访问次数。
"""

import re
import os
import datetime  # 新增datetime模块
from datetime import datetime  # 修正导入方式
import pandas as pd

# 固定配置
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')  # 日志目录
# 生成当天日期字符串
current_date = datetime.now().strftime("%Y%m%d")  # 修正调用方式
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), f'员工访问统计{current_date}.xlsx')
EMPLOYEE_FILE = os.path.join(os.path.dirname(__file__), 'IP信息.xlsx')  # 员工信息文件
START_TIME = '2025-10-01 00:00:00'  # 开始时间
END_TIME = '2025-11-01 00:00:00'  # 结束时间

def parse_nginx_log(log_file):
    """
    解析nginx日志文件，提取IP地址和时间

    Args:
        log_file: nginx日志文件路径

    Returns:
        访问记录列表，每条记录包含IP地址和时间
    """
    access_records = []

    # nginx日志格式的正则表达式
    # 示例: 192.168.8.106 - - [07/May/2025:05:20:17 +0000] "GET /activate?email=...
    pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(\d+/\w+/\d+:\d+:\d+:\d+ [+\-]\d+)\] "POST .*"'

    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                ip = match.group(1)
                time_str = match.group(2)

                # 将nginx日志时间格式转换为datetime对象
                # 格式: 07/May/2025:05:20:17 +0000
                try:
                    # 解析原始时间
                    time_obj = datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S %z')

                    # 将时间调整为北京时间（+8小时）
                    from datetime import timedelta
                    time_obj = time_obj + timedelta(hours=8)

                    access_records.append({'ip': ip, 'time': time_obj})
                except ValueError as e:
                    print(f"时间解析错误: {e}, 原始时间字符串: {time_str}")
                    continue

    return access_records


def filter_by_time_range(records, start_time, end_time):
    """
    按时间范围过滤访问记录

    Args:
        records: 访问记录列表
        start_time: 开始时间
        end_time: 结束时间

    Returns:
        过滤后的访问记录列表
    """
    filtered_records = []

    for record in records:
        if start_time <= record['time'] <= end_time:
            filtered_records.append(record)

    return filtered_records


def count_access_by_employee(records, employee_info):
    """
    统计每个员工的访问次数

    Args:
        records: 访问记录列表
        employee_info: 员工信息DataFrame

    Returns:
        员工访问统计DataFrame
    """
    # 创建IP地址到员工信息的映射
    ip_to_employee = {}
    for _, row in employee_info.iterrows():
        ip_to_employee[row['IP']] = {'工号': row['工号'], '姓名': row['姓名']}

    # 统计每个IP的访问次数
    ip_counts = {}
    for record in records:
        ip = record['ip']
        if ip in ip_counts:
            ip_counts[ip] += 1
        else:
            ip_counts[ip] = 1

    # 创建员工访问统计结果
    result = []
    for _, row in employee_info.iterrows():
        employee_id = row['工号']
        name = row['姓名']
        ip = row['IP']

        # 如果员工IP在访问记录中，获取访问次数，否则为0
        count = ip_counts.get(ip, 0)

        result.append({
            '工号': employee_id,
            '姓名': name,
            'IP': ip,
            '访问次数': count
        })

    return pd.DataFrame(result)


def main():
    # 将输入的时间字符串转换为datetime对象
    try:
        start_time = datetime.strptime(START_TIME, '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.now().astimezone().tzinfo)
        end_time = datetime.strptime(END_TIME, '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.now().astimezone().tzinfo)
    except ValueError:
        print("错误: 时间格式不正确，请使用 YYYY-MM-DD HH:MM:SS 格式")
        return

    # 检查日志目录是否存在
    if not os.path.exists(LOG_DIR) or not os.path.isdir(LOG_DIR):
        print(f"错误: 找不到日志目录 {LOG_DIR} 或者它不是一个目录")
        return

    # 检查员工信息文件是否存在
    if not os.path.exists(EMPLOYEE_FILE):
        print(f"错误: 找不到员工信息文件 {EMPLOYEE_FILE}")
        return

    # 读取员工信息
    try:
        employee_info = pd.read_excel(EMPLOYEE_FILE)
    except Exception as e:
        print(f"读取员工信息文件时出错: {e}")
        return

    # 获取目录中的所有文件
    log_files = []
    for file in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, file)
        if os.path.isfile(file_path):
            log_files.append(file_path)

    if not log_files:
        print(f"警告: 目录 {LOG_DIR} 中没有找到任何文件")
        return

    # 解析所有nginx日志
    print("正在解析nginx日志...")
    all_access_records = []

    for log_file in log_files:
        print(f"正在处理日志文件: {log_file}")
        try:
            access_records = parse_nginx_log(log_file)
            all_access_records.extend(access_records)
            print(f"- 从 {log_file} 解析了 {len(access_records)} 条记录")
        except Exception as e:
            print(f"处理文件 {log_file} 时出错: {e}")
            continue

    print(f"共解析 {len(all_access_records)} 条访问记录")

    # 按时间范围过滤
    print(f"正在过滤 {START_TIME} 到 {END_TIME} 的记录...")
    filtered_records = filter_by_time_range(all_access_records, start_time, end_time)
    print(f"过滤后有 {len(filtered_records)} 条记录")

    # 统计每个员工的访问次数
    print("正在统计每个员工的访问次数...")
    result_df = count_access_by_employee(filtered_records, employee_info)

    # 保存结果到Excel文件
    try:
        result_df.to_excel(OUTPUT_FILE, index=False)
        print(f"结果已保存到 {OUTPUT_FILE}")
    except Exception as e:
        print(f"保存结果时出错: {e}")


if __name__ == "__main__":
    main()

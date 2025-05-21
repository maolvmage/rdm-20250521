import pandas as pd
import os

# 定义Excel文件夹路径
excel_folder = r"e:\workspace\python\rdm\rdm\excel"

# 从员工信息.xlsx中读取姓名和工号，并保留原始顺序
employee_info = pd.read_excel(os.path.join(excel_folder, '员工信息.xlsx'))
employee_info = employee_info[['姓名', '工号']]
employee_info['工号'] = employee_info['工号'].astype(str).str.zfill(4)

# 读取员工考勤月表信息
attendance_file = os.path.join(excel_folder, '员工考勤月表信息.xlsx')
attendance_data = pd.read_excel(attendance_file)

# 计算加班时长
attendance_data['加班时长'] = (attendance_data['实际工作时长（小时）'] + 
                             attendance_data['外出时长（小时）'] - 
                             attendance_data['标准工作时长（小时）']).round()

# 按姓名汇总加班时长
overtime_summary = attendance_data.groupby('姓名')['加班时长'].sum().reset_index()

# 获取文件夹下所有Excel文件，排除员工信息.xlsx
excel_files = [os.path.join(excel_folder, f) for f in os.listdir(excel_folder) 
               if (f.endswith('.xlsx') or f.endswith('.xls')) and f != '员工信息.xlsx']

# 创建一个空的DataFrame用于存储汇总数据
merged_data = pd.DataFrame()

# 遍历所有Excel文件
for file in excel_files:
    try:
        # 读取Excel文件的第一个sheet
        df = pd.read_excel(file, sheet_name=0)
        
        # 检查绩效评定列是否存在
        if '绩效评定' not in df.columns:
            print(f"警告: 文件 {file} 中不存在 '绩效评定' 列")
            continue
            
        # 假设列名为：姓名、绩效评定
        df = df[['姓名', '绩效评定']]
        
        # 将绩效评定转换为大写
        df['绩效评定'] = df['绩效评定'].str.upper()
        
        # 只保留在员工信息.xlsx中的员工
        df = df[df['姓名'].isin(employee_info['姓名'])]
        
        # 将数据添加到汇总DataFrame中
        merged_data = pd.concat([merged_data, df], ignore_index=True)
        
    except Exception as e:
        print(f"处理文件 {file} 时发生错误: {str(e)}")
        continue

# 定义绩效等级
performance_levels = ['B', 'C+', 'C', 'C-', 'D', 'E']

# 按姓名进行汇总
result = merged_data.groupby('姓名').agg({
    '绩效评定': lambda x: x.value_counts().reindex(performance_levels, fill_value=0)
}).reset_index()

# 展开绩效评定列
result = pd.concat([result.drop('绩效评定', axis=1), 
                   result['绩效评定'].apply(pd.Series)], axis=1)

# 重命名列
result.columns = ['姓名'] + performance_levels

# 按照员工信息.xlsx中的顺序排序，并添加工号列
result = employee_info.merge(result, on='姓名', how='left')

# 添加加班总时长
result = result.merge(overtime_summary, on='姓名', how='left')

# 去掉绩效总数为0的记录
result = result[result[performance_levels].sum(axis=1) > 0]

# 将结果保存到新的Excel文件
output_file = r"e:\workspace\python\rdm\rdm\excel\绩效汇总结果.xlsx"
result.to_excel(output_file, index=False)

print(f"数据已成功汇总并保存到: {output_file}")
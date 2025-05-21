import os
import openpyxl

# 定义要处理的Excel文件路径
excel_files = [
    'e:\\workspace\\productui\\excel\\研发中心-2024年5月绩效汇总0619.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2024年6月绩效(2).xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2024年7月绩效-汇总.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2024年8月绩效-汇总(1).xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2024年9月绩效-汇总(1).xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2024年10月绩效-汇总.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2024年11月绩效-汇总.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2024年12月绩效-汇总.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2025年1月绩效-汇总.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2025年2月绩效-汇总.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2025年3月绩效-汇总.xlsx',
    'e:\\workspace\\productui\\excel\\研发中心-2025年4月绩效-汇总.xlsx'
]

# 遍历所有Excel文件
for file_path in excel_files:
    # 打开Excel文件
    wb = openpyxl.load_workbook(file_path)
    
    # 删除第一个工作表
    wb.remove(wb.worksheets[0])
    
    # 保存修改后的文件
    wb.save(file_path)
    print(f'已处理文件: {file_path}')

print('所有文件处理完成！')
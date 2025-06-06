import pandas as pd
from datetime import datetime
from xlsxwriter import Workbook

# redmine问题分析脚本
def analyze_issue_tags_by_project(file_path):
    # 数据读取与清洗
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['项目']).copy()
    df['问题标记（研发）'] = df['问题标记（研发）'].fillna('无标记')

    # 生成统计表格
    stats = df.groupby('项目')['问题标记（研发）'].value_counts().unstack(fill_value=0)
    stats['总问题数'] = stats.sum(axis=1)
    stats['历史遗漏占比'] = (stats.get('历史遗漏', 0) / stats['总问题数']).fillna(0)
    stats = stats.sort_values('总问题数', ascending=False)

    # 生成标准Excel文件
    filename = f"D:\问题统计_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        stats.to_excel(writer, sheet_name='问题统计')
        
        # 设置Excel格式
        workbook = writer.book
        worksheet = writer.sheets['问题统计']
        
        # 设置百分比格式
        percent_format = workbook.add_format({'num_format': '0.00%'})
        worksheet.set_column('G:G', 12, percent_format)  # 假设历史遗漏占比在G列
        
        # 设置自动列宽
        for idx, col in enumerate(stats.columns):
            max_len = max(stats[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_len)

    print(f"结果已保存至：{filename}")

analyze_issue_tags_by_project("D:\issues.csv")
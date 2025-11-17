"""
项目问题统计分析脚本

功能说明：
1. 读取Excel文件中的项目问题数据
2. 按项目编号统计各类问题数量
3. 生成详细统计报告和汇总表格
4. 支持导出结果到Excel文件

数据要求：
Excel文件需包含以下列：
- 版本号
- 问题严重性（产品经理）
- 问题判定（产品经理）
- 项目编号
- 项目阶段

"""

import pandas as pd
import os

def analyze_excel_structure(excel_path):
    """分析Excel文件结构"""
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_path)
        print("Excel文件列名:")
        print(df.columns.tolist())
        print(f"\n数据行数: {len(df)}")
        print(f"数据列数: {len(df.columns)}")
        print("\n前5行数据:")
        print(df.head())
        return df
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return None

def process_project_data(df):
    """
    处理项目数据，按照需求统计各项指标
    """
    if df is None:
        return

    # 检查必要的列是否存在
    required_columns = ['版本号', '问题严重性（产品经理）', '问题判定（产品经理）', '项目编号', '项目阶段']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"缺少必要的列: {missing_columns}")
        return

    # 按项目编号分组统计
    project_stats = {}

    # 获取所有唯一的项目编号
    unique_projects = df['项目编号'].dropna().unique()

    for project_id in unique_projects:
        # 筛选当前项目的数据
        project_data = df[df['项目编号'] == project_id]

        # 1. 统计问题总数
        total_issues = len(project_data)

        # 2. 统计问题判定中包含"无效"的数量
        invalid_issues = len(project_data[project_data['问题判定（产品经理）'].astype(str).str.contains('无效', na=False)])
        valid_issues = total_issues - invalid_issues

        # 3. 统计问题严重性的不同值及数量
        severity_counts = project_data['问题严重性（产品经理）'].value_counts().to_dict()

        # 4. 获取版本号（去重，取第一个）
        version_numbers = project_data['版本号'].dropna().unique()
        version = version_numbers[0] if len(version_numbers) > 0 else "未知"

        # 5. 获取项目阶段（去重，取第一个）
        project_stages = project_data['项目阶段'].dropna().unique()
        stage = project_stages[0] if len(project_stages) > 0 else "未知"

        # 5. 统计问题判定的各种值（除了无效）
        judgment_counts = project_data['问题判定（产品经理）'].value_counts().to_dict()

        # 存储统计结果
        project_stats[project_id] = {
            '版本号': version,
            '项目阶段': stage,
            '问题总数': total_issues,
            '无效': invalid_issues,
            '有效': valid_issues,
            '问题严重性统计': severity_counts,
            '问题判定统计': judgment_counts
        }

    return project_stats

def print_project_statistics(project_stats):
    """
    以表格形式打印项目统计信息
    """
    if not project_stats:
        print("没有统计数据")
        return

    print("\n" + "="*120)
    print("项目问题统计报告")
    print("="*120)

    for project_id, stats in project_stats.items():
        print(f"\n【项目编号】: {project_id}")
        print(f"【版本号】: {stats['版本号']}")
        print(f"【项目阶段】: {stats['项目阶段']}")
        print("=" * 120)

        # 创建统计表格
        print(f"{'统计项目':<25} {'数量':<10}")
        print("-" * 40)
        print(f"{'问题总数':<25} {stats['问题总数']:<10}")
        print(f"{'无效':<25} {stats['无效']:<10}")

        # 显示问题判定的各种值（不包含"无效"的）
        for judgment, count in stats['问题判定统计'].items():
            if pd.notna(judgment) and '无效' not in str(judgment):
                print(f"{str(judgment):<25} {count:<10}")

        # 问题严重性统计
        print(f"\n{'问题严重性':<25} {'数量':<10}")
        print("-" * 40)
        for severity, count in stats['问题严重性统计'].items():
            if pd.notna(severity):
                print(f"{str(severity):<25} {count:<10}")

        print("\n" + "="*120)

def create_summary_table(project_stats):
    """
    创建汇总表格
    """
    if not project_stats:
        return

    print("\n" + "="*170)
    print("项目问题汇总表")
    print("="*170)

    # 表头
    header = f"{'项目编号':<50} {'版本号':<20} {'项目阶段':<15} {'问题总数':<10} {'无效':<10} {'有效BUG':<10} {'非产品BUG':<10} {'其他':<10}"
    print(header)
    print("-" * 170)

    for project_id, stats in project_stats.items():
        # 获取各种问题类型的数量
        valid_bug = stats['问题判定统计'].get('有效BUG', 0)
        non_product_bug = stats['问题判定统计'].get('非产品BUG', 0)
        other_count = stats['问题总数'] - stats['无效'] - valid_bug - non_product_bug

        # 截断过长的项目编号
        short_project_id = project_id[:47] + "..." if len(project_id) > 50 else project_id

        row = f"{short_project_id:<50} {stats['版本号']:<20} {stats['项目阶段']:<15} {stats['问题总数']:<10} {stats['无效']:<10} {valid_bug:<10} {non_product_bug:<10} {other_count:<10}"
        print(row)

    print("="*170)

def export_to_excel(project_stats, output_path="项目问题统计结果.xlsx"):
    """
    将统计结果导出到Excel文件
    """
    if not project_stats:
        print("没有数据可导出")
        return

    try:
        # 准备数据
        data = []
        for project_id, stats in project_stats.items():
            valid_bug = stats['问题判定统计'].get('有效BUG', 0)
            non_product_bug = stats['问题判定统计'].get('非产品BUG', 0)
            other_count = stats['问题总数'] - stats['无效'] - valid_bug - non_product_bug

            # 获取问题严重性统计
            severity_stats = stats['问题严重性统计']

            row = {
                '项目编号': project_id,
                '版本号': stats['版本号'],
                '项目阶段': stats['项目阶段'],
                '问题总数': stats['问题总数'],
                '无效': stats['无效'],
                '有效BUG': valid_bug,
                '非产品BUG': non_product_bug,
                '其他': other_count,
                '严重性-一般': severity_stats.get('一般', 0),
                '严重性-无': severity_stats.get('无', 0),
                '严重性-高': severity_stats.get('高', 0),
                '严重性-低': severity_stats.get('低', 0)
            }
            data.append(row)

        # 创建DataFrame并导出
        df_export = pd.DataFrame(data)
        df_export.to_excel(output_path, index=False, engine='openpyxl')
        print(f"\n统计结果已导出到: {output_path}")

    except Exception as e:
        print(f"导出Excel文件时出错: {e}")

def main():
    """主函数"""
    # Excel文件路径
    excel_path = "rdm/daily/10月.xlsx"

    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"文件不存在: {excel_path}")
        return

    print("正在分析Excel文件结构...")
    df = analyze_excel_structure(excel_path)

    if df is not None:
        print("\n正在处理项目数据...")
        project_stats = process_project_data(df)

        if project_stats:
            # 默认显示汇总表格并导出Excel
            print("\n生成汇总表格并导出Excel文件...")
            create_summary_table(project_stats)
            export_to_excel(project_stats)
        else:
            print("处理项目数据失败")

if __name__ == "__main__":
    main()
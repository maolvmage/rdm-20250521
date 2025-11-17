import os
import pandas as pd
import shutil
from datetime import datetime

def advanced_batch_rename(excel_path, base_directory, backup=False):
    """
    增强版批量重命名函数
    
    参数:
    excel_path: Excel文件路径
    base_directory: 根目录路径
    backup: 是否创建备份
    """
    
    # 创建备份
    if backup:
        backup_dir = os.path.join(base_directory, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(backup_dir)
        print(f"备份创建在：{backup_dir}")
    
    # 读取Excel数据
    df = pd.read_excel(excel_path)
    
    # 验证数据
    required_columns = ['原文件夹名', '新文件夹名']
    if not all(col in df.columns for col in required_columns):
        missing = [col for col in required_columns if col not in df.columns]
        print(f"错误：缺少必要的列：{missing}")
        return False
    
    # 执行重命名
    results = []
    for index, row in df.iterrows():
        old_name = str(row['原文件夹名']).strip()
        new_name = str(row['新文件夹名']).strip()
        
        old_path = os.path.join(base_directory, old_name)
        new_path = os.path.join(base_directory, new_name)
        
        result = {
            '原名称': old_name,
            '新名称': new_name,
            '状态': '未知',
            '错误信息': ''
        }
        
        try:
            if not os.path.exists(old_path):
                result['状态'] = '失败'
                result['错误信息'] = '原文件夹不存在'
            elif os.path.exists(new_path):
                result['状态'] = '失败'
                result['错误信息'] = '目标名称已存在'
            else:
                # 创建备份（如果需要）
                if backup:
                    backup_path = os.path.join(backup_dir, old_name)
                    shutil.copytree(old_path, backup_path)
                
                # 执行重命名
                os.rename(old_path, new_path)
                result['状态'] = '成功'
                
        except Exception as e:
            result['状态'] = '失败'
            result['错误信息'] = str(e)
        
        results.append(result)
        print(f"{old_name} → {new_name}: {result['状态']}")
    
    # 生成报告
    success_count = sum(1 for r in results if r['状态'] == '成功')
    print(f"\n=== 操作报告 ===")
    print(f"总计：{len(results)}，成功：{success_count}，失败：{len(results)-success_count}")
    
    # 保存详细报告
    report_df = pd.DataFrame(results)
    report_path = os.path.join(base_directory, f"重命名报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    report_df.to_excel(report_path, index=False)
    print(f"详细报告已保存至：{report_path}")
    
    return True

# 使用示例
if __name__ == "__main__":
   
    # 增强版用法（带备份）
    advanced_batch_rename(
        excel_path="E:\\DEMO\\重命名列表.xlsx",
        base_directory=r"E:\\DEMO\\demo20251117\\demo",
        backup=False  # 创建备份
    )
import pandas as pd
import re
import os

def export_admin_markdown_files(excel_path, output_dir):
    # 读取Excel文件，仅仅读取第一个sheet
    df=pd.read_excel(excel_path, sheet_name='权限明细表')
    # df = pd.read_excel(excel_path)
    
    # 清理数据：去除空行和NaN值
    df = df.dropna(how='all')
    df = df.fillna('')
    
    # 定义所有要处理的管理员角色列
    admin_columns = [
        # '超级管理员',
        # '系统管理员',
        # '安全审计管理员',
        # '安全保密管理员',
        # '策略管理员',
        # '部门管理员（跨网独有）',
        # '安全运维管理员',
        # '安全运营管理员',
        # '合规管理员',
        # '数审安全管理员',
        # '数审审计管理员',
        # '数审管理员',
        # '分类分级人员',
        '脱敏操作员'
    ]
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 为每个管理员角色生成Markdown文件
    for admin_col in admin_columns:
        if admin_col not in df.columns:
            print(f"警告: 列 '{admin_col}' 不存在于Excel文件中，跳过处理")
            continue
            
        # 初始化Markdown内容
        md_content = f"# {admin_col}权限清单\n\n"
        
        # 初始化当前分类变量
        current_level1 = ""
        current_level2 = ""
        
        # 遍历每一行数据
        for _, row in df.iterrows():
            # 检查当前管理员列是否有对勾（支持√、是、Y等多种表示方式）
            admin_flag = str(row[admin_col]).strip().upper() if admin_col in row else ''
            if not (admin_flag in ['√', '是', 'YES', 'Y', 'TRUE', '1']):
                continue
                
            level1 = str(row['一级分类']).strip()
            level2 = str(row['二级分类']).strip()
            feature = str(row['功能点']).strip()
            
            # 如果一级分类不为空且与当前不同，则添加一级分类
            if level1 and level1 != current_level1:
                md_content += f"\n## {level1}\n"
                current_level1 = level1
                current_level2 = ""  # 重置二级分类
                
            # 如果二级分类不为空且与当前不同，则添加二级分类
            if level2 and level2 != current_level2:
                # 处理二级分类名称中的特殊字符（XMind要求）
                clean_level2 = re.sub(r'[\\/:*?"<>|]', '_', level2)
                md_content += f"\n### {clean_level2}\n"
                current_level2 = level2
                
            # 如果功能点不为空，则添加功能点
            if feature:
                # 处理功能点名称中的特殊字符（XMind要求）
                clean_feature = re.sub(r'[\\/:*?"<>|]', '_', feature)
                md_content += f"- {clean_feature}\n"
        
        # 生成文件名（处理特殊字符）
        clean_admin_name = re.sub(r'[\\/:*?"<>|]', '_', admin_col)
        output_path = os.path.join(output_dir, f"{clean_admin_name}权限.md")
        
        # 写入Markdown文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"{admin_col}权限Markdown文件已生成: {output_path}")

# 使用示例
excel_path = 'D:\明朝万达\产品管理\Chinasec系列产品\统一管理平台\权限梳理\产品角色权限清单.xlsx'  # 替换为你的Excel文件路径
output_dir = 'D:\明朝万达\产品管理\Chinasec系列产品\统一管理平台\权限梳理\权限清单Markdown'     # 输出的Markdown文件目录
export_admin_markdown_files(excel_path, output_dir)
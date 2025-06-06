import pandas as pd
import re

# 处理产品中admin角色权限的脚本

def excel_to_xmind_markdown(excel_path, output_md_path):
    # 读取Excel文件
    df = pd.read_excel(excel_path)
    
    # 清理数据：去除空行和NaN值
    df = df.dropna(how='all')
    df = df.fillna('')
    
    # 初始化Markdown内容
    md_content = "# 产品角色权限清单\n\n"
    
    # 初始化当前分类变量
    current_level1 = ""
    current_level2 = ""
    
    # 遍历每一行数据
    for _, row in df.iterrows():
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
    
    # 写入Markdown文件
    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Markdown文件已生成，保存路径: {output_md_path}")

# 使用示例
excel_path = 'D:\明朝万达\产品管理\Chinasec系列产品\统一管理平台\权限梳理\产品角色权限清单.xlsx'  # 替换为你的Excel文件路径
output_md_path = 'D:\明朝万达\产品管理\Chinasec系列产品\统一管理平台\权限梳理\产品角色权限清单.md'  # 输出的Markdown文件路径
excel_to_xmind_markdown(excel_path, output_md_path)
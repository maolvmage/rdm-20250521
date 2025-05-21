import pandas as pd

# 统计不同任务类型的难度分配的数量以及工时
class TaskAnalysis:
    # 常量定义
    PRODUCT_TYPE = "产品"
    PROJECT_TYPE = "项目"
    DAILY_TYPE = "日常"
    
    TASK_CLT_HIGH = "高"
    TASK_CLT_MIDDLE = "中"
    TASK_CLT_LOW = "低"

    def __init__(self):
        # 初始化各种任务映射
        self.product_high_task_map = {}
        self.product_middle_task_map = {}
        self.product_low_task_map = {}
        
        self.project_high_task_map = {}
        self.project_middle_task_map = {}
        self.project_low_task_map = {}
        
        self.daily_high_task_map = {}
        self.daily_middle_task_map = {}
        self.daily_low_task_map = {}

    def read_excel(self, excel_path):
        try:
            # 使用pandas读取Excel文件
            df = pd.read_excel(excel_path, engine='openpyxl')
            
            # 跳过第一行（标题）
            df = df.iloc[1:]
            
            # 初始化计数器
            count = 0
            
            for index, row in df.iterrows():
                task_type = row.iloc[8]
                clt = row.iloc[3]
                actual_time = float(row.iloc[10])
                
                # 根据任务类型和优先级分类
                if task_type == self.PRODUCT_TYPE:
                    if clt == self.TASK_CLT_HIGH:
                        self.product_high_task_map[str(count)] = actual_time
                    elif clt == self.TASK_CLT_MIDDLE:
                        self.product_middle_task_map[str(count)] = actual_time
                    elif clt == self.TASK_CLT_LOW:
                        self.product_low_task_map[str(count)] = actual_time
                
                elif task_type == self.PROJECT_TYPE:
                    if clt == self.TASK_CLT_HIGH:
                        self.project_high_task_map[str(count)] = actual_time
                    elif clt == self.TASK_CLT_MIDDLE:
                        self.project_middle_task_map[str(count)] = actual_time
                    elif clt == self.TASK_CLT_LOW:
                        self.project_low_task_map[str(count)] = actual_time
                
                elif task_type == self.DAILY_TYPE:
                    if clt == self.TASK_CLT_HIGH:
                        self.daily_high_task_map[str(count)] = actual_time
                    elif clt == self.TASK_CLT_MIDDLE:
                        self.daily_middle_task_map[str(count)] = actual_time
                    elif clt == self.TASK_CLT_LOW:
                        self.daily_low_task_map[str(count)] = actual_time
                
                count += 1
            
            # 打印统计信息
            self.print_map_statistics("产品-高", self.product_high_task_map)
            self.print_map_statistics("项目-高", self.project_high_task_map)
            self.print_map_statistics("日常-高", self.daily_high_task_map)
            
            self.print_map_statistics("产品-中", self.product_middle_task_map)
            self.print_map_statistics("项目-中", self.project_middle_task_map)
            self.print_map_statistics("日常-中", self.daily_middle_task_map)
            
            self.print_map_statistics("产品-低", self.product_low_task_map)
            self.print_map_statistics("项目-低", self.project_low_task_map)
            self.print_map_statistics("日常-低", self.daily_low_task_map)
        
        except Exception as e:
            print(f"读取Excel文件时发生错误: {e}")

    def print_map_statistics(self, map_name, task_map):
        """打印任务映射的统计信息"""
        count = len(task_map)
        total_time = sum(task_map.values())
        print(f"{map_name} {count} {total_time}")


def main():
    task_analysis = TaskAnalysis()
    task_analysis.read_excel(r"D:\明朝万达\研发管理\任务管理\任务审计-202410.xlsx")


if __name__ == "__main__":
    main()
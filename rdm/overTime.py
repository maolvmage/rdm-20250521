import os
import openpyxl

class TimeAnalysis:
    def __init__(self):
        self.white_map = {
            "王志华": "王志华",
            "安鹏": "安鹏"
        }

    def read_excel(self, excel_path):
        try:
            wb = openpyxl.load_workbook(excel_path, read_only=True)
            dkts, qjhour, cgsd, rs, sjgzsc = 0, 0.0, 0, 0, 0.0
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                rs += 1
                name = str(row[0])
                if name in self.white_map:
                    continue

                sjgzsc += float(row[8] or 0) + float(row[29] or 0)
                dkts += int(row[4] or 0)
                cgsd += int(row[11] or 0)

                qjhour_cols = [30, 36, 37, 39, 40, 41, 42]
                for col in qjhour_cols:
                    qjhour += float(row[col] or 0)

            avg_work_hours = (sjgzsc - (dkts * 8)) / (dkts - qjhour / 8) if (dkts - qjhour / 8) != 0 else 0
            if dkts - (qjhour / 8) != 0:
                avg_work_hours = (sjgzsc - (dkts * 8)) / (dkts - (qjhour / 8))
            else:
                avg_work_hours = 0

            print(f"File: {excel_path}")
            print(f"总人数: {rs}, 请假小时数: {qjhour}, 平均工作时长: {avg_work_hours}, 超过时段数: {cgsd}")

            return {
                "total_people": rs,
                "leave_hours": qjhour,
                "avg_work_hours": avg_work_hours,
                "leave_ours": qjhour,  # 这里有个笔误，应该是“leave_ours”还是“leave_ours”
                "avg_work_ours": avg_work_hours,  # 类似的命名问题
                "overtime_periods": cgsd
            }

        except openpyxl.utils.exceptions.InvalidFileException:
            print(f"无效的文件格式: {excel_path}")
        except Exception as e:
            print(f"处理文件 {excel_path} 时发生错误: {e}")
        return None

    def list_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.xlsx', '.xls', '.xlsm')):
                    full_path = os.path.join(root, file)
                    self.read_excel(full_path)

def main(directory_path):
    if not os.path.exists(directory_path):
        print("指定的目录不存在.")
        return

    analyzer = TimeAnalysis()
    analyzer.list_files(directory_path)

if __name__ == "__main__":
    directory_path = r"D:\明朝万达\研发管理\任务管理\工时统计\2024-11"
    main(directory_path)

# 注意事项：
# 1. 需要安装 openpyxl 库：pip install openpyxl
# 2. 请根据实际文件路径和目录结构调整 directory_path
# 3. 可能需要根据实际Excel文件结构调整列索引
    main(directory_path)

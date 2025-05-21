import pytest
import os
from openpyxl import Workbook
from rdm.overTime import TimeAnalysis

@pytest.fixture
def setup_excel_file(tmp_path):
    file_path = tmp_path / "test.xlsx"
    wb = Workbook()
    ws = wb.active

    ws.append(["姓名", "其他列1", "其他列2", "其他列3", "打卡天数", "其他列4", "其他列5", "其他列6", "实际工作时长1", "其他列7", "其他列8", "超过时段数", "其他列9", "其他列10", "其他列11", "其他列12", "其他列13", "其他列14", "其他列15", "其他列16", "其他列17", "其他列18", "其他列19", "其他列20", "其他列21", "其他列22", "其他列23", "其他列24", "其他列25", "实际工作时长2", "请假小时数1", "其他列26", "其他列27", "其他列28", "其他列29", "请假小时数2", "请假小时数3", "其他列30", "请假小时数4", "请假小时数5", "请假小时数6", "请假小时数7", "请假小时数8"])

    ws.append(["张三", "", "", "", 20, "", "", "", 160, "", "", 5, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 40, "", "", "", "", 8, 8, "", 8, 8, 8, 8, 8])
    ws.append(["王志华", "", "", "", 15, "", "", "", 120, "", "", 3, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 30, "", "", "", "", 4, 4, "", 4, 4, 4, 4, 4])

    wb.save(file_path)
    return file_path

def test_read_excel(setup_excel_file):
    analyzer = TimeAnalysis()
    result = analyzer.read_excel(setup_excel_file)

    assert result is not None
    assert result["total_people"] == 1
    assert result["leave_hours"] == 56.0
    assert result["avg_work_hours"] == pytest.approx(4.0, rel=1e-2)
    assert result["overtime_periods"] == 5

def test_list_files(tmp_path, setup_excel_file):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    setup_excel_file.rename(test_dir / "test.xlsx")

    analyzer = TimeAnalysis()
    analyzer.list_files(test_dir)

    assert os.path.exists(test_dir / "test.xlsx")
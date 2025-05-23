import unittest
import tempfile
import os
from datetime import datetime, timedelta
from rdm.nginx_data_analysis.nginx_log_analyzer import parse_nginx_log

class NginxLogAnalyzerTest(unittest.TestCase):
    def test_parse_valid_nginx_log_line(self):
        """测试解析标准nginx日志行（包含有效IP和时间戳）的功能。
        
        该测试用例验证parse_nginx_log函数能否正确解析包含有效IP地址和时间戳的标准nginx日志行。
        测试步骤：
        1. 创建临时日志文件并写入测试数据
        2. 调用待测函数解析日志文件
        3. 验证解析结果：
           - 确保解析出1条记录
           - 验证IP地址正确
           - 验证时间戳正确（原始UTC时间+8小时）
        
        注意事项：
        - 使用tempfile创建临时文件，测试完成后自动清理
        - 包含时区转换验证（UTC+8）
        """
        """Test parsing a standard nginx log line with valid IP and timestamp"""
        # Create a temporary log file with the test line
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("192.168.1.1 - - [07/May/2025:05:20:17 +0000] \"GET /path HTTP/1.1\"\n")
            temp_file_path = temp_file.name
        
        try:
            # Call the function with the temporary file
            result = parse_nginx_log(temp_file_path)
            
            # Verify the results
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['ip'], '192.168.1.1')
            
            # Check the adjusted time (original +8 hours)
            expected_time = datetime.strptime('07/May/2025:13:20:17 +0000', '%d/%b/%Y:%H:%M:%S %z')
            self.assertEqual(result[0]['time'], expected_time)
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)

if __name__ == '__main__':
    unittest.main()
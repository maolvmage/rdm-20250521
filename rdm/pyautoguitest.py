import pyautogui
import time

# 安全设置（防止失控）
pyautogui.FAILSAFE = True  # 启用后，快速移动鼠标到左上角可终止脚本[1,5](@ref)
pyautogui.PAUSE = 0.5      # 每个动作间隔0.5秒（非强制等待）[2](@ref)

try:
    while True:
        # 向右移动100像素（持续0.3秒模拟自然移动）
        pyautogui.moveRel(100, 0, duration=0.3)  # 网页6类似方案改进版[6,9](@ref)
        # 向左移动100像素（回到原位）
        pyautogui.moveRel(-100, 0, duration=0.3)
        
        # 计时器（精确等待剩余时间）
        start_time = time.time()
        while time.time() - start_time < 60:  # 总间隔1分钟
            time.sleep(10)  # 每10秒检测一次
except KeyboardInterrupt:
    print("\n脚本已通过 Ctrl+C 终止")
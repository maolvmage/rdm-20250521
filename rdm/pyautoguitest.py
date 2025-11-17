import pyautogui
import time
import random
import threading
import schedule
import os
from datetime import datetime

def jittery_move(start_x, start_y, max_offset=5):
    """
    模拟人类手部轻微抖动的移动方式
    """
    # 在当前位置周围小范围随机移动
    for _ in range(random.randint(1, 3)):  # 随机移动1-3次
        target_x = start_x + random.randint(-max_offset, max_offset)
        target_y = start_y + random.randint(-max_offset, max_offset)
        # 限制目标位置在屏幕范围内
        target_x = max(0, min(target_x, pyautogui.size()[0] - 1))
        target_y = max(0, min(target_y, pyautogui.size()[1] - 1))
        move_duration = random.uniform(0.05, 0.2)  # 随机移动速度
        pyautogui.moveTo(target_x, target_y, duration=move_duration)
        time.sleep(random.uniform(0.03, 0.1))  # 移动间短暂停顿
    # 最后移回大致原始位置附近，但不是精确的原点
    end_x = start_x + random.randint(-2, 2)
    end_y = start_y + random.randint(-2, 2)
    pyautogui.moveTo(end_x, end_y, duration=random.uniform(0.05, 0.15))

def perform_random_activity():
    """
    执行一组随机的用户活动模拟，可能包括鼠标移动、轻微滚动或极罕见的点击
    """
    screen_width, screen_height = pyautogui.size()
    current_x, current_y = pyautogui.position()

    activity_type = random.choices(
        ['move_only', 'mini_scroll'], 
        weights=[0.85, 0.15],  # 大部分时间只是轻微移动，偶尔滚动
        k=1
    )[0]

    if activity_type == 'move_only':
        # 主要进行小幅随机移动
        jittery_move(current_x, current_y)
    elif activity_type == 'mini_scroll':
        # 偶尔轻微滚动一下（比如在阅读文档）
        scroll_amount = random.choice([-1, 1]) * random.randint(1, 3)
        pyautogui.scroll(scroll_amount)
        time.sleep(random.uniform(0.5, 1.5))

def keep_awake():
    """
    核心循环：使用随机间隔和活动模拟用户存在
    """
    activity_count = 0
    try:
        while True:
            activity_count += 1
            
            # 执行随机活动
            perform_random_activity()
            
            # 随机等待时间：核心是保持在15分钟无操作阈值内，但加入较大随机性
            # 基础间隔8-12分钟，确保小于15分钟，但每次都有±2分钟波动
            base_interval = random.randint(480, 720)  # 8-12分钟，单位秒
            random_variation = random.randint(-120, 120)  # ±2分钟波动
            sleep_time = max(60, base_interval + random_variation)  # 确保不小于1分钟
            
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 下次活动在约{int(sleep_time/60)}分钟后。")
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("模拟用户操作脚本已安全退出。")

def shutdown_computer():
    """
    执行关机操作，提供倒计时提示[1,3](@ref)
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 定时关机任务触发，准备关机...")
    
    # 关机前提示（可根据需要取消注释）
    # try:
    #     import tkinter as tk
    #     from tkinter import messagebox
    #     root = tk.Tk()
    #     root.withdraw()
    #     messagebox.showwarning("定时关机", "电脑将在60秒后关机，请保存好您的工作！")
    # except:
    #     print("关机提示框显示失败，继续执行关机...")
    
    # 执行关机命令[4,5](@ref)
    # Windows系统
    if os.name == 'nt':
        os.system("shutdown /s /t 60")  # 60秒后关机
        print("系统将在60秒后关机，如需取消请运行: shutdown /a")
    # Linux系统
    else:
        os.system("sudo shutdown -h +1")  # 1分钟后关机
        print("系统将在1分钟后关机，如需取消请运行: sudo shutdown -c")

def schedule_checker():
    """
    在一个单独的线程中运行定时任务检查[6,7](@ref)
    """
    # 设置每天22:00执行关机任务[6](@ref)
    schedule.every().day.at("22:00").do(shutdown_computer)
    print("定时关机任务已设置：每天22:00自动关机")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次，减少CPU占用

def main():
    """主函数，程序的入口点"""
    print("防企微离线脚本（增强版）开始运行。")
    screen_width, screen_height = pyautogui.size()
    print(f"屏幕分辨率: {screen_width} x {screen_height}")
    print("脚本将模拟随机、低强度的用户活动（如轻微鼠标移动、偶尔滚动）。")
    print("定时关机功能：每天22:00自动关机（60秒倒计时提示）")
    print("重要提示：使用自动化脚本可能违反企业微信政策，请谨慎使用。")
    print("按下 Ctrl+C 可终止脚本（不会取消已设置的关机计划）。")
    print("如需取消关机计划，可手动运行: shutdown /a (Windows) 或 sudo shutdown -c (Linux)")

    # 在后台线程中运行 keep_awake 函数（防离线）
    awake_thread = threading.Thread(target=keep_awake, daemon=True)
    awake_thread.start()

    # 在后台线程中运行定时关机检查
    schedule_thread = threading.Thread(target=schedule_checker, daemon=True)
    schedule_thread.start()

    # 保持主线程运行，以便接收终止信号
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n检测到用户中断，脚本退出。")
        print("注意：定时关机任务仍在后台运行，如需取消请使用上述命令。")

if __name__ == '__main__':
    main()
import time
import threading

def my_task():
    print("任务正在执行...")

def schedule_task(interval, task):
    def wrapper():
        while True:
            task()
            time.sleep(interval)
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()

if __name__ == "__main__":
    # 每10秒执行一次任务
    schedule_task(10, my_task)
    print("定时任务已启动,按Ctrl+C退出。")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已退出。")
import pyautogui
import time
import os
from datetime import datetime
folder_name = "Screenshots"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
interval = 10
print("Screenshot capturing started...")
while True:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{folder_name}/screenshot_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(file_name)
    print(f"Saved: {file_name}")
    time.sleep(interval)
#To stop the process give ctrl+c

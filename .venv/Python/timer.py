import time
from datetime import datetime

while True:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(1)
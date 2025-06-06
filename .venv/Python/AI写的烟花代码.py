import random
import time
import os
import sys

def clear_screen():
    # Clear the terminal screen for Windows and Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def print_fireworks(times=5, delay=0.4, width=60):
    fireworks_patterns = [
        [
            "      *      ",
            "     ***     ",
            "    *****    ",
            "   *******   ",
            "  *********  ",
            "   *******   ",
            "    *****    ",
            "     ***     ",
            "      *      "
        ],
        [
            "      *      ",
            "     * *     ",
            "    *   *    ",
            "   *     *   ",
            "  *       *  ",
            "   *     *   ",
            "    *   *    ",
            "     * *     ",
            "      *      "
        ]
    ]
    colors = [
        '\033[91m', # Red
        '\033[92m', # Green
        '\033[93m', # Yellow
        '\033[94m', # Blue
        '\033[95m', # Magenta
        '\033[96m', # Cyan
        '\033[97m', # White
    ]
    for _ in range(times):
        clear_screen()
        color = random.choice(colors)
        pattern = random.choice(fireworks_patterns)
        offset = random.randint(0, width // 4)
        for line in pattern:
            print(color + (" " * offset) + line.center(width - offset*2) + '\033[0m')
        time.sleep(delay)
    print('\n' * 2)

if __name__ == "__main__":
    print("烟花表演开始啦！")
    time.sleep(1)
    print_fireworks(times=8, delay=0.3, width=60)
    print("表演结束，祝你开心每一天！")
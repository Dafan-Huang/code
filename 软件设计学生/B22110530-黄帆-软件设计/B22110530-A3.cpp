// 3. 文本编辑器（10分）

// 编辑文本；
// 保存、打开指定位置的文本文件；
// 具有输入输出界面。

#include <iostream>
#include <fstream>
#include <string>

void showMenu() {
    std::cout << "\n--- 文本编辑器 ---\n";
    std::cout << "1. 编辑文本\n";
    std::cout << "2. 保存文本到文件\n";
    std::cout << "3. 打开文件\n";
    std::cout << "4. 显示当前文本\n";
    std::cout << "0. 退出\n";
    std::cout << "请选择操作: ";
}

void editText(std::string &text) {
    std::cout << "请输入文本(输入单独一行END结束):\n";
    text.clear();
    std::string line;
    while (true) {
        std::getline(std::cin, line);
        if (line == "END") break;
        text += line + "\n";
    }
}

void saveToFile(const std::string &text) {
    std::string filename;
    std::cout << "请输入要保存的文件路径: ";
    std::getline(std::cin, filename);
    std::ofstream ofs(filename);
    if (ofs) {
        ofs << text;
        ofs.close();
        std::cout << "保存成功。\n";
    } else {
        std::cout << "保存失败。\n";
    }
}

void openFromFile(std::string &text) {
    std::string filename;
    std::cout << "请输入要打开的文件路径: ";
    std::getline(std::cin, filename);
    std::ifstream ifs(filename);
    if (ifs) {
        text.clear();
        std::string line;
        while (std::getline(ifs, line)) {
            text += line + "\n";
        }
        ifs.close();
        std::cout << "打开成功。\n";
    } else {
        std::cout << "打开失败。\n";
    }
}

void showText(const std::string &text) {
    std::cout << "\n--- 当前文本 ---\n";
    std::cout << text << "\n";
}

#ifdef _WIN32
#include <windows.h>
#else
#include <cstdlib>
#endif

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}


int main() {
    std::string text;
    int choice;
    while (true) {
        showMenu();
        std::string input;
        std::getline(std::cin, input);
        if (input.empty()) continue;
        try {
            choice = std::stoi(input);
        } catch (...) {
            std::cout << "请输入有效的数字。\n";
            continue;
        }
        switch (choice) {
            case 1:
                editText(text);
                clearScreen();
                break;
            case 2:
                saveToFile(text);
                clearScreen();
                break;
            case 3:
                openFromFile(text);
                clearScreen();
                break;
            case 4:
                showText(text);
                break;
            case 0:
                std::cout << "退出程序。\n";
                return 0;
            default:
                std::cout << "无效选择，请重试。\n";
        }
    }
    return 0;
}

/**
 * @brief 程序主函数，提供一个基于菜单的文本编辑器界面。
 *
 * 主循环中显示菜单，等待用户输入操作选项，根据用户选择调用相应的功能函数：
 * - 1: 编辑文本（editText）
 * - 2: 保存文本到文件（saveToFile）
 * - 3: 从文件打开文本（openFromFile）
 * - 4: 显示当前文本内容（showText）
 * - 0: 退出程序
 *
 * 输入非数字或无效选项时会提示用户重新输入。
 * 每次操作后会清屏（clearScreen），除非是显示文本内容。
 *
 * @return int 程序退出状态码（正常退出返回0）
 */
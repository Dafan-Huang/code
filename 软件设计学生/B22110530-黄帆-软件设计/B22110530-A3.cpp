// 3. 文本编辑器（10分）
//
// 编辑文本；
// 保存、打开指定位置的文本文件；
// 具有输入输出界面。

#include <iostream>
#include <fstream>
#include <string>

#ifdef _WIN32
#include <windows.h>
#else
#include <cstdlib>
#endif

//  显示主菜单，提示用户选择操作。
void showMenu() {
    std::cout << "\n--- 文本编辑器 ---\n";
    std::cout << "1. 编辑文本\n";
    std::cout << "2. 保存文本到文件\n";
    std::cout << "3. 打开文件\n";
    std::cout << "4. 显示当前文本\n";
    std::cout << "0. 退出\n";
    std::cout << "请选择操作: ";
}

// 清屏函数，根据操作系统调用不同的清屏命令。
void clearScreen() {
#ifdef _WIN32
    system("cls"); // Windows下清屏
#else
    system("clear"); // Linux/Unix下清屏
#endif
}

//  编辑文本内容，用户输入新内容，输入END结束。
//  text 引用，存储当前文本内容，将被新内容覆盖。
void editText(std::string &text) {
    std::cout << "当前文本内容如下：\n";
    std::cout << text;
    std::cout << "请输入新的文本内容(输入单独一行END结束,将覆盖原内容):\n";
    std::string newText, line;
    while (true) {
        std::getline(std::cin, line); // 逐行读取用户输入
        if (line == "END") break;     // 输入END结束编辑
        newText += line + "\n";       // 拼接新内容
    }
    text = newText; // 用新内容覆盖原内容
}

//  将当前文本内容保存到指定文件。
//  text 当前文本内容。
void saveToFile(const std::string &text) {
    std::string filename;
    std::cout << "请输入要保存的文件路径: ";
    std::getline(std::cin, filename); // 获取文件路径
    std::ofstream ofs(filename);      // 打开输出文件流
    if (ofs) {
        ofs << text;                  // 写入文本内容
        ofs.close();                  // 关闭文件
        std::cout << "保存成功。\n";
    } else {
        std::cout << "保存失败。\n";  // 文件打开失败
    }
}

// 从指定文件读取文本内容，覆盖当前内容。
// text 引用，存储读取到的文本内容。

void openFromFile(std::string &text) {
    std::string filename;
    std::cout << "请输入要打开的文件路径: ";
    std::getline(std::cin, filename); // 获取文件路径
    std::ifstream ifs(filename);      // 打开输入文件流
    if (ifs) {
        text.clear();                 // 清空当前内容
        std::string line;
        while (std::getline(ifs, line)) {
            text += line + "\n";      // 逐行读取并拼接
        }
        ifs.close();                  // 关闭文件
        std::cout << "打开成功。\n";
    } else {
        std::cout << "打开失败。\n";  // 文件打开失败
    }
}


// 显示当前文本内容。
// text 当前文本内容。
void showText(const std::string &text) {
    std::cout << "\n--- 当前文本 ---\n";
    std::cout << text << "\n";
}

/**
 * 程序主函数，提供一个基于菜单的文本编辑器界面。
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
 * int 程序退出状态码（正常退出返回0）
 */
int main() {
    std::string text; // 存储当前文本内容
    int choice;       // 用户菜单选择
    while (true) {
        showMenu();   // 显示菜单
        std::string input;
        std::getline(std::cin, input); // 获取用户输入
        if (input.empty()) continue;   // 输入为空则重新输入
        try {
            choice = std::stoi(input); // 转换为数字
        } catch (...) {
            std::cout << "请输入有效的数字。\n";
            continue;
        }
        switch (choice) {
            case 1:
                editText(text);        // 编辑文本
                clearScreen();         // 清屏
                break;
            case 2:
                saveToFile(text);      // 保存文本
                clearScreen();         // 清屏
                break;
            case 3:
                openFromFile(text);    // 打开文件
                clearScreen();         // 清屏
                break;
            case 4:
                showText(text);        // 显示文本
                break;
            case 0:
                std::cout << "退出程序。\n";
                return 0;              // 退出
            default:
                std::cout << "无效选择，请重试。\n";
        }
    }
    return 0;
}
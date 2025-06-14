//  5. 进制转换器（10分）
//
// 可输入二进制、八进制、十进制、十六进制数；
// 将已输入的数转换成其余进制的数；
// 具有输入输出界面。

#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <cctype>

using namespace std;

// 检查字符串是否为合法的指定进制数
// s: 输入的字符串
// base: 指定的进制（2/8/10/16）
// 返回值: 如果s是合法的base进制数，返回true，否则返回false
bool isValidNumber(const string& s, int base) {
    size_t start = 0;
    // 跳过前缀（如0x, 0b, 0）
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x' || tolower(s[1]) == 'b')) start = 2;
    else if (s.size() > 1 && s[0] == '0' && base == 8) start = 1;
    for (size_t i = start; i < s.size(); ++i) {
        char c = toupper(s[i]);
        if (base <= 10) {
            // 对于2/8/10进制，必须是数字且小于base
            if (!isdigit(c) || c - '0' >= base) return false;
        } else {
            // 对于16进制，允许A-F
            if (!isdigit(c) && (c < 'A' || c >= 'A' + base - 10)) return false;
        }
    }
    return true;
}

// 自动识别进制并转换为十进制
// input: 用户输入的字符串
// value: 转换后的十进制整数
// base: 识别到的进制
// 返回值: 如果转换成功返回true，否则返回false
bool parseInput(const string& input, int& value, int& base) {
    string s = input;
    base = 10; // 默认十进制
    // 判断前缀，识别进制
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x')) {
        base = 16;
        s = s.substr(2); // 去掉0x
    } else if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'b')) {
        base = 2;
        s = s.substr(2); // 去掉0b
    } else if (s.size() > 1 && s[0] == '0') {
        base = 8;
        s = s.substr(1); // 去掉0
    }
    // 检查是否合法
    if (!isValidNumber(input, base)) return false;
    try {
        // 字符串转整数
        value = std::stoi(s, nullptr, base);
    } catch (...) {
        return false;
    }
    return true;
}

// 十进制转为其他进制字符串
// value: 十进制整数
// base: 目标进制（2/8/10/16）
// 返回值: 带前缀的目标进制字符串
string toBase(int value, int base) {
    if (base == 10) return to_string(value); // 十进制直接返回
    string result;
    unsigned int uvalue = static_cast<unsigned int>(value); // 处理负数时的无符号转换
    if (base == 2) {
        result = "0b"; // 二进制前缀
        string bin;
        if (uvalue == 0) bin = "0";
        while (uvalue) {
            bin = char('0' + (uvalue % 2)) + bin;
            uvalue /= 2;
        }
        result += bin;
    } else if (base == 8) {
        result = "0"; // 八进制前缀
        string oct;
        if (uvalue == 0) oct = "0";
        while (uvalue) {
            oct = char('0' + (uvalue % 8)) + oct;
            uvalue /= 8;
        }
        result += oct;
    } else if (base == 16) {
        result = "0x"; // 十六进制前缀
        string hex;
        if (uvalue == 0) hex = "0";
        while (uvalue) {
            int digit = uvalue % 16;
            hex = (digit < 10 ? char('0' + digit) : char('A' + digit - 10)) + hex;
            uvalue /= 16;
        }
        result += hex;
    }
    return result;
}

int main() {
    while (true) {
#ifdef _WIN32
        system("cls"); // 清屏（Windows）
#else
        system("clear"); // 清屏（Linux/Unix）
#endif
        cout << "===== 进制转换器 =====" << endl;
        cout << "请输入一个数(支持二进制0b, 八进制0, 十进制, 十六进制0x前缀):" << endl;
        string input;
        cin >> input;

        int value, base;
        // 解析输入并判断是否合法
        if (!parseInput(input, value, base)) {
            cout << "输入格式错误！" << endl;
        } else {
            // 输出各进制表示
            cout << "输入的数为: " << input << endl;
            cout << "十进制: " << toBase(value, 10) << endl;
            cout << "二进制: " << toBase(value, 2) << endl;
            cout << "八进制: " << toBase(value, 8) << endl;
            cout << "十六进制: " << toBase(value, 16) << endl;
        }

        cout << "\n是否继续转换?(y/n): ";
        string choice;
        cin >> choice;
        if (choice != "y" && choice != "Y") break; // 退出循环
    }
    return 0;
}

/*
    进制转换器程序

    功能简介:
    - 支持输入二进制(0b前缀)、八进制(0前缀)、十进制、十六进制(0x前缀)的数字。
    - 自动识别输入数字的进制，并将其转换为其它三种进制格式输出。
    - 提供简单的输入输出界面，支持多次转换操作。

    主要函数说明:
    1. isValidNumber(const string& s, int base)
        - 检查字符串s是否为合法的指定进制(base)数字。
        - 支持二进制、八进制、十进制、十六进制的合法性判断。

    2. parseInput(const string& input, int& value, int& base)
        - 自动识别输入字符串input的进制类型，并转换为十进制整数value。
        - 识别0b、0x、0前缀，分别对应二进制、十六进制、八进制。
        - 返回识别到的进制base。
        - 若输入非法，返回false。

    3. toBase(int value, int base)
        - 将十进制整数value转换为指定进制(base)的字符串表示。
        - 输出带有标准前缀(如0b, 0, 0x)的格式。

    使用说明:
    - 运行程序后，输入需要转换的数字（支持0b、0、0x前缀）。
    - 程序会输出该数字的十进制、二进制、八进制、十六进制表示。
    - 可选择是否继续进行下一次转换。

    注意事项:
    - 输入格式需符合对应进制的合法字符范围。
    - 输入非法时会提示错误信息。
*/
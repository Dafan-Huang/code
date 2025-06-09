#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <cctype>

using namespace std;

// 检查字符串是否为合法的指定进制数
bool isValidNumber(const string& s, int base) {
    size_t start = 0;
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x' || tolower(s[1]) == 'b')) start = 2;
    else if (s.size() > 1 && s[0] == '0' && base == 8) start = 1;
    for (size_t i = start; i < s.size(); ++i) {
        char c = toupper(s[i]);
        if (base <= 10) {
            if (!isdigit(c) || c - '0' >= base) return false;
        } else {
            if (!isdigit(c) && (c < 'A' || c >= 'A' + base - 10)) return false;
        }
    }
    return true;
}

// 自动识别进制并转换为十进制
bool parseInput(const string& input, int& value, int& base) {
    string s = input;
    base = 10;
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x')) {
        base = 16;
        s = s.substr(2);
    } else if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'b')) {
        base = 2;
        s = s.substr(2);
    } else if (s.size() > 1 && s[0] == '0') {
        base = 8;
        s = s.substr(1);
    }
    if (!isValidNumber(input, base)) return false;
    try {
        value = std::stoi(s, nullptr, base);
    } catch (...) {
        return false;
    }
    return true;
}

// 十进制转为其他进制字符串
string toBase(int value, int base) {
    if (base == 10) return to_string(value);
    stringstream ss;
    if (base == 2) ss << "0b";
    else if (base == 8) ss << "0";
    else if (base == 16) ss << "0x";
    ss << std::setbase(base) << std::uppercase << value;
    return ss.str();
}

int main() {
    while (true) {
#ifdef _WIN32
        system("cls");
#else
        system("clear");
#endif
        cout << "===== 进制转换器 =====" << endl;
        cout << "请输入一个数（支持二进制0b, 八进制0, 十进制, 十六进制0x前缀）:" << endl;
        string input;
        cin >> input;

        int value, base;
        if (!parseInput(input, value, base)) {
            cout << "输入格式错误！" << endl;
        } else {
            cout << "输入的数为: " << input << endl;
            cout << "十进制: " << toBase(value, 10) << endl;
            cout << "二进制: " << toBase(value, 2) << endl;
            cout << "八进制: " << toBase(value, 8) << endl;
            cout << "十六进制: " << toBase(value, 16) << endl;
        }

        cout << "\n是否继续转换？(y/n): ";
        string choice;
        cin >> choice;
        if (choice != "y" && choice != "Y") break;
    }
    return 0;
}
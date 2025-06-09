#include <iostream>

#include <locale>
#include <codecvt>

int main() {
    // 设置全局区域设置为支持UTF-8（适用于部分编译器和终端）
    std::locale::global(std::locale(""));

    std::wcout.imbue(std::locale(""));
    std::wcout << L"你好，世界" << std::endl;
    return 0;
}
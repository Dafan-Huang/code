#include <iostream>
#include <fstream>
#include <string>
#include <windows.h>

// 检查文件是否可读
bool isReadable(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    return file.good();
}

// 检查文件是否可写
bool isWritable(const std::string& filename) {
    std::ofstream file(filename, std::ios::app | std::ios::binary);
    return file.good();
}

// 修改文件权限为可读写
bool setReadWrite(const std::string& filename) {
    return SetFileAttributesA(filename.c_str(), FILE_ATTRIBUTE_NORMAL);
}

// 修改文件权限为只读
bool setReadOnly(const std::string& filename) {
    return SetFileAttributesA(filename.c_str(), FILE_ATTRIBUTE_READONLY);
}

int main() {
    std::string filename;
    std::cout << "请输入要测试的Office文件路径: ";
    std::getline(std::cin, filename);

    std::cout << "文件可读: " << (isReadable(filename) ? "是" : "否") << std::endl;
    std::cout << "文件可写: " << (isWritable(filename) ? "是" : "否") << std::endl;

    std::cout << "\n修改控制指令示例:" << std::endl;
    std::cout << "1. 设置为可读写: setReadWrite(\"" << filename << "\");" << std::endl;
    std::cout << "2. 设置为只读: setReadOnly(\"" << filename << "\");" << std::endl;

    return 0;
}
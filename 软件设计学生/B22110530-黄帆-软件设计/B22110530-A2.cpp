// 2. 打字程序（10分）
//
// 随机产生一字符串，每次产生的字符串内容、长度都不同；
// 根据结果输入字符串，判断输入是否正确，输出正确率；
// 具有输入输出界面。

#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <windows.h>
#include <algorithm>

// 随机生成字符串
// 参数：minLen - 最小长度，maxLen - 最大长度
// 返回值：生成的随机字符串
std::string generateRandomString(int minLen = 5, int maxLen = 10) {
    static const char charset[] =
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"; // 字符集：小写字母、大写字母、数字
    int len = minLen + rand() % (maxLen - minLen + 1); // 随机生成字符串长度
    std::string result;
    for (int i = 0; i < len; ++i) {
        result += charset[rand() % (sizeof(charset) - 1)]; // 随机选择字符
    }
    return result;
}

// 计算正确率
// 参数：target - 目标字符串，input - 用户输入字符串
// 返回值：正确率（百分比）
double calcAccuracy(const std::string& target, const std::string& input) {
    int correct = 0; // 正确字符计数
    int minLen = std::min(target.size(), input.size()); // 取两者较短长度
    for (int i = 0; i < minLen; ++i) {
        if (target[i] == input[i]) ++correct; // 逐字符比较，统计正确数
    }
    return 100.0 * correct / target.size(); // 正确率=正确字符数/目标字符串长度
}

int main() {
    srand((unsigned)time(0)); // 初始化随机数种子
    std::string randomStr = generateRandomString(); // 生成随机字符串
    std::string userInput;

    // 控制台界面
    std::cout << "===== 随机字符串输入测试 =====" << std::endl;
    std::cout << "请根据下方随机字符串输入内容：" << std::endl;
    std::cout << randomStr << std::endl; // 显示随机字符串
    std::cout << "请输入：";
    std::getline(std::cin, userInput); // 获取用户输入

    double accuracy = calcAccuracy(randomStr, userInput); // 计算正确率
    std::cout << "你的输入正确率为：" << accuracy << "%" << std::endl;

    // system("pause"); // 可选：暂停程序
    return 0;
}

/*
    打字程序

    功能描述：
    该程序会随机生成一个字符串（内容和长度均随机），要求用户根据显示的字符串输入内容，
    并判断用户输入的正确率，最后输出正确率结果。程序具有简单的输入输出界面。

    主要功能模块：
    1. 随机字符串生成（generateRandomString）：
        - 随机生成长度在[minLen, maxLen]范围内的字符串，字符集包括大小写字母和数字。
    2. 正确率计算（calcAccuracy）：
        - 比较目标字符串与用户输入字符串的每个字符，统计输入正确的字符数，并计算正确率（以目标字符串长度为基准）。
    3. 控制台交互界面（main）：
        - 显示随机字符串，接收用户输入，调用正确率计算函数并输出结果。

    使用说明：
    - 运行程序后，屏幕会显示一串随机字符串。
    - 用户需在控制台输入该字符串并回车。
    - 程序会输出用户输入的正确率百分比。

    注意事项：
    - 字符串长度和内容每次运行均不同。
    - 正确率以目标字符串长度为基准，输入过长部分不计入正确率。
    - 需在支持C++标准库和Windows头文件的环境下编译运行。
*/
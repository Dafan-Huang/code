#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <windows.h>

// 随机生成字符串
std::string generateRandomString(int minLen = 5, int maxLen = 15) {
    static const char charset[] =
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789";
    int len = minLen + rand() % (maxLen - minLen + 1);
    std::string result;
    for (int i = 0; i < len; ++i) {
        result += charset[rand() % (sizeof(charset) - 1)];
    }
    return result;
}

// 计算正确率
double calcAccuracy(const std::string& target, const std::string& input) {
    int correct = 0;
    int minLen = std::min(target.size(), input.size());
    for (int i = 0; i < minLen; ++i) {
        if (target[i] == input[i]) ++correct;
    }
    return 100.0 * correct / target.size();
}

int main() {
    srand((unsigned)time(0));
    std::string randomStr = generateRandomString();
    std::string userInput;

    // 控制台界面
    std::cout << "===== 随机字符串输入测试 =====" << std::endl;
    std::cout << "请根据下方随机字符串输入内容：" << std::endl;
    std::cout << randomStr << std::endl;
    std::cout << "请输入：";
    std::getline(std::cin, userInput);

    double accuracy = calcAccuracy(randomStr, userInput);
    std::cout << "你的输入正确率为：" << accuracy << "%" << std::endl;

    system("pause");
    return 0;
}
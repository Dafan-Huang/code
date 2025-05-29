#include <cstdlib>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>

int main() {
    // 设置控制台输出为UTF-8，防止中文乱码
#if defined(_WIN32)
    // Windows下设置控制台为UTF-8
    system("chcp 65001");
#endif
    std::ios::sync_with_stdio(false);
    std::cout.tie(nullptr);

    // 获取当前时间戳
    std::time_t t = std::time(nullptr);
    std::stringstream ss;
    ss << "我有在好好工作 " << t;

    // 构造git命令
    std::string cmd = "git add . && git commit -m \"" + ss.str() + "\"";

    // 执行git命令
    int result = std::system(cmd.c_str());
    if (result == 0) {
        std::cout << "提交成功: " << ss.str() << std::endl;
    } else {
        std::cout << "提交失败，请检查git环境。" << std::endl;
    }
    return 0;
}
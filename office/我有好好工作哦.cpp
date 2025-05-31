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

        // 检查是否在git仓库中
    #if defined(_WIN32)
        const char* git_check_cmd = "git rev-parse --is-inside-work-tree >nul 2>&1";
    #else
        const char* git_check_cmd = "git rev-parse --is-inside-work-tree >/dev/null 2>&1";
    #endif
        if (std::system(git_check_cmd) != 0) {
            std::cout << "当前目录不是git仓库,请先初始化git。" << std::endl;
            return 1;
        }
        // 设置环境变量，减少git命令输出
    #if defined(_WIN32)
        _putenv("GIT_TERMINAL_PROMPT=0");
    #else
        setenv("GIT_TERMINAL_PROMPT", "0", 1);
    #endif
    // 检查是否有更改需要提交
    if (std::system("git diff --cached --quiet && git diff --quiet") == 0) {
        std::cout << "没有检测到需要提交的更改。" << std::endl;
        return 0;
    }

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
        std::cout << "提交失败,请检查git环境。" << std::endl;
    }
    return 0;
}
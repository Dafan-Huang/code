#include <iostream>
#include <string>
#include <vector>

// 东北关系简单模拟：家庭、朋友、同事
struct Person {
    std::string name;
    std::vector<std::string> family;
    std::vector<std::string> friends;
    std::vector<std::string> colleagues;
};

void printRelations(const Person& p) {
    std::cout << "姓名: " << p.name << std::endl;
    std::cout << "家庭成员: ";
    for (const auto& f : p.family) std::cout << f << " ";
    std::cout << std::endl;
    std::cout << "朋友: ";
    for (const auto& f : p.friends) std::cout << f << " ";
    std::cout << std::endl;
    std::cout << "同事: ";
    for (const auto& c : p.colleagues) std::cout << c << " ";
    std::cout << std::endl;
}

int main() {
    Person zhangsan{
        "张三",
        {"李四", "王五"}, // 家庭
        {"赵六", "孙七"}, // 朋友
        {"周八"}          // 同事
    };

    printRelations(zhangsan);

    return 0;
}
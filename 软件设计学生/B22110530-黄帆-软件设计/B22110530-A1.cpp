// 1. 分数统计（10分）

// 输入某班级学生的姓名、分数；
// 对分数进行降序排列并输出；
// 具有输入输出界面。

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Student {
    string name;
    int score;
};

// 降序排序
bool cmp(const Student &a, const Student &b) {
    return a.score > b.score;
}

int main() {
    int n;
    cout << "请输入学生人数: ";
    cin >> n;
    vector<Student> students(n);

    for (int i = 0; i < n; ++i) {
        cout << "请输入第" << i + 1 << "位学生的姓名: ";
        cin >> students[i].name;
        cout << "请输入" << students[i].name << "的分数: ";
        cin >> students[i].score;
    }

    sort(students.begin(), students.end(), cmp);

    cout << "\n按分数降序排列结果:\n";
    for (const auto &stu : students) {
        cout << stu.name << " " << stu.score << endl;
    }

    return 0;
}

/*
 * 主函数，负责输入学生信息、排序并输出结果。
 *
 * 程序流程如下：
 * 1. 提示用户输入学生人数，并读取该值。
 * 2. 创建一个包含 n 个 Student 对象的 vector。
 * 3. 循环输入每位学生的姓名和分数。
 * 4. 使用 cmp 比较函数对学生按分数降序排序。
 * 5. 输出排序后的学生姓名和分数。
 *
 * int 程序执行状态码，正常返回 0。
 */
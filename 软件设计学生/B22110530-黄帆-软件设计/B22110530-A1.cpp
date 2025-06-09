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
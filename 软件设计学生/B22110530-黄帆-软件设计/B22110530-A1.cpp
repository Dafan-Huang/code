#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Student {
    string name;
    int score;
};

// ��������
bool cmp(const Student &a, const Student &b) {
    return a.score > b.score;
}

int main() {
    int n;
    cout << "������ѧ������: ";
    cin >> n;
    vector<Student> students(n);

    for (int i = 0; i < n; ++i) {
        cout << "�������" << i + 1 << "λѧ��������: ";
        cin >> students[i].name;
        cout << "������" << students[i].name << "�ķ���: ";
        cin >> students[i].score;
    }

    sort(students.begin(), students.end(), cmp);

    cout << "\n�������������н��:\n";
    for (const auto &stu : students) {
        cout << stu.name << " " << stu.score << endl;
    }

    return 0;
}
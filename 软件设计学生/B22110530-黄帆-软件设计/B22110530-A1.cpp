// 1. ����ͳ�ƣ�10�֣�

// ����ĳ�༶ѧ����������������
// �Է������н������в������
// ��������������档

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

/*
 * ����������������ѧ����Ϣ��������������
 *
 * �����������£�
 * 1. ��ʾ�û�����ѧ������������ȡ��ֵ��
 * 2. ����һ������ n �� Student ����� vector��
 * 3. ѭ������ÿλѧ���������ͷ�����
 * 4. ʹ�� cmp �ȽϺ�����ѧ����������������
 * 5. ���������ѧ�������ͷ�����
 *
 * int ����ִ��״̬�룬�������� 0��
 */
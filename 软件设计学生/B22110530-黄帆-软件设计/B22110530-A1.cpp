// 1. ����ͳ�ƣ�10�֣�
//
// ����ĳ�༶ѧ����������������
// �Է������н������в������
// ��������������档

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// ����ѧ���ṹ�壬���������ͷ���
struct Student {
    string name; // ѧ������
    int score;   // ѧ���ɼ�
};

// ��������ıȽϺ���
// ���a�ķ�������b�ķ�������a����bǰ��
bool cmp(const Student &a, const Student &b) {
    return a.score > b.score;
}

int main() {
    int n; // ѧ������
    cout << "������ѧ������: ";
    cin >> n; // ��ȡѧ������
    vector<Student> students(n); // ����n��ѧ����vector

    // ѭ������ÿλѧ���������ͷ���
    for (int i = 0; i < n; ++i) {
        cout << "�������" << i + 1 << "λѧ��������: ";
        cin >> students[i].name; // ��������
        cout << "������" << students[i].name << "�ķ���: ";
        cin >> students[i].score; // �������
    }

    // ʹ���Զ����cmp������ѧ����������������
    sort(students.begin(), students.end(), cmp);

    // ���������ѧ����Ϣ
    cout << "\n�������������н��:\n";
    for (const auto &stu : students) {
        cout << stu.name << " " << stu.score << endl;
    }

    return 0; // ������������
}

/*
 * @brief ����������������ѧ����Ϣ��������������
 *
 * �����������£�
 * 1. ��ʾ�û�����ѧ������������ȡ��ֵ��
 * 2. ����һ������ n �� Student ����� vector��
 * 3. ѭ������ÿλѧ���������ͷ�����
 * 4. ʹ�� cmp �ȽϺ�����ѧ����������������
 * 5. ���������ѧ�������ͷ�����
 *
 * @return int ����ִ��״̬�룬�������� 0��
 */
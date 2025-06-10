#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <string>
using namespace std;

// �ɼ��ȼ�����
const double PERCENT_USUAL = 0.3;
const double PERCENT_MID = 0.3;
const double PERCENT_FINAL = 0.4;

// �ȼ�����
char getGrade(double score) {
    if (score >= 90) return 'A'; // ��
    if (score >= 80) return 'B'; // ��
    if (score >= 70) return 'C'; // ��
    if (score >= 60) return 'D'; // ����
    return 'E';                  // ������
}

// ѧ����
class Student {
protected:
    string id;
public:
    Student() : id("") {}
    Student(const string& id_) : id(id_) {}
    string getId() const { return id; }
    void setId(const string& id_) { id = id_; }
    virtual ~Student() {}
};

// ѧ���ɼ���
class Marks : public Student {
private:
    double usual, mid, finalExam, total;
    char grade;
public:
    Marks() : Student(), usual(0), mid(0), finalExam(0), total(0), grade('E') {}
    Marks(const string& id_, double u, double m, double f)
        : Student(id_), usual(u), mid(m), finalExam(f) {
        calcTotal();
        grade = getGrade(total);
    }
    void calcTotal() {
        total = usual * PERCENT_USUAL + mid * PERCENT_MID + finalExam * PERCENT_FINAL;
        grade = getGrade(total);
    }
    void readFromStream(istream& in) {
        in >> id >> usual >> mid >> finalExam;
        calcTotal();
    }
    void writeToStream(ostream& out) const {
        out << setw(8) << id << setw(10) << fixed << setprecision(1) << total << setw(8) << grade << endl;
    }
    void show() const {
        cout << setw(8) << id << setw(10) << fixed << setprecision(1) << total << setw(8) << grade << endl;
    }
    double getTotal() const { return total; }
    char getGradeChar() const { return grade; }
};

// ͳ�ƽṹ��
struct Stat {
    int count[5] = {0}; // A,B,C,D,E
    void add(char grade) {
        switch(grade) {
            case 'A': count[0]++; break;
            case 'B': count[1]++; break;
            case 'C': count[2]++; break;
            case 'D': count[3]++; break;
            case 'E': count[4]++; break;
        }
    }
    int total() const {
        return count[0]+count[1]+count[2]+count[3]+count[4];
    }
    void print() const {
        static const char* names[] = {"��(A)", "��(B)", "��(C)", "����(D)", "������(E)"};
        int sum = total();
        cout << left << setw(10) << "�ȼ�" 
             << right << setw(8) << "����" 
             << setw(12) << "ռ��" << endl;
        for(int i=0;i<5;++i) {
            cout << left << setw(10) << names[i]
                 << right << setw(8) << count[i]
                 << setw(11) << fixed << setprecision(2)
                 << (sum ? (count[i]*100.0/sum) : 0) << "%" << endl;
        }
    }
};

void printMenu() {
    cout << "\nѧ���ɼ�����ϵͳ�˵�:\n";
    cout << "1. ��ȡ�ɼ�����������\n";
    cout << "2. ��ʾ��ƽ���ɼ�\n";
    cout << "3. ��ʾ���ȼ��������ٷֱ�\n";
    cout << "4. ���ȼ����ѧ��ѧ�źͳɼ�\n";
    cout << "0. �˳�\n";
    cout << "��ѡ����: ";
}

int main() {
    vector<Marks> students;
    Stat stat;
    double avg = 0.0;
    bool loaded = false;

    while (true) {
        printMenu();
        int choice;
        cin >> choice;
        if (choice == 0) break;
        if (choice == 1) {
            students.clear();
            stat = Stat();
            avg = 0.0;
            ifstream fin("C:/Users/24096/Desktop/code/������ѧ��/B22110530-�Ʒ�-������/note.dat"); // ʹ�þ���·��
            if (!fin) {
                cout << "�޷����ļ� note.dat\n";
                system("pause");
                system("cls");
                continue;
            }
            int n;
            fin >> n;
            for (int i = 0; i < n; ++i) {
                Marks m;
                m.readFromStream(fin);
                students.push_back(m);
                stat.add(m.getGradeChar());
                avg += m.getTotal();
            }
            fin.close();
            avg = n ? avg / n : 0;
            // ����� out.dat
            ofstream fout("out.dat");
            for (const auto& m : students) {
                m.writeToStream(fout);
            }
            fout.close();
            cout << "�ɼ���ȡ��������ɣ���д�� out.dat\n";
            loaded = true;
            system("pause");
        } else if (choice == 2) {
            if (!loaded) { cout << "���ȶ�ȡ�ɼ���\n"; system("pause"); system("cls"); continue; }
            cout << "��ƽ���ɼ�Ϊ: " << fixed << setprecision(2) << avg << endl;
            system("pause");
        } else if (choice == 3) {
            if (!loaded) { cout << "���ȶ�ȡ�ɼ���\n"; system("pause"); system("cls"); continue; }
            stat.print();
            system("pause");
        } else if (choice == 4) {
            if (!loaded) { cout << "���ȶ�ȡ�ɼ���\n"; system("pause"); system("cls"); continue; }
            static const char* names[] = {"��(A)", "��(B)", "��(C)", "����(D)", "������(E)"};
            char grades[] = {'A','B','C','D','E'};
            for (int g = 0; g < 5; ++g) {
                cout << "\n" << names[g] << ":\n";
                cout << setw(8) << "ѧ��" << setw(10) << "����" << setw(8) << "�ȼ�" << endl;
                for (const auto& m : students) {
                    if (m.getGradeChar() == grades[g]) m.show();
                }
            }
            system("pause");
        } else {
            cout << "��Чѡ�������ԡ�\n";
            system("pause");
        }
        system("cls"); // ÿ�β���������
    }
    return 0;
}

/*
 * ѧ���ɼ�����ϵͳ
 * 
 * ���ܼ��:
 * ������ʵ����һ�����������е�ѧ���ɼ�����ϵͳ��֧�ִ��ļ���ȡѧ���ɼ����ݣ����������ɼ���ͳ�Ƴɼ��ȼ��ֲ�������������Ϣ��
 * 
 * ��Ҫ����:
 * 1. ��ȡ�ɼ���������������ָ���ļ�(note.dat)��ȡѧ��ѧ�ż�ƽʱ�ɼ������гɼ�����ĩ�ɼ������������ɼ��͵ȼ�����д������ļ�(out.dat)��
 * 2. ��ʾ��ƽ���ɼ����������ѧ���������ɼ�ƽ��ֵ��
 * 3. ��ʾ���ȼ��������ٷֱȣ�ͳ�Ʋ���ʾ���ɼ��ȼ���A, B, C, D, E������������ռ�ȡ�
 * 4. ���ȼ����ѧ��ѧ�źͳɼ����ֵȼ����ѧ����ѧ�š������ɼ��͵ȼ���
 * 
 * ��Ҫ����ṹ��˵��:
 * - Student: ѧ�����࣬������ѧ����Ϣ��
 * - Marks: �̳���Student������ƽʱ�ɼ������гɼ�����ĩ�ɼ��������ɼ��͵ȼ������ṩ�ɼ��������������������
 * - Stat: ͳ�ƽṹ�壬����ͳ�Ƹ��ȼ����������ͳ����Ϣ��
 * 
 * ��Ҫ����˵��:
 * - getGrade(double score): ���������ɼ����ض�Ӧ�ȼ��ַ���A-E����
 * - printMenu(): ������˵���
 * 
 * �ļ�˵��:
 * - note.dat: �����ļ�������ѧ��������ÿ��ѧ����ѧ�ź�ƽʱ�����С���ĩ�ɼ���
 * - out.dat: ����ļ�������ÿ��ѧ����ѧ�š������ɼ��͵ȼ���
 * 
 * ʹ��˵��:
 * ���г���󣬰���ʾѡ���ܡ��״β������ȶ�ȡ�ɼ����ݡ�
 * 
 * ע������:
 * - �ļ�·�������ʵ�����������
 * - �豣֤�����ļ���ʽ��ȷ��
 */
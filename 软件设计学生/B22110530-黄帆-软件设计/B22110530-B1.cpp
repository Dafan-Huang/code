#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <string>
using namespace std;

// 成绩等级常量
const double PERCENT_USUAL = 0.3;
const double PERCENT_MID = 0.3;
const double PERCENT_FINAL = 0.4;

// 等级区间
char getGrade(double score) {
    if (score >= 90) return 'A'; // 优
    if (score >= 80) return 'B'; // 良
    if (score >= 70) return 'C'; // 中
    if (score >= 60) return 'D'; // 及格
    return 'E';                  // 不及格
}

// 学生类
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

// 学生成绩类
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

// 统计结构体
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
        static const char* names[] = {"优(A)", "良(B)", "中(C)", "及格(D)", "不及格(E)"};
        int sum = total();
        cout << left << setw(10) << "等级" 
             << right << setw(8) << "人数" 
             << setw(12) << "占比" << endl;
        for(int i=0;i<5;++i) {
            cout << left << setw(10) << names[i]
                 << right << setw(8) << count[i]
                 << setw(11) << fixed << setprecision(2)
                 << (sum ? (count[i]*100.0/sum) : 0) << "%" << endl;
        }
    }
};

void printMenu() {
    cout << "\n学生成绩核算系统菜单:\n";
    cout << "1. 读取成绩并计算总评\n";
    cout << "2. 显示总平均成绩\n";
    cout << "3. 显示各等级人数及百分比\n";
    cout << "4. 按等级输出学生学号和成绩\n";
    cout << "0. 退出\n";
    cout << "请选择功能: ";
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
            ifstream fin("C:/Users/24096/Desktop/code/软件设计学生/B22110530-黄帆-软件设计/note.dat"); // 使用绝对路径
            if (!fin) {
                cout << "无法打开文件 note.dat\n";
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
            // 输出到 out.dat
            ofstream fout("out.dat");
            for (const auto& m : students) {
                m.writeToStream(fout);
            }
            fout.close();
            cout << "成绩读取并计算完成，已写入 out.dat\n";
            loaded = true;
            system("pause");
        } else if (choice == 2) {
            if (!loaded) { cout << "请先读取成绩！\n"; system("pause"); system("cls"); continue; }
            cout << "总平均成绩为: " << fixed << setprecision(2) << avg << endl;
            system("pause");
        } else if (choice == 3) {
            if (!loaded) { cout << "请先读取成绩！\n"; system("pause"); system("cls"); continue; }
            stat.print();
            system("pause");
        } else if (choice == 4) {
            if (!loaded) { cout << "请先读取成绩！\n"; system("pause"); system("cls"); continue; }
            static const char* names[] = {"优(A)", "良(B)", "中(C)", "及格(D)", "不及格(E)"};
            char grades[] = {'A','B','C','D','E'};
            for (int g = 0; g < 5; ++g) {
                cout << "\n" << names[g] << ":\n";
                cout << setw(8) << "学号" << setw(10) << "总评" << setw(8) << "等级" << endl;
                for (const auto& m : students) {
                    if (m.getGradeChar() == grades[g]) m.show();
                }
            }
            system("pause");
        } else {
            cout << "无效选择，请重试。\n";
            system("pause");
        }
        system("cls"); // 每次操作后清屏
    }
    return 0;
}

/*
 * 学生成绩核算系统
 * 
 * 功能简介:
 * 本程序实现了一个基于命令行的学生成绩管理系统，支持从文件读取学生成绩数据，计算总评成绩，统计成绩等级分布，并输出相关信息。
 * 
 * 主要功能:
 * 1. 读取成绩并计算总评：从指定文件(note.dat)读取学生学号及平时成绩、期中成绩、期末成绩，计算总评成绩和等级，并写入输出文件(out.dat)。
 * 2. 显示总平均成绩：输出所有学生的总评成绩平均值。
 * 3. 显示各等级人数及百分比：统计并显示各成绩等级（A, B, C, D, E）的人数及其占比。
 * 4. 按等级输出学生学号和成绩：分等级输出学生的学号、总评成绩和等级。
 * 
 * 主要类与结构体说明:
 * - Student: 学生基类，仅包含学号信息。
 * - Marks: 继承自Student，包含平时成绩、期中成绩、期末成绩、总评成绩和等级，并提供成绩计算与输入输出方法。
 * - Stat: 统计结构体，用于统计各等级人数及输出统计信息。
 * 
 * 主要函数说明:
 * - getGrade(double score): 根据总评成绩返回对应等级字符（A-E）。
 * - printMenu(): 输出主菜单。
 * 
 * 文件说明:
 * - note.dat: 输入文件，包含学生人数及每个学生的学号和平时、期中、期末成绩。
 * - out.dat: 输出文件，保存每个学生的学号、总评成绩和等级。
 * 
 * 使用说明:
 * 运行程序后，按提示选择功能。首次操作需先读取成绩数据。
 * 
 * 注意事项:
 * - 文件路径需根据实际情况调整。
 * - 需保证输入文件格式正确。
 */
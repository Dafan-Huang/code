#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <iomanip>
#include <cmath>
using namespace std;

// 常量定义
const double LOCAL_BASE_FEE = 0.5;
const double LOCAL_INC_FEE = 0.2;
const int LOCAL_BASE_TIME = 180; // 3分钟=180秒
const int LOCAL_INC_TIME = 180;  // 每3分钟递增

// 用户类
class User {
public:
    string phone;
    string name;
    User() {}
    User(const string& p, const string& n) : phone(p), name(n) {}
    static map<string, string> loadUsers(const string& filename) {
        map<string, string> users;
        ifstream fin(filename);
        string phone, name;
        while (fin >> phone >> name) {
            users[phone] = name;
        }
        return users;
    }
};

// 话单类
class Callist {
public:
    string caller_area, caller_phone;
    string callee_area, callee_phone;
    int duration; // 秒

    Callist() {}
    Callist(const string& ca, const string& cp, const string& cea, const string& cep, int d)
        : caller_area(ca), caller_phone(cp), callee_area(cea), callee_phone(cep), duration(d) {}

    static vector<Callist> loadCallists(const string& filename) {
        vector<Callist> calls;
        ifstream fin(filename);
        string ca, cp, cea, cep;
        int d;
        while (fin >> ca >> cp >> cea >> cep >> d) {
            calls.emplace_back(ca, cp, cea, cep, d);
        }
        return calls;
    }
};

// 费用类
class Charge : public Callist {
public:
    int type; // 0:本地, 1:长途
    double fee;

    Charge(const Callist& c, int t, double f)
        : Callist(c), type(t), fee(f) {}

    static map<string, double> loadRates(const string& filename) {
        map<string, double> rates;
        ifstream fin(filename);
        string area;
        double rate;
        while (fin >> area >> rate) {
            rates[area] = rate;
        }
        return rates;
    }

    static double calcLocalFee(int seconds) {
        if (seconds <= LOCAL_BASE_TIME) return LOCAL_BASE_FEE;
        int extra = seconds - LOCAL_BASE_TIME;
        int inc = (extra + LOCAL_INC_TIME - 1) / LOCAL_INC_TIME;
        return LOCAL_BASE_FEE + inc * LOCAL_INC_FEE;
    }

    static double calcLongFee(int seconds, double rate) {
        int mins = (seconds + 59) / 60;
        return mins * rate;
    }

    static vector<Charge> calcCharges(const vector<Callist>& calls, const map<string, double>& rates) {
        vector<Charge> charges;
        for (const auto& c : calls) {
            if (c.caller_area == c.callee_area) {
                double fee = calcLocalFee(c.duration);
                charges.emplace_back(c, 0, fee);
            } else {
                double rate = 0.0;
                auto it = rates.find(c.callee_area);
                if (it != rates.end()) rate = it->second;
                double fee = calcLongFee(c.duration, rate);
                charges.emplace_back(c, 1, fee);
            }
        }
        return charges;
    }

    static void saveCharges(const vector<Charge>& charges, const string& filename) {
        ofstream fout(filename);
        for (const auto& ch : charges) {
            fout << ch.caller_phone << " " << ch.type << " " << fixed << setprecision(2) << ch.fee << endl;
        }
    }

    // 查询费用
    static void queryFee(const string& phone, const string& chargefile, const map<string, string>& users) {
        ifstream fin(chargefile);
        string p;
        int type;
        double fee;
        double local = 0, longd = 0;
        while (fin >> p >> type >> fee) {
            if (p == phone) {
                if (type == 0) local += fee;
                else longd += fee;
            }
        }
        string name = users.count(phone) ? users.at(phone) : "未知";
        cout << "--------------------------------------------------------" << endl;
        cout << left << setw(10) << "用户名" 
             << setw(15) << "电话号码" 
             << setw(12) << "本地话费" 
             << setw(12) << "长途话费" 
             << setw(12) << "话费总计" << endl;
        cout << "--------------------------------------------------------" << endl;
        cout << left << setw(10) << name
             << setw(15) << phone
             << setw(12) << fixed << setprecision(2) << local
             << setw(12) << longd
             << setw(12) << (local + longd) << endl;
        cout << "--------------------------------------------------------" << endl;
    }

    // 查询话单
    static void queryCallist(const string& phone, const vector<Callist>& calls, const map<string, string>& users) {
        string name = users.count(phone) ? users.at(phone) : "未知";
        cout << "---------------------------------------------------------------" << endl;
        cout << left << setw(10) << "用户名"
             << setw(15) << "主叫号码"
             << setw(15) << "被叫号码"
             << setw(10) << "通话时长" << endl;
        cout << "---------------------------------------------------------------" << endl;
        for (const auto& c : calls) {
            if (c.caller_phone == phone) {
                cout << left << setw(10) << name
                     << setw(15) << c.caller_phone
                     << setw(15) << c.callee_phone
                     << setw(10) << c.duration << endl;
            }
        }
        cout << "---------------------------------------------------------------" << endl;
    }
};

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void pauseScreen() {
#ifdef _WIN32
    system("pause");
#else
    cout << "按任意键继续..." << endl;
    cin.ignore();
    cin.get();
#endif
}

void menu() {
    cout << "======================================" << endl;
    cout << "      电话计费系统" << endl;
    cout << "======================================" << endl;
    cout << " 1. 计算通话费用" << endl;
    cout << " 2. 话费查询" << endl;
    cout << " 3. 话单查询" << endl;
    cout << " 0. 退出" << endl;
    cout << "======================================" << endl;
    cout << "请选择操作：";
}

#include <cstdlib>

int main() {
    map<string, string> users = User::loadUsers("C:/Users/24096/Desktop/code/软件设计学生/B22110530-黄帆-软件设计/yh.dat");
    vector<Callist> calls = Callist::loadCallists("C:/Users/24096/Desktop/code/软件设计学生/B22110530-黄帆-软件设计/hd.dat");
    map<string, double> rates = Charge::loadRates("C:/Users/24096/Desktop/code/软件设计学生/B22110530-黄帆-软件设计/fl.dat");
    vector<Charge> charges;
    bool fee_calculated = false;

    while (true) {
        clearScreen();
        menu();
        int op;
        cin >> op;
        clearScreen();
        if (op == 0) {
            cout << "感谢使用，再见！" << endl;
            break;
        }
        if (op == 1) {
            charges = Charge::calcCharges(calls, rates);
            Charge::saveCharges(charges, "fy.dat");
            cout << "费用计算完成，已保存到 fy.dat" << endl;
            fee_calculated = true;
        } else if (op == 2) {
            if (!fee_calculated) {
                cout << "请先进行费用计算！" << endl;
                pauseScreen();
                continue;
            }
            cout << "请输入电话号码: ";
            string phone;
            cin >> phone;
            clearScreen();
            Charge::queryFee(phone, "fy.dat", users);
        } else if (op == 3) {
            cout << "请输入电话号码: ";
            string phone;
            cin >> phone;
            clearScreen();
            Charge::queryCallist(phone, calls, users);
        } else {
            cout << "无效操作" << endl;
        }
        pauseScreen();
    }
    return 0;
}

/*
 * 电话计费系统
 * 
 * 本程序实现了一个简单的电话计费系统，支持用户信息、话单信息、费率信息的读取，
 * 并能根据本地和长途通话规则计算费用，支持费用查询和话单查询功能。
 * 
 * 主要功能模块：
 * 1. 用户信息管理（User类）
 *    - 读取用户数据文件，建立电话号码与用户名的映射。
 * 
 * 2. 话单信息管理（Callist类）
 *    - 读取话单数据文件，保存每条通话的主叫、被叫、通话时长等信息。
 * 
 * 3. 费率与费用计算（Charge类）
 *    - 读取各地区长途费率。
 *    - 支持本地通话与长途通话的费用计算：
 *        本地：前3分钟0.5元，之后每3分钟0.2元，不足3分钟按3分钟计。
 *        长途：按分钟计费，不足1分钟按1分钟计，费率由地区决定。
 *    - 费用结果保存到文件，支持按电话号码查询本地/长途/总费用。
 *    - 支持按电话号码查询通话详单。
 * 
 * 4. 用户交互界面
 *    - 提供菜单操作，支持费用计算、费用查询、话单查询和退出。
 *    - 支持跨平台清屏与暂停。
 * 
 * 文件说明：
 * - yh.dat : 用户信息文件（格式：电话号码 用户名）
 * - hd.dat : 话单信息文件（格式：主叫区号 主叫号码 被叫区号 被叫号码 通话时长(秒)）
 * - fl.dat : 长途费率文件（格式：区号 费率(元/分钟)）
 * - fy.dat : 计算结果文件（格式：主叫号码 类型(0本地/1长途) 费用）
 * 
 */
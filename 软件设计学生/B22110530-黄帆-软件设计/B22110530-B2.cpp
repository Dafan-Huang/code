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
        cout << "用户名  电话号码  本地话费  长途话费  话费总计" << endl;
        cout << name << "  " << phone << "  "
             << fixed << setprecision(2) << local << "  "
             << longd << "  " << (local + longd) << endl;
    }

    // 查询话单
    static void queryCallist(const string& phone, const vector<Callist>& calls, const map<string, string>& users) {
        string name = users.count(phone) ? users.at(phone) : "未知";
        cout << "用户名  主叫号码  被叫号码  通话时长" << endl;
        for (const auto& c : calls) {
            if (c.caller_phone == phone) {
                cout << name << "  " << c.caller_phone << "  " << c.callee_phone << "  " << c.duration << endl;
            }
        }
    }
};

void menu() {
    cout << "1. 计算通话费用" << endl;
    cout << "2. 话费查询" << endl;
    cout << "3. 话单查询" << endl;
    cout << "0. 退出" << endl;
}

#include <cstdlib>

int main() {
    map<string, string> users = User::loadUsers("yh.dat");
    vector<Callist> calls = Callist::loadCallists("hd.dat");
    map<string, double> rates = Charge::loadRates("fl.dat");
    vector<Charge> charges;
    bool fee_calculated = false;

    while (true) {
        system("cls"); // 清屏
        menu();
        int op;
        cin >> op;
        if (op == 0) break;
        system("cls"); // 清屏
        if (op == 1) {
            charges = Charge::calcCharges(calls, rates);
            Charge::saveCharges(charges, "fy.dat");
            cout << "费用计算完成,已保存到fy.dat" << endl;
            fee_calculated = true;
        } else if (op == 2) {
            if (!fee_calculated) {
                cout << "请先进行费用计算！" << endl;
                system("pause");
                continue;
            }
            cout << "请输入电话号码: ";
            string phone;
            cin >> phone;
            Charge::queryFee(phone, "fy.dat", users);
        } else if (op == 3) {
            cout << "请输入电话号码: ";
            string phone;
            cin >> phone;
            Charge::queryCallist(phone, calls, users);
        } else {
            cout << "无效操作" << endl;
        }
        system("pause"); // 暂停，等待用户按键
    }
    return 0;
}
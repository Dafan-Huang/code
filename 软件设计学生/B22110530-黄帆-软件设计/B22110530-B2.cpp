#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <iomanip>
#include <cmath>
using namespace std;

// ��������
const double LOCAL_BASE_FEE = 0.5;      // ����ͨ���������ã�ǰ3����0.5Ԫ��
const double LOCAL_INC_FEE = 0.2;       // ����ͨ��ÿ����3���ӵķ��ã�0.2Ԫ��
const int LOCAL_BASE_TIME = 180;        // ����ͨ������ʱ����3����=180�룩
const int LOCAL_INC_TIME = 180;         // ����ͨ������ʱ����ÿ3����=180�룩

// �û��࣬�����û���Ϣ
class User {
public:
    string phone;   // �绰����
    string name;    // �û���
    User() {}
    User(const string& p, const string& n) : phone(p), name(n) {}
    // ���ļ������û���Ϣ�����ص绰���뵽�û�����ӳ��
    // �ļ���ʽ��ÿ�С��绰���� �û�����
    static map<string, string> loadUsers(const string& filename) {
        map<string, string> users;
        ifstream fin(filename);
        string phone, name;
        while (fin >> phone >> name) {
            users[phone] = name; // �����绰���뵽�û�����ӳ��
        }
        return users;
    }
};

// �����࣬����ÿһ��ͨ����¼
class Callist {
public:
    string caller_area, caller_phone;   // �������š����к���
    string callee_area, callee_phone;   // �������š����к���
    int duration;                       // ͨ��ʱ�����룩

    Callist() {}
    Callist(const string& ca, const string& cp, const string& cea, const string& cep, int d)
        : caller_area(ca), caller_phone(cp), callee_area(cea), callee_phone(cep), duration(d) {}

    // ���ļ��������л���������ͨ����¼��vector
    // �ļ���ʽ���������� ���к��� �������� ���к��� ͨ��ʱ��(��)
    static vector<Callist> loadCallists(const string& filename) {
        vector<Callist> calls;
        ifstream fin(filename);
        string ca, cp, cea, cep;
        int d;
        while (fin >> ca >> cp >> cea >> cep >> d) {
            calls.emplace_back(ca, cp, cea, cep, d); // ���һ��ͨ����¼
        }
        return calls;
    }
};

// �����࣬�̳���Callist������ͨ�����ͺͷ���
class Charge : public Callist {
public:
    int type;       // 0:����, 1:��;
    double fee;     // ͨ������

    Charge(const Callist& c, int t, double f)
        : Callist(c), type(t), fee(f) {}

    // ���ļ����س�;���ʣ��������ŵ����ʵ�ӳ��
    // �ļ���ʽ������ ����(Ԫ/����)
    static map<string, double> loadRates(const string& filename) {
        map<string, double> rates;
        ifstream fin(filename);
        string area;
        double rate;
        while (fin >> area >> rate) {
            rates[area] = rate; // �������ŵ����ʵ�ӳ��
        }
        return rates;
    }

    // ���㱾��ͨ������
    // ǰ3����0.5Ԫ��֮��ÿ3����0.2Ԫ������3���Ӱ�3���Ӽ�
    static double calcLocalFee(int seconds) {
        if (seconds <= LOCAL_BASE_TIME) return LOCAL_BASE_FEE;
        int extra = seconds - LOCAL_BASE_TIME;
        int inc = (extra + LOCAL_INC_TIME - 1) / LOCAL_INC_TIME; // ����ȡ����������
        return LOCAL_BASE_FEE + inc * LOCAL_INC_FEE;
    }

    // ���㳤;ͨ������
    // �����ӼƷѣ�����1���Ӱ�1���Ӽƣ������ɵ�������
    static double calcLongFee(int seconds, double rate) {
        int mins = (seconds + 59) / 60; // ����ȡ��������
        return mins * rate;
    }

    // ��������ͨ���ķ��ã�����Charge�����vector
    static vector<Charge> calcCharges(const vector<Callist>& calls, const map<string, double>& rates) {
        vector<Charge> charges;
        for (const auto& c : calls) {
            if (c.caller_area == c.callee_area) { // ����ͨ��
                double fee = calcLocalFee(c.duration);
                charges.emplace_back(c, 0, fee);
            } else { // ��;ͨ��
                double rate = 0.0;
                auto it = rates.find(c.callee_area);
                if (it != rates.end()) rate = it->second;
                double fee = calcLongFee(c.duration, rate);
                charges.emplace_back(c, 1, fee);
            }
        }
        return charges;
    }

    // �����з�����ϸ���浽�ļ�
    // �ļ���ʽ�����к��� ����(0����/1��;) ����
    static void saveCharges(const vector<Charge>& charges, const string& filename) {
        ofstream fout(filename);
        for (const auto& ch : charges) {
            fout << ch.caller_phone << " " << ch.type << " " << fixed << setprecision(2) << ch.fee << endl;
        }
    }

    // ��ѯĳ���绰����ķ�����ϸ�����
    // ���ܱ��غͳ�;���ã�����û��������롢����/��;/�ܷ���
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
        string name = users.count(phone) ? users.at(phone) : "δ֪";
        cout << "--------------------------------------------------------" << endl;
        cout << left << setw(10) << "�û���" 
             << setw(15) << "�绰����" 
             << setw(12) << "���ػ���" 
             << setw(12) << "��;����" 
             << setw(12) << "�����ܼ�" << endl;
        cout << "--------------------------------------------------------" << endl;
        cout << left << setw(10) << name
             << setw(15) << phone
             << setw(12) << fixed << setprecision(2) << local
             << setw(12) << longd
             << setw(12) << (local + longd) << endl;
        cout << "--------------------------------------------------------" << endl;
    }

    // ��ѯĳ���绰�����ͨ���굥�����
    // ����ú�����Ϊ���е�����ͨ����¼
    static void queryCallist(const string& phone, const vector<Callist>& calls, const map<string, string>& users) {
        string name = users.count(phone) ? users.at(phone) : "δ֪";
        cout << "---------------------------------------------------------------" << endl;
        cout << left << setw(10) << "�û���"
             << setw(15) << "���к���"
             << setw(15) << "���к���"
             << setw(10) << "ͨ��ʱ��" << endl;
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

// ����������֧��Windows��Linux
void clearScreen() {
#ifdef _WIN32
    system("cls"); // Windows������
#else
    system("clear"); // Linux������
#endif
}

// ��ͣ��Ļ������֧��Windows��Linux
void pauseScreen() {
#ifdef _WIN32
    system("pause"); // Windows����ͣ
#else
    cout << "�����������..." << endl;
    cin.ignore();
    cin.get();
#endif
}

// �˵���ʾ����
void menu() {
    cout << "======================================" << endl;
    cout << "      �绰�Ʒ�ϵͳ" << endl;
    cout << "======================================" << endl;
    cout << " 1. ����ͨ������" << endl;
    cout << " 2. ���Ѳ�ѯ" << endl;
    cout << " 3. ������ѯ" << endl;
    cout << " 0. �˳�" << endl;
    cout << "======================================" << endl;
    cout << "��ѡ�������";
}

#include <cstdlib>

int main() {
    // �����û�����������������
    // �û���Ϣ�ļ���yh.dat
    map<string, string> users = User::loadUsers("C:/Users/24096/Desktop/code/������ѧ��/B22110530-�Ʒ�-������/yh.dat");
    // ������Ϣ�ļ���hd.dat
    vector<Callist> calls = Callist::loadCallists("C:/Users/24096/Desktop/code/������ѧ��/B22110530-�Ʒ�-������/hd.dat");
    // ��;�����ļ���fl.dat
    map<string, double> rates = Charge::loadRates("C:/Users/24096/Desktop/code/������ѧ��/B22110530-�Ʒ�-������/fl.dat");
    vector<Charge> charges;
    bool fee_calculated = false; // ����Ƿ��Ѽ������

    while (true) {
        clearScreen();
        menu();
        int op;
        cin >> op;
        clearScreen();
        if (op == 0) { // �˳�
            cout << "��лʹ�ã��ټ���" << endl;
            break;
        }
        if (op == 1) { // �������
            // ��������ͨ�����ò����浽fy.dat
            charges = Charge::calcCharges(calls, rates);
            Charge::saveCharges(charges, "fy.dat");
            cout << "���ü�����ɣ��ѱ��浽 fy.dat" << endl;
            fee_calculated = true;
        } else if (op == 2) { // ���Ѳ�ѯ
            if (!fee_calculated) {
                cout << "���Ƚ��з��ü��㣡" << endl;
                pauseScreen();
                continue;
            }
            cout << "������绰����: ";
            string phone;
            cin >> phone;
            clearScreen();
            // ��ѯ�ú���ķ�����ϸ
            Charge::queryFee(phone, "fy.dat", users);
        } else if (op == 3) { // ������ѯ
            cout << "������绰����: ";
            string phone;
            cin >> phone;
            clearScreen();
            // ��ѯ�ú����ͨ���굥
            Charge::queryCallist(phone, calls, users);
        } else {
            cout << "��Ч����" << endl;
        }
        pauseScreen();
    }
    return 0;
}

/*
 * �绰�Ʒ�ϵͳ
 * 
 * ������ʵ����һ���򵥵ĵ绰�Ʒ�ϵͳ��֧���û���Ϣ��������Ϣ��������Ϣ�Ķ�ȡ��
 * ���ܸ��ݱ��غͳ�;ͨ�����������ã�֧�ַ��ò�ѯ�ͻ�����ѯ���ܡ�
 * 
 * ��Ҫ����ģ�飺
 * 1. �û���Ϣ����User�ࣩ
 *    - ��ȡ�û������ļ��������绰�������û�����ӳ�䡣
 * 
 * 2. ������Ϣ����Callist�ࣩ
 *    - ��ȡ���������ļ�������ÿ��ͨ�������С����С�ͨ��ʱ������Ϣ��
 * 
 * 3. ��������ü��㣨Charge�ࣩ
 *    - ��ȡ��������;���ʡ�
 *    - ֧�ֱ���ͨ���볤;ͨ���ķ��ü��㣺
 *        ���أ�ǰ3����0.5Ԫ��֮��ÿ3����0.2Ԫ������3���Ӱ�3���Ӽơ�
 *        ��;�������ӼƷѣ�����1���Ӱ�1���Ӽƣ������ɵ���������
 *    - ���ý�����浽�ļ���֧�ְ��绰�����ѯ����/��;/�ܷ��á�
 *    - ֧�ְ��绰�����ѯͨ���굥��
 * 
 * 4. �û���������
 *    - �ṩ�˵�������֧�ַ��ü��㡢���ò�ѯ��������ѯ���˳���
 *    - ֧�ֿ�ƽ̨��������ͣ��
 * 
 * �ļ�˵����
 * - yh.dat : �û���Ϣ�ļ�����ʽ���绰���� �û�����
 * - hd.dat : ������Ϣ�ļ�����ʽ���������� ���к��� �������� ���к��� ͨ��ʱ��(��)��
 * - fl.dat : ��;�����ļ�����ʽ������ ����(Ԫ/����)��
 * - fy.dat : �������ļ�����ʽ�����к��� ����(0����/1��;) ���ã�
 * 
 */
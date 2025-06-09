//  5. ����ת������10�֣�

// ����������ơ��˽��ơ�ʮ���ơ�ʮ����������
// �����������ת����������Ƶ�����
// ��������������档

#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <cctype>

using namespace std;

// ����ַ����Ƿ�Ϊ�Ϸ���ָ��������
bool isValidNumber(const string& s, int base) {
    size_t start = 0;
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x' || tolower(s[1]) == 'b')) start = 2;
    else if (s.size() > 1 && s[0] == '0' && base == 8) start = 1;
    for (size_t i = start; i < s.size(); ++i) {
        char c = toupper(s[i]);
        if (base <= 10) {
            if (!isdigit(c) || c - '0' >= base) return false;
        } else {
            if (!isdigit(c) && (c < 'A' || c >= 'A' + base - 10)) return false;
        }
    }
    return true;
}

// �Զ�ʶ����Ʋ�ת��Ϊʮ����
bool parseInput(const string& input, int& value, int& base) {
    string s = input;
    base = 10;
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x')) {
        base = 16;
        s = s.substr(2);
    } else if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'b')) {
        base = 2;
        s = s.substr(2);
    } else if (s.size() > 1 && s[0] == '0') {
        base = 8;
        s = s.substr(1);
    }
    if (!isValidNumber(input, base)) return false;
    try {
        value = std::stoi(s, nullptr, base);
    } catch (...) {
        return false;
    }
    return true;
}

// ʮ����תΪ���������ַ���
string toBase(int value, int base) {
    if (base == 10) return to_string(value);
    string result;
    unsigned int uvalue = static_cast<unsigned int>(value);
    if (base == 2) {
        result = "0b";
        string bin;
        if (uvalue == 0) bin = "0";
        while (uvalue) {
            bin = char('0' + (uvalue % 2)) + bin;
            uvalue /= 2;
        }
        result += bin;
    } else if (base == 8) {
        result = "0";
        string oct;
        if (uvalue == 0) oct = "0";
        while (uvalue) {
            oct = char('0' + (uvalue % 8)) + oct;
            uvalue /= 8;
        }
        result += oct;
    } else if (base == 16) {
        result = "0x";
        string hex;
        if (uvalue == 0) hex = "0";
        while (uvalue) {
            int digit = uvalue % 16;
            hex = (digit < 10 ? char('0' + digit) : char('A' + digit - 10)) + hex;
            uvalue /= 16;
        }
        result += hex;
    }
    return result;
}

int main() {
    while (true) {
#ifdef _WIN32
        system("cls");
#else
        system("clear");
#endif
        cout << "===== ����ת���� =====" << endl;
        cout << "������һ����(֧�ֶ�����0b, �˽���0, ʮ����, ʮ������0xǰ׺):" << endl;
        string input;
        cin >> input;

        int value, base;
        if (!parseInput(input, value, base)) {
            cout << "�����ʽ����" << endl;
        } else {
            cout << "�������Ϊ: " << input << endl;
            cout << "ʮ����: " << toBase(value, 10) << endl;
            cout << "������: " << toBase(value, 2) << endl;
            cout << "�˽���: " << toBase(value, 8) << endl;
            cout << "ʮ������: " << toBase(value, 16) << endl;
        }

        cout << "\n�Ƿ����ת��?(y/n): ";
        string choice;
        cin >> choice;
        if (choice != "y" && choice != "Y") break;
    }
    return 0;
}

/*
    ����ת��������

    ���ܼ��:
    - ֧�����������(0bǰ׺)���˽���(0ǰ׺)��ʮ���ơ�ʮ������(0xǰ׺)�����֡�
    - �Զ�ʶ���������ֵĽ��ƣ�������ת��Ϊ�������ֽ��Ƹ�ʽ�����
    - �ṩ�򵥵�����������棬֧�ֶ��ת��������

    ��Ҫ����˵��:
    1. isValidNumber(const string& s, int base)
        - ����ַ���s�Ƿ�Ϊ�Ϸ���ָ������(base)���֡�
        - ֧�ֶ����ơ��˽��ơ�ʮ���ơ�ʮ�����ƵĺϷ����жϡ�

    2. parseInput(const string& input, int& value, int& base)
        - �Զ�ʶ�������ַ���input�Ľ������ͣ���ת��Ϊʮ��������value��
        - ʶ��0b��0x��0ǰ׺���ֱ��Ӧ�����ơ�ʮ�����ơ��˽��ơ�
        - ����ʶ�𵽵Ľ���base��
        - ������Ƿ�������false��

    3. toBase(int value, int base)
        - ��ʮ��������valueת��Ϊָ������(base)���ַ�����ʾ��
        - ������б�׼ǰ׺(��0b, 0, 0x)�ĸ�ʽ��

    ʹ��˵��:
    - ���г����������Ҫת�������֣�֧��0b��0��0xǰ׺����
    - �������������ֵ�ʮ���ơ������ơ��˽��ơ�ʮ�����Ʊ�ʾ��
    - ��ѡ���Ƿ����������һ��ת����

    ע������:
    - �����ʽ����϶�Ӧ���ƵĺϷ��ַ���Χ��
    - ����Ƿ�ʱ����ʾ������Ϣ��
*/
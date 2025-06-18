//  5. ����ת������10�֣�
//
// ����Ҫ��
// 1. �û�������������ơ��˽��ơ�ʮ���ƻ�ʮ�����Ƶ�����
// 2. �����Զ�ʶ���������Ľ��ƣ�������ת��Ϊ�������ֽ��Ƶı�ʾ��
// 3. �ṩ�򵥵�����������棬֧�ֶ��ת����
//
// ֧�ֵ������ʽ��
// - �����ƣ���0b��0B��ͷ������0b1010
// - �˽��ƣ���0��ͷ������0123
// - ʮ���ƣ�ֱ���������֣�����123
// - ʮ�����ƣ���0x��0X��ͷ������0x1A3F

#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <cctype>

using namespace std;

// ����ַ����Ƿ�Ϊ�Ϸ���ָ��������
// ������
//   s    ���û�������ַ��������ܰ�������ǰ׺����0x, 0b, 0��
//   base ��ָ��Ҫ���Ľ��ƣ�2/8/10/16��
// ����ֵ��
//   ���s�ǺϷ���base������������true�����򷵻�false
// ˵����
//   - ��������ǰ׺�󣬼��ÿ���ַ��Ƿ���ϸý��ƵĺϷ��ַ���Χ��
//   - ������ֻ�ܰ���0��1���˽���ֻ�ܰ���0-7��ʮ����ֻ�ܰ���0-9��ʮ�����ƿɰ���0-9��A-F/a-f��
bool isValidNumber(const string& s, int base) {
    size_t start = 0;
    // ����ǰ׺����0x, 0b, 0��
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x' || tolower(s[1]) == 'b')) start = 2;
    else if (s.size() > 1 && s[0] == '0' && base == 8) start = 1;
    for (size_t i = start; i < s.size(); ++i) {
        char c = toupper(s[i]);
        if (base <= 10) {
            // ����2/8/10���ƣ�������������С��base
            if (!isdigit(c) || c - '0' >= base) return false;
        } else {
            // ����16���ƣ�����A-F
            if (!isdigit(c) && (c < 'A' || c >= 'A' + base - 10)) return false;
        }
    }
    return true;
}

// �Զ�ʶ�������ַ����Ľ������ͣ���ת��Ϊʮ��������
// ������
//   input ���û�������ַ��������ܴ��н���ǰ׺��
//   value �����������ת�����ʮ��������
//   base  �����������ʶ�𵽵Ľ��ƣ�2/8/10/16��
// ����ֵ��
//   ���ת���ɹ�����true�����򷵻�false
// ˵����
//   - ����ǰ׺�жϽ������ͣ�0b/0BΪ�����ƣ�0x/0XΪʮ�����ƣ�0Ϊ�˽��ƣ�����Ϊʮ���ƣ���
//   - ��������Ƿ�Ϸ���ʹ��stoi���н���ת����
bool parseInput(const string& input, int& value, int& base) {
    string s = input;
    base = 10; // Ĭ��ʮ����
    // �ж�ǰ׺��ʶ�����
    if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'x')) {
        base = 16;
        s = s.substr(2); // ȥ��0x
    } else if (s.size() > 2 && s[0] == '0' && (tolower(s[1]) == 'b')) {
        base = 2;
        s = s.substr(2); // ȥ��0b
    } else if (s.size() > 1 && s[0] == '0') {
        base = 8;
        s = s.substr(1); // ȥ��0
    }
    // ����Ƿ�Ϸ�
    if (!isValidNumber(input, base)) return false;
    try {
        // �ַ���ת����
        value = std::stoi(s, nullptr, base);
    } catch (...) {
        return false;
    }
    return true;
}

// ��ʮ��������ת��Ϊָ�����Ƶ��ַ�����ʾ
// ������
//   value ��Ҫת����ʮ��������
//   base  ��Ŀ����ƣ�2/8/10/16��
// ����ֵ��
//   ����׼ǰ׺��Ŀ������ַ�������0b, 0, 0x��
// ˵����
//   - �����������0b��ͷ���˽�����0��ͷ��ʮ��������0x��ͷ��ʮ����ֱ��������֡�
//   - ֧�ָ��������޷��ŷ�ʽ������
string toBase(int value, int base) {
    if (base == 10) return to_string(value); // ʮ����ֱ�ӷ���
    string result;
    unsigned int uvalue = static_cast<unsigned int>(value); // ������ʱ���޷���ת��
    if (base == 2) {
        result = "0b"; // ������ǰ׺
        string bin;
        if (uvalue == 0) bin = "0";
        while (uvalue) {
            bin = char('0' + (uvalue % 2)) + bin;
            uvalue /= 2;
        }
        result += bin;
    } else if (base == 8) {
        result = "0"; // �˽���ǰ׺
        string oct;
        if (uvalue == 0) oct = "0";
        while (uvalue) {
            oct = char('0' + (uvalue % 8)) + oct;
            uvalue /= 8;
        }
        result += oct;
    } else if (base == 16) {
        result = "0x"; // ʮ������ǰ׺
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
        system("cls"); // ������Windows��
#else
        system("clear"); // ������Linux/Unix��
#endif
        cout << "===== ����ת���� =====" << endl;
        cout << "������һ����(֧�ֶ�����0b, �˽���0, ʮ����, ʮ������0xǰ׺):" << endl;
        string input;
        cin >> input;

        int value, base;
        // �������벢�ж��Ƿ�Ϸ�
        if (!parseInput(input, value, base)) {
            cout << "�����ʽ����" << endl;
        } else {
            // ��������Ʊ�ʾ
            cout << "�������Ϊ: " << input << endl;
            cout << "ʮ����: " << toBase(value, 10) << endl;
            cout << "������: " << toBase(value, 2) << endl;
            cout << "�˽���: " << toBase(value, 8) << endl;
            cout << "ʮ������: " << toBase(value, 16) << endl;
        }

        cout << "\n�Ƿ����ת��?(y/n): ";
        string choice;
        cin >> choice;
        if (choice != "y" && choice != "Y") break; // �˳�ѭ��
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
        - ��������ǰ׺�󣬼��ÿ���ַ��Ƿ��ںϷ���Χ�ڡ�

    2. parseInput(const string& input, int& value, int& base)
        - �Զ�ʶ�������ַ���input�Ľ������ͣ���ת��Ϊʮ��������value��
        - ʶ��0b��0x��0ǰ׺���ֱ��Ӧ�����ơ�ʮ�����ơ��˽��ơ�
        - ����ʶ�𵽵Ľ���base��
        - ������Ƿ�������false��

    3. toBase(int value, int base)
        - ��ʮ��������valueת��Ϊָ������(base)���ַ�����ʾ��
        - ������б�׼ǰ׺(��0b, 0, 0x)�ĸ�ʽ��
        - ֧�ָ�����ת�������޷��ŷ�ʽ������

    ʹ��˵��:
    - ���г����������Ҫת�������֣�֧��0b��0��0xǰ׺����
    - �������������ֵ�ʮ���ơ������ơ��˽��ơ�ʮ�����Ʊ�ʾ��
    - ��ѡ���Ƿ����������һ��ת����

    ע������:
    - �����ʽ����϶�Ӧ���ƵĺϷ��ַ���Χ��
    - ����Ƿ�ʱ����ʾ������Ϣ��
    - ��֧�������Ľ���ת������֧��С����
*/
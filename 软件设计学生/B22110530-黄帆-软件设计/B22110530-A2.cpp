// 2. ���ֳ���10�֣�
//
// �������һ�ַ�����ÿ�β������ַ������ݡ����ȶ���ͬ��
// ���ݽ�������ַ������ж������Ƿ���ȷ�������ȷ�ʣ�
// ��������������档

#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <windows.h>
#include <algorithm>

// ��������ַ���
// ������minLen - ��С���ȣ�maxLen - ��󳤶�
// ����ֵ�����ɵ�����ַ���
std::string generateRandomString(int minLen = 5, int maxLen = 10) {
    static const char charset[] =
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"; // �ַ�����Сд��ĸ����д��ĸ������
    int len = minLen + rand() % (maxLen - minLen + 1); // ��������ַ�������
    std::string result;
    for (int i = 0; i < len; ++i) {
        result += charset[rand() % (sizeof(charset) - 1)]; // ���ѡ���ַ�
    }
    return result;
}

// ������ȷ��
// ������target - Ŀ���ַ�����input - �û������ַ���
// ����ֵ����ȷ�ʣ��ٷֱȣ�
double calcAccuracy(const std::string& target, const std::string& input) {
    int correct = 0; // ��ȷ�ַ�����
    int minLen = std::min(target.size(), input.size()); // ȡ���߽϶̳���
    for (int i = 0; i < minLen; ++i) {
        if (target[i] == input[i]) ++correct; // ���ַ��Ƚϣ�ͳ����ȷ��
    }
    return 100.0 * correct / target.size(); // ��ȷ��=��ȷ�ַ���/Ŀ���ַ�������
}

int main() {
    srand((unsigned)time(0)); // ��ʼ�����������
    std::string randomStr = generateRandomString(); // ��������ַ���
    std::string userInput;

    // ����̨����
    std::cout << "===== ����ַ���������� =====" << std::endl;
    std::cout << "������·�����ַ����������ݣ�" << std::endl;
    std::cout << randomStr << std::endl; // ��ʾ����ַ���
    std::cout << "�����룺";
    std::getline(std::cin, userInput); // ��ȡ�û�����

    double accuracy = calcAccuracy(randomStr, userInput); // ������ȷ��
    std::cout << "���������ȷ��Ϊ��" << accuracy << "%" << std::endl;

    // system("pause"); // ��ѡ����ͣ����
    return 0;
}

/*
    ���ֳ���

    ����������
    �ó�����������һ���ַ��������ݺͳ��Ⱦ��������Ҫ���û�������ʾ���ַ����������ݣ�
    ���ж��û��������ȷ�ʣ���������ȷ�ʽ����������м򵥵�����������档

    ��Ҫ����ģ�飺
    1. ����ַ������ɣ�generateRandomString����
        - ������ɳ�����[minLen, maxLen]��Χ�ڵ��ַ������ַ���������Сд��ĸ�����֡�
    2. ��ȷ�ʼ��㣨calcAccuracy����
        - �Ƚ�Ŀ���ַ������û������ַ�����ÿ���ַ���ͳ��������ȷ���ַ�������������ȷ�ʣ���Ŀ���ַ�������Ϊ��׼����
    3. ����̨�������棨main����
        - ��ʾ����ַ����������û����룬������ȷ�ʼ��㺯������������

    ʹ��˵����
    - ���г������Ļ����ʾһ������ַ�����
    - �û����ڿ���̨������ַ������س���
    - ���������û��������ȷ�ʰٷֱȡ�

    ע�����
    - �ַ������Ⱥ�����ÿ�����о���ͬ��
    - ��ȷ����Ŀ���ַ�������Ϊ��׼������������ֲ�������ȷ�ʡ�
    - ����֧��C++��׼���Windowsͷ�ļ��Ļ����±������С�
*/
// 4. ���ܣ�10�֣�
//
// ��������һ�γ���Ϊ n ������ M���Լ���Կ K��
// ���ݹ�ʽ `Ci = mi + K`��i = 0,1,��,n-1��K Ϊ��Կ������ת��Ϊ���� C��
// ��������������档

#include <iostream>
#include <string>

int main() {
    std::string plaintext, ciphertext = ""; // plaintext�洢���ģ�ciphertext�洢����
    int key; // ��Կ

    // ��ʾ�û���������
    std::cout << "����������: ";
    std::getline(std::cin, plaintext); // ��ȡ�������ģ������ո�

    // ��ʾ�û�������Կ
    std::cout << "��������Կ (����): ";
    std::cin >> key; // ��ȡ��Կ

    // ���������е�ÿ���ַ�
    for (char ch : plaintext) {
        // ��ÿ���ַ���ASCIIֵ������Կ���õ����ܺ���ַ�
        ciphertext += static_cast<char>(ch + key);
    }

    // ������ܺ������
    std::cout << "���ܺ������Ϊ: " << ciphertext << std::endl;

    return 0; // ������������
}

/**
 * @brief ��������ʵ�ּ򵥵Ŀ��������㷨��
 *
 * �����������£�
 * 1. ��ʾ�û����������ַ�����
 * 2. ��ʾ�û�����һ��������Ϊ��Կ��
 * 3. �������е�ÿ���ַ�������ASCIIֵ������Կ���������ġ�
 * 4. ������ܺ�����ġ�
 *
 * @return int ����ִ��״̬�룬������������0��
 */
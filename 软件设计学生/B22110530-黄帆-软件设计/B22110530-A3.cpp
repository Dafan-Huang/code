// 3. �ı��༭����10�֣�
//
// �༭�ı���
// ���桢��ָ��λ�õ��ı��ļ���
// ��������������档

#include <iostream>
#include <fstream>
#include <string>

#ifdef _WIN32
#include <windows.h>
#else
#include <cstdlib>
#endif

//  ��ʾ���˵�����ʾ�û�ѡ�������
void showMenu() {
    std::cout << "\n--- �ı��༭�� ---\n";
    std::cout << "1. �༭�ı�\n";
    std::cout << "2. �����ı����ļ�\n";
    std::cout << "3. ���ļ�\n";
    std::cout << "4. ��ʾ��ǰ�ı�\n";
    std::cout << "0. �˳�\n";
    std::cout << "��ѡ�����: ";
}

// �������������ݲ���ϵͳ���ò�ͬ���������
void clearScreen() {
#ifdef _WIN32
    system("cls"); // Windows������
#else
    system("clear"); // Linux/Unix������
#endif
}

//  �༭�ı����ݣ��û����������ݣ�����END������
//  text ���ã��洢��ǰ�ı����ݣ����������ݸ��ǡ�
void editText(std::string &text) {
    std::cout << "��ǰ�ı��������£�\n";
    std::cout << text;
    std::cout << "�������µ��ı�����(���뵥��һ��END����,������ԭ����):\n";
    std::string newText, line;
    while (true) {
        std::getline(std::cin, line); // ���ж�ȡ�û�����
        if (line == "END") break;     // ����END�����༭
        newText += line + "\n";       // ƴ��������
    }
    text = newText; // �������ݸ���ԭ����
}

//  ����ǰ�ı����ݱ��浽ָ���ļ���
//  text ��ǰ�ı����ݡ�
void saveToFile(const std::string &text) {
    std::string filename;
    std::cout << "������Ҫ������ļ�·��: ";
    std::getline(std::cin, filename); // ��ȡ�ļ�·��
    std::ofstream ofs(filename);      // ������ļ���
    if (ofs) {
        ofs << text;                  // д���ı�����
        ofs.close();                  // �ر��ļ�
        std::cout << "����ɹ���\n";
    } else {
        std::cout << "����ʧ�ܡ�\n";  // �ļ���ʧ��
    }
}

// ��ָ���ļ���ȡ�ı����ݣ����ǵ�ǰ���ݡ�
// text ���ã��洢��ȡ�����ı����ݡ�

void openFromFile(std::string &text) {
    std::string filename;
    std::cout << "������Ҫ�򿪵��ļ�·��: ";
    std::getline(std::cin, filename); // ��ȡ�ļ�·��
    std::ifstream ifs(filename);      // �������ļ���
    if (ifs) {
        text.clear();                 // ��յ�ǰ����
        std::string line;
        while (std::getline(ifs, line)) {
            text += line + "\n";      // ���ж�ȡ��ƴ��
        }
        ifs.close();                  // �ر��ļ�
        std::cout << "�򿪳ɹ���\n";
    } else {
        std::cout << "��ʧ�ܡ�\n";  // �ļ���ʧ��
    }
}


// ��ʾ��ǰ�ı����ݡ�
// text ��ǰ�ı����ݡ�
void showText(const std::string &text) {
    std::cout << "\n--- ��ǰ�ı� ---\n";
    std::cout << text << "\n";
}

/**
 * �������������ṩһ�����ڲ˵����ı��༭�����档
 *
 * ��ѭ������ʾ�˵����ȴ��û��������ѡ������û�ѡ�������Ӧ�Ĺ��ܺ�����
 * - 1: �༭�ı���editText��
 * - 2: �����ı����ļ���saveToFile��
 * - 3: ���ļ����ı���openFromFile��
 * - 4: ��ʾ��ǰ�ı����ݣ�showText��
 * - 0: �˳�����
 *
 * ��������ֻ���Чѡ��ʱ����ʾ�û��������롣
 * ÿ�β������������clearScreen������������ʾ�ı����ݡ�
 *
 * int �����˳�״̬�루�����˳�����0��
 */
int main() {
    std::string text; // �洢��ǰ�ı�����
    int choice;       // �û��˵�ѡ��
    while (true) {
        showMenu();   // ��ʾ�˵�
        std::string input;
        std::getline(std::cin, input); // ��ȡ�û�����
        if (input.empty()) continue;   // ����Ϊ������������
        try {
            choice = std::stoi(input); // ת��Ϊ����
        } catch (...) {
            std::cout << "��������Ч�����֡�\n";
            continue;
        }
        switch (choice) {
            case 1:
                editText(text);        // �༭�ı�
                clearScreen();         // ����
                break;
            case 2:
                saveToFile(text);      // �����ı�
                clearScreen();         // ����
                break;
            case 3:
                openFromFile(text);    // ���ļ�
                clearScreen();         // ����
                break;
            case 4:
                showText(text);        // ��ʾ�ı�
                break;
            case 0:
                std::cout << "�˳�����\n";
                return 0;              // �˳�
            default:
                std::cout << "��Чѡ�������ԡ�\n";
        }
    }
    return 0;
}
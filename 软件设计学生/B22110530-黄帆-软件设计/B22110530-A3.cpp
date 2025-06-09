// 3. �ı��༭����10�֣�

// �༭�ı���
// ���桢��ָ��λ�õ��ı��ļ���
// ��������������档

#include <iostream>
#include <fstream>
#include <string>

void showMenu() {
    std::cout << "\n--- �ı��༭�� ---\n";
    std::cout << "1. �༭�ı�\n";
    std::cout << "2. �����ı����ļ�\n";
    std::cout << "3. ���ļ�\n";
    std::cout << "4. ��ʾ��ǰ�ı�\n";
    std::cout << "0. �˳�\n";
    std::cout << "��ѡ�����: ";
}

void editText(std::string &text) {
    std::cout << "�������ı�(���뵥��һ��END����):\n";
    text.clear();
    std::string line;
    while (true) {
        std::getline(std::cin, line);
        if (line == "END") break;
        text += line + "\n";
    }
}

void saveToFile(const std::string &text) {
    std::string filename;
    std::cout << "������Ҫ������ļ�·��: ";
    std::getline(std::cin, filename);
    std::ofstream ofs(filename);
    if (ofs) {
        ofs << text;
        ofs.close();
        std::cout << "����ɹ���\n";
    } else {
        std::cout << "����ʧ�ܡ�\n";
    }
}

void openFromFile(std::string &text) {
    std::string filename;
    std::cout << "������Ҫ�򿪵��ļ�·��: ";
    std::getline(std::cin, filename);
    std::ifstream ifs(filename);
    if (ifs) {
        text.clear();
        std::string line;
        while (std::getline(ifs, line)) {
            text += line + "\n";
        }
        ifs.close();
        std::cout << "�򿪳ɹ���\n";
    } else {
        std::cout << "��ʧ�ܡ�\n";
    }
}

void showText(const std::string &text) {
    std::cout << "\n--- ��ǰ�ı� ---\n";
    std::cout << text << "\n";
}

#ifdef _WIN32
#include <windows.h>
#else
#include <cstdlib>
#endif

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}


int main() {
    std::string text;
    int choice;
    while (true) {
        showMenu();
        std::string input;
        std::getline(std::cin, input);
        if (input.empty()) continue;
        try {
            choice = std::stoi(input);
        } catch (...) {
            std::cout << "��������Ч�����֡�\n";
            continue;
        }
        switch (choice) {
            case 1:
                editText(text);
                clearScreen();
                break;
            case 2:
                saveToFile(text);
                clearScreen();
                break;
            case 3:
                openFromFile(text);
                clearScreen();
                break;
            case 4:
                showText(text);
                break;
            case 0:
                std::cout << "�˳�����\n";
                return 0;
            default:
                std::cout << "��Чѡ�������ԡ�\n";
        }
    }
    return 0;
}

/**
 * @brief �������������ṩһ�����ڲ˵����ı��༭�����档
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
 * @return int �����˳�״̬�루�����˳�����0��
 */
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
    std::cout << "�������ı������뵥��һ��END��������\n";
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

int main() {
    std::string text;
    int choice;
    while (true) {
        showMenu();
        std::string input;
        std::getline(std::cin, input);
        if (input.empty()) continue;
        choice = std::stoi(input);
        switch (choice) {
            case 1:
                editText(text);
                break;
            case 2:
                saveToFile(text);
                break;
            case 3:
                openFromFile(text);
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
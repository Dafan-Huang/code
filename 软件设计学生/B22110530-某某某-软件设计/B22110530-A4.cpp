#include <iostream>
#include <string>

int main() {
    std::string plaintext, ciphertext = "";
    int key;

    std::cout << "����������: ";
    std::getline(std::cin, plaintext);

    std::cout << "��������Կ (����): ";
    std::cin >> key;

    for (char ch : plaintext) {
        ciphertext += static_cast<char>(ch + key);
    }

    std::cout << "���ܺ������Ϊ: " << ciphertext << std::endl;

    return 0;
}
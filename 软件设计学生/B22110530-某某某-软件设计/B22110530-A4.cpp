#include <iostream>
#include <string>

int main() {
    std::string plaintext, ciphertext = "";
    int key;

    std::cout << "请输入明文: ";
    std::getline(std::cin, plaintext);

    std::cout << "请输入密钥 (整数): ";
    std::cin >> key;

    for (char ch : plaintext) {
        ciphertext += static_cast<char>(ch + key);
    }

    std::cout << "加密后的密文为: " << ciphertext << std::endl;

    return 0;
}
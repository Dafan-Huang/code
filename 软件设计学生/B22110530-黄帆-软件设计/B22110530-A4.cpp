// 4. 加密（10分）

// 输入任意一段长度为 n 的明文 M，以及密钥 K；
// 根据公式 `Ci = mi + K`（i = 0,1,…,n-1，K 为密钥）将其转换为密文 C；
// 具有输入输出界面。

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
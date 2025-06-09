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

/**
 * @brief 主函数，实现简单的凯撒加密算法。
 *
 * 程序流程如下：
 * 1. 提示用户输入明文字符串。
 * 2. 提示用户输入一个整数作为密钥。
 * 3. 对明文中的每个字符，将其ASCII值加上密钥，生成密文。
 * 4. 输出加密后的密文。
 *
 * @return int 程序执行状态码，正常结束返回0。
 */
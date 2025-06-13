#include <iostream>
#include <string>

// 模拟 Office 功能的类
class Office {
public:
    Office(const std::string& name) : officeName(name) {}

    void addDocument(const std::string& doc) {
        documents.push_back(doc);
        std::cout << "已添加文档: " << doc << std::endl;
    }

    void listDocuments() const {
        std::cout << officeName << " 的文档列表:" << std::endl;
        for (const auto& doc : documents) {
            std::cout << "- " << doc << std::endl;
        }
    }

private:
    std::string officeName;
    std::vector<std::string> documents;
};

int main() {
    Office myOffice("测试Office");

    myOffice.addDocument("报告.docx");
    myOffice.addDocument("数据表.xlsx");
    myOffice.addDocument("演示文稿.pptx");

    myOffice.listDocuments();

    return 0;
}
#include <iostream>
#include <string>
#include <vector>

// 需要安装并链接 OpenXLSX 库: https://github.com/troldal/OpenXLSX
#include "OpenXLSX.hpp"

int main() {
    std::string filePath = "test.xlsx"; // Excel 文件路径
    try {
        OpenXLSX::XLDocument doc;
        doc.open(filePath);

        auto wks = doc.workbook().worksheet("Sheet1"); // 读取第一个工作表
        auto dims = wks.dimensions();
        int rowCount = dims.rowCount();
        int colCount = dims.colCount();

        std::cout << "Excel内容如下：" << std::endl;
        for (int row = 1; row <= rowCount; ++row) {
            for (int col = 1; col <= colCount; ++col) {
                auto cell = wks.cell(OpenXLSX::XLCellReference(row, col));
                std::cout << cell.value().asString() << "\t";
            }
            std::cout << std::endl;
        }
        doc.close();
    } catch (const std::exception& ex) {
        std::cerr << "读取Excel文件失败: " << ex.what() << std::endl;
    }
    return 0;
}
#include <iostream>
#include <comdef.h>
#include <comutil.h>
#include <windows.h>
#import "C:\\Program Files\\Microsoft Office\\root\\Office16\\MSPPT.OLB" rename_namespace("PPT"), named_guids

int main() {
    HRESULT hr = CoInitialize(NULL);
    if (FAILED(hr)) {
        std::cout << "COM初始化失败" << std::endl;
        return -1;
    }

    try {
        PPT::ApplicationPtr pptApp;
        hr = pptApp.CreateInstance(__uuidof(PPT::Application));
        if (FAILED(hr)) {
            std::cout << "无法启动PowerPoint应用程序" << std::endl;
            CoUninitialize();
            return -1;
        }

        pptApp->Visible = msoTrue;

        PPT::PresentationsPtr presentations = pptApp->Presentations;
        PPT::PresentationPtr presentation = presentations->Add(msoTrue);

        PPT::SlidesPtr slides = presentation->Slides;

        // 添加第1页
        PPT::SlidePtr slide1 = slides->Add(1, PPT::PpSlideLayout::ppLayoutText);
        slide1->Shapes->Item(1)->TextFrame->TextRange->Text = _bstr_t(L"Hello, PowerPoint!");
        slide1->Shapes->Item(2)->TextFrame->TextRange->Text = _bstr_t(L"这是第1页内容。");

        // 添加第2页
        PPT::SlidePtr slide2 = slides->Add(2, PPT::PpSlideLayout::ppLayoutText);
        slide2->Shapes->Item(1)->TextFrame->TextRange->Text = _bstr_t(L"第二页标题");
        slide2->Shapes->Item(2)->TextFrame->TextRange->Text = _bstr_t(L"这是第2页内容。");

        // 添加第3页
        PPT::SlidePtr slide3 = slides->Add(3, PPT::PpSlideLayout::ppLayoutText);
        slide3->Shapes->Item(1)->TextFrame->TextRange->Text = _bstr_t(L"第三页标题");
        slide3->Shapes->Item(2)->TextFrame->TextRange->Text = _bstr_t(L"这是第3页内容。");

        // 保存
        _bstr_t filePath = L"C:\\Users\\24096\\Desktop\\code\\office\\test.pptx";
        presentation->SaveAs(filePath);

        // 读取所有幻灯片内容
        PPT::PresentationPtr openedPresentation = presentations->Open(filePath, msoFalse, msoFalse, msoFalse);
        PPT::SlidesPtr openedSlides = openedPresentation->Slides;
        long slideCount = openedSlides->Count;
        for (long i = 1; i <= slideCount; ++i) {
            PPT::SlidePtr openedSlide = openedSlides->Item(i);
            std::wcout << L"第" << i << L"页 标题: "
                << (wchar_t*)openedSlide->Shapes->Item(1)->TextFrame->TextRange->Text << std::endl;
            std::wcout << L"第" << i << L"页 内容: "
                << (wchar_t*)openedSlide->Shapes->Item(2)->TextFrame->TextRange->Text << std::endl;
        }

        openedPresentation->Close();
        presentation->Close();
        pptApp->Quit();
    } catch (_com_error &e) {
        std::wcout << L"COM错误: " << e.ErrorMessage() << std::endl;
        std::wcout << L"详细信息: " << (wchar_t*)e.Description() << std::endl;
    }

    CoUninitialize();
    return 0;
}
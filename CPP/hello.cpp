#include <iostream>
using namespace std;

/**
 * @brief 打印Hello World
 */
void printHelloWorld();

/**
 * @brief 绘制爱心
 */
void drawLove();

int main()
{
    printHelloWorld();
    drawLove();
    return 0;
}

void printHelloWorld()
{
    cout << "Hello World!" << endl;
}

// 绘制爱心
void drawLove()
{
    cout << "    **    **" << endl;
    cout << " *******" << endl;
    cout << "  *****" << endl;
    cout << "   ***" << endl;
    cout << "    *" << endl;
}

```

### 2.2 编译

```shell
g++ hello.cpp -o hello
```

### 2.3 运行

```shell
./hello
```

### 2.4 输出

```shell
Hello World!
    **    **
 *******
  *****
   ***
    *
    * 
    * 
    * 
    * 
    * 
    * 
    * 
    * 
    * 

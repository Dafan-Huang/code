function ga
    % 1. 定义适应度函数
    function f = fitness(x)
        f = sin(x)+cos(x);
    end

    % 2. 初始化种群参数和范围
    options = gaoptimset('Generations', 100, 'PopulationSize',50); % 设定遗传算法的配置
    nvars = 1; % 设定决策变量的个数
    lb = 0;    % 定义决策变量的下限
    ub = 10;   % 定义决策变量的上限

    % 3. 运行遗传算法
    [x, fval] = ga(@fitness, nvars, [], [], [], [], lb, ub, [], [], options);

    % 4. 输出结果和画图
    fprintf('The optimal value of x is: %f\n', x);
    fprintf('The optimal value of the function is: %f\n', -fval);

    x_plot = linspace(lb, ub, 500); % 生成用于画图的横轴数据
    y_plot = sin(x_plot)+cos(x_plot); % 计算用于画图的纵轴数据
    plot(x_plot, y_plot, '-b', 'LineWidth', 2) % 画目标函数图像
    hold on
    plot(x, -fval, '*r', 'MarkerSize', 10) % 标出最优解对应的点
    xlabel('x')
    ylabel('f(x)=-exp(x)+xln(x)')
    title('Minimum of -exp(x)+xln(x) using GA')
end

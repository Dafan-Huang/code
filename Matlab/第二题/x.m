numGenerations = 20; % 世代数量

% % 设置向量长度
% n = 3;
% % 生成随机向量
% vec = rand(1, n);
% % 将向量元素归一化，使其和为1
% vec = vec / sum(vec);

genotypeFreq = zeros(numGenerations, 3); % 保存每个世代的基因型频率
initialGenotypeFreq = [0.2 0.6 0.2]; % 初始基因型频率 [AA, Aa, aa]
genotypeFreq(1, :) = initialGenotypeFreq;



% 迭代模拟每个世代的基因型频率变化
for gen = 2:numGenerations
    AA = genotypeFreq(gen-1, 1)^2+genotypeFreq(gen-1, 1)*genotypeFreq(gen-1, 2)+1/4*genotypeFreq(gen-1, 2)^2
    Aa = genotypeFreq(gen-1, 1)*genotypeFreq(gen-1, 2)+2*genotypeFreq(gen-1, 1)*genotypeFreq(gen-1, 3)+1/2*genotypeFreq(gen-1, 2)^2+genotypeFreq(gen-1, 2)*genotypeFreq(gen-1, 3)
    aa = genotypeFreq(gen-1, 3)^2+genotypeFreq(gen-1, 3)*genotypeFreq(gen-1, 2)+1/4*genotypeFreq(gen-1, 2)^2
    
    singma = 0.01;
    t=singma*randn(1,1);
    
    AA = AA + t;
    Aa = Aa - t;
    aa = aa ;

    genotypeFreq(gen,:) = [AA, Aa, aa];

end

% 绘制基因型频率随世代变化的图像
figure;
plot(1:numGenerations, genotypeFreq(:, 1), 'r-', 'LineWidth', 2); hold on;
plot(1:numGenerations, genotypeFreq(:, 2), 'g-', 'LineWidth', 2);
plot(1:numGenerations, genotypeFreq(:, 3), 'b-', 'LineWidth', 2);
legend('AA', 'Aa', 'aa');
xlabel('世代');
ylabel('基因型频率');
title('基因型频率随世代变化');

finalGenotypeFreq = genotypeFreq(end, :)
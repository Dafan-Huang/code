numGenerations = 10; % 世代数量
genotypeFreq = zeros(numGenerations, 3); % 保存每个世代的基因型频率
initialGenotypeFreq = [0.2, 0.6, 0.2]; % 初始基因型频率 [AA, Aa, aa]
genotypeFreq(1, :) = initialGenotypeFreq;
singma=0.01;
t=random('Normal',0.5,singma,1,10);
% 迭代模拟每个世代的基因型频率变化
for gen = 2:numGenerations
    AA = (genotypeFreq(gen-1, 1)+1/2*genotypeFreq(gen-1, 2))^2
    Aa = 2*(genotypeFreq(gen-1, 1)+1/2*genotypeFreq(gen-1, 2))*(genotypeFreq(gen-1, 3)+1/2*genotypeFreq(gen-1, 2))
    aa = (genotypeFreq(gen-1, 3)+1/2*genotypeFreq(gen-1, 2))^2

    genotypeFreq(gen, 1) = AA;
    genotypeFreq(gen, 2) = Aa;
    genotypeFreq(gen, 3) = aa;
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
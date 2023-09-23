 % 设置初始参数
 populationSize = 1000; % 种群大小
 numGenerations = 10; % 世代数量
 initialGenotypeFreq = [0.2, 0.6, 0.2]; % 初始基因型频率 [AA, Aa, aa]
 
 % 模拟哈迪-温伯格定律
 genotypeFreq = zeros(numGenerations, 3); % 保存每个世代的基因型频率
 
 % 第一代的基因型频率为初始频率
 genotypeFreq(1, :) = initialGenotypeFreq;
 
 % 迭代模拟每个世代的基因型频率变化
 for gen = 2:numGenerations
     % 随机进行交配和基因重组
     offspring = reshape(randsample(1:populationSize, populationSize, true, genotypeFreq(gen-1, :)), [], 2);
 
     % 统计每个基因型的数量
     AA_count = sum(all(offspring == 1, 2));
     Aa_count = sum(sum(offspring == 1, 2) == 1);
     aa_count = sum(all(offspring == 3, 2));
 
     % 计算下一代的基因型频率
     genotypeFreq(gen, :) = [AA_count, Aa_count, aa_count] / (2 * populationSize);
 end
 
 % 绘制基因型频率随世代变化的曲线图
 figure;
 plot(1:numGenerations, genotypeFreq(:, 1), 'r-', 'LineWidth', 2); hold on;
 plot(1:numGenerations, genotypeFreq(:, 2), 'g-', 'LineWidth', 2);
 plot(1:numGenerations, genotypeFreq(:, 3), 'b-', 'LineWidth', 2);
 legend('AA', 'Aa', 'aa');
 xlabel('世代');
 ylabel('基因型频率');
 title('基因型频率随世代变化');
 
 % 输出最终稳定的基因型频率
 finalGenotypeFreq = genotypeFreq(end, :)
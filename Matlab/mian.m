%%%%%遗传算法%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%
%%参数设置
inn=50;  %初始种群规模
gnmax=1000;   %最大迭代数
pmutation=0.1;  %变异概率
pcross=0.7;%交叉概率
lenchrom=1;  %染色体长度，因为我们要求的解的个数为2

acc=-3;%需要的精度，小数点后2位，配合roundn函数使用
bound=[min(min(x),min(y)),max(max(x),max(y))]; %染色体的边界值

disp('--------遗传算法开始计算----------');
tic;  %计时

%产生初始种群
s=chushi(inn,lenchrom,bound,acc);

bestpop=[ ];  %适应度值最好的染色体

for gn=1:gnmax
    f=objf(s);%f是行向量   
    f=f';
    minf1(gn)=min(f);  %每次迭代的最小成本
    [xx,yy]=find(f==min(minf1(gn)));%找最优
    bestpop(gn,:)=s(xx(1),:);%当代最优染色体
    
    [ii,jj]=sort(f);  %对适应度函数进行排序

    finv=ranking(f);
    selch=select('sus',s,finv);%选择操作
    
    for j=1:inn
        s_cross=Cross(selch,inn,lenchrom,pcross,acc); %交叉
    end
    for j=1:inn
        s_mutation=mutation(s_cross,inn,lenchrom,pmutation,gn,gnmax,bound,acc); %变异  
    end
    
    s=s_mutation;

end

runtime=toc;
minf=min(minf1(1));
[xx1,yy1]=min(minf1);%找最优
bestpop1=bestpop(yy1(1),:);%最优染色体

figure(1);
plot(minf1,'-*');%画种群进化图
set(gca,'xlim',[1,gn+1]);
title('遗传算法收敛图')
xlabel('染色体种群进化代数');
ylabel('每一代种群的适应度值');
legend('最优值的变化');
disp(['最优选址坐标：',num2str(bestpop1)]);
disp(['最小成本：',num2str(minf)]);
disp(['计算时间：',num2str(runtime),'秒.']);
disp('--------遗传算法结束计算----------');

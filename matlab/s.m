function s=f(x)
    m=2;n=floor(x/2);s=[];
    while isempty(s) && m<=n
        if isprime(m) && isprime(x-m)
            s=[m,x-m];
        end
        m=m+1;
    end

f=inline('x^2+y^2');f(1,2)

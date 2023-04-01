means = [0, 0, 0]  
loan = 0
rate = 0
pay = 0
investment = 0
annual_rate = 0


# ���㶨ͶԤ������
# ��Ͷ����ļ��㹫ʽΪ��M=a(1+x)[-1+(1+x)^n]/x;
# ����M����Ԥ�����棬a����ÿ�ڶ�Ͷ��x���������ʣ���n����Ͷ������
# �����û�ÿ�¶�Ͷ���Ϊ300Ԫ��һ��Ҳ����3600Ԫ����������Ϊ15%��
# ��Ͷ����Ϊ35�꣬����Լ��������Ϊ3600(1+15%)[-1+(1+15%)^35]/15%=3648044Ԫ��
def fixed_investment(inv, a_rate, y):
    global means
    inv = 12 * inv
    a_rate = a_rate / 100
    if a_rate == 0:
        expected = 0
    else:
        expected = inv * (1 + a_rate) * (pow((1 + a_rate), y) - 1) / a_rate
    print("��Ͷ��Ԥ������Ϊ: %.2f" % expected)
    means[1] = expected
    return expected


def balance():
    total = 0
    for i in means:
        total += i
    print("����ʲ��ܶ�Ϊ��%.2f" % total)
    print("����ʲ���ϸΪ��\n")
    print("��%.2f" % means[0])
    print("��ƣ�%.2f" % means[1])
    print("��ծ��%.2f" % means[2])


def saving(amount):
    global means
    if amount < 0:
        print("������С�� 0��")
    else:
        means[0] += amount
        print("�Ѵ�%.2f Ԫ" % amount)
        print("��ǰ��%.2f Ԫ" % means[0])


def draw_money(drawing):
    global means
    if drawing < 0:
        print("ȡ�����С�� 0��")
    elif drawing > means[0]:
        print("ȡ����ɳ�����")
    else:
        means[0] -= drawing
        print("��ȡ� %.2f Ԫ" % drawing)
        print("��ǰ�� %.2f Ԫ" % means[0])


def loans(loan, rate, pay, years):
    global means
    if pay < (loan - pay) * rate:
        print("���ǻ�����ģ�����")
    else:
        if years == 0:
            count = 0
            while loan > 0:
                loan -= pay
                loan *= (1 + rate)
                count += 1
            print("���� %d �������" % count)
        else:
            for _ in range(years):
                loan -= pay
                if loan == 0:
                    break
                else:
                    loan *= (1 + rate)
                    print("�����ڵĸ�ծ��: %.2f" % loan)
            # means[2] = loan
            return loan


# δ������״��
def future(years):
    income = fixed_investment(investment, annual_rate, years)
    debt = loans(loan, rate, pay, years)
    captial = means[0] + income - debt
    print("���%i������ʲ���: %.3f" % (years, captial))


def init():
    print()
    print('''����Ϊ�ɰ����ҵ��
        1. ��ѯ�ʲ�
        2. ���
        3. ȡ��
        4. ���㸴��
        5. �������
        6. ����δ���ʲ�
        q. �˳�''')


def main():
    init()
    while True:
        choice = input("��������Ҫ�����ҵ�����: ")
        #  ��ѯ���
        if choice == "1":
            balance()
        # ���
        elif choice == "2":
            inc = float(input("����������: "))
            saving(inc)
        # ȡ��
        elif choice == "3":
            dec = float(input("������ȡ����: "))
            draw_money(dec)
        # ���㶨Ͷ
        elif choice == "4":
            investment = float(input("������ÿ�¶�Ͷ���: "))
            annual_rate = float(input("��������������: "))
            years = int(input("�����붨Ͷ����(��): "))
            if investment <= 0 or annual_rate <= 0 or years <= 0:
                print("�������������")
            else:
                money = fixed_investment(investment, annual_rate, years)
            print("�����ջ�: %.2f Ԫ" % money)
        # �������
        elif choice == "5":
            loan = float(input("�����뵱ǰ����: "))
            rate = float(input("������������: "))
            pay = float(input("������ÿ�껹��: "))
            if loan <= 0 or rate <= 0 or pay <= 0:
                print("�������������")
            else:
                loans(loan, rate, pay, 0)
        elif choice == "6":
            years = int(input("ϣ����ѯ�������Ĳ���״��? "))
            future(years)
        # �˳�
        elif choice == "q":
            print("��ӭ�´ι��٣��ټ���")
            break
        else:
            print("�������ָ����������������\n")


if __name__ == '__main__':
    main()
# Author: melon
# CreatTime:2023/03/2023/3/15
# FileName：分期还款
# Description: focus on the code
a=[]
myhke = 0
def benxi():
    dkbj = float(input("请输入你的贷款本金"))
    yll = float(input("请输入你的月利率"))
    zhkys = int(input("请输入你的总还款月数"))
    zhkys1 = zhkys
    while(zhkys!=0):
            myhke = (dkbj*yll*((1+yll)**zhkys1))/(((1+yll)**zhkys1)-1)
            zhkys = zhkys-1
            a.append(myhke)
    print(a)
def benjin():
    dkbj = float(input("请输入你的贷款本金"))
    yll = float(input("请输入你的月利率"))
    zhkys = int(input("请输入你的总还款月数"))
    yhkys = 0
    zhkys1 = zhkys
    while(zhkys!=0):
            myhke = (dkbj/zhkys1)+(dkbj-(dkbj/zhkys1)*yhkys)*yll
            yhkys = yhkys + 1
            zhkys = zhkys -1
            a.append(myhke)
    print(a)
def main():
    hkfs = str(input("请输入你的还款方式"))
    if(hkfs=='AC'):
       benjin()
    elif(hkfs=='ACPI'):
       benxi()
    else:
       print("还款方式输入错误")
if __name__ =='__main__':
     main()

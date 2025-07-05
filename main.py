import re
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve, diff, sqrt, I, simplify
import numpy as np
import math
from matplotlib.widgets import Button

pmView = 5

def on_button_click():
    print("버튼이 눌렸습니다!")

def getAddr1(sDef) :
    # 일차함수 입력받을 경우, 좌표값 반환
    #반환값 : x절편과 y절편

    addrListX = []
    addrListY = []

    """"
    sDef[0] > 상수항
    sDef[1] > 일차항    
    """

    # 함수식 정의
    x = symbols('x') 
    fxDEF = sDef[0]+sDef[1]*x #일차식 생성

    # x1
    dy1 = fxDEF.subs(x, 0)  # x=0 대입
    addrListX.append(0)
    addrListY.append(dy1)

    # x2
    dy2 = fxDEF.subs(x, 1)  # x=1 대입
    addrListX.append(1)
    addrListY.append(dy2)
    
    return addrListX, addrListY

def is_imaginary(x):
    return isinstance(x, complex) and x.imag != 0

def getAddr(sDef) :
    print("{0}차 함수 그리기".format(len(sDef)-1))

    fxDEF = 0

    # make def
    x = symbols('x') 
    for i in range(len(sDef)) :
        fxDEF += sDef[i]*(x**i)

    print(fxDEF)

    # get silgeon + get Max solution
    solution = solve(Eq(fxDEF, 0), x)  # 방정식 풀기
    print(solution)
    solution = [simplify(e) for e in solution if simplify(e).as_real_imag()[1] == 0]
    print(solution)
    if len(solution) > 0 :
        Msol = 0
        for sol in solution :
            if Msol < abs(sol) :
                Msol = sol
    else :
        f_prime = diff(fxDEF, x)
        f_prime_solution = solve(Eq(f_prime, 0), x)  # 방정식 풀기
        Msol = 0
        for sol in f_prime_solution :
            if Msol < abs(sol) :
                Msol = sol

    # 미분해서 극값 구하기
    


    print(solution)
    print(Msol)

    xArray = np.arange(float(getRange(Msol, pmView)[0]), float(getRange(Msol, pmView)[1]), 0.1)
    yArray = []

    for xA in xArray :
        yArray.append(fxDEF.subs(x, xA))

    return xArray, yArray, Msol

def splitDef(sDef2) :
    max = 0
    maxfinder = []
    numfinder = []
    xfinder =[]
    cpsdef2 = []
    zero = 0

    sDef2 = sDef2.replace(' ','')
    sDef2 = re.split(r'([+-])',sDef2)
    if sDef2[0] == '':
        sDef2.remove('')

    #앞에 +가 없으면 +를 추가
    if sDef2[0] not in ['+','-']:
        sDef2.insert(0,'+')

    #각 항목이 x를 포함하지 않는 경우
    if not any('x' in List for List in sDef2):
        if len(sDef2) == 1:
            cpsdef2 = [int(sDef2[0])]
        else:
            cpsdef2 = [int(sDef2[0]+sDef2[1])]

    #각 항목이 x를 포함하는 경우
    else:
        #각 항목이 ^를 포함하지 않는 경우
        if not any('^' in List for List in sDef2):
            max = 1

        #각 항목이 ^를 포함하는 경우
        else:
            for i,enu in enumerate(sDef2): 
                if '^' in sDef2[i]:
                    maxfinder.append(sDef2[i].split('^')[1])
        #^가 없는 경우
        if max == 1:
            for i,enu in enumerate(sDef2):
                if 'x' in enu:
                    xfinder.append(i)
                elif not re.search(r'[+-]', enu):
                    numfinder.append(i)
            cpsdef2 = [float(sDef2[numfinder[0]-1]+sDef2[numfinder[0]]), float(sDef2[xfinder[0]].split('x')[0])]
        #^가 있는 경우
        else:
            maxfinder.sort()
            for i, enu in enumerate(sDef2):
                if 'x' in enu:
                    xfinder.append(i)
                elif not re.search(r'[+-]', enu):
                    numfinder.append(i)
            
            for i in range(int(maxfinder[0])):
                if i == 0:
                    for j, enu in enumerate(sDef2):
                        if enu[len(enu)-1] in 'x':
                            cpsdef2.append(float(sDef2[j-1]+sDef2[j].split('x')[0]))
                            zero =1
                    if zero == 0:
                        cpsdef2.append(0.0)
                else:
                    for j, enu in enumerate(sDef2):
                        if 'x^' + str(i+1) in enu:
                            cpsdef2.append(float(sDef2[j-1]+sDef2[j].split('x^'+str(i+1))[0]))
                            zero = 1
                    if zero ==0:
                        cpsdef2.append(0.0)
            cpsdef2.insert(0, float(sDef2[numfinder[0]-1]+sDef2[numfinder[0]]))
    return cpsdef2


def getRange(fMax, pm) :
    if fMax < 0 :
        return math.floor(fMax)-pm, -1*math.floor(fMax)+pm
    elif fMax >= 0 :
        return -1*math.ceil(fMax)-pm, math.ceil(fMax)+pm

# 화면 구성

Function = input("함수 식을 입력하세요: y = ")
print(splitDef(Function))
Addr = getAddr(splitDef(Function))
print(Addr)
xL = Addr[0]
yL = Addr[1]

xm = float(getRange(Addr[2], pmView)[0])
xM = float(getRange(Addr[2], pmView)[1])

print(type(xm), type(xM))

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # 버튼 공간 확보
ax.plot(xL, yL)

plt.title('hahaha')
ax.set_xlim(xm, xM)
ax.set_ylim(xm, xM)
# x, y축 눈금 간격을 1로 설정
ax.set_xticks(np.arange(xm, xM, 1))
ax.set_yticks(np.arange(xm, xM, 1))

ax.axhline(y=0, color='black', linewidth=1)
ax.axvline(x=0, color='black', linewidth=1)

ax.tick_params(axis='both', labelsize=4, labelcolor='blue')  # 크기 12, 파란색

button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])
btn = Button(button_ax, '눌러보세요')
btn.on_clicked(on_button_click)

plt.legend()
plt.grid(True)
plt.show()


#a = splitDef(Function)
#print(a)




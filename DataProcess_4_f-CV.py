'''=========================================================================
****************************************************************************
基于中科院苏州纳米所测试平台Keithley 4200的变频CV测试xls数据预处理脚本@@Powered by 徐法师@@
****************************************************************************
========================================================================='''



'''-------------------------------------------------------------
加载所需要的模块，运行前请采用pip或其他途径预先安装
-------------------------------------------------------------'''
#import csv
import glob
import pandas as pd
import xlrd
import math
import matplotlib.pyplot as plt
'''-----------------------------------------------------------'''


'''-------------------------------------------------------------
需要输入的参数
-------------------------------------------------------------'''
D_MIS = 20/1e7                                                                          #栅介质厚度，单位nm，此处除1e7后单位为cm
D_Barrier = 23/1e7                                                                      #势垒层厚度，单位nm，此处除1e7后单位为cm
Radius = 70/10000                                                                       #CV测试图形的半径（针对圆形），单位um，此处除10000后单位为cm
#Radius = float(input('请输入CV测试图形的半径(um):'))/10000
Temp = 300                                                                              #测试温度
Step2Condition = 3.4e-11                                                                #判定条件对应的电容值，单位F
'''-----------------------------------------------------------'''



'''-------------------------------------------------------------
提前定义或计算得到的参数
--------------------------------------------------------------'''
Vaccum_DielectricConstant = 8.854187817e-14                                             #真空介电常数
Al_composition = 0.23                                                                   #AlGaN势垒层Al组分
MIS_DielectricConstant = 9.4                                                            #介质介电常数，9.4 for pre-PDA-Al2O3，8.9 for post-PDA-Al2O3[1]
K = 8.6173324e-5                                                                        #玻尔兹曼常数
q = 1.602e-19                                                                           #电荷量
CaptureCrossSection = 1e-14                                                             #电子俘获截面[2]
Size = Radius*Radius*math.pi                                                            #math.pi是圆周率，此处计算CV测试图形的面积
Barrier_DielectricConstant = 8.9-(8.9-8.5)*Al_composition                               #计算得AlGaN势垒层介电常数,8.9 for GaN，8.5 for AlN
C_ox = MIS_DielectricConstant*Vaccum_DielectricConstant*Size/(D_MIS*Size)               #计算得介质层电容
C_AlGaN = Barrier_DielectricConstant*Vaccum_DielectricConstant*Size/(D_Barrier*Size)    #计算得势垒层电容
'''-----------------------------------------------------------'''

print('介质层单位面积电容为'+str(C_ox))
print('势垒层单位面积电容为'+str(C_AlGaN))

'''-------------------------------------------------------------
遍历文件和pandas模块打印参数设置
--------------------------------------------------------------'''
xlsx_list = glob.glob('*.xls')                                                          #利用glob工具遍历文件夹下全部的xls文件，所有的文件名合并为列表“xlsx_list”
print('总共发现%s个xls文件'% len(xlsx_list))                                            #打印列表“xlsx_list”的长度，即当前路径下的xls文件数目
pd.set_option('display.max_columns', None)                                              #取消列数显示限制
pd.set_option('display.max_rows', None)                                                 #取消行数显示限制
'''-----------------------------------------------------------'''



'''-------------------------------------------------------------
先行定义所有使用到的列表
-------------------------------------------------------------'''
getData_xls = []
getParam_xls = []
getC_pd = []
getV_pd = []
i = 0
j = 0
k = 0
num = []
col = []
Freq = []
Freq_sort = []
Von = []
delta_Edis = []
delta_Von = []
Dit = []

'''-----------------------------------------------------------'''



'''-------------------------------------------------------------
数据合并整理部分
-------------------------------------------------------------'''

#------------将xls文件按照测试频率从低到高进行排序-----------
for i in range(len(xlsx_list)):
    getParam_xls.append(pd.read_excel(xlsx_list[i],sheet_name='Settings'))              #通过pd.read_excel模块和xlrd模块将第j个xls文件的Settings页转换为pd数据格式，并扩展给getParam_xls变量
    num.append(0)                                                                       #num列表第j位置赋0
    while str(getParam_xls[i].iat[num[i],0]) != 'Frequency':                            #判断getParam_xls中Frequency所在的行数                                                             
        num[i] += 1
    Freq.append(float(getParam_xls[i].iat[num[j],3]))                                   #得到测试频率

df = pd.DataFrame({'FileName':xlsx_list,'Frequency':Freq})                              #将文件名和对应的测试频率合并为Pandas的DataFrame格式
df_sort = df.sort_values('Frequency')                                                   #将文件名按照频率从小到大排列
df_sort.reset_index(drop=True,inplace=True)                                             #更新索引



for j in range(len(xlsx_list)):                                                         #循环体条件，遍历xlsx_list列表中的每个xls文件
    print(df_sort['FileName'][j])                                                       #打印当前循环体到达的文件位置

    getData_xls.append(pd.read_excel(df_sort['FileName'][j],sheet_name='Data'))         #通过pd.read_excel模块和xlrd模块将按照频率排序后第j个xls文件的Data页转换为pd数据格式，并扩展给getData_xls变量
    getC_pd.append(getData_xls[j].loc[:,'C'])                                           #获取电容数据，添加到get_pd列表中(缺省)
#    getC_pd.append(abs(getData_xls[j].loc[:,'C']))                                     #测试电容值取绝对值（optional）
    getV_pd.append(getData_xls[j].loc[:,'V'])                                           #获取电压数据
    
    
    col.append(0)
    while getC_pd[j][col[j]] < Step2Condition:                                          #当电容值大于第二个台阶出现的判定条件时，输出该电容所在的行数
        col[j] += 1
    Von.append(getV_pd[j][col[j]])                                                      #利用所得到的行数，输出第二个台阶的开启电压Von
    Freq_sort.append(df_sort['Frequency'][j])                                           #排序后的频率

#    deltaE.append(K*Temp*math.log())

    

print('频率为'+str(Freq_sort))
print('开启电压为'+str(Von))

for k in range(len(xlsx_list)-1):
    delta_Edis.append(K*Temp*math.log(Freq_sort[k+1]/Freq_sort[k]))

    delta_Von.append(Von[k+1]-Von[k])

    

#    deltaT_avg.append()

    Dit.append(C_ox*delta_Von[k]/(q*delta_Edis[k])-(C_ox+C_AlGaN)/q)


print('delta_Edis为'+str(delta_Edis))
print('delta_Von为'+str(delta_Von))
print('Dit为'+str(Dit))
for k in range(len(xlsx_list)-1):
    print('%E' % Dit[k])
Dit.append(0) 



tx = pd.DataFrame(getC_pd,dtype=float)
t2 = pd.DataFrame(tx.values.T,index=getV_pd[0],columns=Dit,)
t2.plot()
t2.to_csv('Data.csv.tmp')
plt.axhline(Step2Condition,color='r',linestyle='--',label='StepCondition')
plt.legend(loc='upper left')
plt.savefig('Plot.png')
plt.show()




'''
----------------------------------Reference-------------------
[1]Sun Z, Huang H, Wang R, Sun N, Tao P, Ren Y, Song S, Wang H, Li S, Cheng W, Gao J. Improving performances of enhancement-mode AlGaN/GaN MIS-HEMTs on 6-inch Si substrate utilizing SiON/Al 2 O 3 stack dielectrics. IEEE Electron Device Letters. 2019 Dec 3;41(1):135-8.
[2]Hua M, Zhang Z, Wei J, Lei J, Tang G, Fu K, Cai Y, Zhang B, Chen KJ. Integration of LPCVD-SiN x gate dielectric with recessed-gate E-mode GaN MIS-FETs: Toward high performance, high stability and long TDDB lifetime. In2016 IEEE International Electron Devices Meeting (IEDM) 2016 Dec 3 (pp. 10-4). IEEE.
'''

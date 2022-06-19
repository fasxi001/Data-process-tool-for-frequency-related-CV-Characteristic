# Data-process-tool-for-frequency-related-CV-Characteristic
# 变频CV测试数据处理脚本

基于中科院苏州纳米所测试平台Keithley 4200测试设备的GaN HEMT变频CV测试数据处理脚本，用于将设备输出的大量xls表格文件整合计算得出介质层与AlGaN势垒层之间的界面态密度；脚本基于python3，请预先安装：

/glob

/pandas

/xlrd

/matplotlib

缺省状态下脚本针对带有Al2O3介质层的AlGaN/GaN异质结CV测试图形，测试和计算表面态的方法基于港科杨树博士的文献：
https://ieeexplore.ieee.org/document/7103310

DOI:10.1109/TED.2015.2420690



## 测试方法简介
界面态俘获与释放载流子的现象表现出电容特性，通过限定条件的CV测试可以特异的表征出界面态密度

界面态在禁带的能级上连续分布，只有费米能级附近的界面态会响应外部的小信号变化；定义界面态缺陷时间常数对应的频率为$f_{it}$，则有公式(1)，由于时间常数较长的界面态来不及响应更快的交流小信号，所以当界面态缺陷对应的频率高于测试小信号的频率时，界面态缺陷才会影响CV测试的结果

![image](https://github.com/fasxi001/Data-process-tool-for-frequency-related-CV-Characteristic/blob/main/MEDIA/Fig_1.png)

$$f_{it} = {{1} \over {2 \pi \tau_e}} = {{v_{th} \sigma_n N_C} \over 2 {\pi}} exp(-{{E_C-E_T} \over {kT}}) 
\tag{1}$$

<center>

$\tau_e$是陷阱释放电子的时常数，$v_{th}$是电子热运动速率，$\sigma_n$是电子的俘获截面，$N_C$是导带的有效态密度

</center>

针对MIS/AlGaN/GaN结构，随着直流偏置的提高，形成2DEG后，CV曲线度过第一个斜坡进入平台，此时AlGaN/GaN异质结界面态能级低于费米能级，不响应交流小信号，不影响CV测试的结果；此时费米能级附近的界面态仍然是深能级陷阱，时常数较长，频率较低，不响应CV测试小信号，所以此时的CV曲线平直；随着直流偏置的进一步提高，费米能级距离导带底越来越近，费米能级附近的界面态的频率越来越高，与CV测试频率相近后开始响应，表现为测试电容值的上升

根据上述现象，给定不同的CV测试频率，则电容离开平台开始上升的电压值也会相应变化；例如较低的测试频率下，能级位置更深的界面态也会响应测试小信号，则CV曲线会更早的离开平台，进入第二个上升斜坡(更低的膝电压)；两条不同频率的CV测试曲线，对应的第二个上升斜坡的膝电压值($V_{ON}$)之间存在差距$\Delta V_{ON}$，这一部分差距的来源就是更高频率下不响应的低频界面态(能级更深)，据此就可以特异的表征出不同能级位置的界面态的态密度

![image](https://github.com/fasxi001/Data-process-tool-for-frequency-related-CV-Characteristic/blob/main/MEDIA/Fig_2.png)
![image](https://github.com/fasxi001/Data-process-tool-for-frequency-related-CV-Characteristic/blob/main/MEDIA/Fig_3.png)

计算界面态密度所用的公式如下所示：

$$ D_{it}(E_C-E_T = \Delta E_{T\_AVG}) = {{C_{ox} · \Delta V_{on}} \over {q · \Delta E_{dis}}} - {{C_{ox}+C_B} \over {q^2}} 
\tag{2}$$

$$\Delta E_{T\_AVG} = {{\Delta E_T(f_1,T_1) + \Delta E_T(f_2,T_2)} \over {2}} 
\tag{3}$$

$$\Delta E_{dis} = \Delta E_T(f_1,T_1) - \Delta E_T(f_2,T_2) 
\tag{4}$$

$$\Delta V_{ON} = V_{ON} (f_2,T_2) - V_{ON}(f_1,T_1) 
\tag{5}$$



## 脚本使用方法
将xls格式的原始数据与.py文件置于同一路径下，根据实际测试的参数修改脚本内定义的变量值后运行脚本即可，脚本会输出不同测试频率对应的界面态密度，单位为($eV^{-1}·cm^{-2}$)，测试频率根据公式(1)可以换算为能级位置



## 脚本介绍
glob模块读取脚本文件所在路径下的xls数据文件的文件名；

pandas模块遍历所有xls数据文件，获取'Settings'选项卡中'Frequency'的数值；

通过sort根据'Frequency'的数值对文件进行排序；

pandas模块按照'Frequency'从小到大的顺序遍历xls数据文件，获取不同测试频率下的电容C和电压V的CV曲线数据；

遍历某一测试频率下的CV曲线数据，当电容值大于定义好的判定条件时，认为该电容值对应的电压值为该频率下的$V_{ON}$，据此获得所有测试频率所对应的$V_{ON}$；

根据测试方法简介中的公式计算得到界面态密度


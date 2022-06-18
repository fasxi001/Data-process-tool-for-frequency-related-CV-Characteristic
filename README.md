# Data-process-tool-for-frequency-related-CV-Characteristic
# 变频CV测试数据处理脚本
## 摘要
基于中科院苏州纳米所测试平台Keithley 4200测试设备的GaN HEMT变频CV测试数据处理脚本，用于将设备输出的大量xls表格文件整合计算得出界面态密度；脚本基于python3，请预先安装：

/glob

/pandas

/xlrd

/matplotlib

缺省状态下脚本针对带有Al2O3介质层的AlGaN/GaN异质结CV测试图形，测试和计算表面态的方法基于港科杨树博士的文献：
https://ieeexplore.ieee.org/document/7103310

DOI:10.1109/TED.2015.2420690

---

## 测试方法简介
    
$$f_{it} = {{1} \over {2 \pi \tau_e}} = {{v_{th} \sigma_n N_C} \over 2 {\pi}} exp(-{{E_C-E_T} \over {kT}})$$


$$ D_{it}(E_C-E_T = \Delta E_{T\_AVG}) = {{C_{ox} · \Delta V_{on}} \over {q · \Delta E_{dis}}} - {{C_{ox}+C_B} \over {q^2}} $$


$$\Delta E_{T\_AVG} = {{\Delta E_T(f_1,T_1) + \Delta E_T(f_2,T_2)} \over {2}}$$

$$\Delta E_{dis} = \Delta E_T(f_1,T_1) - \Delta E_T(f_2,T_2)$$

$$\Delta V_{ON} = V_{ON} (f_2,T_2) - V_{ON}(f_1,T_1) $$

---

## 脚本使用方法
将xls格式的原始数据与.py文件置于同一路径下，运行脚本即可，脚本会输出不同测试频率对应的界面态密度，单位为($eV^{-1}·cm^{-2}$)，测试频率可以换算为能级位置。

---

## 脚本介绍
glob模块读取脚本文件所在路径下的xls数据文件的文件名；

pandas模块遍历所有xls数据文件，获取'Settings'选项卡中'Frequency'的数值；

通过sort根据'Frequency'的数值对文件进行排序；

pandas模块按照'Frequency'从小到大的顺序遍历xls数据文件，获取不同测试频率下的电容C和电压V的CV曲线数据；

遍历某一测试频率下的CV曲线数据，当电容值大于定义好的判定条件时，认为该电容值对应的电压值为该频率下的$V_{ON}$，据此获得所有测试频率所对应的$V_{ON}$；

根据测试方法简介中的公式计算得到界面态密度。


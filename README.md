# Data-process-tool-for-frequency-related-CV-Characteristic
基于中科院苏州纳米所测试平台Keithley 4200测试设备的GaN HEMT变频CV测试数据处理脚本，用于将设备输出的大量xls表格文件整合计算得出界面态密度；脚本基于python3，请预先安装glob/pandas/xlrd/matplotlib模块；缺省状态下脚本针对带有Al2O3介质层的AlGaN/GaN异质结CV测试图形，测试和计算表面态的方法基于港科杨树博士的文献https://ieeexplore.ieee.org/document/7103310，DOI:10.1109/TED.2015.2420690。

# electronic-nose-system
基于labview和python的人工嗅觉测试系统，需搭配硬件使用

**深度学习版本：https://github.com/bbpp222006/elec_nose_plus**

history文件夹内有纯算法的历史版本，包含有重要的原理测试记录，各位可以参考里面的readme.pdf文件。

## 常见问题以及解决方法
>为什么我的.vi文件打不开（打开报错）？
* 之前版本的labview没有卸载干净，或者安装出错，重装应该可以解决。

>为什么打开不能运行（start按钮无效）？
* 请连接上硬件后重启软件再次尝试，若仍没有反应，则需要修改硬件名称为（Dev1）[参考链接](https://jingyan.baidu.com/article/8cdccae90882f9315413cdfb.html)  
**建议使用`自定义命名（2）`的方法进行修改**

>为什么程序运行（start）后出错？
* 出现这种情况有很多可能，请先尝试以下解决方法，若仍有报错，这种情况请附上报错信息发起issue。issue
格式参考[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way)

1. **检查项目文件夹路径是否含有中文（最好是纯英文目录）。**
2. 软件安装过程环境是否配好，漏掉步骤等。
3. 重新下载本项目文件，并尝试运行。


## 软件安装教程

本教程主要分为三个板块
1. 必要软件安装
2. 软件环境下载以及配置
3. 测试文件结构和功能

## 必要软件安装
 
### python3.6
python3.7不知道行不行，没做兼容性测试，所以还是3.6为好……  
[下载地址](https://www.python.org/)  
**注意安装时勾选上path**  




### labview2018
网上教程一堆，这里给个链接[提取码2333](https://pan.baidu.com/s/1Gmcm8GtB_m1Z47FB9IOPaA)  
链接中含有详细的安装和破解教程。注意查看  
**注意版本，一定要2018或更新**

### labview硬件驱动安装
[官方链接](https://www.ni.com/zh-cn/support/downloads/drivers/download.ni-daqmx.html#325032)
  
软件版本改为18.0  
直接安装即可。

---


## 软件环境配置
python的各种依赖包
现成算法只用到了
1. sklearn
2. matplotlib

接下来是操作流程
按下win+r，输入cmd打开命令行窗口  
复制粘贴以下内容   
**逐行输入，等安装完了再输下一条**
```
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install scikit-learn -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 测试文件结构和功能  
train文件夹：存放采集到的数据，用于训练  

test文件夹：预留测试数据接口，正常使用请勿删除  

main:knn以及kmeans算法主体文件，可对超参数进行调整  

sort_data:原始数据平滑处理文件，可根据要求修改为不同算法。  

main-6003:labview运行文件，安装完以上环境后运行这个就行。  

whole_data：训练完成后的缓存文件，再次测试时会直接调用此文件进行预测，缩短程序运行时间。

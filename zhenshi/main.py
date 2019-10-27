import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from collections import  Counter
import time
from scipy import signal
from sort_data import pinghua


def draw_pic(pre,train_dic):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # ax1.set_yticks()
    # ax1.set_yticklabels(['空气']+list(train_dic.keys()), rotation=30, fontsize='small')
    time = np.arange(len(pre))
    plt.plot(time, pre)
    # python要用show展现出来图
    plt.yticks(np.arange(len(train_dic) + 1),
               ['空气'] + list(train_dic.keys()))
    plt.show()


class lab_view():
    def __init__(self):
        #常数定义
        self.chuangkou = 10
        self.knn_neighbors = 10
        self.train_path = 'train'
        self.test_path = 'test'
        self.scaler = StandardScaler()
        self.knn = KNeighborsClassifier(n_neighbors=self.knn_neighbors)

        #加载数据
        self.train_dic = self.get_train_file_list()
        self.test_file_list = self.new_report(self.test_path, 1)
        print('训练用数据', self.train_dic)  # 有待优化输出
        print('测试用数据', self.test_file_list)

        #拟合数据
        self.traindata, self.testdata = self.load_data()
        self.train_knn()


    def new_report(self,test_report,length = 3):
        lists = os.listdir(test_report)                                    #列出目录的下所有文件和文件夹保存到lists
        if length>len(lists):
            length = len(lists)
        lists.sort(key=lambda fn:os.path.getmtime(test_report + "/" + fn))#按时间排序
        file_new = lists[-length:]                   #获取最新的文件保存到file_new
        file_new = list(map(lambda fn:test_report + "/" + fn,file_new))
        return file_new


    def get_train_file_list(self):
        train_path = self.train_path
        train_dic = {}
        trian_file_lists = os.listdir(train_path)
        for trian_file in trian_file_lists:
            if not os.path.isdir(train_path+'/'+trian_file):  # 排除非文件夹的文件
                trian_file_lists.remove(trian_file)
            else:
                file_content_data_list = list(map(lambda fn: train_path + "/" + trian_file + "/" +fn
                                                  ,os.listdir(train_path+'/'+trian_file)))
                train_dic[trian_file] = file_content_data_list
        return train_dic


    def gen_kmeans_pre(self,filedata,index = 0):
        content = filedata[:, 1:]
        kmeans = KMeans(n_clusters=2).fit(content)
        pred = kmeans.predict(content)  # 0为背景，index+1为有效信号
        pred_pretime = pred[pred.shape[0]*8 // 9:]
        if Counter(pred_pretime)[1] >= Counter(pred_pretime)[0]:  # 默认中间1/5时间内信号多于背景0
            pred = -(index + 1) * (pred - 1)

        else:
            pred = (index + 1) * pred
        print(len(pred),Counter(pred)[index + 1])
        return pred


    def load_data(self,learn_flag = 0):
        if (not os.path.exists('whole_data.txt')) or learn_flag:
            print('未发现存在的整合数据，开始生成')
            for index, files in enumerate(self.train_dic):
                for file in self.train_dic[files]:
                    filedata = np.genfromtxt(file, delimiter='	')
                    #此处加入平滑处理
                    filedata = pinghua(filedata)


                    pred = self.gen_kmeans_pre(filedata, index)
                    filedata[:, 0] = pred
                    try:
                        traindata = np.append(traindata, filedata, axis=0)
                    except:
                        traindata = filedata
            np.savetxt('whole_data.txt', traindata, fmt='%0.8f')
            print('生成数据完成')
        else:
            print('发现存在数据，加载中')
            traindata = np.genfromtxt('whole_data.txt', delimiter=' ')
            print('加载完成')

        for index, file in enumerate(self.test_file_list):
            filedata = np.genfromtxt(file, delimiter='	')
            filedata[:, 0] = -index  # 随便写点啥
            try:
                testdata = np.append(testdata, filedata, axis=0)
            except:
                testdata = filedata

        return traindata, testdata


    def train_knn(self):

        y_train = self.traindata[:,0].astype(int)
        x_train = self.traindata[:,1:]
        x_test = self.testdata[:,1:]

        print('打标结束')

        x_trainstd = self.scaler.fit_transform(x_train)  # 标准化
        x_teststd = self.scaler.transform(x_test)
        print('加载数据结束，开始knn拟合')
        time_start=time.time()
        # clf = SVC(probability=True)
        # clf.fit(x_trainstd, y_train)
        # # 训练模型
        #
        # # 计算测试集精度
        # pre = clf.predict(x_teststd)

        self.knn.fit(x_trainstd,y_train)
        pre = self.knn.predict(x_teststd)

        time_end=time.time()
        print('totally cost',time_end-time_start)
        print('拟合结束，开始绘图')
        return pre



    def get_current_pre(self,time_list):  #此处传入的time_list为带头的矩阵文件，就是有时间标记的
        #
        # x_test = time_list[:, 1:]
        # x_teststd = self.scaler.transform(x_test)
        # pre = self.knn.predict(x_teststd)
        # # draw_pic(pre,train_dic)
        # obj = Counter(pre[:max(len(pre),10)])
        # current_pre = sorted(obj.items(), key=lambda x: x[1])[0][0]
        return self.get_whole_pre(time_list)[-1]


    def get_whole_pre(self,time_list):  #此处传入的time_list为带头的矩阵文件，就是有时间标记的
        if time_list.shape[1] == 0:
            x_test=np.array([[1,1,1,1,1,1]])
        if time_list.shape[1] == 7:
            x_test = time_list[:,1:]
        else:
            x_test = time_list
        x_teststd = self.scaler.transform(x_test)
        pre = self.knn.predict(x_teststd)
        for i, rs in enumerate(pre):

            obj = Counter(pre[i:min(len(pre), i+self.chuangkou)])
            current_pre = sorted(obj.items(), key=lambda x: x[1])[0][0]
            pre[i] = current_pre

        return pre

    def get_name_list(self):
        name_list = list(self.train_dic.keys())
        return name_list


    def get_persent(self,time_list):
        # x_test = time_list[:, 1:]
        # x_teststd = self.scaler.transform(x_test)
        pre = self.get_whole_pre(time_list)
        obj = Counter(pre)
        per_list = np.ones(len(name_list))
        for i in range(len(name_list)):
            try:
                per_list[i] = obj[i + 1] / (len(pre) - obj[0])
            except:
                per_list[i] = 0
        return per_list

test = lab_view()

name_list = test.get_name_list()
# 重写whole_data
def creatdata():
    test.load_data(learn_flag = 1)
    return 1
# 文件夹list
def listlist():
    return (test.get_name_list())
    # return (["1","2","3","4","5号"])

# 当前
def lastpre(time_list):
    time_list=np.array([time_list])
    return (test.get_current_pre(time_list= time_list))
# 全部
def perlist(time_list):
    time_list=np.array(time_list)

    b = str([0]+list(test.get_persent(time_list= time_list)))
    # a = str(time_list.shape)
    with open('test.txt','a') as f:
        # f.write(a)
        f.write(b)
    return ([0]+list(test.get_persent(time_list= time_list)))

# 总长 最有可能的 id 和 百分率
def mostlike(time_list):
    time_list=np.array(time_list)
    mat=test.get_persent(time_list= time_list)
    return ([len(mat),np.argmax(mat),100*max(mat)])


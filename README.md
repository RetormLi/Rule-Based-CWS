# 中文分词

基于规则实现的简单中文分词



## 文件

-   main.py：程序主要运行入口
-   data_process.py：处理数据集，获得词表
-   analyze.py：封装句子处理，方法有FMM，RMM，BMM
-   preprocess.py：定义了需要预处理的正则
-   eval.py：用precision，recall，F1来评价分词效果
-   data：用来存放数据集
-   vocab：用来存放词表



## 额外数据集

-   30wChinese：30万词中文词表
-   THUOCL：财经，食物，地名，成语数据集
-   English_Cn_Name_Corpus：48万英译中人名
-   places：中国行政区划
-   pku_training：人民日报分词语料



## 运行方法

1.  运行```data_process.py```，处理数据集，获得词表，存放在vocab文件夹中

2.  运行```main.py```，获得测试集分词结果



## 评价

测试集F1-Score: 0.92689


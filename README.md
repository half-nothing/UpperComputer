# UpperComputer
## 构建可执行文件
首先安装环境,需要python >= 3.10
```shell
pip install -r requirements.txt
```
[```UpperComputer-Mutil```](UpperComputer-Mutil.spec)用来构建分散的可执行文件  
```shell
pyinstaller UpperComputer-Mutil.spec
```
构建出来的文件在[```dist/UpperComputer```](./dist/UpperComputer)下  
[```UpperComputer-Single```](UpperComputer-Single.spec)用来构建单个的可执行文件  
```shell
pyinstaller UpperComputer-Single.spec
```
构建出来的文件在[```dist```](./dist)下

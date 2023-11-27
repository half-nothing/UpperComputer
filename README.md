<h1 align="center">
    UpperComputer
</h1>
<p align="center">
    基于 PyQt6 的 智能车上位机
</p>
<p align="center">
    <a href="https://www.github.com/half-nothing/UpperComputer/releases/latest">
        <img alt="GitHub release" src="https://img.shields.io/github/v/release/half-nothing/UpperComputer">
    </a>
    <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/half-nothing/UpperComputer">
    <br/>
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/half-nothing/UpperComputer/python-build.yml">
    <img alt="GitHub commits since latest release" src="https://img.shields.io/github/commits-since/half-nothing/UpperComputer/latest/main">
    <img alt="GPLv3" src="https://img.shields.io/badge/License-GPLv3-blue"/>
    <img alt="Platform Win32" src="https://img.shields.io/badge/Platform-Win32%20-blue"/>
</p>  

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

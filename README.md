# Alice_QQBot
基于QQ开放平台和ollama的QQ对话机器人

## 准备工作

### 注册QQ开放平台

平台官网：https://q.qq.com/

注册完后在主页应用管理中点击创建机器人

填完基础信息后在开发设置中查看机器人的AppID和Token

### 安装ollama

ollama是一个简单易用的本地大语言模型运行框架

ollama下载地址：https://ollama.com/

在ollama的GitHub官网有他的使用方法：https://github.com/ollama/ollama

安装路径改不了，只能是C盘，但是模型下载路径能变，需要配置系统环境变量

配置完记得重启电脑

```bash
OLLAMA_HOST     0.0.0.0
OLLAMA_MODELS   D:\ollama\models # 模型的存放位置
```

配置好后就可以下载大模型了，在ollama官网有很多模型，可以找自己需要的

模型仓库： https://ollama.com/library

这里用谷歌的gemma2来举例

在桌面按Win+R，输入cmd回车

在打开的命令提示符窗口中输入：ollama run gemma2

等下载完成后会在命令行自动运行gemma2模型，可以直接输入消息和他对话

### 安装Python环境

Python我使用的事3.11版本，记得创建虚拟环境

```bash
pip install qq-botpy
pip install ollama
```

QQ机器人的基础搭建参考官方教程：https://github.com/tencent-connect/botpy

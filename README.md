# Alice_QQBot
基于QQ开放平台和ollama的QQ对话机器人

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

在打开的命令提示符窗口中输入：
```bash
ollama run gemma2
```

等下载完成后会在命令行自动运行gemma2模型，可以直接输入消息和他对话

### 安装Python环境

Python我使用的事3.11版本，记得创建虚拟环境

```bash
pip install qq-botpy
pip install ollama
```

### 搭建框架

- QQ机器人官方文档：https://bot.q.qq.com/wiki/#
- QQ机器人GitHub：https://github.com/tencent-connect/botpy

#### 实现接收消息

在QQ机器人GitHub的源码中找到examples文件夹

我们只下载其中的demo_c2c_reply_text.py文件，或者直接复制源码粘贴到本地

修改里面主函数，按照下面的填

```python
if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True) # 别忘了这里加入is_sandbox=True启用沙箱功能
    client.run(appid="这里填你注册机器人的AppID", secret="这里是令牌")
```

现在运行代码，机器人就能收到你发送的消息了，消息在message中

```python
class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_c2c_message_create(self, message: C2CMessage): # 这里的message是消息体
        # 消息在这里发送
        await message._api.post_c2c_message(
            openid=message.author.user_openid, 
            msg_type=0, msg_id=message.id, 
            content=f"我收到了你的消息：{message.content}" # 这里的message.content就是你发送的消息内容
        )
```

### 调用ollama

#### 导包

```python
from ollama import Client
```

#### 连接ollama接口

```python
olm_client = Client(host='http://localhost:11434') # ollama默认开放端口为11434
```

#### 调用模型对话

这里至少要传入两个值，一个是你要调用的模型名称，一个是你的对话信息

对话信息是一个数组，里面是json结构：

其中"role"有三个值，"system"、"user"、"assistant"，分别为“系统设定内容”、“用户输入内容”、“AI输出内容”
下面的"content"就是具体的消息内容

我们需要将接收到的消息加入数组中，把整个数组传给AI，这样AI就知道我们的对话进度，也就是拥有了记忆

```json
[
  {
    "role": "system",
    "content": "这里写AI的设定"
  },{
    "role": "user",
    "content": "这里是你发送的消息"
  },{
    "role": "assistant",
    "content": "这里是AI返回的消息"
  }
]
```

调用模型

```python
# 构建消息
messages = [{"role": "system","content": "你叫爱丽丝·玛格特罗伊德，是用户的好友"},{"role": "user", message.content}] # 这里传入你的消息内容
# 调用大模型
response = olm_client.chat(model="gemma2", messages=messages)
# 打印响应内容
print(f"消息内容为{response['message']['content']}")
```

控制台输出结果

```bash
>>>您好！请问您有什么问题想问我呢？很高兴为您服务。
```

这样调用AI对话就实现了

### 构建完整对话流程

很简单，把上面调用模型的代码塞到on_c2c_message_create方法里面就行了

完整代码：
```python
import asyncio
import os

import botpy
from botpy import logging
from botpy.message import C2CMessage
log = logging.get_logger()

from ollama import Client
olm_client = Client(host='http://localhost:11434') # ollama默认开放端口为11434

# 在这里构建你的记忆
message_list = [{"role": "system","content": "你叫爱丽丝·玛格特罗伊德，是用户的好友"}]


class MyClient(botpy.Client):
    async def on_ready(self):
        log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_c2c_message_create(self, message: C2CMessage):
        
        
        # 构建消息，将你的消息加入记忆中
        messages = message_list.append({"role":"user","content":message.content})
        # 调用大模型
        response = olm_client.chat(model="gemma2", messages=messages)
        
        # 将AI的消息也加入记忆中
        message_list.append({"role":"assistant","content":response["message"]["content"]})
        
        # 将消息返回
        await message._api.post_c2c_message(
            openid=message.author.user_openid, 
            msg_type=0, msg_id=message.id, 
            content=response["message"]["content"]
        )


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid="你的AppID", secret="你的令牌")
```

这样基础的对话就实现了，但是只能实现最基本的文本对话，图片、表情、文件都无法识别

不过我上传的代码中都有实现对应的功能（还没写完），还做了菜单，感兴趣的可以直接clone到本地（我的对话消息还残留着）

### 最后

如果有好的想法，可以联系我 QQ：647929196

没了

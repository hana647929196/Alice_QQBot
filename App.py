from Config import Config
from datetime import date
from Ollama import Ollama
import requests
import os

# import requests.packages.urllib3.util.ssl_
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


# 模型对象
ollama = Ollama()

# 配置信息
config = Config()


def main(message):
    """
    主流程
    Args:
        message: 消息体

    Returns:响应内容

    """
    # 打印消息体
    print(f"""
            用户id：{message.author.user_openid},
            消息内容：{message.content},
            对话id：{message.id},
            提及：{message.mentions},
            附件：{message.attachments},
            消息序列：{message.msg_seq},
            发送时间：{message.timestamp},
            事件id：{message.event_id},
            """)

    # 下载文件
    if len(message.attachments) > 0:
        url_download(message=message)

    content = menu(message=message)

    if content:
        return content

    # 拼凑上下文
    messages = get_memory(user_id=message.author.user_openid)
    messages.append({"role": "user", "content": message.content})

    # 调用对话接口
    response = ollama.chat(messages=messages, model=config.get_chat_model())

    # 写入记忆
    messages.append(response)
    config.write_memory()

    # 获取响应结果
    content = response["content"]

    return content


# 菜单
def menu(message):
    """
    菜单
    Args:
        message: 消息体
    """
    if message.content == "菜单":
        content = "清空记忆\n模型列表\n切换模型\n模式列表\n切换模式\n角色设定\n故事进度"

    elif ("清除" in message.content or "清空" in message.content) and "记忆" in message.content:
        content = clear_memory(message=message)

    elif "模型" in message.content and (
            "全部" in message.content or "所有" in message.content or "列表" in message.content):
        content = get_model_list()

    elif '切换' in message.content and '模型' in message.content:
        content = switch_model(message=message)

    elif "模式" in message.content and (
            "全部" in message.content or "列表" in message.content or "所有" in message.content or "当前" in message.content):
        content = get_all_pattern()

    elif '切换' in message.content and "模式" in message.content:
        content = switch_pattern(message=message)

    elif "角色" in message.content and ("信息" in message.content or "设定" in message.content):
        content = config.get_role_setting()

    elif "故事进度" in message.content:
        content = get_story_schedule(message=message)
    else:
        content = False
    return content


# 获取对话记录
def get_memory(user_id):
    """
    获取对话记录，拼凑上下文
    Args:
        user_id: 消息体

    Returns:消息列表

    """

    # 获取对话记录
    store = config.get_memory()

    # 判断用户是否在列表中有记录
    if user_id in store:

        # 将消息记录返回
        return store[user_id]

    # 如果当前用户没有记录，则新建记录
    else:
        # 初始化角色设定
        store[user_id] = [{"role": "system", "content": config.get_role_setting()}]

        # 将新记录返回
        return store[user_id]


# 清除记忆
def clear_memory(message):
    """
    记忆清除
    Args:
        message:消息体

    Returns:记忆被清除了

    """
    # 判断是否存在消息记录
    if message.author.user_openid in config.get_memory():
        # 删除消息记录
        del config.get_memory()[message.author.user_openid]
        # 写入消息记录
        config.write_memory()
    return "记忆被清除了..."


# 处理消息
def process_message(content):
    """
    处理表情符号,提取消息内容
    Args:
        content:消息内容

    Returns:处理完毕后的消息内容

    """
    # 判断是否存在表情
    if "<faceType=" in content and ",faceId=" in content and ">" in content:

        # 提取表情type、id和ext
        fase_type = content.split("<faceType=")[1].split(',')[0]
        face_id = content.split("<faceType=")[1].split(',faceId="')[1].split('"')[0]
        face_ext = content.split("<faceType=")[1].split(',faceId="')[1].split(',ext="')[1].split('"')[0]

        # 检索表情
        emoji = config.get_emoji_dict()[fase_type][face_id]

        # 组成表情原文
        emoji_code = f'<faceType={fase_type},faceId="{face_id}",ext="{face_ext}">'

        # 对话内容切片
        content_arr = content.split(emoji_code)

        # 开始处理消息
        new_content = ''
        for i in range(len(content_arr)):
            if i + 1 == len(content_arr):
                new_content += content_arr[i]
                break
            new_content += content_arr[i] + f"（{emoji}）"

        content = new_content
        process_message(content=content)
    return content


# 获取模型列表
def get_model_list():
    """
    获取模型列表
    Returns:模型列表

    """

    models = f'Chat :\n{config.get_chat_model()}\nEmbed :\n{config.get_embed_model()}\nGenerate :\n{config.get_generate_model()}\nAll Model :\n'
    model_list = ollama.list()
    for model in model_list:
        models += model['name'] + '\n'
    return models


# 切换模型
def switch_model(message):
    """
    切换当前模型
    Args:
        message:消息体

    Returns:当前模型状态

    """
    # 获取消息内容
    content = message.content

    # 设定切换的类型
    model_type = "chat_model"
    if 'embed' in content or 'Embed' in content or "向量" in content:
        model_type = "embed_model"
    elif 'generate' in content or 'Generate' in content or '多模态' in content:
        model_type = "generate_model"

    # 获取模型
    model_list = ollama.list()
    for model in model_list:
        if model['name'] in content:
            config.setting[model_type] = model["name"]
            config.write_setting()
            return f'切换成功!当前模型为：{config.setting[model_type]}'

    return '无效的模型'


# 获取模式列表
def get_all_pattern():
    """
    获取模式
    Returns:

    """

    content = f'current pattern :{config.get_pattern()}\n'
    for temp in config.get_pattern_list():
        content += temp + '\n'

    return content


# 切换模式
def switch_pattern(message):
    """
    切换模式
    Args:
        message:消息体

    Returns:当前模式

    """
    # 获取消息
    content = message.content

    # 判断模式
    for temp in config.get_pattern_list():
        if temp in content:
            config.setting['pattern'] = temp
            config.write_setting()
            return f'切换成功!当前为：{config.get_pattern()}模式'

    return '无效的模式'


# 修改角色信息
def update_role(message):
    """
    修改角色设定
    Args:
        message:消息体

    Returns:修改结果

    """
    # 获取消息
    content = message.content

    # 获取模式
    temp_pattern = content.split('修改角色-')[1].split(':')[0]

    # 修改设定
    if temp_pattern in config.setting:
        config.setting[temp_pattern] = content.split(f'修改角色-{temp_pattern}:')[1]
        config.write_setting()
        return f"修改成功！当前{temp_pattern}设定为：{config.setting[temp_pattern]}"

    return "无效"


# 当前故事进度
def get_story_schedule(message):
    """
    获取故事进度
    Args:
        message: 消息体

    Returns: 故事进度
    """
    store = config.get_memory()
    # 是否存在进度
    if message.author.user_openid not in store:
        return "当前进度为0"

    # 获取消息列表
    message_list = store[message.author.user_openid]

    # 初始化故事信息
    story_schedule = ""
    # 迭代消息
    for msg in message_list:
        if msg['role'] == 'user':
            story_schedule += f"我：{msg['content']}\n"
        elif msg['role'] == 'assistant':
            story_schedule += f"爱丽丝：{msg['content']}\n"

    # 构建提示词
    messages = [{
        'role': 'system',
        'content': '你的工作是对文章内容进行总结，用户会给你发一篇对话记录，你需要将对话记录总结成故事并返回给用户，篇幅不要太长，内容保持在300字以内'
    }, {
        'role': 'user',
        'content': story_schedule
    }]

    response = ollama.chat(messages=messages, model='leeplenty/lumimaid-v0.2:latest')

    # 读取消息
    content = ''
    for res in response:
        content += res['message']['content']

    return content


# 下载消息文件
def url_download(message):
    """
    下载消息文件
    Args:
        message: 消息体

    Returns: null
    """
    # 获取日期
    today = date.today()

    # 创建文件夹
    file_path = f"E:\\alice\\files\\{today.year}\\{today.month}\\{today.day}"
    folder = os.path.exists(file_path)

    # 判断是否存在文件夹
    if not folder:
        # 新建路径
        os.makedirs(file_path)

    # 遍历消息中的文件
    for file in message.attachments:
        # 获取网络地址
        url = file.url
        # 拼凑文件名
        file_name = f"{file_path}\\{file.filename}"

        try:
            # 读取文件
            response = requests.get(url=url)
            # 写入文件
            with open(file_name, "wb") as f:
                f.write(response.content)
                print(f"文件{file.filename}下载成功")
        except Exception as e:
            print(e)

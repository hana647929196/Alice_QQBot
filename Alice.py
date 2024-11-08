# -*- coding: utf-8 -*-
import botpy
from botpy import logging
from App import main
from botpy.message import C2CMessage

logs = logging.get_logger()


# 消息连接类
class MyClient(botpy.Client):

    # 开机
    async def on_ready(self):
        """
        开机
        Returns:on_ready!

        """
        logs.info(f"robot 「{self.robot.name}」 on_ready!")

    # 对话
    async def on_c2c_message_create(self, message: C2CMessage):
        """
        获取消息并返回
        Args:
            message: 消息体

        Returns:消息内容
        """

        # 调用菜单
        content = main(message=message)

        # 配置回复信息
        print(f"返回结果：{content}")
        try:
            message_result = await message.api.post_c2c_message(
                openid=message.author.user_openid,
                msg_type=0,
                msg_id=message.id,
                content=content
            )
        except Exception as e:
            message_result = await message.api.post_c2c_message(
                openid=message.author.user_openid,
                msg_type=0,
                msg_id=message.id,
                content="Error:消息发送失败"
            )

        # 返回消息
        logs.info(message_result)


# 开机
if __name__ == "__main__":
    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid="102439258", secret="rEbyMk8WuIg5UtIh6VvLlBb1RsJkBc3U")

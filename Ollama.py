from ollama import Client


# ollama
class Ollama:

    def __init__(self):
        """
        连接ollama
        """
        self.olm_client = Client(host='http://localhost:11434')

    def list(self):
        """
        获取模型列表
        """
        return self.olm_client.list()['models']

    def chat(self, messages, model):
        """
        语言模型调用
        Args:
            messages: 消息
            model: 模型

        Returns:消息记录

        """

        # 调用语言模型
        response = self.olm_client.chat(model=model, messages=messages, stream=True)
        # 读取消息
        content = ''
        for res in response:
            content += res['message']['content']

        result = {
            'role': 'assistant',
            'content': content
        }

        return result

    def embed(self, text, model):
        """
        向量模型调用
        Args:
            text: 文本
            model: 模型

        Returns:向量值

        """
        # 调用消息模型
        response = self.olm_client.embed(model=model, input=text)
        return response

    def generate(self, message, model):
        """
        调用生成接口
        Args:
            message: 消息体
            model: 模型

        Returns:响应结果

        """
        response = self.olm_client.generate(prompt=message.content, model=model)
        return response["response"]

    def agent(self, ):
        pass

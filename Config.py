import json


# 设定
class Config:

    # 初始化设定对象
    def __init__(self):
        # 加载设定文件
        with open('json/setting.json', 'r', encoding='utf-8') as f:
            self.setting = json.load(f)

        # 加载记忆文件
        with open('json/memory.json', 'r', encoding='utf-8') as f:
            self.memory = json.load(f)

    # 获取表情字典
    def get_emoji_dict(self):
        return self.setting["emoji_list"]

    # 获取模式字典
    def get_pattern_list(self):
        return self.setting["pattern_list"]

    # 获取当前模式
    def get_pattern(self):
        return self.setting["pattern"]

    # 获取管理员ID
    def get_master_id(self):
        return self.setting["master_id"]

    # 获取对话模型
    def get_chat_model(self):
        return self.setting["chat_model"]

    # 获取向量模型
    def get_embed_model(self):
        return self.setting["embed_model"]

    # 获取多模态模型
    def get_generate_model(self):
        return self.setting["generate_model"]

    # 获取角色设定
    def get_role_setting(self):
        return self.setting[self.get_pattern()]

    # 获取记忆
    def get_memory(self):
        return self.memory[self.get_pattern()]

    # 写入设定文件
    def write_setting(self):
        """
        写入设定json文件
        Returns:True

        """
        with open('json/setting.json', 'w', encoding='utf-8') as setting_write:
            json.dump(self.setting, setting_write, ensure_ascii=False)

    # 写入记忆文件
    def write_memory(self):
        """
        写入记忆json文件
        Returns:True

        """
        with open('json/memory.json', 'w', encoding='utf-8') as memory_write:
            json.dump(self.memory, memory_write, ensure_ascii=False)

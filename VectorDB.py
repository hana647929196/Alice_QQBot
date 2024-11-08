import chromadb


# 向量库
class VectorDB:

    # 初始化向量库对象
    def __init__(self, message, embed):
        """
            创建向量库连接
            Args:
                message: 消息体
            """
        # 连接数据库
        chroma_client = chromadb.PersistentClient(path="E:\\alice\\chromadb")
        # 创建集合
        self.collection = chroma_client.get_or_create_collection(name=message.author.user_openid)
        self.embed = embed

    # 灌库
    def chroma_add(self, documents):
        """
        切片灌库
        Args:
            documents: 文档切片
        """
        # 切片转向量
        embedding = self.embed(documents=documents)
        # 创建索引
        ids = [f"id{i}" for i in range(len(documents))]
        # 灌库
        self.collection.add(
            embeddings=embedding,
            documents=documents,
            ids=ids
        )

    # 检索
    def chroma_query(self, query, top):
        """
        检索文档
        Args:
            query: 用户问题
            top: 优先级
        Returns: 检索结果
        """
        embedding = self.embed(query)

        result = self.collection.query(
            query_embeddings=embedding,
            n_results=top
        )

        return result

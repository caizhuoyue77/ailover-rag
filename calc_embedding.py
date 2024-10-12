"""
该脚本通过bge-m3将段落转换为embedding，并将结果存储到Qdrant数据库中。
"""

from FlagEmbedding import BGEM3FlagModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 初始化BGE M3模型
model = BGEM3FlagModel('../bge-m3', use_fp16=True)

# 初始化Qdrant客户端
client = QdrantClient(url="http://localhost:6333")

# 创建集合以存储embedding
client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)

def calc_embedding(file_path: str) -> dict:
    """
    从指定文件读取内容，按段落切分为句子，每12句计算一次embedding并存储到Qdrant数据库中。

    参数:
        file_path (str): 文件路径

    返回:
        dict: 每句话和对应embedding的字典
    """
    try:
        # 读取文件内容并按\n切分为段落
        with open(file_path, 'r', encoding='utf-8') as file:
            sentences = file.read().splitlines()
        
        # 存储结果的字典
        sentence_embedding_dict = {}
        
        # 打印读取的句子数量
        print(f"共读取到句子数量: {len(sentences)}")

        # 按12句一组进行embedding计算
        for i in range(0, len(sentences), 12):
            batch_sentences = sentences[i:i + 12]
            print(f"处理第 {i//12 + 1} 组句子: {batch_sentences}")

            # 计算embedding
            embeddings = model.encode(
                batch_sentences,
                batch_size=12,
                max_length=2000,
            )['dense_vecs']
            
            # 打印每个句子及其对应的embedding
            for sentence, embedding in zip(batch_sentences, embeddings.tolist()):
                sentence_embedding_dict[sentence] = embedding
                print(f"句子: \"{sentence}\" 的 embedding: {embedding}")

                # 将embedding插入到Qdrant数据库
                point = PointStruct(id=len(sentence_embedding_dict), vector=embedding, payload={"sentence": sentence})
                operation_info = client.upsert(collection_name="test_collection", points=[point])
                
                # 打印插入数据库的状态信息
                print(f"插入到Qdrant数据库的状态: {operation_info}")

        return sentence_embedding_dict
    
    except FileNotFoundError as fnf_error:
        print(f"文件未找到: {fnf_error}")
        return {}
    except Exception as exc:
        print(f"出现错误: {exc}")
        return {}

# 使用示例
if __name__ == "__main__":
    file_path = "你的文件路径.txt"  # 替换为你的文件路径
    embeddings = calc_embedding(file_path)
    print(f"最终结果: {embeddings}")  # 打印每句话及其对应的embedding
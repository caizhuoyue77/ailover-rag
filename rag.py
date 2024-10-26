"""
该脚本通过bge-m3将段落转换为embedding，并将结果存储到Qdrant数据库中。
"""
import uuid
from FlagEmbedding import BGEM3FlagModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 初始化BGE M3模型
model = BGEM3FlagModel('../bge-m3', use_fp16=True)

COLLECTION_NAME = "ailover_test_collection_shenkong_241026_1"
client = QdrantClient(url="http://localhost:6333")

创建集合以存储embedding
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=1024, distance=Distance.DOT),
)

def read_file(file_path: str) -> list:
    """
    读取文件并按段落切分。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            print(f"共读取到段落数量: {len(paragraphs)}")
            return paragraphs
    except FileNotFoundError as fnf_error:
        print(f"文件未找到: {fnf_error}")
        return []
    except Exception as exc:
        print(f"读取文件时出现错误: {exc}")
        return []


def batch_sentences(paragraphs: list, batch_size: int = 12) -> list:
    """
    将段落按指定大小分组。
    """
    return [paragraphs[i:i + batch_size] for i in range(0, len(paragraphs), batch_size)]


def calculate_embeddings(sentences: list) -> list:
    """
    计算一组句子的embedding。
    """
    try:
        embeddings = model.encode(
            sentences,
            batch_size=len(sentences),
            max_length=2000,
        )['dense_vecs']
        return embeddings.tolist()
    except Exception as exc:
        print(f"计算embedding时出现错误: {exc}")
        return []


def insert_into_qdrant(sentences: list, embeddings: list) -> None:
    """
    将句子及其embedding插入到Qdrant数据库中。
    """
    try:
        for sentence, embedding in zip(sentences, embeddings):
            point = PointStruct(id=str(uuid.uuid4()), vector=embedding, payload={"content": sentence})
            operation_info = client.upsert(collection_name=COLLECTION_NAME, points=[point])
            print(f"插入到Qdrant数据库的状态: {operation_info}")
    except Exception as exc:
        print(f"插入到Qdrant时出现错误: {exc}")


def save_content_to_database(file_path: str) -> dict:
    """
    计算指定文件中的段落的embedding并存储到Qdrant数据库中。
    """
    paragraphs = read_file(file_path)
    if not paragraphs:
        return {}

    paragraph_embedding_dict = {}

    for batch in batch_sentences(paragraphs):
        embeddings = calculate_embeddings(batch)
        if embeddings:
            for sentence, embedding in zip(batch, embeddings):
                paragraph_embedding_dict[sentence] = embedding
            insert_into_qdrant(batch, embeddings)

    return paragraph_embedding_dict


def search_blocks(query_text: str, limit: int):
    
    query_embedding = calculate_embeddings([query_text])[0]

    # 从 Qdrant 数据库中查找最匹配的 embedding
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit
    )

    # 提取查询结果
    contents = []
    
    print(search_results)
    
    for result in search_results:
        content = {
            "score": result.score, 
            "content": result.payload.get("content", "")
        }
        contents.append(content)
    
    return {"results": contents}

# 使用示例
if __name__ == "__main__":
    file_path = "./data/story.txt"  # 替换为你的文件路径
    embeddings = save_content_to_database(file_path)
    # print(f"最终结果: {embeddings}")
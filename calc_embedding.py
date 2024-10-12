# 通过bge-m3把一段话变为embedding
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('../bge-m3',  
                       use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation


def calc_embedding(sentences_1):
    sentences_1 = ["What is BGE M3?", "Defination of BM25"]

    embeddings_1 = model.encode(sentences_1, 
                            batch_size=12, 
                            max_length=2000, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                            )['dense_vecs']
    
    embeddings_1 = embeddings_1.tolist()
    print(embeddings_1)
    return embeddings_1

# 读取文件中的内容切分为段落（按照\n来切分），然后12句一组去计算embedding，最后返回每句话和对应的embedding的一个dict，存储到下面的数据库



from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)

from qdrant_client.models import PointStruct

operation_info = client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ],
)

print(operation_info)

search_result = client.query_points(
    collection_name="test_collection",
    query=[0.2, 0.1, 0.9, 0.7],
    with_payload=False,
    limit=3
).points

print(search_result)





# ailover-rag

ChatAILover的客服机器人RAG仓库。

## 前置准备
embedding模型下载好
docker跑qdrant数据库

## 代码结构
- /data 数据集
- api.py fastapi有关代码
- rag.py 和rag有关的代码：计算embedding、搜索、插入向量数据库等
- concat_content.py 数据清洗的代码，把flowus导出的内容转为可以导入qdrant的格式（一个txt文件）
- natapp 内网穿透的软件

## 启动方式

docker启动qdrant
```shell
docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

nohup ./natapp [你对应的key] >> api-nohup.out
注意配置端口和natapp的端口一样

请求方式（这个natapp的链接可能会变）
curl -X POST "http://btu57v.natappfree.cc/search" -H "Content-Type: application/json" -d '{"query_text": " 如何切換模型？", "limit": 1}'


## 服务器配置

112服务器
深空：ailover_test_collection_shenkong_241026_4
光夜：ailover_test_collection_guangye_241026_2
光夜付费：ailover_test_collection_guangyefufei_241026_1

113服务器
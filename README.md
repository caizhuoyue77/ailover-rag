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
nohup ./natapp [你对应的key] >> api-nohup.out
注意配置端口和natapp的端口一样

请求方式（这个natapp的链接可能会变）
curl -X POST "http://btu57v.natappfree.cc/search" -H "Content-Type: application/json" -d '{"query_text": " 如何切換模型？", "limit": 1}'

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import BGEM3FlagModel, calculate_embeddings, search_blocks

# 初始化 FastAPI
app = FastAPI()


# Pydantic 模型用于定义请求结构
class SaveRequest(BaseModel):
    file_path: str


class SearchRequest(BaseModel):
    query_text: str
    limit: int = 3


# 根据查询文本返回最匹配结果的端点
@app.post("/search")
async def search_embeddings(request: SearchRequest):
    """
    根据用户输入的查询文本，计算其 embedding，并在 Qdrant 数据库中查找最匹配的 embedding。
    """

    try:
        result = search_blocks(request.query_text, request.limit)
        return result

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"查询失败: {exc}")


# 测试端点
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI API!"}
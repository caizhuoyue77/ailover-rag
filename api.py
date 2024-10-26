from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import BGEM3FlagModel, calculate_embeddings, search_blocks

# 初始化 FastAPI
app = FastAPI()

class SearchRequest(BaseModel):
    query_text: str
    bot_type: str  # 新增字段，用于选择 bot 类型
    limit: int = 3

    class Config:
        schema_extra = {
            "example": {
                "query_text": "示例查询文本",
                "bot_type": "guangye",
                "limit": 3
            }
        }

# 根据查询文本返回最匹配结果的端点
@app.post("/search")
async def search_embeddings(request: SearchRequest):
    """
    根据用户输入的查询文本，计算其 embedding，并在 Qdrant 数据库中查找最匹配的 embedding。
    """
    try:
        # 将 bot_type 传递给 search_blocks 函数
        result = search_blocks(request.query_text, request.bot_type, request.limit)
        return result

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"查询失败: {exc}")


# 测试端点
@app.get("/")
async def root():
    return {"message": "Welcome to the ChatAILover!"}
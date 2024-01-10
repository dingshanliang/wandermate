from fastapi import FastAPI
from api.api import router
from db.session import Base, engine

#  创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='wondermate'
)

#  添加路由
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
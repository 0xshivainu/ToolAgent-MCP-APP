# 使用官方 Python 基礎映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔與程式碼
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# 暴露 Cloud Run 指定端口（預設8080，且不能更改）
ENV PORT 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]



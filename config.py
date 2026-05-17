import os
from typing import List
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", 10))
    REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", 5.0))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    # 解析测试URL列表
    raw_urls = os.getenv("MOCK_URLS", "https://httpbin.org/post")
    MOCK_URLS = [url.strip() for url in raw_urls.split(",") if url.strip()]
import asyncio
import aiohttp
import json
import logging
import signal
from config import Config

# 配置企业级结构化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("AsyncEngine")

class AsyncNotificationEngine:
    def __init__(self):
        self.semaphore = asyncio.Semaphore(Config.MAX_CONCURRENCY)
        self.connector = aiohttp.TCPConnector(limit=500, limit_per_host=50)
        self.session = None
        self._is_cancelled = False

    async def start(self):
        """显式初始化会话"""
        self.session = aiohttp.ClientSession(connector=self.connector)
        # 注册优雅退出信号
        self._register_signal_handlers()

    async def close(self):
        """优雅关闭网络连接"""
        if self.session and not self.session.closed:
            await self.session.close()
        await asyncio.sleep(0.25) # 留出时间给底层连接库释放垃圾
        logger.info("引擎连接池已安全关闭。")

    def _register_signal_handlers(self):
        """监听系统退出信号，实现优雅退出"""
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown()))
            except NotImplementedError:
                # Windows 环境可能不支持某些信号处理，做个兼容
                pass

    async def shutdown(self):
        """触发熔断退出"""
        if self._is_cancelled:
            return
        logger.warning("接收到系统终止信号，正在强行熔断后续任务并安全退出...")
        self._is_cancelled = True

    async def send_task(self, url: str, task_id: int, user_id: str):
        """单条高可用任务执行逻辑"""
        if self._is_cancelled:
            return

        payload = {"task_id": task_id, "user_id": user_id, "msg": "System Alert"}
        
        async with self.semaphore:
            for attempt in range(Config.MAX_RETRIES):
                if self._is_cancelled:
                    return
                try:
                    async with self.session.post(url, json=payload, timeout=Config.REQUEST_TIMEOUT) as response:
                        if response.status == 200:
                            logger.info(f"任务 [{task_id}] 发送成功 | 目标: {url}")
                            return
                        else:
                            logger.warning(f"任务 [{task_id}] 响应异常, 状态码: {response.status} | 准备重试")
                except asyncio.TimeoutError:
                    logger.error(f"任务 [{task_id}] 第 {attempt+1} 次请求超时")
                except Exception as e:
                    logger.error(f"任务 [{task_id}] 发生网络异常: {e}")

                # 指数退避重试
                if attempt < Config.MAX_RETRIES - 1 and not self._is_cancelled:
                    await asyncio.sleep(2 ** attempt)

    async def dispatch_all(self, user_id: str, total_tasks: int):
        """批量任务分发中心"""
        await self.start()
        
        tasks = []
        task_id = 1
        # 循环构建任务矩阵
        for url in Config.MOCK_URLS:
            for _ in range(total_tasks):
                tasks.append(self.send_task(url, task_id, user_id))
                task_id += 1

        logger.info(f"🚀 异步调度中心启动，共计部署 {len(tasks)} 个网络事件请求...")
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass
        finally:
            await self.close()
import asyncio
import time
import logging
from engine import AsyncNotificationEngine

logger = logging.getLogger("Main")

async def main():
    start_time = time.time()
    
    # 初始化引擎
    engine = AsyncNotificationEngine()
    
    # 模拟向 10 个用户批量分发通知
    await engine.dispatch_all(user_id="github_user_geng", total_tasks=10)
    
    logger.info(f"✨ 核心业务流执行完毕。总耗时: {time.time() - start_time:.4f} 秒")

if __name__ == "__main__":
    # 运行主事件循环
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序已被用户手动终止。")
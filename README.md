# 🚀 Async Notification Engine

基于 Python `asyncio` 与 `aiohttp` 构建的轻量级、高可用异步网络分发引擎。

## 💡 项目亮点

本项目跳出了传统的同步阻塞请求模型，采用现代微服务架构中常用的异步 I/O 方案。核心解决在面对多渠道、高并发的网络请求时，系统性能受限的问题。
（注：本项目旨在探讨网络工程中的并发调度与容灾防御机制，彻底解构“网络重放攻击/短信轰炸”的底层原理。）

* **🔥 高性能并发**：利用协程（Coroutine）实现单线程下的大规模并发任务调度。
* **🛡️ 流量控制**：通过 `asyncio.Semaphore` (信号量) 实现精确的并发限流，防止瞬间打满系统句柄或被目标服务器 WAF 拦截。
* **⚙️ 熔断与容灾**：内置基于指数退避（Exponential Backoff）的网络重试机制，从容应对网络抖动。
* **🔌 底层网络优化**：自定义 TCP 连接池大小，复用底层 TCP 握手。

## 🛠️ 技术栈

* Python 3.7+
* `asyncio` (核心事件循环)
* `aiohttp` (异步 HTTP 客户端)
* `python-dotenv` (环境变量管理)

## 📦 快速启动

1. **克隆项目**
   ```bash
   git clone [https://github.com/你的用户名/Async-Notification-Engine.git](https://github.com/你的用户名/Async-Notification-Engine.git)
   cd Async-Notification-Engine

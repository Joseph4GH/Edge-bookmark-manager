import asyncio
import aiohttp

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            # 判断HTTP响应状态码是否为200
            if response.status == 200:
                print(f"URL有效: {url}")
            else:
                print(f"URL无效: {url}, 状态码: {response.status}")
    except Exception as e:
        print(f"验证URL时出错: {url}, 错误: {e}")

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = [
        "https://confluence.honeywell.com/display/HONPS/Cyber+University",
        "https://honeywell.service-now.com/itdirect?id=order_something",
        "https://cilidog.fun/",
        "http://cilibao.biz/"
        # 添加更多URL进行验证
    ]
    asyncio.run(main(urls))

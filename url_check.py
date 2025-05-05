import requests
from urllib.parse import urlparse

def is_valid_url(url):
    """验证URL格式是否合法"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # 确保协议和域名都存在
    except:
        return False

def check_url_validity(url, timeout=5, max_retries=2):
    """验证URL是否有效，并处理超时问题"""
    if not is_valid_url(url):
        print(f"URL格式不合法: {url}")
        return False
    
    for attempt in range(max_retries + 1):  # 尝试最多max_retries+1次
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                print(f"URL有效: {url}")
                return True
            else:
                print(f"URL返回状态码 {response.status_code}: {url}")
                return False
        except requests.exceptions.Timeout:
            print(f"请求超时，尝试重新连接... ({attempt + 1}/{max_retries + 1})")
            continue
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return False
    return False

# 示例：验证一组URL
urls_to_check = [
    "https://confluence.honeywell.com/display/HONPS/Cyber+University",
    "https://honeywell.service-now.com/itdirect?id=order_something",
    "https://cilidog.fun/",
    "http://cilibao.biz/"
]

for url in urls_to_check:
    check_url_validity(url)
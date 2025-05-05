import os
import json
import logging
import requests
import asyncio
import aiohttp
'''
Edge书签管理器类
方法名	功能
__init__	初始化书签路径
load_bookmarks	读取书签 JSON 数据
save_bookmarks	保存修改后的书签数据
print_bookmark_tree	打印书签结构，支持显示路径
update_bookmark_url	更新指定 URL 的书签
delete_bookmark	删除指定名称或 URL 的书签
find_bookmark	查找书签，并返回匹配节点及其路径

'''



# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class EdgeBookmarkManager:
    def __init__(self, profile_name="Default", edge_profile_base=None):
        """
        :param profile_name: 浏览器的用户配置文件名称，默认为 "Default"
        :param edge_profile_base: Edge 用户数据根目录路径（默认为当前系统用户的 Edge 数据路径）
        """
        self.edge_profile_base = edge_profile_base or os.path.expanduser(
            "~/Library/Application Support/Microsoft Edge")
        self.profile_path = os.path.join(self.edge_profile_base, profile_name)
        self.bookmarks_path = os.path.join(self.profile_path, "Bookmarks")
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(f"初始化书签管理器，使用配置文件路径：{self.profile_path}")

    def load_bookmarks(self):
        """加载书签数据"""
        if not os.path.exists(self.bookmarks_path):
            self.logger.error(f"书签文件不存在: {self.bookmarks_path}")
            raise FileNotFoundError(f"Edge书签文件不存在，请检查路径是否正确: {self.bookmarks_path}")
        with open(self.bookmarks_path, 'r', encoding='utf-8') as f:
            self.logger.info("成功加载书签文件")
            return json.load(f)

    def save_bookmarks(self, data):
        """保存修改后的书签数据回文件"""
        with open(self.bookmarks_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.logger.info("书签文件已保存")

    def print_bookmark_tree(self, nodes, indent=0, path=""):
        """递归打印书签树，并显示路径"""
        for node in nodes:
            current_path = f"{path} > {node.get('name')}" if path else node.get('name')
            if node.get('type') == 'url':
                print('  ' * indent + f"└─ {node.get('name')} [{node.get('url')}] (路径: {current_path})")
            elif node.get('type') == 'folder':
                print('  ' * indent + f"├─ {node.get('name')}")
                if 'children' in node:
                    self.print_bookmark_tree(node['children'], indent + 1, current_path)
    
    async def remove_invalid_bookmarks_async(self, nodes):
        """异步清理失效的书签"""
        tasks = []
        for node in nodes:
            if node.get('type') == 'url':
                tasks.append(self.check_and_remove_url(node, nodes))
            elif node.get('type') == 'folder' and 'children' in node:
                await self.remove_invalid_bookmarks_async(node['children'])
        await asyncio.gather(*tasks)

    async def check_and_remove_url(self, node, nodes):
        """异步检查 URL 并删除无效书签"""
        url = node.get('url')
        if not await self.is_url_valid_async(url):
            self.logger.info(f"删除失效书签: {node.get('name')} [{url}]")
            nodes.remove(node)

    async def is_url_valid_async(self, url):
        """异步检查 URL 是否有效"""
        try:
            # 设置超时时间为10秒
            timeout=aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True, timeout=timeout) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.warning(f"URL 无效: {url} ({e})")
            return False
    '''
    if __name__ == "__main__":
    manager = bm.EdgeBookmarkManager(profile_name="Default")
    data = manager.load_bookmarks()

    # 异步清理失效书签
    asyncio.run(manager.remove_invalid_bookmarks_async(data['roots']['bookmark_bar']['children']))

    # 打印书签树并保存
    manager.print_bookmark_tree(data['roots']['bookmark_bar']['children'])
    manager.save_bookmarks(data)
    '''   
    def update_bookmark_url(self, nodes, old_url, new_url):
        """递归更新书签URL"""
        for node in nodes:
            if node.get('type') == 'url' and node.get('url') == old_url:
                node['url'] = new_url
                self.logger.info(f"已更新 URL: {old_url} -> {new_url}")
            elif node.get('type') == 'folder' and 'children' in node:
                self.update_bookmark_url(node['children'], old_url, new_url)

    def delete_bookmark(self, nodes, target_name=None, target_url=None):
        """递归删除书签"""
        i = 0
        while i < len(nodes):
            node = nodes[i]
            if node.get('type') == 'url':
                if (target_name and node.get('name') == target_name) or \
                   (target_url and node.get('url') == target_url):
                    self.logger.info(f"删除书签: {node.get('name')} [{node.get('url')}]")
                    nodes.pop(i)
                    continue
            elif node.get('type') == 'folder' and 'children' in node:
                self.delete_bookmark(node['children'], target_name, target_url)
            i += 1

    def find_bookmark(self, nodes, target_name=None, target_url=None, return_first=True):
        """递归查找书签并记录路径"""
        results = []

        def recursive_search(current_nodes, path=""):
            found = []
            for node in current_nodes:
                current_path = f"{path} > {node.get('name')}" if path else node.get('name')
                if node.get('type') == 'url':
                    if (target_name and node.get('name') == target_name) or \
                       (target_url and node.get('url') == target_url):
                        item = {'node': node, 'path': current_path}
                        if return_first:
                            return item
                        found.append(item)
                elif node.get('type') == 'folder' and 'children' in node:
                    child_result = recursive_search(node['children'], current_path)
                    if isinstance(child_result, list):
                        found.extend(child_result)
                    elif child_result:
                        found.append(child_result)
            return found

        result = recursive_search(nodes)
        if return_first and isinstance(result, list) and len(result) > 0:
            return result[0]
        return result
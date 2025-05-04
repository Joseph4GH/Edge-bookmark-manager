import os
import json

def print_bookmark_tree(nodes, indent=0):
    """递归函数，用来打印书签树
    :param nodes: 当前层级的书签节点列表
    :param indent: 当前缩进级别
    """
    for node in nodes:
        if 'type' in node and node['type'] == 'url':
            # 如果是书签节点，打印URL信息
            print('  ' * indent + f"└─ {node.get('name')} [{node.get('url')}]")
        elif 'type' in node and node['type'] == 'folder':
            # 如果是文件夹节点，打印文件夹名称并递归处理子节点
            print('  ' * indent + f"├─ {node.get('name')}")
            if 'children' in node:
                print_bookmark_tree(node['children'], indent + 1)

def update_bookmark_url(nodes, old_url, new_url):
    """递归函数,用于更新书签树中的指定URL
    :param nodes: 当前层级的书签节点列表
    :param target_name: 要删除的书签名称(可选）
    :param target_url: 要删除的书签URL(可选）
    """
    for node in nodes:
        if 'type' in node and node['type'] == 'url':
            if node.get('url') == old_url:
                node['url'] = new_url  # 更新URL
        elif 'type' in node and node['type'] == 'folder' and 'children' in node:
            update_bookmark_url(node['children'], old_url, new_url)  # 递归处理子节点
''' 使用方法
if __name__ == "__main__":
    bookmarks_path = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Bookmarks")

    if not os.path.exists(bookmarks_path):
        print("Edge书签文件不存在,请检查路径是否正确")
    else:
        with open(bookmarks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 更新书签栏中的URL
        update_bookmark_url(data['roots']['bookmark_bar']['children'], "https://old-url.com", "https://new-url.com")

        # 更新其他书签中的URL
        update_bookmark_url(data['roots']['other']['children'], "https://old-url.com", "https://new-url.com")

        # 将修改后的书签写回文件
        with open(bookmarks_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
'''

def delete_bookmark(nodes, target_name=None, target_url=None):
    """递归地从书签树中删除匹配的节点。
    :param nodes: 当前层级的书签节点列表
    :param target_name: 要删除的书签名称(可选）
    :param target_url: 要删除的书签URL(可选）
    """
    i = 0
    while i < len(nodes):
        node = nodes[i]
        if 'type' in node:
            if node['type'] == 'url':
                # 检查是否匹配名称或URL
                if (target_name and node.get('name') == target_name) or (target_url and node.get('url') == target_url):
                    nodes.pop(i)  # 删除该节点
                    continue  # 索引不增加，因为后面的元素已经前移
            elif node['type'] == 'folder' and 'children' in node:
                # 递归处理子文件夹
                delete_bookmark(node['children'], target_name, target_url)
        i += 1
'''
使用方法
if __name__ == "__main__":
    bookmarks_path = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Bookmarks")

    if not os.path.exists(bookmarks_path):
        print("Edge书签文件不存在,请检查路径是否正确")
    else:
        with open(bookmarks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 删除书签栏中的指定书签 (例如按名称或URL)
        delete_bookmark(data['roots']['bookmark_bar']['children'], target_name="示例书签", target_url=None)

        # 删除“其他书签”中的指定书签
        delete_bookmark(data['roots']['other']['children'], target_url="https://example.com")

        # 将修改后的书签写回文件
        with open(bookmarks_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
'''

def find_bookmark(nodes, target_name=None, target_url=None, return_first=True):
    """递归查找匹配的书签节点。
    :param nodes: 当前层级的书签节点列表
    :param target_name: 要查找的书签名称（可选）
    :param target_url: 要查找的书签URL（可选）
    :param return_first: 如果为 True，返回第一个匹配项；否则返回所有匹配项的列表
    :return: 匹配到的书签节点（dict）或列表（list），如果没有找到则返回 None 或空列表
    """
    results = []

    def recursive_search(current_nodes):
        for node in current_nodes:
            if node.get('type') == 'url':
                # 判断是否匹配名称或URL
                if (target_name and node.get('name') == target_name) or \
                   (target_url and node.get('url') == target_url):
                    if return_first:
                        return node
                    else:
                        results.append(node)
            elif node.get('type') == 'folder' and 'children' in node:
                child_result = recursive_search(node['children'])
                if not return_first:
                    results.extend(child_result)
                elif child_result:
                    return child_result
        return None

    result = recursive_search(nodes)

    if return_first:
        return result
    else:
        return results
'''
使用方法
if __name__ == "__main__":
    bookmarks_path = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Bookmarks")

    if not os.path.exists(bookmarks_path):
        print("Edge书签文件不存在,请检查路径是否正确")
    else:
        with open(bookmarks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 查找第一个匹配的书签
        bookmark = find_bookmark(data['roots']['bookmark_bar']['children'], target_name="示例书签", return_first=True)
        if bookmark:
            print("找到书签:", bookmark)
        else:
            print("未找到指定书签")
        
        # 查找所有匹配的书签
        bookmarks = find_bookmark(data['roots']['other']['children'], target_url="https://example.com", return_first=False)
        if bookmarks:
            print("找到以下书签:")
            for bm in bookmarks:
                print(bm)
        else:
            print("未找到指定URL的书签")
'''

def read_and_print_edge_bookmarks():
    # 定义书签文件路径
    bookmarks_path = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Bookmarks")
    
    if not os.path.exists(bookmarks_path):
        print("Edge书签文件不存在，请检查路径是否正确")
        return
    
    # 打开并读取书签文件
    with open(bookmarks_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 分别处理书签栏和其他书签
    print("书签栏:")
    print_bookmark_tree(data['roots']['bookmark_bar']['children'])
    
    print("\n其他书签:")
    print_bookmark_tree(data['roots']['other']['children'])

if __name__ == "__main__":
    read_and_print_edge_bookmarks()
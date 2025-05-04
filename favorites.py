import os
import json

def read_edge_bookmarks():
    # 定义书签文件路径
    bookmarks_path = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Bookmarks")
    
    if not os.path.exists(bookmarks_path):
        print("Edge书签文件不存在，请检查路径是否正确")
        return
    
    # 打开并读取书签文件
    with open(bookmarks_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 解析书签条目
    def traverse_bookmarks(nodes):
        for node in nodes:
            if 'type' in node and node['type'] == 'url':
                print(f"标题: {node.get('name')}, URL: {node.get('url')}")
            elif 'type' in node and node['type'] == 'folder':
                print(f"文件夹: {node.get('name')}")
                traverse_bookmarks(node.get('children', []))
    
    # 遍历根节点下的书签栏和其他书签
    traverse_bookmarks(data['roots']['bookmark_bar']['children'])
    traverse_bookmarks(data['roots']['other']['children'])

if __name__ == "__main__":
    read_edge_bookmarks()
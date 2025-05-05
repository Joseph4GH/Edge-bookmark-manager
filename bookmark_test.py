import bookmarkutility as bm
import logging
import asyncio

if __name__ == "__main__":
    # 设置日志级别
    logging.basicConfig(level=logging.INFO)

    # 加载 Default 配置文件
    manager_default = bm.EdgeBookmarkManager(profile_name="Default")
    data_default = manager_default.load_bookmarks()
   
    # 打印书签结构
    manager_default.print_bookmark_tree(data_default['roots']['bookmark_bar']['children'])
   
    # 加载 Profile 1 配置文件
    '''
    manager_profile1 = bm.EdgeBookmarkManager(profile_name="Profile 1")
    data_profile1 = manager_profile1.load_bookmarks()
    manager_profile1.print_bookmark_tree(data_profile1['roots']['bookmark_bar']['children'])
    manager_profile1.save_bookmarks(data_profile1)
    '''

    # 查找书签并获取路径
    result = manager_default.find_bookmark(data_default['roots']['bookmark_bar']['children'], target_name="车生活", return_first=True)
    if result:
        print(f"\n找到书签: {result['node']}，路径为: {result['path']}")

    # 异步清理失效书签
    asyncio.run(manager_default.remove_invalid_bookmarks_async(data_default['roots']['bookmark_bar']['children']))


    # 查找所有匹配项
    results = manager_default.find_bookmark(data_default['roots']['other']['children'], target_url="https://pvp.qq.com/match/kpl/kingproleague/index.html", return_first=False)
    if results:
        print("\n找到以下书签:")
        for item in results:
            print(f"{item['node']}，路径为: {item['path']}")

    # 更新书签 URL 示例
    manager_default.update_bookmark_url(data_default['roots']['bookmark_bar']['children'],
                                "https://wx.qq.com/",
                                "https://wx.qq.com/index.html")

    # 删除书签示例
    manager_default.delete_bookmark(data_default['roots']['bookmark_bar']['children'], target_name="软件下载页面 - 射频技术学习")

    # 保存修改
    manager_default.save_bookmarks(data_default)
# Proj-03

Simple Netease Cloudmusic Lyrics Downloader

> 简易网易云音乐歌词下载器

## 描述

我们将要编写程序，从网易云音乐平台上下载LRC格式歌词文件到本地。

> 其实在GitHub上也有很多做这个的项目了，可以去看看。

## 准备

照例创建项目文件夹，创建虚拟环境，安装依赖。这次我们换一种网页解析方法，使用`BeautifulSoup`库。

```powershell
pip install beautifulsoup4 requests types-requests retry
```

> Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.

网易云音乐只有少数接口未做鉴权，能直接访问。虽然也有第三方项目实现了nodejs形式的接口代理，但是对于仅下载歌词这样的偏简单的操作来说，似乎有些大材小用了。
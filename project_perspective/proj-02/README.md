# Proj-02

Simple Video Downloader for Bilibili

> 简易B站视频下载器

## 背景

还在为自己不能随时随地离线~~溜冰~~观影吗，还在为心爱的视频被申鹤干掉而感到惋惜吗，还在坐视自己的收藏夹逐渐变得空旷吗，现在就将你喜欢的视频留存到硬盘中！~~（草~~

> 其实在GitHub上已经能找到很多写好的下载器，但是果然还是自己实现一个比较舒服（
>
> 你也可以去参考他们的代码看看他们是如何实现的。

在本节中我们要开始使用B站的API了。很巧(?)，有一个质量很高的进行B站API收集的仓库，本节中很多API参考都来自于它，它就是[Bilibili-API-Collect](https://github.com/SocialSisterYi/bilibili-API-collect)（简称`BAC`）。

## 准备

首先照例创建项目文件夹，创建虚拟环境，安装依赖`requests`。

为了能够使用B站的被加密的API，我们需要大佬们的帮助。从BAC的一个子页面获取到[WBI签名的Python实现](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md#python)，将它保存为`wbi.py`，「稍作修改」使它能作为模块被使用。

之后我们就可以更方便地使用B站的API了。

查阅BAC，得到[获取视频详情](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/info.md)和[获取视频流](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/videostream_url.md)的API，将它们封装成函数，保存到`biliapis.py`中。


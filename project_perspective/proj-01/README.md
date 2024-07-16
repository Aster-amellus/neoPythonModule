# Proj-01

Simple Video Cover Extractor for Bilibili  

> 简易B站封面提取器  

> 由于这是我们的第一节，仍然会杂一些比较基础的东西。

## 背景

> 想起我最开始学Py的时候，也是从B站下手的（逃）

我们在刷B站的时候，有可能经常会看到一些用某些「好书」来当作封面的视频。为了丰富我们的「知识库存」，我们势必要拿到封面去做以图搜源。 ~~为此有些B站老哥在视频评论区向鸽子UP主苦苦求了几万年（大雾）~~

啊肯定有些机智的朋友知道些别的途径 ~~，像用那些在线工具啊、用「一个■函」APP啊、在网页端按Ctrl+U然后慢慢找啊之类的。~~ 不过我们这次要来尝试自己写一写用来做这个的程序。

## 准备工作

由于这是我们第一次正式开始搓Python项目，我们需要养成一些良好的习惯。 ~~不要像我这样埋头弄三年结果PEP8都不知道~~

在上一节我们已经装好了Python。由于这次我们会用到第三方库，所以要配置虚拟环境。

> 你也不想污染在上一节中刚弄好的全局环境罢（）

照例创建一个项目文件夹，然后使用VSCode打开，信任此文件夹的作者。

### 创建虚拟环境

接下来我们创建虚拟环境（通过VSCode和Venv）。

按`Ctrl+Shift+P`组合键呼出VSCode顶部的运行指令菜单，找到`Python: Create Environment...`

![Create Env 1](./images/create_env_1.png)

环境类型选择`Venv`

![Create Env 2](./images/create_env_2.png)

选择合适的解释器

![Create Env 3](./images/create_env_3.png)

等待创建完成后，在VSCode窗口右下角确认选择的虚拟环境是否正确

![Create Env 4](./images/create_env_4.png)

> 关于手动创建，参见[补录](./notes.md#手动创建虚拟环境)。

至此，虚拟环境创建完成。

### 安装第三方库

由于Python的标准库中的网络请求库使用体验比较糟糕，所以这里选择第三方库`requests`作为替代。

在VSCode中打开一个新的终端
> 按 `Ctrl+Shift+`\` 启动一个新的终端，或者按 `Ctrl+`\` 切换到已打开的终端。

安装请求库`requests`

```powershell
pip install requests types-requests
```
> 安装`types-requests`是为了支持`mypy`静态检查

安装XML解析库` lxml`

```powershell
pip install lxml
```

等待完成后，将已安装的包固定为`requirements.txt`

```powershell
pip freeze > ./requirements.txt
```

> 这样一来下次安装时就可以使用`-r`参数一键搞定了。

## 开始喵

### 寻找途径

首先我们要明确我们的目标，是要获取到B站的某个视频的封面是吧。想想我们有哪些方法。总之找一个视频做样本罢。

刷刷首页——袜这个封面好卡瓦，就它了！ ~~（草~~

![Sample Video](./images/sample_video_preview.png)

获得它的网址：`https://www.bilibili.com/video/BV1iW421R71g`

> 网址后面可能会跟上一串乱七八糟的东西（用来追踪用户行为的特征字段），但是熟悉B站的朋友们都知道，定位一个视频只需要AV号（记作`aid`或`avid`）或者BV号（记作`bvid`）就行了。

得到它的关键数据`BV1iW421R71g`（bvid），保留备用。

进入视频详情页，将光标悬停在分享按钮上，右击弹出的分享框中的封面，可得到封面网址。

![Get Cover Manually](./images/get_cover_manually.png)

得到了这样一个URL：`https://i0.hdslb.com/bfs/archive/2ff337f507754e0d172298d3e9b815413b4a63b7.jpg@518w_290h_1c_!web-video-share-cover.avif`

它看上去很小，并且保存下来也是`.avif`文件，不便查看。

但是细心观察不难看出，整个URL由图片本体和调整参数组成，去除`@`符及其往后的内容再打开便是原始图像了。

> 这样做一般是为了减小带宽压力，将图片在服务端压缩后再提供给客户端。

现在我们拿到了封面URL，可以反过来用URL来定位它在网页中的位置了。

按下`F12`打开开发者选项，找到`元素`选项卡，`Ctrl+F`打开查找选项再一粘贴搜索，欸怎么没有呢

将搜索范围缩小到后半段的图片哈希值，成功找到元素。

![Find Element](./images/find_element.png)

如果之后要通过`lxml`库解析网页的话，现在就记下这个元素的`XPath`备用。

> 注意网页的结构具有时效性，因为你不知道它多久会再改版，页面结构的改变会使你得到的`XPath`之类的记录元素位置的信息失效。
>
> 因此更理想的方法一般是找到网页的API，直接请求API拿到信息。不过现在B站的很多API都有加密，所以暂时先留到以后再说，本节我们先做这个。

### 写！

新建一个py文件，就叫`main.py`好了。

我们将要实现一个函数，这个函数接收视频的URL，返回视频封面的URL。大概长这个样子。

```python
def get_video_cover(url: str) -> str:
    pass
```

基础语法参见[补注](./notes.md#关于基础语法)或者另一组写的文档，或者搜索引擎启动

实践流程见[notebook](./example.ipynb)

### 优化！

我们已经在[notebook](./example.ipynb)编写了一遍最简单的代码。接下来我们将它封装为函数。

完整代码见source

## 结束了喵！

现在程序还有一些地方值得改进，尝试自己解决吧！
- 程序不会检查用户的输入，这意味着它会尝试请求任何用户输入的东西，甚至不管它是不是URL。
  > Hint: 尝试提取输入中的AV号或BV号，拼接成网页URL后再拿去做请求。
- 程序只是打印出了封面URL，却没有将它自动下载下来。为它加上这个功能吧！
- （续）难道下载的文件的名字要叫那一长串哈希字符串吗？尝试获取视频的标题，然后将它当作下载的封面的文件名吧！



以及，去尝试通过这种方式获取更多网页中的信息吧！

> 注意请勿违反国家法律法规，滥用造成的任何后果都与我们无关。
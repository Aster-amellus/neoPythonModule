# Proj-01

Simple Video Cover Extractor for Bilibili  

> 简易B站封面提取器  

> 由于这是我们的第一节，仍然会杂一些比较基础的东西。熟悉Python的朋友们可以继续量子速读了。

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

等待创建完成后，在VSCode窗口右下角确认选择的虚拟环境

![Create Env 4](./images/create_env_4.png)

> 关于手动创建，参见[补录](./notes.md#手动创建虚拟环境)。

至此，虚拟环境创建完成。

### 安装第三方库

由于Python的标准库中的网络请求库使用体验比较糟糕，所以这里选择第三方库`requests`作为替代。

在VSCode中打开一个新的终端
> 按 `Ctrl+Shift+`\` 启动一个新的终端，或者按 `Ctrl+`\` 切换到已打开的终端。

```powershell
pip install requests types-requests 
```
> 安装`types-requests`是为了支持`mypy`静态检查
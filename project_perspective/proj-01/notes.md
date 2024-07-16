# 补注喵

## 关于虚拟环境

### 虚拟环境是什么

是一种用于隔离项目依赖关系的工具。每个虚拟环境都有自己的解释器和库。

> 通常虚拟环境中的解释器会指向全局环境中的解释器，也就是说在爆改全局环境（主要是更改解释器位置）后别忘了重建你的虚拟环境。

### 为什么需要虚拟环境

主要是能够避免不同项目的依赖的冲突。比如有一个项目需求低版本的`numpy`但是另一个需求高版本，把它们放在同一个环境中尝试安装依赖时就会出问题。

### 手动创建虚拟环境

在VSCode中创建详见正文。这里尝试讲解手动使用`venv`模块安装。

在项目文件夹中打开终端，使用下面的指令创建虚拟环境。

```powershell
python -m venv ./.venv
```

大概就是调用Python的一个叫`venv`的模块，在当前目录下的`.venv`文件夹下创建虚拟环境。

> 虚拟环境所在文件夹命名为`.venv`的原因
>
> 嗯，主要是为了跟VSCode的创建行为保持一致，此外`.gitignore`里大概一般也是这么写的。

稍等一下就能完成。很快地，项目文件夹下多出了一个叫`.venv`的文件夹。

在终端下执行`./.venv/Scripts/activate`就能手动激活虚拟环境。

> 若遇到`powershell`阻止，按照提示进行设置即可。

要检查是否处于虚拟环境，使用powershell指令`Get-Command`查找`python`解释器的位置，判断一下是否处于正确的位置（`.venv/Scripts/python`）就行了。

## 关于`requests`库

很帅的一个多线程安全的网络请求库。个人觉得比Python自带的`urllib`库好用太多。

## 关于基础语法

> 仅尝试讲解正文中使用到的

### 导入模块

`import`语句用于导入模块。

> 有一个叫`importlib`的库也可以用来导入模块，而且动态

常用的写法：

```python
import math 
import os.path
# 直接导入
from lxml import etree  
# 从某个模块中导入对象
from tkinter import *   
# 导入某个模块中的所有对象到当前命名空间中，强烈不推荐
from tkinter import messagebox as msgbox    
# 换个名称导入
from urllib import request, parse   
# 导入多个对象
# 上述指定了模块名的叫做绝对导入，从项目的根目录开始导入模块（推荐）。

# 下面的是相对导入，一般用在库的内部模块之间。
from . import utils 
from ..module_a import func
```
> 向上超过当前文件所在路径的相对导入是不推荐的，[PEP 8](https://peps.python.org/pep-0008/#imports) 说的。

关于机制细节，Python会按顺序搜索`sys.path`列表中的每个目录，查找与模块名匹配的文件。

> `sys.path`默认包括：
> - 当前文件所在目录
> - `%PYTHONPATH%`环境变量指定的目录
> - 标准库目录，通常是`python/Lib`
> - 安装的第三方包的目录，通常是`python/Lib/site-packages`

> 你甚至可以手动为`sys.path`添加路径，让它去额外的目录找模块
> ——但是不推荐就是了

更多内容参见[官方文档](https://docs.python.org/zh-cn/3/reference/simple_stmts.html#import)，或者问AI去

yysy，Python官方的文档怎么着都比我写得好罢，快去看。

### 函数

使用`def`或者`lambda`定义，后者叫做匿名函数。

嗯你问函数是什么…… ~~函数它就是函数啊~~

Python中的函数是**封装**了代码块的**对象**。使用它可以复用代码，减少重复。


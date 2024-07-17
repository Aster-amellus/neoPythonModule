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

很优雅的一个多线程安全的网络请求库。个人觉得比Python自带的`urllib`库好用。

> 你也可以尝试只用Python标准库实现这个项目，这是可以做到的！

## 关于基础语法

> 这里仅尝试讲解正文中使用到的。
>
> 快去看[官方文档](https://docs.python.org/zh-cn/3/reference/index.html)

> *Python很容易入门，语法限制也很少。但这不意味着它很简单，更不意味着它很随便。*
>
> —— MelodyEcho

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

快去看[官方文档](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#function)ww

一个典型的函数大概长这样：
```python
#      参数  参数类型标注（可选）
#        vv vvvvvvvvvvv
def join(ss : list[str]) -> str:
#   ^^^^---------------- ^^^^^^
#  函数名    参数列表    返回值类型标注（可选）
    return "".join(ss)
```

> 为什么要做类型标注(Type Hints)？
>
> 你可能觉得Python是一种动态类型语言，类型标注似乎没什么用。但实际上，类型标注有很多好处。除了提升代码的可维护性和可读性，以及便于生成文档之外，在面对稍微复杂一些的代码时，单靠IDE进行类型推导会显得有些吃力。编写代码时顺手加上类型标注，可以帮助IDE进行自动补全和错误检测等工作。
>
> 不过最终写不写还是取决于你就是了。

### 异常

[官方文档](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-try-statement)

#### 异常捕获

完全体的异常处理大概像这样：

```python
try:
    # 可能会出错的代码
    x = 1 / int(input("Your Number:"))
    assert 1 == 0, "oops, 1 != 0"
except ZeroDivisionError as e:
    ... # 发生除零错误时会执行的代码
except AssertionError as e:
    ... # 发生断言错误时会执行的代码
except Exception as e:
    ... # 发生一般错误时会执行的代码
else:
    ... # 没有发生错误时会执行的代码
finally:
    ... # 不管发生了什么都会执行的代码
```

异常匹配顺序从上到下，匹配成功后便不再继续匹配。若最终都没有匹配上则错误还是会被抛出（但`finally`块仍然有效）

> 关于裸`except:`
>
> 等价于`except BaseException:`，可以捕获**所有**异常，包括系统退出和中断的异常，像 `SystemExit`、`KeyboardInterrupt` 和 `GeneratorExit`。因为捕获得太多了而且语义不明确所以不建议使用。
>
> 一般日常建议使用`except Exception:`。就算你真的想捕获系统级异常，也应该使用`except BaseException:`进行平替，因为它的语义更明确一些。

> `...`？
>
> 没错`...`也是一个对象，叫做`Ellipsis`，表示省略或占位。在某些特殊的场景很有用（比如`numpy`中创建多维数组）。

`except ... as ...`可以将捕获的异常实例保存到一个变量中，方便后续做处理

#### 异常抛出

使用`raise`语句抛出一个异常**对象**。

> 在抛出之前，先要将异常类实例化，在实例化时可以传递具体的错误消息。（不实例化就抛出是py2的做法）

```python
raise RuntimeError("A runtime error.")
```

`raise ... from ...`可以从一个已有的异常实例抛出一个新异常，原有异常会被保存在新异常的`__cause__`属性中。常用在`except`块下。

### 变量作用域与生命周期

Python中的局部变量的作用域是它直接所在的函数，全局变量的则是它所在的模块。

在一个变量超出它的作用域，且它的引用计数变为`0`时，它就会被删除。

> 对于循环引用，Python的垃圾回收器负责清理它们。可以通过调用`gc.collect()`来手动执行垃圾回收。

> Python没有像C/C++或Java那样的块级作用域(Block Scope)，在控制结构 (`if`/`while`/`match`/`for`/`...`) 中声明的变量在控制结构之外依然可以访问，只要是在相同的函数或全局作用域中。

~~来点C语言笑话：~~
```c
void just_a_test(void){
    // 我 有 异 域 症
    {int i;}
    {i = 0;}
}
```

### 引用与拷贝

Python中的**所有数据都是对象**。变量名实际上是指向这些对象的引用。当你赋值一个变量时，你只是将这个变量名绑定到某个对象上，并不复制对象本身。

```python
>>> a = [1, 2, 3]
>>> a
[1, 2, 3]
>>> b = a
>>> b.append(4)
>>> a
[1, 2, 3, 4]
```

> 要复制对象，可使用`copy`库中的`copy()`和`deepcopy()`函数，或某些对象内置的`copy()`方法
>
> - `copy()`: 浅拷贝，仅复制顶层结构，产生的新对象内层仍然共享。
> - `deepcopy()`: 深拷贝，复制整个对象，产生的新对象完全独立

Python中的对象分为可变和（e.g.列表/字典/集合）不可变（e.g.整数/字符串/元组）两种。

对于不可变的对象，对它做修改或赋值会在原地生成一个新的对象，再将这个对象绑定到变量上。这就是数字/字符串变量之间进行赋值看起来像拷贝的原因。

```python
>>> a = 1
>>> b = a
>>> b = 2
>>> a
1
>>> b
2
```

> 常见的不可变对象包括：
> - 整数`int`
> - 浮点数`float`
> - 字符串`str`
> - 元组`tuple`
> - 布尔值`bool`
> - 字节串`bytes`
> - 不可变集合`frozenset`
>
> 详见[官方文档](https://docs.python.org/zh-cn/3/reference/datamodel.html)

### with语句

[官方文档](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#with)

对于很多对外部资源有引用的对象，可以使用`with`来进行上下文管理。

离开`with`语句块时，对象的`close()`方法会被自动调用。

```python
with open("./result.txt", "w+", encoding="utf-8") as fp:
    fp.write("Pretending to be data")
```

> `requests`中的请求也可以用噢，看看[本节的项目代码](./source.py)？
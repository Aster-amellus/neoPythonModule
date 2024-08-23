# 补注喵

For Proj-04

## 并发编程

Python中的并发有三种形式，多线程、多进程和多协程[^1]。其中多线程和多协程适合IO密集型的场合，多进程则更适合CPU密集型的场合。

在对IO要求极高的场合，可以将它们结合起来使用[^2]。由于GIL的存在，Python中的CPU密集型任务一般会通过多进程完成[^3]。

可阅读[这篇博客](https://www.glowmem.com/archives/python-concurrency)[^4]了解更多信息w

这次我们使用多线程来应对并发网络请求。

[^1]: 协程是异步的一种实现方式
[^2]: 不过这种情况高性能异步应该也够了大概，在有现成的第三方库支持的情况下
[^3]: 因为每个进程都会获得一个GIL而线程不行。当然也可以使用C/C++编写扩展模块来绕过这个限制，或者使用一些高性能第三方库
[^4]: 关注律姐姐喵，关注律姐姐谢谢喵

### 多线程

Python中一般使用标准库`threading`进行多线程操作。参见[官方文档](https://docs.python.org/zh-cn/3.7/library/threading.html)。

线程能够共享相同的内存和资源，所以需要处理访问冲突（竞争条件/数据竞争）的问题。在多个线程可能同时读写共享资源时需要加锁。

很多时候直接把可调用对象作为`Thread`类的参数`target`传进去，然后操作实例化出来的Thread对象就能满足要求。但对于更复杂的需求，还是继承于`Thread`类再自己实现一些功能更方便。

## 依赖注入

依赖注入是一种设计模式，将对象的依赖关系从内部转移到外部，由外部代码来管理和传递依赖对象。

正文中提到的 API 类，实例化时需要传入发送请求时需要的`requests.Session`对象，这就是一种依赖注入。

依赖注入有助于提高代码的可维护性、可测试性和灵活性。

## 一些小花招

### _

临时变量，或者需要忽略的变量可以用且仅用单个下划线`_`命名。

比如……

```python
# 在仅需要 walk *文件*的时候
for root, _, files in os.walk():
    for file in files:
        ...
# 在解包正则表达式匹配结果的时候
a, _, b, _ = re.findall(r"...", s, re.I)[0] # 没有检查结果，请勿模仿
```

### :=

`:=`，「海象运算符」，在 Python `3.8+` 版本中可用，允许在表达式中进行赋值操作，用于减少冗余代码和重复计算次数。

```python
def find_bvid(s: str) -> str | None:
    if _ := re.search(r"(?<![A-Za-z])(BV[a-zA-Z0-9]{10})", s):
        return _.group(1)
    return None
```

算是不错的语法糖，但是同时也需要注意可读性（）

### 三目运算符

> 也被称作条件表达式

语法是：

```py
value_if_true if condition else value_if_false
```

表达式将会根据`condition`的值决定整个表达式的结果是`value_if_true`还是`value_if_false`的值。

一个简单的例子，求得两个值中的较大值：

```py
x = 10
y = 20
max_value = x if x > y else y
```

可以嵌套使用，但这时可读性很差。这时建议拆成普通的`if-else`系列语句。

<details><summary>别看 有史</summary>

```py
# (省略的定义用`...`表示)
...
class VideoWorker(threading.Thread, ...):
    ...
    def _worker(self):
        ...
        finalfile = os.path.join(
            self._savedir,
            filename_escape(
                (
                    f"{title}"
                    + (
                        (f"_P{pindex+1}" if len(cidlist) > 1 else "")
                        if self._correct_pindex is None
                        else f"_P{self._correct_pindex}"
                    )
                    + (f"_{ptitle}" if ptitle != title or self._correct_ptitle else "")
                    + (
                        f"_{bilicodes.stream_dash_audio_quality.get(aqid)}"
                        if self._audio_only
                        else f"_{bilicodes.stream_dash_video_quality.get(vqid)}"
                    )
                )
                + (
                    (".flac" if is_lossless else ".mp3")
                    if self._audio_only
                    else (".mkv" if is_lossless else ".mp4")
                )
            ),
        )
        ...
    ...
```

~~懒得喷~~

</details>

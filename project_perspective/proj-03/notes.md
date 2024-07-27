# 补注喵

for Proj-03

## 一些工具的介绍

<details><summary>让GPT-4o做了张表，可以看看对比</summary>

| 特性             | Pylance                               | Pylint                               | Mypy                             | Flake8                                   |
| ---------------- | ------------------------------------- | ------------------------------------ | -------------------------------- | ---------------------------------------- |
| 主要功能         | 提供智能代码补全、类型检查和错误检测  | 静态代码分析，检测代码中的潜在问题   | 类型检查，确保代码符合类型提示   | 静态代码分析，检测代码中的样式和潜在问题 |
| 集成开发环境     | VSCode                               | 独立工具，但与各种IDE兼容            | 独立工具，但与各种IDE兼容        | 独立工具，但与各种IDE兼容                |
| 类型检查         | 是                                    | 部分支持（主要通过推断类型）         | 是                               | 否                                       |
| 代码样式检查     | 否                                    | 是                                   | 否                               | 是                                       |
| 配置难易度       | 简单（主要通过 VSCode 设置）         | 中等（通过配置文件进行详细配置）     | 简单（通过配置文件进行详细配置） | 简单（通过配置文件进行详细配置）         |
| 错误报告详细程度 | 高                                    | 高                                   | 中等                             | 中等                                     |
| 性能             | 高（由于其基于静态分析和类型推断）    | 中等（进行详细的静态分析，可能较慢） | 高（主要进行类型检查，性能较好） | 高（主要进行样式检查，性能较好）         |
| 主要用途         | 提高开发效率，减少错误                | 提高代码质量，减少潜在问题           | 确保类型正确性，减少类型相关错误 | 提高代码质量，确保符合编码规范           |
| 扩展性           | 通过插件扩展功能                      | 通过插件和自定义规则扩展功能         | 主要功能集中在类型检查           | 通过插件和自定义规则扩展功能             |
| 社区支持         | 强（由于与 VSCode 集成，社区用户多） | 强（长期以来受到广泛使用）           | 强（逐渐普及，社区支持逐渐增加） | 强（广泛使用，社区支持多）               |

</details>

以下的则是我写的，说法也不一定准确就是了。

### Black

[Black on PyPI](https://pypi.org/project/black/)，以及它的[在线演示网站](https://black.vercel.app/)

本身是个命令行工具，但是在VSCode扩展`Black Formatter`中有搭载，能够即装即用。

相当「固执」的代码格式化工具，仅提供那么几个配置选项。

在一段代码前加上注释`# fmt: off`，后加上`# fmt: on`，可以让`black`不格式化这段代码。包含`# fmt: skip`的单行也不会被格式化。更多使用方法参见Black的[使用文档](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)。

> `black`的格式化可能不会完全满足别的风格检查工具的要求

### Flake8

[Flake8 on PyPI](https://pypi.org/project/flake8/)

同样是一个命令行工具，但在VSCode扩展`Flake8`中也有搭载，能够即装即用。

速度超快的风格检查工具。

在代码中使用注释`# noqa`或`# noqa: <具体条目>`来禁用某行的全部或某些风格检查（以逗号分隔）。或者在某个程序文件中包含`# flake8: noqa`来禁用此文件内的所有检查。

> 例如：`# noqa: F401,E234`

更多信息参见Flake8的[使用文档](https://flake8.pycqa.org/en/latest/index.html)

> noqa = NO-QA (NO Quality Assurance)

### Pylint

[Pylint on PyPI](https://pypi.org/project/pylint/)

仍然是一个命令行工具，但在VSCode扩展`Pylint`中有搭载，能够即装即用。

速度稍慢的静态分析工具，包含风格检查。

在参数中添加`--disable=<具体条目或类型>`来禁用某些检查（以逗号分隔）。

可在Pylint的[官方文档](https://pylint.readthedocs.io/en/stable/user_guide/messages/messages_overview.html)中查阅所有条目。

> 例如：`--disable=C,R,line-too-long,W4903`

### Mypy

[Mypy on PyPI](https://pypi.org/project/mypy/)

是命令行工具。在VSCode扩展`Mypy Type Checker`中有搭载。另一个可用的替代扩展`Mypy`中没有搭载，如果使用则需要安装。

强大的类型检查工具。

可在Mypy的[官方文档](https://mypy.readthedocs.io/en/stable/)中查阅更多信息。

### isort

[isort on PyPI](https://pypi.org/project/isort/)

是命令行工具。且在VSCode扩展`isort`中有搭载。

import语句顺序检查与自动排序工具。

在模块的docstring里加上`isort:skip_file`以忽略整个文件，使用注释`# isort:skip`以忽略一整行。

更多信息参见isort的[官方文档](https://pycqa.github.io/isort/)

**可能与`Black`冲突**，解决方法参考[官方文档](https://pycqa.github.io/isort/docs/configuration/black_compatibility.html)，或者只用它们的其中一个

## 关于`colorama`库

这是一个跨平台的终端文字着色库，用起来挺简单的。去[PyPI](https://pypi.org/project/colorama/)看看？

## 关于音乐的元数据

元数据`metadata`是描述数据的数据。那么音乐的元数据就是描述音乐的信息、特征的数据，像采样率、位深度、比特率、标题、作曲家、专辑、流派、音轨号等等。有很多人为赋予它的信息需要额外地存储到音频文件中，就产生了音频文件标签`tag`。类似地，其他地方也有类似的用来存放此类信息的机制。参见[Tag (metadata)](https://en.wikipedia.org/wiki/Tag_(metadata))。

在[Exif Tools](https://exiftool.org/TagNames/)这个网站上可以进行一些简单的字段的查阅，此外借助搜索引擎也能找到很多内容。比如ID3格式的标签也可以参见[ID3 on Wiki](https://en.wikipedia.org/wiki/ID3)。

正文中提到了[`mutagen`](https://mutagen.readthedocs.io/en/latest/) [`tinytag`](https://github.com/tinytag/tinytag)等Python库，能够读取音频文件标签。此外还有一些通用的命令行工具也可以，比如[`ffprobe`](https://ffmpeg.org/ffprobe.html)。

## 网络相关

给我去读 [MDN Docs](https://developer.mozilla.org/zh-CN/)

# testtools-cli
testtools命令行工具，主要提供脚手架辅助功能

## 安装

```shell
pip install testtools-cli
```

## 如何使用

### testtools-cli init

在指定目录(默认当前目录)创建测试工具脚手架内容,当前支持语言：

- python

使用例子：

```shell
testtools-cli init
```

```shell
testtools-cli init --workdir /tmp/jagma
```

> 测试工具建议使用小写英文名称。

### testtools-cli check

检查指定目录(默认当前目录)的脚手架内容还有哪些要修改的。
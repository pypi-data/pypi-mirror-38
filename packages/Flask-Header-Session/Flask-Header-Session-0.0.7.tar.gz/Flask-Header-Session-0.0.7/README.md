# `Header` Based Flask-Session

A variant of Flask-Session, [Flask-Session](https://pypi.python.org/pypi/Flask-Session). Move cookie based approach into `HTTP Header` based apporach.

This apporach exists because some client environment doesn't allow cookies, e.g. Weixi mini program.

## Installation

Python2: `pip install Flask-Header-Session`

Python3: `pip3 install Flask-Header-Session`

## Include

``` Python
# As usual import flask
import flask
# Import our package
from flask_header_session import Session

# Some configs
app.config['SESSION_TYPE'] = ......

# Use
Session(app)

```
## Modifiation

This project rewrited `open_session` and `save_session` function to use `HTTP Header` as the vehicle instead of cookie

## Supported Backend

These backends are fully supported and tested:
1. `SQLAlchemy` 
2. `Redis` 

## Configuration Variables Honored

The session header name can be set:
```Python
SESSION_HEADER_NAME='X-HTTP-HaHaHa'
```
Default value is `X-Header-Session`.

## Examples

See `./test_session.py` to see the sample usage.

## Test

1. Create some temp data folders. `mkdir -p ./docker/volumes/varlibmysql`
2. Go to the test executable folder. cd `./docker/test/`
3. Then run `./up.sh` to run the tests in local docker containers.

## Bug Report

1. Leave an issue.
2. Email me.


# 基于`HTTP Header`的 Flask-Session

Flask-Session的一个变种, [Flask-Session源码](https://pypi.python.org/pypi/Flask-Session). 将原来的cookie的session 放入Header里面，有更好的适应性。

这个需求存在于无法使用cookie记录客户的场合，例如**微信小程序不允许使用cookie**。

## 安装

Python2: `pip install Flask-Header-Session`

Python3: `pip3 install Flask-Header-Session`

## 引用方法

``` Python
# 引入flask
import flask
# 引入库package
from flask_header_session import Session

# 设置好环境变量
app.config['SESSION_TYPE'] = ......

# 初始化Session
Session(app)

```
## 针对源代码的修改部分

重写了 `open_session` 和 `save_session` 方法，使用`HTTP Header` 而不是 `cookie` 来装载session内容。

## 支持的存储后端

以下都是完全测试过 并且支持的:
1. `SQLAlchemy` 
2. `Redis` 

## 环境变量

HTTP Header名字可以更改:
```Python
SESSION_HEADER_NAME='X-HTTP-HaHaHa'
```
若不更改，则缺省值是 `X-Header-Session`.

## 代码举例

翻看 `./test_session.py` 有两种支持后端的使用案例.

## 测试

1. 创建一些临时文件夹. `mkdir -p ./docker/volumes/varlibmysql`
2. 去往测试执行所在的文件夹. cd `./docker/test/`
3. 执行 `./up.sh` 在本地的docker环境里执行测试.

## Bug 汇报

1. 开个 issue.
2. 给我发送 Email.
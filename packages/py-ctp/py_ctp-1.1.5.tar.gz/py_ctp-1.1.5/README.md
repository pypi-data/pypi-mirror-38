
# python CTP api

上期技术期货交易api之python封装，实现接口调用。支持windows linux.

## 环境需求

* python 3.6+
* 64位
* 采用官方接口 6.3.11_20180109

## 使用说明

* 第一层封装接口测试
  * test_api.py

* 第二层封装交易接口测试
  * test_trade

## 测试

```python
import time
from py_ctp.test_trade import TestTrade


if __name__ == "__main__":
    tt = TestTrade()
    # t.OnConnected = t.ReqUserLogin('008105', '1', '9999')
    # t.ReqConnect('tcp://180.168.146.187:10000')
    tt.run()

    time.sleep(6)
    for inst in tt.t.instruments.values():
        print(inst)
    input()
    tt.release()
```
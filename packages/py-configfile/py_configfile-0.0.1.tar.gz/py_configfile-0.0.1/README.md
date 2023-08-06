Python ConfigFile Package
======

### 说明
这是一个 Python 配置文件加载模块，主要解决 Ymal, Json 配置文件的快速加载，同时支持网络配置动态加载。

### 使用
```python
from configfile import ConfigFile

configfile = ConfigFile()
configfile.config_dir = 'files'

print(configfile.load_app('config'))
print(configfile.load_app_json('config'))
```

### 加载动态配置
```python
import json
import time
from configfile import ConfigFile


timestamp1 = time.time()
timestamp2 = False

configfile = ConfigFile()
configfile.config_dir = 'files'

def callback():
    global timestamp1
    global timestamp2
    if timestamp2 is False:
        timestamp2 = timestamp1
    else:
        timestamp2 = time.time()
    return json.dumps({"timestamp": timestamp2})

print(configfile.load_dynamic_json('config', callback, 3))
time.sleep(1)
print(configfile.load_dynamic_json('config', callback, 3))
time.sleep(3)
print(configfile.load_dynamic_json('config', callback, 3))
```

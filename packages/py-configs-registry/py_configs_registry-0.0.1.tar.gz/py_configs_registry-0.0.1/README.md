Python Registry Package
======

### 说明
这是一个 Python 配置快速调用模块，主要解决 Json or Yaml 深层次配置调用问题。

### 使用
```python
from registry import Registry

registry = Registry()

registry.set('a', 'a')
registry.set('b', {'bb': 'bbb'})
registry.set('c.h', 'h')

print(registry.get())
print(registry.get('b.bb'))
```

### 加载字典
```python
from registry import Registry

registry = Registry()

registry.load({'a': {'aa': 'aaa'}})

print(registry.get('a.aa'))
```

### 合并字典
```python
from registry import Registry

registry = Registry()

registry.load({'a': {'a1': 'aaa1'}})
registry.merge('a', {'a2': 'aaa2' })

print(registry.get('a'))
```

### 设置默认值
```python
from registry import Registry

registry = Registry()

registry.set('a', 'aaa')
registry.default('a', 'bbb')

registry.default('c', 'ccc')

print(registry.get('a'))
print(registry.get('c'))
```

### 高级用法
```python
### 实例化 Redis
Redis(**registry.get(prefix))

### 初始化 Mysql
Mysql(**registry.get(prefix))
```

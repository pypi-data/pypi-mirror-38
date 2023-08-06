# 操作更方便的配置文件读取模块


#####  某ini文件
```
[table]
data = mydata
```

#####  读取代码如下
```
import zinifile

ini = zinifile.load(文件名)
ini = zinifile.load_text(ini内容)
print(ini.table.data)
```

#####  你可以将zinifile创建的实例当做一个字典或者迭代器.
```
for key in ini
for key, value in ini.items()
value = ini.get('键')
value = ini['键']
```

### 更新日志
> 18-11-15 1.0.4

> 1.空值不会再返回一个空的str了,而是返回None

> 2.用xx.xx如果属性不存在则返回zinifile.empty_node对象, 这个对象可以像_node一样使用,
> 但是获取任何数据都是空数据, 他的布尔检测为False

>
```
empty_node is None  #False
empty_node == None  #True
bool(empty_node)    #False
```

- - -
本项目仅供所有人学习交流使用, 禁止用于商业用途

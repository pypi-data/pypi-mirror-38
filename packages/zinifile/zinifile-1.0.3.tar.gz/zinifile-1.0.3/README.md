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

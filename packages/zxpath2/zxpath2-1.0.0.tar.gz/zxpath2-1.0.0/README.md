# 操作更方便的xpath

### 使用方法类似于Beautiful Soup4, 但是比他更快速, 功能更强大

```
import zxpath2

def find(name=None, class_=None, text=None, deep=True, index: None or int = None, **attrs):
    '''
    查询节点
    :param name: 元素名, 如果不是str类型则查找所有元素
    :param class_: class属性
    :param text: 文本值
    :param deep: 是否深度查询孙节点
    :param index: 取出第几个结果
    :param attrs: 属性名前加下划线_会排除这个属性, 如_id=True表示不存在id的元素, 属性值为True, 表示这个属性匹配任意值
    :return: index存在时: 成功返回_Element对象, 失败返回None, index不存在时:返回包含_Element对象的列表
    '''
    pass

zx = zxpath2.load('etree对象或者html源码') #加载

zx.find('div', id='content') #查询id为'content'的所有div, 返回包含_Element对象的列表
zx.find('div', id=False, index=0) #查询不存在id的第一个div, 返回_Element对象
zx.find('div', _id='content', deep=False) #在当前节点中查询id不为'content'的所有div, 返回包含_Element对象的列表
zx.find('div', id='content', index=-1) #查询id为'content'的最后一个div, 返回_Element对象

zx('div', id='content') #_Element对象可以作为函数名直接调用find
```

> #_Element对象
> node = zx.find('div')
>
> node.id #获取id属性
> node.text #获取文本
> node.string #获取整个div的所有文本
> node.a #获取在这个节点下搜索到的第一个a元素节点
> node.html #获取这个节点的html源码
> node.find
> node(*attr, **kw) #同find
> node.xpath #使用原始xpath代码查询, 根据

更新日志:
>     2018-11-03  1.0.0
>     重构zxpath架构, 项目改名为zxpath2, 更改了绝大部分的方法名和参数

- - -
本项目仅供所有人学习交流使用, 禁止用于商业用途

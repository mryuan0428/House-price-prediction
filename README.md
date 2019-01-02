 - 语言：python3

 - 文件内容说明：
```
    |--data_spider文件夹
        |--dataset文件夹 -- 爬取的原始数据
        |--Spider.py -- 爬虫
        |--url.txt -- 爬虫url
        |--数据结构 -- 说明爬到数据的信息
    |--process_first文件夹
        |--update.py -- 统一原始数据格式，缺失标签补空值
        |--dataset2文件夹 -- 小区名转换成经纬坐标后的数据集
        |--POI_COMMUNITY_SH文件夹 -- 之前爬取的上海小区POI点
        |--modifyCommunity.py -- 将POI点提取到POI_COMMUNITY_SH文件夹下的community0.txt文件
        |--modifyCoordinate.py -- 将小区名、经纬度坐标、房屋均价信息提取到coordinate.csv文件，便于后边可视化
        |--searchForCommunity.py -- 将dataset中小区名转换成经纬坐标后，保存在dataset2
        |--map.py -- 画出上海房价分布热力图
        |--map.png -- 上海房价分布热力图
    |--process&module文件夹
        |--dataset.py -- 包含大量数据处理函数，如facility_process(),dataset()
            |--facility_process()函数 -- 将数据集中关于设备的描述关键词分类
            |--dataset()函数 -- 数据集接口，返回dict类型的数据集
        |--dataset3文件夹 -- facility_process()处理过后的数据集
        |--建模过程.docx -- 简述建模过程，其中说明了process&module文件夹下tocsv.py，data_c.csv……文件的意义
        |--result_pictures文件夹 -- 建模过程中各个模型的回归曲线
        |--……其余文件，包含训练、测试数据集，建模文件，模型… 在建模过程.docx中有说明
```


 - dataset()函数用法说明：
```
dataset(*, src='./data2', dst='./dataset', load_from_source=False)
```

 - Keyword arguments:
    * `src` -- `str`, source data path
    * `dst` -- `str`, dataset path
    * `load_from_source` -- `bool`, flag if load from source (`False` in default)

    - Notes:
        * `Info` turn dictionaries into object-like instances
            - inherits from `dict` type
            - iterable, and support all functions as `dict`
            - immutable, thus cannot set or delete attributes after initialisation
            - `infotodict` -- reverse `Info` object into `dict` type
        * `Dataset` object herits from `tuple`
            ```python
            # returns from `dataset` function
            >>> data = dataset()
            # subscriptable as normal tuples
            >>> data[0]
            >>> data[1:10]
            # or to fetch certain keys
            >>> data[1, 'apt', 'lift']
            Info(apt=(2,), lift=(1,))
            >>> data[1:3, 'price', 'average']
            Info(price=(2600000.0, 3080000.0), average=(44636, 36032))
            ```

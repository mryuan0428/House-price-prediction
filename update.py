import json, os


labels = ['ID', '标题', '副标题', '总价', '总价单位', '均价', '小区名称', '所在区域', '房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型',
          '房屋朝向', '建筑结构', '装修情况', '梯户比例', '配备电梯', '产权年限', '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息',
          '房本备件', '房源标签', '税费解析', '交通出行', '核心卖点', '别墅类型', '售房详情', '周边配套', '小区介绍', '户型介绍', '装修描述', '权属抵押', '适宜人群',
          '投资分析']
path1 = "data/"
path2 = "data2/"
files = os.listdir(path1)

for i in files:
    with open(path1+i, 'r') as file:
        tmp = json.load(file)
    for j in range(len(tmp)):
        for key in labels:
            if key not in tmp[j]:
                tmp[j][key] = ''
    with open(path2+i, 'w') as file:
        json.dump(tmp, file)

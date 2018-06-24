# -*- coding: utf-8 -*-

import collections
import datetime
import json
import os
import pathlib
import re
import warnings

import dateutil.parser


__all__ = ['dataset']


with open(os.path.join(os.path.split(os.path.abspath(__file__))[0],
                       './POI_COMMUNITY_SH/community0.txt')) as file:
    COMMUNITY = json.load(file)

DIVISION_CODE = {
    '黄埔': 310101,
    '徐汇': 310104,
    '长宁': 310105,
    '静安': 310106,
    '普陀': 310107,
    '虹口': 310109,
    '杨浦': 310110,
    '闵行': 310112,
    '宝山': 310113,
    '嘉定': 310114,
    '浦东': 310115,
    '金山': 310116,
    '松江': 310117,
    '青浦': 310118,
    '奉贤': 310120,
    '崇明': 310151,
}

FLOOR_LEVEL = {
    '低': 0,
    '中': 1,
    '高': 2,
    '地下室': 4,
}

STRUCTURE_CODE = {
    '复式': 0,
    '平层': 1,
    '跃层': 2,
    '错层': 3,
}

BUILDING_TYPE = {
    '塔楼': 0,
    '板楼': 1,
}

ORIENTATION_CODE = {
    '东': 0,
    '南': 2,
    '西': 4,
    '北': 6,
    '东南': 1,
    '西南': 3,
    '西北': 5,
    '东北': 7,
}

FRAMEWORK_CODE = {
    '砖混结构': 0,
    '钢混结构': 1,
}

CONDITION_CODE = {
    '毛坯': 0,
    '简装': 1,
    '精装': 2,
}

ELEVATOR_CODE = {
    '无': 0,
    '有': 1,
}

TRADING_RIGHTS = {
    '动迁安置房': 0,
    '售后公房': 1,
    '商品房': 2,
}

PURPOSE_CODE = {
    '别墅': 0,
    '新式里弄': 1,
    '旧式里弄': 2,
    '普通住宅': 3,
    '老公寓': 4,
    '花园洋房': 5,
}

HOUSE_TERM = {
    '未满两年': 0,
    '满两年': 1,
    '满五年': 2,
}

PROPERTY_OWNERSHIP = {
    '非共有': 0,
    '共有': 1,
}

DEED_CODE = {
    '未上传房本照片': 0,
    '已上传房本照片': 1,
}

VILLA_TYPE = {
    '联排': 0,
    '独栋': 1,
    '双拼': 2,
    '叠拼': 3,
}

TAG_CODE = {
    '房本满两年': 0,
    '房本满五年': 1,
    '随时看房': 2,
    '地铁': 3,
}

CHINESE_ARABIC = {
    '一': 1,
    '二': 2,
    '两': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
}

POI_DICT = {    # 购物 教育 交通 健身 环境 医疗
    0: ['购物', '市场', '商场', '商铺', '巴黎春天', '卜蜂莲花', '大润发', '乐购'],
    1: ['学校', '学区', '幼儿园', '小学', '中学', '大学'],
    2: ['号线', '地铁', '公交', '车站'],
    3: ['健身', '球场', '游泳'],
    4: ['公园', '绿化'],
    5: ['医'],
}

HOUSE_TYPE = re.compile(r'''
    \A\s*                       # optional whitespace at the start, then
    (?P<room>\d*)               # number of bedrooms, then
    (?:\u5ba4)                  # followed by character “室”, then
    (?P<saloon>\d*)             # number of saloons, then
    (?:\u5385)                  # followed by character “厅”, then
    (?P<kitchen>\d*)            # number of kitchens, then
    (?:\u53a8)                  # followed by character “厨”, then
    (?P<bath>\d*)               # number of bathrooms, then
    (?:\u536b)                  # followed by character “卫”, then
    \s*\Z                       # and optional whitespace to finish
''', re.IGNORECASE | re.VERBOSE)

FLOOR_FORMAT = re.compile(r'''
    \A\s*                       # optional whitespace at the start, then
    (?P<level>\w*)?             # level of this floor, then
    (?:\u697c\u5c42|\u5730\u4e0b\u5ba4)
                                # followed by characters “楼层” or “地下室”, then
    (?:\s)                      # optional whitespace, then
    (?:\u0028\u5171)            # followed by left bracket and character “共”, then
    (?P<total>\d*)              # total number of floors, then
    (?:\u5c42\u0029)            # followed by character “层” and right bracket, then
    \s*\Z                       # and optional whitespace to finish
''', re.IGNORECASE | re.VERBOSE)

RATIO_FORMAT = re.compile(r'''
    \A\s*                       # optional whitespace at the start, then
    (?P<lift>\w*)               # elevators per building, then
    (?:\u68af)                  # followed by character “梯”, then
    (?P<room>\w*)               # houses per floor, then
    (?:\u6237)                  # followed by character “户”, then
    \s*\Z                       # and optional whitespace to finish
''', re.IGNORECASE | re.VERBOSE)


class ParseError(Exception):
    def __init__(self, *args, **kwargs):
        sys.tracelimit = 0
        super().__init__(*args, **kwargs)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {'val': obj.isoformat(), '_spec_type': 'datetime'}
        else:
            return super().default(obj)


def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if _spec_type:
        if _spec_type == 'datetime':
            return dateutil.parser.parse(obj['val'])
        raise ParseError(f'unknown {_spec_type}')
    return obj


class Dataset(tuple):
    """Make tuple-like datasets.

    # returns from `dataset` function
    >>> data = dataset()
    # subscriptable as normal tuples
    >>> data[0]
    >>> data[1:10]
    # or to fetch certain keys
    >>> data[1, 'apt', 'lift']
    >>> data[1:3, 'price', 'average']

    """

    def __getitem__(self, key, *args):
        if isinstance(key, tuple):
            args = tuple(key[1:])
            key = key[0]
        if isinstance(key, str):
            return self.__getitem_slice__(slice(None, None, None), *((key,) + args))
        elif isinstance(key, int):
            return self.__getitem_slice__(slice(key, key + 1, None), *args)
        elif isinstance(key, slice):
            return self.__getitem_slice__(key, *args)
        else:
            raise IndexError('Dataset index out of range')

    def __getitem_slice__(self, key, *args):
        temp = super().__getitem__(key)
        if args == tuple():
            return temp[0] if len(temp) == 1 else temp

        info = collections.defaultdict(list)
        for item in temp:
            retd = self.__getitem_str__(item, *args)
            for key, value in retd.items():
                info[key].append(value)
        for key, value in info.items():
            info[key] = tuple(value)
        return Info(info)

    def __getitem_str__(self, item, *args):
        temp = dict()
        for arg in args:
            if arg in ('name', 'intro', 'coordinate'):
                temp[arg] = item.community[arg]
            elif arg in ('district', 'station', 'ring'):
                temp[arg] = item.region[arg]
            elif arg in ('room', 'saloon', 'kitchen', 'bath'):
                temp[arg] = item.type[arg]
            elif arg in ('level', 'total'):
                temp[arg] = item.floor[arg]
            elif arg in ('condition', 'description'):
                temp[arg] = item.decoration[arg]
            elif arg in ('lift', 'apt'):
                temp[arg] = item.ratio[arg]
            elif arg in ('flag', 'info', 'comment'):
                temp[arg] = item.mortgage[arg]
            else:
                temp[arg] = item[arg]
        return temp


class Info(dict):
    """Turn dictionaries into object-like instances.

    Methods:
        * infotodict -- reverse Info object into dict type

    Notes:
        * Info objects inherit from `dict` type
        * Info objects are iterable, and support all functions as `dict`
        * Info objects are one-time-modeling, thus cannot set or delete
            attributes after initialisation

    """

    def __new__(cls, dict_=None, **kwargs):
        def __read__(dict_):
            __dict__ = dict()
            for (key, value) in dict_.items():
                if isinstance(value, dict):
                    __dict__[key] = Info(value)
                else:
                    # if isinstance(key, str):
                    #     key = re.sub('\W', '_', key)
                    __dict__[key] = value
            return __dict__

        self = super().__new__(cls)
        if dict_ is not None:
            if isinstance(dict_, Info):
                self = copy.deepcopy(dict_)
            else:
                self.__dict__.update(__read__(dict_))

        self.__dict__.update(__read__(kwargs))
        return self

    def __repr__(self):
        temp = list()
        for (key, value) in self.__dict__.items():
            temp.append(f'{key}={value}')
        args = ', '.join(temp)
        return f'Info({args})'

    __str__ = __repr__

    def __iter__(self):
        return iter(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __contains__(self, name):
        return (name in self.__dict__)

    def __setattr__(self, name, value):
        raise AttributeError("can't set attribute")

    def __delattr__(self, name):
        raise AttributeError("can't delete attribute")

    def infotodict(self):
        dict_ = dict()
        for (key, value) in self.__dict__.items():
            if isinstance(value, Info):
                dict_[key] = value.infotodict()
            elif isinstance(value, (tuple, list)):
                temp = list()
                for item in value:
                    if isinstance(item, Info):
                        temp.append(item.infotodict())
                    else:
                        temp.append(item)
                dict_[key] = value.__class__(temp)
            else:
                dict_[key] = value
        return dict_


def parse_price(price, unit):
    if unit == '亿':
        temp = float((price or '').strip() or 0) * 100_000_000
    elif unit == '万':
        temp = float((price or '').strip() or 0) * 10_000
    else:
        raise ParseError(f'unknown unit {unit}')
    return temp


def parse_community(name, intro):
    temp = re.split(r'\(|\uff08', (name or '').strip())[0]

    coordinate = tuple()
    for community in COMMUNITY:
        if temp in community:
            coordinate = tuple(COMMUNITY[community])
            break

    return dict(
        name=(name or '').strip() or None,
        intro=(intro or '').strip() or None,
        coordinate=coordinate,
    )


def parse_region(region):
    temp = (region or '').strip().split()
    if len(temp) in (2, 3):
        return dict(
            district=DIVISION_CODE.get(temp[0], 310000),
            station=temp[1],
            ring=temp[2] if len(temp) == 3 else None,
        )
    return dict(district=None, station=None, ring=None)


def parse_type(htype):
    match = HOUSE_TYPE.match(htype)
    if match is None:
        raise ParseError(f'illegal house type {htype}')
    return dict(
        room=int(match.group('room')),
        saloon=int(match.group('saloon')),
        kitchen=int(match.group('kitchen')),
        bath=int(match.group('bath')),
    )


def parse_floor(floor):
    match = FLOOR_FORMAT.match(floor)
    if match is None:
        raise ParseError(f'illegal floor discription {floor}')
    return dict(
        level=FLOOR_LEVEL.get(match.group('level') or '地下室', -1),
        total=int(match.group('total')),
    )


def parse_orientation(orientation):
    temp = (orientation or '').strip().split()
    ret = [0 for _ in range(8)]
    for desc in temp:
        index = ORIENTATION_CODE.get(desc)
        if index is None:
            return tuple(ret)
        ret[index] = 1
    return tuple(ret)


def parse_decoration(condition, description):
    return dict(
        condition=CONDITION_CODE.get(condition, -1),
        description=(description or '').strip() or None,
    )


def parse_ratio(ratio):
    def convert(string):
        sum_ = 0
        temp = 1
        for char in string:
            temp *= CHINESE_ARABIC[char]
            if char in ('十',):
                sum_ += temp
                temp = 1
        return sum_ if char in ('十',) else (sum_ + temp)

    match = RATIO_FORMAT.match(ratio)
    if match is None:
        return dict(list=0, apt=0)
    return dict(
        lift=convert(match.group('lift')),
        apt=convert(match.group('room')),
    )


def parse_time(time):
    temp = (time or '').replace('暂无数据', '')
    return datetime.datetime.strptime(temp, '%Y-%m-%d') if temp else None


def parse_mortgage(mortgage, ownership):
    return dict(
        flag=bool(mortgage),
        info=tuple((mortgage or '').strip().split()) if mortgage else None,
        comment=(ownership or '').strip() or None,
    )


def parse_tags(tags):
    temp = (tags or '').strip().split()
    ret = [0 for _ in range(4)]
    for tag in temp:
        index = TAG_CODE.get(tag)
        if index is None:
            raise ParseError(f'unknown tag {tag}')
        ret[index] = 1
    return tuple(ret)


def parse_facility(facility):
    desc = str(facility or '').strip()
    temp = [0, 0, 0, 0, 0, 0]
    for index, POI in POI_DICT.items():
        for keyword in POI:
            if keyword in desc:
                temp[index] = 1
                break
    return tuple(temp)


def parse(data):
    report = list()
    for item in data:
        temp = dict(
            id=int(item['ID']),
            title=(item['标题'] or '').strip() or None,
            heading=(item['副标题'] or '').strip() or None,
            price=parse_price(item['总价'], item['总价单位']),
            average=float((item['均价'] or '').strip('元/平米') or 0),
            community=parse_community(item['小区名称'], item['小区介绍']),
            region=parse_region(item['所在区域']),
            type=parse_type(item['房屋户型']),
            floor=parse_floor(item['所在楼层']),
            scale=float((item['建筑面积'] or '').strip(
                '㎡').replace('暂无数据', '') or 0),
            structure=STRUCTURE_CODE.get((item['户型结构'] or '').strip(), -1),
            area=float((item['套内面积'] or '').strip(
                '㎡').replace('暂无数据', '') or 0),
            building=BUILDING_TYPE.get((item['建筑类型'] or '').strip(), -1),
            orientation=parse_orientation(item['房屋朝向']),
            framework=FRAMEWORK_CODE.get((item['建筑结构'] or '').strip(), -1),
            decoration=parse_decoration(item['装修情况'], item['装修描述']),
            ratio=parse_ratio(item['梯户比例']),
            elevator=ELEVATOR_CODE.get((item['配备电梯'] or '').strip(), -1),
            title_term=int(re.split('未知|年', item['产权年限'])[0] or 0),
            listing_time=parse_time(item['挂牌时间']),
            rights=TRADING_RIGHTS.get((item['交易权属'] or '').strip(), -1),
            last_transaction=parse_time(item['上次交易']),
            purpose=PURPOSE_CODE.get((item['房屋用途'] or '').strip(), -1),
            house_term=HOUSE_TERM.get((item['房屋年限'] or '').strip(), -1),
            ownership=PROPERTY_OWNERSHIP.get((item['产权所属'] or ''), -1),
            mortgage=parse_mortgage(item['抵押信息'], item['权属抵押']),
            deed=DEED_CODE.get((item['房本备件'] or '').strip(), -1),
            tags=parse_tags(item['房源标签']),
            intro=(item['户型介绍'] or '').strip() or None,
            inspiration=(item['核心卖点'] or '').strip() or None,
            transport=(item['交通出行'] or '').strip() or None,
            details=(item['售房详情'] or '').strip() or None,
            tax=(item['税费解析'] or '').strip() or None,
            suitable=(item['适宜人群'] or '').strip() or None,
            villa=VILLA_TYPE.get((item['别墅类型'] or '').strip(), -1),
            analysis=(item['投资分析'] or '').strip() or None,
            facility=parse_facility(item['周边配套']),
        )
        report.append(Info(temp))
    return tuple(report)


def load(*, path='./dataset3'):
    dataset = list()
    for file in os.listdir(path):
        if os.path.splitext(file)[1] != '.json':
            continue
        with open(f'{path}/{file}', 'r') as load_file:
            data = json.load(load_file, object_hook=object_hook)
        for item in data:
            dataset.append(Info(item))
    return Dataset(dataset)


def dump(*, src='./data2', dst='./dataset3'):
    pathlib.Path(dst).mkdir(exist_ok=True, parents=True)

    dataset = list()
    for file in os.listdir(src):
        if os.path.splitext(file)[1] != '.json':
            continue
        with open(f'{src}/{file}', 'r') as load_file:
            data = json.load(load_file, object_hook=object_hook)
            temp = parse(data)
        with open(f'{dst}/{file}', 'w') as dump_file:
            print(dump_file.name)
            json.dump(temp, dump_file, cls=JSONEncoder)
        dataset.extend(temp)
    return Dataset(dataset)


def dataset(*, src='./data2', dst='./dataset3', load_from_source=False):
    if load_from_source:
        warnings.filterwarnings('default')
        warnings.warn('load_from_source is deprecated; '
                      'directly load dataset instead', DeprecationWarning, stacklevel=2)
        # return dump(src=src, dst=dst)
    return load(path=dst)

def check(line):
    if line['average']<= 0:
        return 0
    elif not line['community']['coordinate']:
        return 0
    elif not line['facility']:
        return 0
    else: return 1


if __name__ == '__main__':
    import pprint
    import sys

    data = dataset()

    for line in data:
        if 'average' in line.keys():
            '''values = [line['average'],line['community']['coordinate'][0],
                      line['community']['coordinate'][1],line['decoration']['condition'],line['deed'],
                      line['elevator'],line['facility'][0],line['facility'][1],line['facility'][2],
                      line['facility'][3],line['facility'][4],line['facility'][5],line['floor']['level'],
                      line['floor']['total'],line['framework'],line['house_term'],
                      line['ownership'],line['price'],line['purpose'],line['ratio']['apt'],line['ratio']['lift'],
                      line['region']['district'],line['rights'],line['scale'],line['structure'],line['type']['bath'],
                      line['type']['kitchen'],line['type']['room'],line['type']['saloon']]'''
            print(line.keys())

    sys.exit(0)

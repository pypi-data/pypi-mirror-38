# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:52:18 2017

@author: zsj
"""
import vendor.gaode.api as gaodeAPI
import database.operation as userAPI
import database.cache as cache
import utils.decorator as decorator
import pandas as pd
import numpy as np


###############################################################################
def keywords_search(keywords='', types='', city='', citylimit='',
                    children='', offset='10', page='', building='',
                    floor='', extensions='all'):
    '''
    POI关键字搜索
    keywords:查询关键字,多个关键字用“|”分割。#keywords与types必填至少一个。
    types:多个类型用“|”分割；可选值：分类代码 或 汉字（若用汉字，请严格按照附件之中
          的汉字填写）。
    city：查询城市。可选值：城市中文、中文全拼、citycode、adcode；
          如：北京/beijing/010/110000；填入此参数后，会尽量优先返回此城市数据，
          但是不一定仅局限此城市结果，若仅需要某个城市数据请调用citylimit参数。
    citylimit：仅返回指定城市数据。可选值：true/false。默认false。
    children：是否按照层级展示子POI数据；可选值：children=1。默认值0。
              当为0的时候，子POI都会显示。当为1的时候，子POI会归类到父POI之中。
    offset：每页记录数据。强烈建议不超过25，若超过25可能造成访问报错。默认20。
    page：当前页数，最大翻页数100，可选，默认值1。
    building：建筑物的POI编号，传入建筑物POI编号之后，则只在该建筑物之内进行搜索。
    floor：搜索楼层。
    extensions：返回结果控制；此项默认返回基本地址信息；取值为all返回地址信息、
                附近POI、道路以及道路交叉口信息；可选；默认值base。
    sig：数字签名。
    output：返回数据格式类型；可选值：JSON，XML；可选；默认值JSON。
    callback：回调函数；callback值是用户定义的函数名称，
              此参数只在output=JSON时有效。
    '''
    s = {'keywords': keywords,
         'types': types,
         'city': city,
         'citylimit': citylimit,
         'children': children,
         'offset': offset,
         'page': page,
         'building': building,
         'floor': floor,
         'extensions': extensions
         }

    testlist = gaodeAPI.Keywords_Search(s)
    lst = testlist.get()
    return lst


def surrounding_search(location='', keywords='', types='', city='', radius='',
                       sortrule='', offset='10', page='', extensions='all'):
    '''
    周边搜索
    location:中心点坐标;规则： 经度和纬度用","分割，经度在前，纬度在后，经纬度小数点
    后不得超过6位.#必填
    keywords:查询关键字;规则： 多个关键字用“|”分割。
    types：查询POI类型；多个类型用“|”分割；可选值：分类代码 或 汉字 （若用汉字，
    请严格按照附件之中的汉字填写）；分类代码由六位数字组成，一共分为三个部分，
    前两个数字代表大类；中间两个数字代表中类；最后两个数字代表小类。
    若指定了某个大类，则所属的中类、小类都会被显示。
    例如：010000为汽车服务（大类）010100为加油站（中类）010101为中国石化（小类）
          010900为汽车租赁（中类）010901为汽车租赁还车（小类）
          当指定010000，则010100等中类、010101等小类都会被包含。
          当指定010900，则010901等小类都会被包含。
          当keywords和types均为空的时候，默认指定types为050000（餐饮服务）、
          070000（生活服务）、120000（商务住宅）
    city：查询城市；可选值：城市中文、中文全拼、citycode、adcode；如：
    北京/beijing/010/110000；当用户指定的经纬度和city出现冲突，若范围内有用户指定
    city的数据，则返回相关数据，否则返回为空。如：经纬度指定石家庄，而city却指定天
    津，若搜索范围内有天津的数据则返回相关数据，否则返回为空。（全国范围内搜索）
    radius：查询半径；取值范围:0-50000。规则：大于50000按默认值，单位：米；默认值3000。

    sortrule：排序规则；规定返回结果的排序规则。按距离排序：distance；
    综合排序：weight；默认值distance
    offset：每页记录数据；强烈建议不超过25，若超过25可能造成访问报错；默认值20。
    page：当前页数；最大翻页数100。默认值1。
    extensions：返回结果控制；此项默认返回基本地址信息；取值为all返回地址信息、
    附近POI、道路以及道路交叉口信息。默认值base。
    '''
    s = {'location': location,
         'keywords': keywords,
         'types': types,
         'city': city,
         'radius': radius,
         'sortrule': sortrule,
         'offset': offset,
         'page': page,
         'extensions': extensions
         }
    testlist = gaodeAPI.Surrounding_Search(s)
    pois = testlist.get()['pois']
    # pois_df = pd.DataFrame(pois)
    # pois_output = pois_df.to_dict('records')
    pois_data = decorator.formatTool(pois)
    return pois_data


def ip_location(ip_address=''):
    '''
    IP定位
    ip_address:ip地址,需要搜索的IP地址（仅支持国内）;若用户不填写IP,
               则取客户http之中的请求来进行定位。
    '''
    s = {}
    if not ip_address == '':
        s['ip'] = ip_address
    testlist = gaodeAPI.IP_Location(s)
    lst = testlist.get()
    return lst


def id_search(poi_id=''):
    '''
    ID查询
    id:兴趣点ID;兴趣点的唯一标识ID。
    '''
    s = {'id': poi_id}
    testlist = gaodeAPI.ID_Search(s)
    lst = testlist.get()
    return lst


def geocode(address='', city='', batch='false'):
    '''
    地理编码
    address:结构化地址信息;规则遵循：国家、省份、城市、区县、城镇、乡村、街道、门牌
    号码、屋邨、大厦，如：北京市朝阳区阜通东大街6号。如果需要解析多个地址的话，请用
    "|"进行间隔，并且将 batch 参数设置为 true，最多支持 10 个地址进进行"|"分割形式
    的请求。#必填。
    city:指定查询的城市。可选输入内容包括：指定城市的中文（如北京）、指定城市的中文
    全拼（beijing）、citycode（010）、adcode（110000）。当指定城市查询内容为空时，
    会进行全国范围内的地址转换检索。无，会进行全国范围内搜索。
    batch：批量查询控制；batch 参数设置为 true 时进行批量查询操作，最多支持 10 个地
    址进行批量查询。batch 参数设置为 false 时进行单点查询，此时即使传入多个地址也只
    返回第一个地址的解析查询结果。默认值false。
    '''
    s = {'address': address,
         'city': city,
         'batch': batch
         }
    testlist = gaodeAPI.Geocode(s)
    lst = testlist.get()
    return lst


def regeocode(location='', poitype='', radius='', extensions='all',
              batch='false', roadlevel='0'):
    '''
    逆地理编码
    location:经纬度坐标;传入内容规则：经度在前，纬度在后，经纬度间以“,”分割，经纬度
    小数点后不要超过 6 位。如果需要解析多个经纬度的话，请用"|"进行间隔，并且将 batch
    参数设置为 true，最多支持传入 20 对坐标点。每对点坐标之间用"|"分割。
    #必填
    poitype:返回附近POI类型;以下内容需要 extensions 参数为 all 时才生效。逆地理编
    码在进行坐标解析之后不仅可以返回地址描述，也可以返回经纬度附近符合限定要求的POI内
    容（在 extensions 字段值为 all 时才会返回POI内容）。设置 POI 类型参数相当于为上
    述操作限定要求。参数仅支持传入POI TYPECODE，可以传入多个POI TYPECODE，相互之间
    用“|”分隔。该参数在 batch 取值为 true 时不生效。获取 POI TYPECODE 可以参考POI
    分类码表;无默认值。
    radius:搜索半径;radius取值范围在0~3000，默认是1000。单位：米。
    extensions:返回结果控制;参数默认取值是 base，也就是返回基本地址信息；
    取值为 all 时会返回基本地址信息、附近 POI 内容、道路信息以及道路交叉口信息。
    batch:批量查询控制;batch 参数设置为 true 时进行批量查询操作，最多支持 20 个经纬
    度点进行批量地址查询操作。参数设置为 false 时进行单点查询，此时即使传入多个经纬
    度也只返回第一个经纬度的地址解析查询结果。默认false。
    roadlevel：道路等级。以下内容需要 extensions 参数为 all 时才生效。可选值：0，1。 
    当roadlevel=0时，显示所有道路 ；=1时，过滤非主干道路，仅输出主干道路数据。 
    无默认值。
    homeorcorp：是否优化POI返回顺序；以下内容需要 extensions 参数为 all 时才生效。
    homeorcorp 参数的设置可以影响召回 POI 内容的排序策略，目前提供三个可选参数：
    0：不对召回的排序策略进行干扰。1：综合大数据分析将居家相关的 POI 内容优先返回，
    即优化返回结果中 pois 字段的poi顺序。2：综合大数据分析将公司相关的 POI 内容优先
    返回，即优化返回结果中 pois 字段的poi顺序。默认值0。
    '''
    s = {'location': location,
         'poitype': poitype,
         'radius': radius,
         'extensions': extensions,
         'batch': batch,
         'roadlevel': roadlevel
         }
    testlist = gaodeAPI.ReGeocode(s)
    lst = testlist.get()
    return lst


def convert(locations='', coordsys='gps'):
    '''
    坐标转换
    locations:坐标点;经度和纬度用","分割，经度在前，纬度在后，经纬度小数点后不得超
    过6位。多个坐标对之间用”|”进行分隔最多支持40对坐标。#必填。
    coordsys：原坐标系；可选值：gps;mapbar;baidu;autonavi(不进行转换)；
    默认值autonavi
    '''
    s = {'locations': locations,
         'coordsys': coordsys
         }
    testlist = gaodeAPI.Convert(s)
    lst = testlist.get()
    return lst


def distance(origins='', destination='', distype='1'):
    '''
    距离测量
    origins:出发点;支持100个坐标对，坐标对间用“| ”分隔；经度和纬度用","分隔;#必填。
    destination：目的地；规则： lon，lat（经度，纬度）， “,”分割；
    如117.500244, 40.417801；经纬度小数点不超过6位；#必填。
    type：路径计算的方式和方法；0：直线距离；1：驾车导航距离（仅支持国内坐标）。
    必须指出，当为1时会考虑路况，故在不同时间请求返回结果可能不同。此策略和driving接
    口的 strategy=4策略一致；2：公交规划距离（仅支持同城坐标）；
    3：步行规划距离（仅支持5km之间的距离）。默认值1。
    '''
    s = {'origins': origins,
         'destination': destination,
         'type': distype
         }
    testlist = gaodeAPI.Distance(s)
    lst = testlist.get()
    return lst


###############################################################################
def gps2gaode(gps=''):
    '''
    GPS坐标转为高德坐标
    gps_address:GPS坐标，经度在前维度在后，'，'分隔，如：'121.179406,31.280342'。
    '''
    gaode = convert(locations=gps, coordsys='gps')
    return gaode.get('locations', '')


def gps2gaode_batch(gps=''):
    '''
    GPS坐标转为高德坐标
    gps_address:GPS坐标，经度在前维度在后，'，'分隔,如：'121.179406,31.280342'；
    坐标对间用“| ”分隔。
    '''
    gaode = convert(locations=gps, coordsys='gps')
    return gaode.get('locations', '').split(';')


def get_adcode_citycode(gaode_address):
    '''
    获取adcode和citycode
    gaode_address:高德坐标;经度和纬度用","分割，经度在前，纬度在后。
    '''
    temp = regeocode(location=gaode_address, extensions='all',
                     batch='false', roadlevel='0')
    temp = temp.get('regeocode', '')
    if temp != '':
        temp = temp.get('addressComponent', '{}')
        adcode = temp.get('adcode', '')
        citycode = temp.get('citycode', '')
    else:
        adcode = ''
        citycode = ''
    return adcode, citycode


def get_concat(favorlist=['']):
    '''
    拼接高德坐标地址，经度在前维度在后，'，'分隔，如：'121.179406,31.280342'。
    '''
    origins = ''
    for i in favorlist:
        origins += i + '|'
    origins = origins[:-1]
    return origins


####批量接口###########################################################################

def batch_distance(favorlist=[''], destination='', distype='1'):
    '''
    批量获得POI点到目标点距离,POI点不超过100个。
    distype：0：直线距离；1：驾车导航距离（仅支持国内坐标）。
    必须指出，当为1时会考虑路况，故在不同时间请求返回结果可能不同。此策略和driving接
    口的 strategy=4策略一致；2：公交规划距离（仅支持同城坐标）；
    3：步行规划距离（仅支持5km之间的距离）。默认值1。
    '''
    if len(favorlist) > 100:
        favorlist = favorlist[0:100]
    origins = get_concat(favorlist)
    temp = distance(origins, destination, distype)
    dist = temp.get('results', '')
    return dist


def bat_distance(favorlist=[''], destination='', distype='1'):
    '''
    
    '''
    s = {
        'destination': destination,
        'type': distype
    }
    part = len(favorlist)
    if part % 100 == 0:
        part = part // 100
    else:
        part = part // 100 + 1
    lst = []
    for j in range(part):
        origins = []
        if j < (part - 1):
            origins = get_concat(favorlist[j * 100:(j + 1) * 100])
        else:
            origins = get_concat(favorlist[j * 100:])
        ss = s.copy()
        ss['origins'] = origins
        lst.append(ss)
    dists_batch = gaodeAPI.batch_distances(lst)
    dists = []
    for i in dists_batch:
        temp = i.get('body', '')
        if temp != '':
            temp = temp.get('results', '')
            if temp != '':
                if isinstance(temp, list):
                    dists = dists + temp
    return dists


def bat_search_surrds_typ(location, types, radius, offset, pages):
    '''
    批量请求高德周边搜索,按类型搜索
    '''
    s = {'location': location,
         'types': types,
         'radius': radius,
         'offset': offset,
         'extensions': 'all'
         }
    lst = []
    if int(pages) <= 20:
        pages = int(pages)
    else:
        pages = 20
    for i in range(1, pages + 1):
        ss = s.copy()
        ss['page'] = str(i)
        lst.append(ss)
    pois_batch = gaodeAPI.batch_search_surroudings(lst)
    pois = []
    temp = pois_batch[0].get('body', '')
    if temp != '':
        countnum = temp.get('count', '')
    if countnum != '' and countnum != '0':
        for i in pois_batch:
            temp = i.get('body', '')
            if temp != '':
                temp = temp.get('pois', '')
                if temp != '':
                    if isinstance(temp, list):
                        pois = pois + temp
    return pois


def bat_search_surrds_keys(location, keywords, types, radius, offset, pages):
    '''
    批量请求高德周边搜索,按关键字搜索
    keywords:list of strs,如['安亭','美食']
    '''
    s = {'location': location,
         'types': types,
         'radius': radius,
         'offset': offset,
         'extensions': 'all'
         }
    if isinstance(keywords, list):
        keywords = get_concat(keywords)
    s['keywords'] = keywords
    lst = []
    if int(pages) <= 20:
        pages = int(pages)
    else:
        pages = 20
    for i in range(1, pages + 1):
        ss = s.copy()
        ss['page'] = str(i)
        lst.append(ss)
    pois_batch = gaodeAPI.batch_search_surroudings(lst)
    pois = []
    temp = pois_batch[0].get('body', '')
    if temp != '':
        countnum = temp.get('count', '')
    if countnum != '' and countnum != '0':
        for i in pois_batch:
            temp = i.get('body', '')
            if temp != '':
                temp = temp.get('pois', '')
                if temp != '':
                    if isinstance(temp, list):
                        pois = pois + temp
    return pois


def bat_search_keys(keywords, types, city, offset, pages):
    '''
    批量请求高德关键字搜索
    keywords:list of strs,如['安亭','美食']
    '''
    s = {
        'types': types,
        'city': city,
        'offset': offset,
        'extensions': 'all'
    }
    if isinstance(keywords, list):
        keywords = get_concat(keywords)
    s['keywords'] = keywords
    lst = []
    if int(pages) <= 20:
        pages = int(pages)
    else:
        pages = 20
    for i in range(1, pages + 1):
        ss = s.copy()
        ss['page'] = str(i)
        lst.append(ss)
    pois_batch = gaodeAPI.batch_search_keys(lst)
    pois = []
    temp = pois_batch[0].get('body', '')
    if temp != '':
        countnum = temp.get('count', '')
    if countnum != '' and countnum != '0':
        for i in pois_batch:
            temp = i.get('body', '')
            if temp != '':
                temp = temp.get('pois', '')
                if temp != '':
                    if isinstance(temp, list):
                        pois = pois + temp
    pois_data = decorator.formatTool(pois)
    return pois_data


def bat_id(poi_u_list):
    '''
    批量id搜索
    '''
    part = len(poi_u_list)
    if part % 20 == 0:
        part = part // 20
    else:
        part = part // 20 + 1
    pois_u = []
    for j in range(part):
        if j < (part - 1):
            poi_u = gaodeAPI.batch_search_ids(poi_u_list[j * 20:(j + 1) * 20])
        else:
            poi_u = gaodeAPI.batch_search_ids(poi_u_list[j * 20:])
        if isinstance(poi_u, dict) and poi_u.get('info', '') != '':
            # 检查返回是否出错
            break
        else:
            for i in poi_u:
                temp = i.get('body', '')
                if temp != '':
                    temp = temp.get('pois', '')
                    if temp != '':
                        pois_u = pois_u + temp
    return pois_u


###子函数############################################################################
def types_upperlimit(types):
    types = int(types)
    if types % 10000 == 0:
        types_upper_limit = ((types // 10000) + 1) * 10000
    elif types % 100 == 0:
        types_upper_limit = ((types // 100) + 1) * 100
    else:
        types_upper_limit = types + 1

    if types_upper_limit // 100000 == 0:
        return '0' + str(types_upper_limit)
    else:
        return str(types_upper_limit)


def get_userlist(id_int, num=100):
    User_info = cache.User(id_int)
    hist_list = User_info.poi_history_list
    return hist_list


def get_city(gaode='', ip=''):
    '''
    获取当前城市名
    gaode:高德坐标
    ip：IP地址
    '''
    city = ''
    if gaode != '':
        address = regeocode(location=gaode, extensions='base').get('regeocode', '')
        if address != '':
            current = address.get('addressComponent', '')
            if current != '':
                if current.get('adcode', '') != '':
                    city = current.get('city')
                    if current.get('city') == []:
                        city = current.get('province')
    elif ip != '':
        city = ip_location(ip).get('city', '')
    return city


###main############################################################################
def surroundings_typ(id_int, center_gps, types, radius='3000', offset='25', pages='10'):
    '''
    周边类型搜索
    center_gps：中心点GPS坐标
    pages<='20'
    '''
    # 坐标转换
    center = convert(center_gps, coordsys='gps').get('locations', '')
    if center == '':
        return []
        # 批量请求高德周边搜索
    pois = bat_search_surrds_typ(center, types, radius, offset, pages)
    if len(pois) == 0:
        return []
    pois_df = pd.DataFrame(pois)

    # 获取用户信息
    if id_int == '':
        userlist = None
    else:
        userlist = get_userlist(int(id_int))
    if userlist != None:
        poi_u_df = pd.DataFrame(userlist)
        # 根据次数先行排序
        poi_u_df = poi_u_df.sort_values(by='used_times', ascending=False)

        # 按分类初筛
        types_upper = types_upperlimit(types)
        poi_u_df_sel = poi_u_df[(poi_u_df.typecode < types_upper)
                                & (poi_u_df.typecode >= types)].copy()

        # 测距
        if len(poi_u_df_sel) != 0:
            locs = list(poi_u_df_sel.location)
            dists = batch_distance(locs, center, '0')
            if len(poi_u_df_sel) == len(dists):
                distances = []
                dist_int = []
                for temp in dists:
                    distances.append(temp['distance'])
                    dist_int.append(int(temp['distance']))
                poi_u_df_sel['distance'] = distances
                poi_u_df_sel['dist_int'] = dist_int
                poi_u_df_sel = poi_u_df_sel[poi_u_df_sel.dist_int <= int(radius)].sort_values(
                    by='dist_int')

        # 批量id搜索高德请求
        if len(poi_u_df_sel) != 0:
            poi_u_list = pd.DataFrame(poi_u_df_sel.loc[:, 'id']).to_dict('records')
            pois_u = bat_id(poi_u_list)
            pois_u_df = pd.DataFrame(pois_u)
            pois_u_df.distance = list(poi_u_df_sel.distance)

        # 拼接pd
        if len(pois_u_df) != 0:
            pois_df = pd.concat([pois_u_df, pois_df]).fillna('')  # 'alias'为''或[]或str
    pois_df = pois_df.drop_duplicates('id')

    # 转为list,每条为一个dict
    pois_output = pois_df.to_dict('records')
    return pois_output


###############################################################################

def surroundings_keys(id_int, center_gps, keywords, types='', radius='3000', offset='25', pages='10'):
    '''
    周边关键词搜索
    center_gps：中心点GPS坐标
    pages<='20'
    keywords:可以为str或list of str，如['安亭','美食']或'安亭美食'，
            推荐使用'安亭美食'，结果更为准确
    '''
    # 坐标转换
    center = convert(center_gps, coordsys='gps').get('locations', '')
    if center == '':
        return []
    # 批量请求高德周边搜索
    pois = bat_search_surrds_keys(center, keywords, types, radius, offset, pages)
    if len(pois) == 0:
        return []

    # 获取用户信息
    if id_int is None:
        userlist = None
    else:
        userlist = get_userlist(int(id_int))
    if userlist != None:
        poi_u_df = pd.DataFrame(userlist)
        # 根据次数先行排序
        poi_u_df = poi_u_df.sort_values(by='used_times', ascending=False)

        # 按分类初筛

        if types != '':
            types_upper = types_upperlimit(types)
            poi_u_df_sel = poi_u_df[(poi_u_df.typecode < types_upper)
                                    & (poi_u_df.typecode >= types)].copy()
        else:
            poi_u_df_sel = poi_u_df.copy()

        # 按是否在关键词搜索结果中初筛
        pois_df = pd.DataFrame(pois)
        poi_u_df_sel = poi_u_df_sel[poi_u_df_sel['id'].isin(list(pois_df['id']))]

        # 测距
        if len(poi_u_df_sel) != 0:
            locs = list(poi_u_df_sel.location)
            dists = batch_distance(locs, center, '0')
            if len(poi_u_df_sel) == len(dists):
                distances = []
                dist_int = []
                for temp in dists:
                    distances.append(temp['distance'])
                    dist_int.append(int(temp['distance']))

                poi_u_df_sel['distance'] = distances
                poi_u_df_sel['dist_int'] = dist_int
                poi_u_df_sel = poi_u_df_sel[poi_u_df_sel.dist_int <= int(radius)].sort_values(
                    by='dist_int')

        # 批量id搜索高德请求
        if len(poi_u_df_sel) != 0:
            poi_u_list = pd.DataFrame(poi_u_df_sel.loc[:, 'id']).to_dict('records')
            pois_u = bat_id(poi_u_list)

            pois_u_df = pd.DataFrame(pois_u)
            if len(pois_u_df) == len(poi_u_df_sel):
                pois_u_df.distance = list(poi_u_df_sel.distance)

                # 拼接pd

                if len(pois_u_df) != 0:
                    pois_df = pd.concat([pois_u_df, pois_df]).fillna('')  # 'alias'为''或[]或str
    else:
        pois_df = pd.DataFrame(pois)
    pois_df = pois_df.drop_duplicates('id')
    # 转为list,每条为一个dict
    pois_output = pois_df.to_dict('records')
    return pois_output


###############################################################################
def search_keys(id_int, keywords, types='', city='',
                gps='', ip='', offset='25', pages='10'):
    '''
    关键词搜索
    gps为车辆当前所在地GPS坐标，仅用于显示目标距当前所在地距离，不用于筛选排序
    pages<='20'
    keywords:可以为str或list of str，如['安亭','美食']或'安亭美食'，
            推荐使用'安亭美食'，结果更为准确
    '''
    # 坐标转换
    gaode = convert(gps, coordsys='gps').get('locations', '')
    # 获取当前所在城市（仅精确到地级市）
    if city == '':
        city = get_city(gaode, ip)

    # 批量请求高德搜索
    pois = bat_search_keys(keywords, types, city, offset, pages)
    if len(pois) == 0:
        return []

    # 获取用户信息
    if id_int is None:
        userlist = None
    else:
        userlist = get_userlist(int(id_int))
    if userlist != None:
        poi_u_df = pd.DataFrame(userlist)
        # 根据次数先行排序
        poi_u_df = poi_u_df.sort_values(by='used_times', ascending=False)

        # 按分类初筛

        if types != '':
            types_upper = types_upperlimit(types)
            poi_u_df_sel = poi_u_df[(poi_u_df.typecode < types_upper)
                                    & (poi_u_df.typecode >= types)].copy()
        else:
            poi_u_df_sel = poi_u_df.copy()

        # 按是否在关键词搜索结果中初筛
        pois_df = pd.DataFrame(pois)
        poi_u_df_sel = poi_u_df_sel[poi_u_df_sel['id'].isin(list(pois_df['id']))]

        # 批量id搜索高德请求
        if len(poi_u_df_sel) != 0:
            poi_u_list = pd.DataFrame(poi_u_df_sel.loc[:, 'id']).to_dict('records')
            pois_u = bat_id(poi_u_list)

            pois_u_df = pd.DataFrame(pois_u)

            # 拼接pd
            if len(pois_u_df) != 0:
                pois_df = pd.concat([pois_u_df, pois_df]).fillna('')  # 'alias'为''或[]或str
    else:
        pois_df = pd.DataFrame(pois)
    pois_df = pois_df.drop_duplicates('id')
    # 测距
    if len(pois_df) != 0 and gaode != '':
        locs = list(pois_df.location)
        dists = bat_distance(locs, gaode, '0')
        if len(pois_df) == len(dists):
            distances = []
            for temp in dists:
                distances.append(temp['distance'])
            pois_df.distance = distances

    # 转为list,每条为一个dict
    pois_output = pois_df.to_dict('records')
    return pois_output


###############################################################################
def broadcast(current_gps, last_gps):
    '''
    风情播报
    GPS原始坐标，经度在前维度在后，'，'分隔,如：'121.179406,31.280342'
    返回值如下：
    {'country': '中国', 'province': '上海市', 'city': '上海市', 
    'citycode': '021', 'district': '嘉定区', 'adcode': '310114', 
    'township': '安亭镇', 'towncode': '310114103000', 'neighborhood': 
    {'name': [], 'type': []}, 'building': {'name': [], 'type': []}, 
    'streetNumber': {'street': '泽普路', 'number': '143号', 
    'location': '121.162229,31.2912233', 'direction': '西北', 
    'distance': '57.618'}, 'businessAreas': 
    [{'location': '121.16208721909425,31.29547976499391',
    'name': '安亭', 'id': '310114'}]}
    '''
    locs = get_concat([current_gps, last_gps])
    locs_gaode = gps2gaode_batch(locs)
    locs_gaode = get_concat(locs_gaode)
    address = regeocode(location=locs_gaode, extensions='base', batch='true')
    temp = address.get('regeocodes', '')
    if temp != '' and len(temp) == 2:
        current = temp[0].get('addressComponent', '')
        last = temp[1].get('addressComponent', '')
        if current != '' and last != '':
            if (current.get('adcode', '') != ''
                    and last.get('adcode', '') != ''
                    and current.get('adcode', '') != last.get('adcode', '')):
                if current.get('city') == []:
                    current['city'] = current.get('province')
                return current
    return 'no broadcast'

####test##########################################################################
# center="121.580587,30.927573"
# t1=surroundings_typ(888888, center, types='050000', radius='3000')
# t1_ori=bat_search_surrds_typ(center, types='050000', radius='3000')
# t2=surroundings_keys(888888, center, '美食', types='', radius='3000')
# t3=surroundings_keys(888888, center, '嘉定办事中心', types='', radius='3000')
# t4=search_keys(888888, center, '美食', types='', city='上海')
# t5=search_keys(888888, center, '美食', types='')
# t6=search_keys(888888, center, '嘉定办事中心', types='', city='shanghai')
# b1 = broadcast("121.579092,30.924306", "121.580587,30.927573")
# b2 = broadcast("121.173757,31.278605", "121.580587,30.927573")
# b3 = broadcast("121.580587,30.927573","121.173757,31.278605")

#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/9 11:07
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : expection
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""
BASE_CODE = 20000


class Common(Exception):
    _status_code = 0
    _status_info = 'Success.'

    @property
    def code(self):
        return self._status_code

    @property
    def info(self):
        return self._status_info

    def __str__(self):
        return repr(self._status_info)


class Success(Common):
    _status_code = 0
    _status_info = 'Success.'


class InternalError(Common):
    _status_code = BASE_CODE + 500
    _status_info = 'Internal fault.'


class GetTokenFailed(Common):
    _status_code = BASE_CODE + 501
    _status_info = 'Get token failed from vendor.'


class NoTimeStampError(Common):
    _status_code = BASE_CODE + 1001
    _status_info = 'No timestamp in the request params!'


class NoVinError(Common):
    _status_code = BASE_CODE + 1002
    _status_info = 'No vin in the request params!'


class NoKeyWordError(Common):
    _status_code = BASE_CODE + 1003
    _status_info = 'No keyword in the request params!'


class PikaConnectionError(Common):
    _status_code = BASE_CODE + 1004
    _status_info = 'RabbitMQ connected error!'


class NoTrackIdError(Common):
    _status_code = BASE_CODE + 1005
    _status_info = 'No track id in the request params!'


class NoPlayListIdError(Common):
    _status_code = BASE_CODE + 1006
    _status_info = 'No playlist id in the request params!'


class NoAlbumIdError(Common):
    _status_code = BASE_CODE + 1007
    _status_info = 'No album id in the request params!'


class WebHandlerError(Common):
    _status_code = BASE_CODE + 1008
    _status_info = 'Error in the handler!'


class SQLConnectError(Common):
    _status_code = BASE_CODE + 1009
    _status_info = 'Database connect error!'


class CacheConnectError(Common):
    _status_code = BASE_CODE + 1010
    _status_info = 'Cache connect error!'


class NoItemIdError(Common):
    _status_code = BASE_CODE + 1011
    _status_info = 'No item id in the request params!'


class NoPlayListNameError(Common):
    _status_code = BASE_CODE + 1012
    _status_info = 'No playlistname in the request params!'


class NoSelfListError(Common):
    _status_code = BASE_CODE + 1013
    _status_info = 'No selflist in the request params!'


class NoArtistIdError(Common):
    _status_code = BASE_CODE + 1014
    _status_info = 'No artist id in the request params!'


class NoCategoryIdIdError(Common):
    _status_code = BASE_CODE + 1015
    _status_info = 'No categoryid id in the request params!'


class NoUserIdIdError(Common):
    _status_code = BASE_CODE + 1016
    _status_info = 'No user id in the request params!'


class GaoDeApiError(Common):
    _status_code = BASE_CODE + 1017
    _status_info = 'Gaode api error!'


class NoIpError(Common):
    _status_code = BASE_CODE + 1018
    _status_info = 'Internal error, ip info lost!'


class NoLocationError(Common):
    _status_code = BASE_CODE + 1019
    _status_info = 'No location in the request params!'


class NoPoiIdError(Common):
    _status_code = BASE_CODE + 1020
    _status_info = 'No poi_id in the request params!'


class NoBoradcastOnError(Common):
    _status_code = BASE_CODE + 1021
    _status_info = 'No broadcast_on in the request params!'


class InValidServiceError(Common):
    _status_code = BASE_CODE + 1022
    _status_info = 'Invalid service! Please check the input.'


class VendorAPIError(Common):
    _status_code = BASE_CODE + 1023
    _status_info = 'Vendor API Error!'


class NullKeywordsError(Common):
    _status_code = BASE_CODE + 1024
    _status_info = 'keywords is null'


class NullLocationError(Common):
    _status_code = BASE_CODE + 1025
    _status_info = 'location is null'


class NullPoiIdError(Common):
    _status_code = BASE_CODE + 1026
    _status_info = 'poiid is null'


class ParameterTooMuchError(Common):
    _status_code = BASE_CODE + 1027
    _status_info = ' Too much parameter '


class NullKeywordsOrPoiIdError(Common):
    _status_code = BASE_CODE + 1028
    _status_info = ' keywords or poiid could not be both empty '


class NullTypeError(Common):
    _status_code = BASE_CODE + 1029
    _status_info = ' type could not be both empty '


class NullKeyOrTypeError(Common):
    _status_code = BASE_CODE + 1030
    _status_info = ' poi_id or address could not be both empty '


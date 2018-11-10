# -*- coding: utf-8 -*-

KIRK_HOST = {
    'APPGLOBAL': "https://controller-api.sdk.com",  # 公有云 APP API
    'APPPROXY': "http://controller.qcos.sdk",  # 内网 APP API
    'APIPROXY': "http://api.qcos.sdk",  # 内网 API
}

CONTAINER_UINT_TYPE = {
    '1U1G': '单核(CPU)，1GB(内存)',
    '1U2G': '单核(CPU)，2GB(内存)',
    '1U4G': '单核(CPU)，4GB(内存)',
    '1U8G': '单核(CPU)，8GB(内存)',
    '2U2G': '双核(CPU)，2GB(内存)',
    '2U4G': '双核(CPU)，4GB(内存)',
    '2U8G': '双核(CPU)，8GB(内存)',
    '2U16G': '双核(CPU)，16GB(内存)',
    '4U8G': '四核(CPU)，8GB(内存)',
    '4U16G': '四核(CPU)，16GB(内存)',
    '8U16G': '八核(CPU)，16GB(内存)',
}

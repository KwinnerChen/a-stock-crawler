
# 股票信息获取网址({0}指股票代码）
INFO_URL = 'https://gupiao.baidu.com/stock/{0}.html'

# 使用的数据库（支持Mongodb，Mysql）
DATABASE = 'mysql'

# 集合名（仅用于MongoDB）
# COLLECTION_NAME = 'chn_stock'

# 仅用于MySQL数据库，表名，还有字段定义。（注意：不需定义id，和时间，默认定义。）
TABLE_STRUCTOR ={'chn_stock':
                     {
                         '股票名称':'text',
                         '今开':'text',
                         '成交量':'text',
                         '最高':'text',
                         '涨停':'text',
                         '内盘':'text',
                         '成交额':'text',
                         '委比':'text',
                         '流通市值':'text',
                         '市盈率':'text',
                         '每股收益':'text',
                         '总股本':'text',
                         '昨收':'text',
                         '换手率':'text',
                         '最低':'text',
                         '跌停':'text',
                         '外盘':'text',
                         '振幅':'text',
                         '量比':'text',
                         '总市值':'text',
                         '市净率':'text',
                         '每股净资产':'text',
                         '流通股本':'text',
                         '净值':'text',
                         '折价率':'text',

                     },
                }

# 股票信息提取Xpath表达式


# 无头浏览器
# WEBDRIVER = 'Firefox'

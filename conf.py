
# 股票信息获取网址({0}指股票代码）
INFO_URL = 'https://gupiao.baidu.com/stock/{0}.html'

# 使用的数据库（支持Mongodb，Mysql）
DATABASE = 'mysql'

# 集合名（MongoDB）
COLLECTION_NAME = 'chn_stock'

# 仅用于MySQL数据库，表名，还有字段定义。
TABLE_STRUCTOR ={'chn_stock':
                     {
                         '今开':'float',
                         '昨收':'float',
                         '最高':'float',
                         '最低':'float',
                         '成交量':'int',
                         '市值':'bigint',
                         '52周高':'float',
                         '52周低':'float',
                         '每股收益':'float',
                         '市盈率':'float',
                     },
                }

# 股票信息提取Xpath表达式
INFO_XPATH = {
    '今开': '//div[@class="bets-col-10"]//dd[1]/text()',
    '昨收': '//div[@class="bets-col-10"]//dd[2]/text()',
    '最高': '//div[@class="bets-col-10"]//dd[3]/text()',
    '最低': '//div[@class="bets-col-10"]//dd[4]/text()',
    '成交量': '//div[@class="bets-col-10"]//dd[5]/text()',
    '市值': '//div[@class="bets-col-10"]//dd[6]/text()',
    '52周高': '//div[@class="bets-col-10"]//dd[7]/text()',
    '52周低': '//div[@class="bets-col-10"]//dd[8]/text()',
    '每股收益': '//div[@class="bets-col-10"]//dd[9]/text()',
    '市盈率': '//div[@class="bets-col-10"]//dd[10]/text()',
}

# 无头浏览器
# WEBDRIVER = 'Firefox'

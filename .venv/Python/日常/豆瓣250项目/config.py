#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
包含应用程序的所有配置常量
"""

# 网络请求配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0'
}

# 请求延迟（秒）
REQUEST_DELAY = 1

# 重试延迟（秒）
RETRY_DELAY = 2

# 最大重试次数
MAX_RETRIES = 3

# 超时时间（秒）
TIMEOUT = 15

# 分页配置
PAGE_SIZE = 25

# 界面配置
WINDOW_CONFIG = {
    'title': '豆瓣电影Top250',
    'width': 1200,
    'height': 800,
    'min_width': 900,
    'min_height': 650,
    'max_width': 1400,
    'max_height': 900,
    'screen_ratio': 0.8,
    'bg_color': '#f5f5f5'
}

# 详情窗口配置
DETAIL_WINDOW_CONFIG = {
    'width': 800,
    'height': 600,
    'min_width': 600,
    'min_height': 400,
    'bg_color': '#ffffff'
}

# 颜色配置
COLORS = {
    'primary': '#1890ff',
    'secondary': '#722ed1',
    'success': '#52c41a',
    'warning': '#fa8c16',
    'error': '#f5222d',
    'text': '#262626',
    'text_secondary': '#8c8c8c',
    'bg': '#f5f5f5',
    'bg_secondary': '#ffffff',
    'border': '#d9d9d9',
    'hover': '#e6f7ff'
}

# 样式配置
STYLES = {
    'title': {
        'font': ('Microsoft YaHei', 16, 'bold'),
        'fg': COLORS['text']
    },
    'subtitle': {
        'font': ('Microsoft YaHei', 12, 'bold'),
        'fg': COLORS['text_secondary']
    },
    'text': {
        'font': ('Microsoft YaHei', 10),
        'fg': COLORS['text']
    },
    'button': {
        'font': ('Microsoft YaHei', 10),
        'bg': COLORS['primary'],
        'fg': 'white',
        'relief': 'flat',
        'bd': 0,
        'padx': 20,
        'pady': 8
    },
    'entry': {
        'font': ('Microsoft YaHei', 10),
        'relief': 'solid',
        'bd': 1,
        'highlightthickness': 1
    }
}

# 海报配置
POSTER_CONFIG = {
    'width': 120,
    'height': 160,
    'quality': 85,
    'format': 'JPEG',
    'cache_size': 100,
    'placeholder_color': '#e6e6e6'
}

# 网络测试配置
NETWORK_TEST_URLS = [
    'https://www.douban.com',
    'https://movie.douban.com',
    'https://www.baidu.com'
]

# 备用电影数据（当网络不可用时使用）
BACKUP_MOVIES = [
    {
        'rank': 1,
        'title': '肖申克的救赎',
        'year': '1994',
        'score': '9.7',
        'director': '弗兰克·德拉邦特',
        'actors': ['蒂姆·罗宾斯', '摩根·弗里曼'],
        'genre': '剧情/犯罪',
        'country': '美国',
        'poster': 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp',
        'detail_url': 'https://movie.douban.com/subject/1292052/',
        'quote': '希望让人自由。',
        'description': '20世纪40年代末，小有成就的青年银行家安迪（蒂姆·罗宾斯 Tim Robbins 饰）因涉嫌杀害妻子及她的情人而锒铛入狱。在这座名为肖申克的监狱内，希望似乎虚无缥缈，终身监禁的惩罚无疑注定了安迪接下来的人生。'
    },
    {
        'rank': 2,
        'title': '霸王别姬',
        'year': '1993',
        'score': '9.6',
        'director': '陈凯歌',
        'actors': ['张国荣', '张丰毅', '巩俐'],
        'genre': '剧情/爱情/同性',
        'country': '中国大陆',
        'poster': 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p1910813120.webp',
        'detail_url': 'https://movie.douban.com/subject/1291546/',
        'quote': '风华绝代。',
        'description': '段小楼（张丰毅）与程蝶衣（张国荣）是一对打小一起长大的师兄弟，两人一个演生，一个演旦，一向配合天衣无缝，尤其一出《霸王别姬》，更是誉满京城，为此，两人约定合演一辈子《霸王别姬》。'
    },
    {
        'rank': 3,
        'title': '阿甘正传',
        'year': '1994',
        'score': '9.5',
        'director': '罗伯特·泽米吉斯',
        'actors': ['汤姆·汉克斯', '罗宾·怀特'],
        'genre': '剧情/爱情',
        'country': '美国',
        'poster': 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p510876377.webp',
        'detail_url': 'https://movie.douban.com/subject/1292720/',
        'quote': '一部美国近现代史。',
        'description': '阿甘（汤姆·汉克斯 饰）于二战结束后不久出生在美国南方阿拉巴马州一个闭塞的小镇，他先天弱智，智商只有75，然而他的妈妈是一个性格坚强的女性，她常常鼓励阿甘"傻人有傻福"。'
    },
    {
        'rank': 4,
        'title': '泰坦尼克号',
        'year': '1997',
        'score': '9.4',
        'director': '詹姆斯·卡梅隆',
        'actors': ['莱昂纳多·迪卡普里奥', '凯特·温丝莱特'],
        'genre': '剧情/爱情/灾难',
        'country': '美国',
        'poster': 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p457760035.webp',
        'detail_url': 'https://movie.douban.com/subject/1292722/',
        'quote': '失去的才是永恒的。',
        'description': '1912年4月14日，载着1316号乘客和891名船员的豪华巨轮泰坦尼克号与冰山相撞而沉没，这场海难被认为是20世纪人间十大灾难之一。'
    },
    {
        'rank': 5,
        'title': '千与千寻',
        'year': '2001',
        'score': '9.4',
        'director': '宫崎骏',
        'actors': ['柊瑠美', '入野自由', '夏木真理'],
        'genre': '剧情/动画/家庭',
        'country': '日本',
        'poster': 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p1606727862.webp',
        'detail_url': 'https://movie.douban.com/subject/1291561/',
        'quote': '最好的宫崎骏，最好的久石让。',
        'description': '千寻和爸爸妈妈一同驱车前往新家，在郊外的小路上不慎进入了一个奇特的隧道——他们去到了另外一个诡异世界—一个中世纪的小镇。'
    }
]

# 豆瓣URL配置
DOUBAN_URLS = {
    'base': 'https://movie.douban.com/top250',
    'detail_base': 'https://movie.douban.com/subject/'
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'douban_movie.log'
}

# 缓存配置
CACHE_CONFIG = {
    'enable': True,
    'dir': 'cache',
    'max_size': 100,  # MB
    'expire_time': 3600 * 24 * 7  # 7天
}

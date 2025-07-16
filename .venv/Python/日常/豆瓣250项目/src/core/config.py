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
    'bg_color': '#f8f9fa'
}

# 颜色配置
COLORS = {
    'primary': '#1976d2',
    'secondary': '#424242',
    'success': '#4caf50',
    'warning': '#ff9800',
    'error': '#f44336',
    'info': '#2196f3',
    'bg': '#f5f5f5',
    'surface': '#ffffff',
    'text': '#333333',
    'text_secondary': '#666666',
    'border': '#e0e0e0',
    'hover': '#e3f2fd',
    'selected': '#bbdefb'
}

# 样式配置
STYLES = {
    'Main.TFrame': {
        'background': '#f5f5f5'
    },
    'Toolbar.TFrame': {
        'background': '#e0e0e0',
        'relief': 'flat'
    },
    'Toolbar.TButton': {
        'font': ('微软雅黑', 10),
        'padding': (8, 4)
    },
    'Loading.TLabel': {
        'background': '#e0e0e0',
        'foreground': '#1976d2',
        'font': ('微软雅黑', 10)
    },
    'Content.TFrame': {
        'background': '#f5f5f5'
    },
    'List.TFrame': {
        'background': '#ffffff',
        'relief': 'sunken'
    },
    'Search.TLabel': {
        'background': '#ffffff',
        'font': ('微软雅黑', 10)
    },
    'Search.TEntry': {
        'fieldbackground': '#ffffff',
        'font': ('微软雅黑', 10)
    },
    'Movie.Treeview': {
        'background': '#ffffff',
        'fieldbackground': '#ffffff',
        'selectbackground': '#e3f2fd',
        'font': ('微软雅黑', 10),
        'rowheight': 30
    },
    'Movie.Treeview.Heading': {
        'background': '#e0e0e0',
        'foreground': '#333333',
        'font': ('微软雅黑', 10, 'bold')
    },
    'Poster.TFrame': {
        'background': '#f5f5f5',
        'relief': 'sunken'
    },
    'Poster.TLabel': {
        'background': '#f5f5f5',
        'font': ('微软雅黑', 10),
        'anchor': 'center'
    },
    'Status.TFrame': {
        'background': '#e0e0e0',
        'relief': 'flat'
    },
    'Status.TLabel': {
        'background': '#e0e0e0',
        'foreground': '#666666',
        'font': ('微软雅黑', 9)
    },
    'treeview': {
        'font': ('微软雅黑', 11),
        'rowheight': 35,
        'background': '#ffffff',
        'fieldbackground': '#ffffff',
        'selectbackground': '#e3f2fd'
    },
    'heading': {
        'font': ('微软雅黑', 12, 'bold'),
        'background': '#e0e0e0',
        'foreground': '#333333'
    },
    'button': {
        'font': ('微软雅黑', 11),
        'padding': (10, 5)
    },
    'frame': {
        'background': '#f5f5f5'
    },
    'label': {
        'background': '#f5f5f5',
        'font': ('微软雅黑', 11)
    }
}

# 海报配置
POSTER_CONFIG = {
    'hover_size': (150, 220),
    'detail_size': (200, 280),
    'delay': 300,  # 毫秒
    'border_color': '#333333'
}

# 网络测试配置
NETWORK_TEST_URLS = {
    'basic': 'https://www.baidu.com',
    'douban': 'https://movie.douban.com/top250'
}

# 备用数据 - 豆瓣Top250经典电影
BACKUP_MOVIES = [
    {
        'title': '肖申克的救赎',
        'rating': '9.7',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292052/',
        'info': '导演: 弗兰克·德拉邦特 主演: 蒂姆·罗宾斯 / 摩根·弗里曼',
        'quote': '希望让人自由。',
        'rating_people': '2800000人评价'
    },
    {
        'title': '霸王别姬',
        'rating': '9.6',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910813120.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291546/',
        'info': '导演: 陈凯歌 主演: 张国荣 / 张丰毅 / 巩俐',
        'quote': '风华绝代。',
        'rating_people': '1800000人评价'
    },
    {
        'title': '阿甘正传',
        'rating': '9.5',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p510876377.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292720/',
        'info': '导演: 罗伯特·泽米吉斯 主演: 汤姆·汉克斯 / 罗宾·怀特',
        'quote': '一部美国近现代史。',
        'rating_people': '1900000人评价'
    },
    {
        'title': '泰坦尼克号',
        'rating': '9.4',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p457760035.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292722/',
        'info': '导演: 詹姆斯·卡梅隆 主演: 莱昂纳多·迪卡普里奥 / 凯特·温丝莱特',
        'quote': '失去的才是永恒的。',
        'rating_people': '1600000人评价'
    },
    {
        'title': '这个杀手不太冷',
        'rating': '9.4',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p511118051.jpg',
        'detail_url': 'https://movie.douban.com/subject/1295644/',
        'info': '导演: 吕克·贝松 主演: 让·雷诺 / 娜塔莉·波特曼',
        'quote': '完美的杀手。',
        'rating_people': '1700000人评价'
    },
    {
        'title': '辛德勒的名单',
        'rating': '9.5',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p492406163.jpg',
        'detail_url': 'https://movie.douban.com/subject/1295124/',
        'info': '导演: 史蒂文·斯皮尔伯格 主演: 连姆·尼森 / 拉尔夫·费因斯',
        'quote': '拯救一个人，就是拯救整个世界。',
        'rating_people': '1200000人评价'
    },
    {
        'title': '盗梦空间',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p513344864.jpg',
        'detail_url': 'https://movie.douban.com/subject/3541415/',
        'info': '导演: 克里斯托弗·诺兰 主演: 莱昂纳多·迪卡普里奥 / 玛丽昂·歌迪亚',
        'quote': '我们所经历的现实，或许只是一场梦。',
        'rating_people': '1500000人评价'
    },
    {
        'title': '忠犬八公的故事',
        'rating': '9.4',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p524964016.jpg',
        'detail_url': 'https://movie.douban.com/subject/3011091/',
        'info': '导演: 莱塞·霍尔斯道姆 主演: 理查·基尔 / 琼·艾伦',
        'quote': '永远都不能忘记你所爱的人。',
        'rating_people': '1100000人评价'
    },
    {
        'title': '星际穿越',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2206492400.jpg',
        'detail_url': 'https://movie.douban.com/subject/1889243/',
        'info': '导演: 克里斯托弗·诺兰 主演: 马修·麦康纳 / 安妮·海瑟薇',
        'quote': '爱是一种力量，让我们超越时空的维度。',
        'rating_people': '1300000人评价'
    },
    {
        'title': '楚门的世界',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p479682972.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292064/',
        'info': '导演: 彼得·威尔 主演: 金·凯瑞 / 劳拉·琳妮',
        'quote': '如果再也不能见到你，祝你早安，午安，晚安。',
        'rating_people': '1000000人评价'
    },
    {
        'title': '三傻大闹宝莱坞',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p579729551.jpg',
        'detail_url': 'https://movie.douban.com/subject/3793023/',
        'info': '导演: 拉库马·希拉尼 主演: 阿米尔·汗 / 卡琳娜·卡普尔',
        'quote': '英俊版憨豆，高情商版谢耳朵。',
        'rating_people': '1600000人评价'
    },
    {
        'title': '机器人总动员',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1461851991.jpg',
        'detail_url': 'https://movie.douban.com/subject/2131459/',
        'info': '导演: 安德鲁·斯坦顿 主演: 本·贝尔特 / 艾丽莎·奈特',
        'quote': '小瓦力，大情怀。',
        'rating_people': '1000000人评价'
    },
    {
        'title': '放牛班的春天',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910824951.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291549/',
        'info': '导演: 克里斯托夫·巴拉蒂 主演: 热拉尔·朱诺 / 让-巴蒂斯特·莫尼耶',
        'quote': '天籁一般的童声，是最接近上帝的存在。',
        'rating_people': '900000人评价'
    },
    {
        'title': '大话西游之大圣娶亲',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2455050536.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292213/',
        'info': '导演: 刘镇伟 主演: 周星驰 / 朱茵 / 吴孟达',
        'quote': '一生所爱。',
        'rating_people': '1200000人评价'
    },
    {
        'title': '千与千寻',
        'rating': '9.4',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2557573348.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291561/',
        'info': '导演: 宫崎骏 主演: 柊瑠美 / 入野自由 / 夏木真理',
        'quote': '最好的宫崎骏，最好的久石让。',
        'rating_people': '1800000人评价'
    },
    {
        'title': '熔炉',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1363250216.jpg',
        'detail_url': 'https://movie.douban.com/subject/5912992/',
        'info': '导演: 黄东赫 主演: 孔侑 / 郑有美 / 金志映',
        'quote': '我们一路奋战不是为了改变世界，而是为了不让世界改变我们。',
        'rating_people': '600000人评价'
    },
    {
        'title': '无间道',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2564556863.jpg',
        'detail_url': 'https://movie.douban.com/subject/1307914/',
        'info': '导演: 刘伟强 / 麦兆辉 主演: 刘德华 / 梁朝伟 / 黄秋生',
        'quote': '香港电影史上永不过时的杰作。',
        'rating_people': '900000人评价'
    },
    {
        'title': '疯狂动物城',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2614500649.jpg',
        'detail_url': 'https://movie.douban.com/subject/25662329/',
        'info': '导演: 拜伦·霍华德 / 瑞奇·摩尔 主演: 金妮弗·古德温 / 杰森·贝特曼',
        'quote': '迪士尼给我们营造的乌托邦就是这样，永远善良勇敢，永远出人意料。',
        'rating_people': '1500000人评价'
    },
    {
        'title': '控方证人',
        'rating': '9.6',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1505392928.jpg',
        'detail_url': 'https://movie.douban.com/subject/1296141/',
        'info': '导演: 比利·怀德 主演: 泰隆·鲍华 / 玛琳·黛德丽',
        'quote': '比利·怀德满分作品。',
        'rating_people': '300000人评价'
    },
    {
        'title': '触不可及',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1454261925.jpg',
        'detail_url': 'https://movie.douban.com/subject/3319755/',
        'info': '导演: 奥利维·那卡什 / 艾力克·托兰达 主演: 弗朗索瓦·克鲁塞 / 奥马·希',
        'quote': '满满温情的高雅喜剧。',
        'rating_people': '800000人评价'
    },
    {
        'title': '蝙蝠侠：黑暗骑士',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p462657443.jpg',
        'detail_url': 'https://movie.douban.com/subject/1851857/',
        'info': '导演: 克里斯托弗·诺兰 主演: 克里斯蒂安·贝尔 / 希斯·莱杰',
        'quote': '无尽的黑暗。',
        'rating_people': '700000人评价'
    },
    {
        'title': '少年派的奇幻漂流',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1784592701.jpg',
        'detail_url': 'https://movie.douban.com/subject/1929463/',
        'info': '导演: 李安 主演: 苏拉·沙玛 / 伊尔凡·汗',
        'quote': '瑰丽壮观、无人能及的冒险之旅。',
        'rating_people': '1400000人评价'
    },
    {
        'title': '指环王3：王者无敌',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2494956417.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291552/',
        'info': '导演: 彼得·杰克逊 主演: 维果·莫腾森 / 奥兰多·布鲁姆',
        'quote': '史诗的终章。',
        'rating_people': '700000人评价'
    },
    {
        'title': '哈尔的移动城堡',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2174346180.jpg',
        'detail_url': 'https://movie.douban.com/subject/1308807/',
        'info': '导演: 宫崎骏 主演: 倍赏千恵子 / 木村拓哉',
        'quote': '带着心爱的人，去到任何地方。',
        'rating_people': '1000000人评价'
    },
    {
        'title': '摔跤吧！爸爸',
        'rating': '9.0',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2457983084.jpg',
        'detail_url': 'https://movie.douban.com/subject/26387939/',
        'info': '导演: 涅提·蒂瓦里 主演: 阿米尔·汗 / 法缇玛·萨那·纱卡',
        'quote': '你是我的骄傲。',
        'rating_people': '1700000人评价'
    },
    {
        'title': '当幸福来敲门',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1665997400.jpg',
        'detail_url': 'https://movie.douban.com/subject/1849031/',
        'info': '导演: 加布里埃莱·穆奇诺 主演: 威尔·史密斯 / 贾登·史密斯',
        'quote': '平凡中的力量。',
        'rating_people': '1200000人评价'
    },
    {
        'title': '怦然心动',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p501177648.jpg',
        'detail_url': 'https://movie.douban.com/subject/3319755/',
        'info': '导演: 罗伯·莱纳 主演: 玛德琳·卡罗尔 / 卡兰·麦克奥利菲',
        'quote': '真正的爱情是专一的，爱情的领域是非常的狭小，它狭到只能容下两个人生存。',
        'rating_people': '1500000人评价'
    },
    {
        'title': '寻梦环游记',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2503997609.jpg',
        'detail_url': 'https://movie.douban.com/subject/20645662/',
        'info': '导演: 李·昂克里奇 / 阿德里安·莫利纳 主演: 安东尼·冈萨雷斯 / 盖尔·加西亚·贝纳尔',
        'quote': '死亡不是生命的终点，遗忘才是。',
        'rating_people': '1300000人评价'
    },
    {
        'title': '龙猫',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2540924496.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291560/',
        'info': '导演: 宫崎骏 主演: 日高法子 / 坂本千夏',
        'quote': '人人心中都有个龙猫，童年就永远不会消失。',
        'rating_people': '900000人评价'
    },
    {
        'title': '教父',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2190556185.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291841/',
        'info': '导演: 弗朗西斯·福特·科波拉 主演: 马龙·白兰度 / 阿尔·帕西诺',
        'quote': '跨越了类型的界限，缔造了一个完整的史诗。',
        'rating_people': '800000人评价'
    },
    {
        'title': '末代皇帝',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2560717825.jpg',
        'detail_url': 'https://movie.douban.com/subject/1293172/',
        'info': '导演: 贝纳尔多·贝托鲁奇 主演: 尊龙 / 陈冲 / 邬君梅',
        'quote': '"不要跟我比惨，我比你更惨"再适合不过了。',
        'rating_people': '400000人评价'
    },
    {
        'title': '海上钢琴师',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2574551676.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292001/',
        'info': '导演: 朱塞佩·托纳多雷 主演: 蒂姆·罗斯 / 普路特·泰勒·文斯',
        'quote': '每个人都要走一条自己坚定了的路，就算是粉身碎骨。',
        'rating_people': '1200000人评价'
    },
    {
        'title': '天空之城',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1446261379.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291583/',
        'info': '导演: 宫崎骏 主演: 田中真弓 / 横泽启子',
        'quote': '克服困难，用爱发电。',
        'rating_people': '800000人评价'
    },
    {
        'title': '闻香识女人',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910813120.jpg',
        'detail_url': 'https://movie.douban.com/subject/1298624/',
        'info': '导演: 马丁·布雷斯特 主演: 阿尔·帕西诺 / 克里斯·奥唐纳',
        'quote': 'Hoo-ah！',
        'rating_people': '600000人评价'
    },
    {
        'title': '美丽人生',
        'rating': '9.5',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p510861873.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292063/',
        'info': '导演: 罗伯托·贝尼尼 主演: 罗伯托·贝尼尼 / 尼可莱塔·布拉斯基',
        'quote': '最美的谎言。',
        'rating_people': '800000人评价'
    },
    {
        'title': '辞典情人',
        'rating': '8.9',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1826040327.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291818/',
        'info': '导演: 安东尼·明格拉 主演: 拉尔夫·费因斯 / 朱丽叶·比诺什',
        'quote': '拉尔夫·费因斯的颜值巅峰。',
        'rating_people': '300000人评价'
    },
    {
        'title': '飞屋环游记',
        'rating': '9.0',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2598473080.jpg',
        'detail_url': 'https://movie.douban.com/subject/2129039/',
        'info': '导演: 彼特·道格特 / 鲍勃·彼德森 主演: 爱德华·阿斯纳 / 乔丹·长井',
        'quote': '最后那些最无聊的事情，能让人最怀念的，就是梦想。',
        'rating_people': '1100000人评价'
    },
    {
        'title': '十二怒汉',
        'rating': '9.4',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2173577632.jpg',
        'detail_url': 'https://movie.douban.com/subject/1293182/',
        'info': '导演: 西德尼·吕美特 主演: 亨利·方达 / 马丁·鲍尔萨姆',
        'quote': '1957年的理想主义。',
        'rating_people': '300000人评价'
    },
    {
        'title': '素媛',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2118532944.jpg',
        'detail_url': 'https://movie.douban.com/subject/21937452/',
        'info': '导演: 李濬益 主演: 薛景求 / 严志媛',
        'quote': '受过伤害的人总是笑得最开心，因为他们不愿意让身边的人承受一样的痛苦。',
        'rating_people': '400000人评价'
    },
    {
        'title': '鬼子来了',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1464543919.jpg',
        'detail_url': 'https://movie.douban.com/subject/1291858/',
        'info': '导演: 姜文 主演: 姜文 / 香川照之',
        'quote': '对敌人的仁慈，就是对自己残忍。',
        'rating_people': '600000人评价'
    },
    {
        'title': '大话西游之月光宝盒',
        'rating': '9.0',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2455050536.jpg',
        'detail_url': 'https://movie.douban.com/subject/1299398/',
        'info': '导演: 刘镇伟 主演: 周星驰 / 吴孟达 / 朱茵',
        'quote': '旷古烁今的无厘头经典。',
        'rating_people': '1100000人评价'
    },
    {
        'title': '钢琴家',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1910824951.jpg',
        'detail_url': 'https://movie.douban.com/subject/1296736/',
        'info': '导演: 罗曼·波兰斯基 主演: 艾德里安·布洛迪 / 艾米丽娅·福克斯',
        'quote': '音乐能化解仇恨。',
        'rating_people': '300000人评价'
    },
    {
        'title': '猫鼠游戏',
        'rating': '9.0',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p453924541.jpg',
        'detail_url': 'https://movie.douban.com/subject/1305487/',
        'info': '导演: 史蒂文·斯皮尔伯格 主演: 莱昂纳多·迪卡普里奥 / 汤姆·汉克斯',
        'quote': '猫鼠游戏，你做猫还是做鼠？',
        'rating_people': '800000人评价'
    },
    {
        'title': '活着',
        'rating': '9.3',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2513253791.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292365/',
        'info': '导演: 张艺谋 主演: 葛优 / 巩俐',
        'quote': '张艺谋最好的电影。',
        'rating_people': '600000人评价'
    },
    {
        'title': '让子弹飞',
        'rating': '8.8',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1512562287.jpg',
        'detail_url': 'https://movie.douban.com/subject/3742360/',
        'info': '导演: 姜文 主演: 姜文 / 葛优 / 周润发',
        'quote': '姜文就是中国电影的王。',
        'rating_people': '1600000人评价'
    },
    {
        'title': '窃听风暴',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1808872109.jpg',
        'detail_url': 'https://movie.douban.com/subject/1900841/',
        'info': '导演: 弗洛里安·亨克尔·冯·多纳斯马尔克 主演: 乌尔里希·穆埃 / 马蒂娜·戈黛特',
        'quote': '别样人生。',
        'rating_people': '400000人评价'
    },
    {
        'title': '两杆大烟枪',
        'rating': '9.1',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p792443418.jpg',
        'detail_url': 'https://movie.douban.com/subject/1293350/',
        'info': '导演: 盖·里奇 主演: 杰森·弗莱明 / 德克斯特·弗莱彻',
        'quote': '4个臭皮匠顶个诸葛亮，盖·里奇果然不是盖的。',
        'rating_people': '400000人评价'
    },
    {
        'title': '毒枭',
        'rating': '9.0',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2435904665.jpg',
        'detail_url': 'https://movie.douban.com/subject/25796129/',
        'info': '导演: 安德烈斯·拜斯 主演: 瓦格纳·马拉 / 博伊德·霍布鲁克',
        'quote': '当年奈飞原创神作。',
        'rating_people': '300000人评价'
    },
    {
        'title': '红辣椒',
        'rating': '9.0',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p456825720.jpg',
        'detail_url': 'https://movie.douban.com/subject/1865703/',
        'info': '导演: 今敏 主演: 林原惠美 / 古谷彻',
        'quote': '梦的挽歌。',
        'rating_people': '200000人评价'
    },
    {
        'title': '喜剧之王',
        'rating': '8.7',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2579932167.jpg',
        'detail_url': 'https://movie.douban.com/subject/1302425/',
        'info': '导演: 周星驰 / 李力持 主演: 周星驰 / 莫文蔚',
        'quote': '我是一个演员。',
        'rating_people': '800000人评价'
    },
    {
        'title': '致命魔术',
        'rating': '8.9',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p480383375.jpg',
        'detail_url': 'https://movie.douban.com/subject/1780330/',
        'info': '导演: 克里斯托弗·诺兰 主演: 休·杰克曼 / 克里斯蒂安·贝尔',
        'quote': '诺兰给出了一个精彩的答案。',
        'rating_people': '600000人评价'
    },
    {
        'title': '春光乍泄',
        'rating': '8.9',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p465939041.jpg',
        'detail_url': 'https://movie.douban.com/subject/1292679/',
        'info': '导演: 王家卫 主演: 张国荣 / 梁朝伟',
        'quote': '王家卫的纯爱。',
        'rating_people': '400000人评价'
    },
    {
        'title': '功夫',
        'rating': '8.7',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2219011938.jpg',
        'detail_url': 'https://movie.douban.com/subject/1299398/',
        'info': '导演: 周星驰 主演: 周星驰 / 元秋',
        'quote': '中国功夫片巅峰。',
        'rating_people': '1200000人评价'
    },
    {
        'title': '辩护人',
        'rating': '9.2',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2166070055.jpg',
        'detail_url': 'https://movie.douban.com/subject/21937445/',
        'info': '导演: 杨宇硕 主演: 宋康昊 / 吴达洙',
        'quote': '电影的力量。',
        'rating_people': '400000人评价'
    },
    {
        'title': '消失的爱人',
        'rating': '8.7',
        'img_url': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2221768894.jpg',
        'detail_url': 'https://movie.douban.com/subject/21318488/',
        'info': '导演: 大卫·芬奇 主演: 本·阿弗莱克 / 罗莎曼德·派克',
        'quote': '年度最佳心理惊悚片。',
        'rating_people': '800000人评价'
    }
]

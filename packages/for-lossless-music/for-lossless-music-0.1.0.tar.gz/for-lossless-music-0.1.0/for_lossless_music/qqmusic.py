import requests
import urllib.parse
from .song import Song
from .source import *
from .quality import *


def sec2humantime(sec):
    import math
    m = math.ceil(sec / 60)
    s = sec % 60
    return '{:02d}:{:02d}'.format(m, s)


class QQMusic:
    @staticmethod
    def search(keyword, page=1, num=20):
        """search by keyword

        :param keyword: search keyword
        :type keyword: str
        :param page: page index
        :type page: int
        :param num: how many items display on one page you want
        :type num: int
        :return: list[Song]
        """

        # pc
        'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?'
        'p={page}&n={num}&w={keyword}&format=json&inCharset=utf8&outCharset=utf-8'
        r = requests.get(
            # mobile
            'https://c.y.qq.com/soso/fcgi-bin/search_for_qq_cp?'
            'format=json&inCharset=utf-8&outCharset=utf-8&notice=0&platform=h5&needNewCode=1&w={keyword}'
            '&zhidaqu=1&catZhida=1&t=0&flag=1&ie=utf-8&sem=1&aggr=0&perpage={page}&n={num}&p=1&remoteplace=txt.mqq.all'
            .format(page=page, num=num, keyword=urllib.parse.quote_plus(keyword)),
            headers={
                'referer': 'https://y.qq.com/m/index.html'
            },
        )
        json = r.json()
        total = json['data']['song']['totalnum']

        ret = []
        songlist = json['data']['song']['list']
        for i, e in enumerate(songlist):
            # handle tags
            tags = []
            size = {
                'sizeflac': 'FLAC',
                'sizeape' : 'APE',
                'size320' : '320MP3',
                'size128' : '128MP3',
            }
            for k in size:
                if k in e and e[k] > 0:
                    tags.append(size[k])
            ###
            ret.append(Song(id=num*(page-1) + i+1,
                            name=e['songname'],
                            singers=[s['name'] for s in e['singer']],
                            album=e['albumname'],
                            interval=sec2humantime(e['interval']),
                            tags=tags,
                            source=Source.QQ,
                            token=e['songmid'],  # mobile
                            # token=e['media_mid'], # pc
                            ))

        return total, ret

    @staticmethod
    def get_download_urls(song):
        size = {
            # item mean
            # music type: token head
            'FLAC'  : 'F000',
            'APE'   : 'A000',
            '320MP3': 'M800',
            '128MP3': 'M500',
        }

        ret = {}
        for t in song.tags:
            if t in size:
                ret[t] = ('http://streamoc.music.tc.qq.com/{token}.{suffix}?'
                          'vkey=FE178EBB4D55DCF868B4759ADD7A8ACBEFAF88B6558162E8E8DA5A01DFCFB93CEDE02918C068E105E3A3E99267DFF1DCB94B4E8745ABFDD2&guid=MS&uin=123456&fromtag=8'
                          .format(token=size[t] + song.token, suffix=get_suffix_by_quality(t)))
        return ret


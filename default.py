# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, urllib, urllib2, os, re, sys, datetime, time
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from metahandlerpt import metahandlerspt
from tools import *
from datetime import date
import mechanize, cookielib, base64
from resolvers import *

import re, htmlentitydefs
reload(sys)
sys.setdefaultencoding('utf-8')


####################################################### CONSTANTES #####################################################

versao = '0.4.1'
addon_id = 'plugin.video.onsaleuk'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
art = addonfolder + '/resources/art/'
metagetpt = metahandlerspt.MetaData(preparezip=False)
selfAddon = xbmcaddon.Addon(id=addon_id)
username = urllib.quote(selfAddon.getSetting('username'))
password = selfAddon.getSetting('password')
metadata = selfAddon.getSetting('metadata')
ver_intro = True
base_server = 'http://178.62.95.238:8008/'
novelas_base = 'https://assistirnovelas.tv/'
series_base = 'http://assistirserieshd.com/'


################################################### MENUS PLUGIN ######################################################


PUBLIC_TRACKERS = [
    "udp://tracker.publicbt.com:80/announce",
    "udp://tracker.openbittorrent.com:80/announce",
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.istole.it:6969",
    "udp://tracker.coppersurfer.tk:80",
    "udp://tracker.ccc.de:80",
    "udp://tracker.istole.it:80",
    "udp://tracker.1337x.org:80/announce",
    "udp://pow7.com:80/announce",
    "udp://tracker.token.ro:80/announce",
    "udp://9.rarbg.me:2710/announce",
    "udp://ipv4.tracker.harry.lu:80/announce",
    "udp://coppersurfer.tk:6969/announce",
    "udp://bt.rghost.net:80/announce",
    "udp://tracker.publichd.eu/announce",
    "udp://www.eddie4.nl:6969/announce",
    "http://tracker.ex.ua/announce",
    "http://mgtracker.org:2710/announce",
]

def torrent2magnect(url):
    import base64
    import bencode
    import hashlib
    import urllib
    #from xbmctorrent.utils import url_get
    torrent_data = urllib2.urlopen(url).read()
    try:
        import zlib
        torrent_data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(torrent_data)
    except:
        pass
    metadata = bencode.bdecode(torrent_data)
    hashcontents = bencode.bencode(metadata['info'])
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    params = {
        'dn': metadata['info']['name'],
        'tr': metadata['announce'],
    }
    paramstr = urllib.urlencode(params)

    def _boost_magnet(magnet):
        from urllib import urlencode
        return "%s&%s" % (magnet, urlencode({"tr": PUBLIC_TRACKERS}, True))

    magnet = 'magnet:?%s&%s' % ('xt=urn:btih:%s' % b32hash, paramstr)
    return urllib.quote_plus(_boost_magnet(magnet))

def abrir_cookie(url, New=False):
        import mechanize
        import cookielib

        br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
	if not New:
	    cj.load(os.path.join(xbmc.translatePath("special://temp"),"addon_cookies_onsaleuk"), ignore_discard=False, ignore_expires=False)
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        if New:
	    br.open(base_server + 'admin/')
	    br.select_form(nr=0)
	    br.form['password']=password
	    br.form['username']=username
	    br.submit()
	    cj.save(os.path.join(xbmc.translatePath("special://temp"),"addon_cookies_onsaleuk"))
        br.open(url)
        return br.response().read()


def getSoup(url):
    data = abrir_cookie(url).decode('utf8')
    return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)

def Ver_intro():
    if os.path.exists(os.path.join(xbmc.translatePath("special://temp"), "today")):
        ftoday = open(os.path.join(xbmc.translatePath("special://temp"), "today")).read()
        today = str(date.today())
    else:
        ftoday = ''
        today = str(date.today())
    if ftoday != today:
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.m4v')
        while xbmc.Player().isPlaying():
            ftoday = open(os.path.join(xbmc.translatePath("special://temp"), "today"), 'w')
            #today = str(date.today())
            ftoday.write(today)
            ftoday.close()
            time.sleep(1)
        return True

def Menu_inicial():
        #intro = Ver_intro()
    try:
        abrir_cookie(base_server + 'canais/liberar/', True)
        addDir("Tv", "", 1, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
        addDir("Filmes", "1", 1002, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
        addDir("Series", "", 5001, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
        addDir("Programas de TV", "", 4001, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
        xbmc.executebuiltin("Container.SetViewMode(51)")
    except:
        addDir("Apenas para usuários.", "", "-", "https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
        addDir("Caso já tenha login/senha, insira na configuração do addon.", "", "-", "https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
        while xbmc.Player().isPlaying():
            time.sleep(1)
        xbmc.executebuiltin("Container.SetViewMode(502)")



def Menu_Inicial_Tv():
    addDir("Streams Principais", "", 1, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
    addDir("Streams do Brasil(Baixa e Media Qualidade)", "", 1000, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
    #addDir("Opção 3","",2000,"http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
    addDir("Streams Franceses", "", 3000, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    xbmc.executebuiltin("Container.SetViewMode(51)")

def Menu_Inicial_Filmes():
    addDir("1-FILMES ONSALEUK", "1", 201, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("2-FILMES WEB 1", "1", 8820, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("3-FILMES WEB 2", "1", 7001, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    xbmc.executebuiltin("Container.SetViewMode(51)")

def Menu_icial_Melfilme():
    #base_server = 'http://127.0.0.1:8000/canais/'
    categorias = eval(abrir_cookie(base_server + 'canais/melfilme?action=0'))
    for categoria in categorias:
        addDir(unescape(categoria[0]).encode('utf8'), unescape(categoria[1]).encode('utf8') + '|1', 7002, '')

def Categoria(url):
    params = url.split('|')
    print params
    cat = params[0]
    pg = params[1]
    #base_server = 'http://127.0.0.1:8000/canais/'
    filmes = eval(abrir_cookie(base_server + 'canais/melfilme?action=1&cat=%s&pg=%s' % (cat, pg)))
    for filme in filmes:
        addDir(unescape(filme[0]).encode('utf8'), filme[3], 7003, filme[2], pasta=True, total=len(filmes))
    addDir('Proximos >>', cat + '|' + str(int(pg) + 1), 7002, '')
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    xbmc.executebuiltin("Container.SetViewMode(50)")

def melfilme_play(url):
    #base_server = 'http://127.0.0.1:8000/canais/'
    filme = eval(abrir_cookie(base_server + 'canais/melfilme?action=2&id_=%s' % url))
    # play_filme_vod(url,sub,server)
    # addDir(name,url,mode,iconimage,total=0,pasta=True)
    if filme['arquivo_dublado']:
        addDir('Dublado', filme['arquivo_dublado'][0] + "|" + filme['legenda'][0], 7004, '', 2, False)
    if filme['arquivo_legendado']:
        addDir('Legendado', filme['arquivo_legendado'][0] + "|" + filme['legenda'][0], 7004, '', 2, False)


def Menu_Inicial_Series():
    addDir("1-Series WEB", "http://www.filmesonlinegratis.net/series", 8823, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("2-Esportes Gravados", "1", 601, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    xbmc.executebuiltin("Container.SetViewMode(51)")

def canais_master():
    canais = getSoup('https://www.dropbox.com/s/ju2tycbdzwviviy/NovaLista.xml?dl=1')
    for canal in canais('item'):
        addLink(canal.title.text, canal.link.text, canal.thumbnail.text)
    xbmc.executebuiltin("Container.SetViewMode(500)")


def canais_playtvfr():
    canais = eval(abrir_cookie(base_server + 'canais/playtvfr?action=1'))
    for canal in canais:
        addDir(canal[0].encode('utf-8', 'ignore'), canal[2], '3001', canal[1], len(canais), False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def play_playtvfr(url):
    m3u8 = abrir_cookie(base_server + 'canais/playtvfr?action=2&ch=%s' % url)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(m3u8 + '|User-agent=')


def canais_tvzune():
    canais = eval(abrir_cookie(base_server + 'canais/tvzune?action=1'))
    for canal in canais:
        addDir(unescape(canal[0]), unescape(canal[1]), '2001', canal[2], len(canais), False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def play_tvzune(url):
    m3u8 = abrir_cookie(base_server + 'canais/tvzune?action=2&ch=%s' % url)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(m3u8 + '|User-agent=')

def menu_filmes():
    addDir("Pesquisar...", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=mystery|1", 2, "https://www.ibm.com/developerworks/mydeveloperworks/blogs/e8206aad-10e2-4c49-b00c-fee572815374/resource/images/Search-icon.png")
    addDir("+Populares", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Sci-Fi", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=sci-fi|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Acão", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=action|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Comédia", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=comedy|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Thriller", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=thriller|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Romance", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=romance|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Animação", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=animation|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Documentários", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=documentary|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Horror", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=horror|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Drama", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=drama|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Thriller", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=thriller|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
    addDir("Mistério", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=mystery|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")


def listar_filmes(request):
    import json
    pagina = request.split('|')[1]
    request = request.split('|')[0]
    filmes = json.loads(abrir_cookie(base_server + 'filme/filmes?%s' % request))
    # print filmes
    for filme in filmes['MovieList']:
        if not metadata:
            meta_imdb = metagetpt.get_meta('movie', '', imdb_id=filme['imdb'])
        total = len(filmes)
        try:
            if metadata:
                addDirM(filme['title'], str({'torrents': filme['items'], 'imdb': filme['imdb'], 'poster': filme['poster_big']}), 6, filme['poster_big'], total, True)
            else:
                addDirM(filme['title'], str({'torrents': filme['items'], 'imdb': filme['imdb'], 'poster': filme['poster_big']}), 6, filme['poster_big'], total, True, meta_imdb)
        except:
            pass
    addDir("Proximos >>", request.replace("page=%s" % pagina, "page=%s" % str(int(pagina) + 1)) + "|" + str(int(pagina) + 1), 2, "")
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin('Container.SetViewMode(503)')

def listar_torrents(url):
    _dict = eval(url)
    torrents = _dict['torrents']
    for torrent in torrents:
        url = torrent['torrent_url']
        # print torrent
        addDir('[COLOR green](S:%s)[/COLOR][COLOR red](L:%s)[/COLOR]-%s' % (torrent['torrent_seeds'], torrent['torrent_peers'], torrent['file'].encode('utf-8')), str({'torrent': url, 'imdb': _dict['imdb']}), 3, _dict['poster'], 1, False)
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    xbmc.executebuiltin("Container.SetViewMode(51)")

def play_filme(url):
    import thread
    def set_sub(url):
        import os.path
        import glob
        import zipfile
        # os.chdir(xbmc.translatePath("special://temp"))
        # for file_ in glob.glob("*.srt"):
        #        os.remove(file_)
        zip_file = os.path.join(xbmc.translatePath("special://temp"), 'sub2.zip')
        urllib.urlretrieve(url, zip_file)
        zfile = zipfile.ZipFile(zip_file)
        print zfile.namelist()
        #XBMC.Extract(zip_file, xbmc.translatePath("special://temp"))
        #xbmc.executebuiltin("XBMC.Extract(%s, %s)" % (zip_file, xbmc.translatePath("special://temp")))
        print "Sub: " + os.path.join(xbmc.translatePath("special://temp"), zfile.namelist()[0])
        zfile.extract(zfile.namelist()[0], xbmc.translatePath("special://temp"))
        while not xbmc.Player().isPlaying():
            time.sleep(1)
        xbmc.Player().setSubtitles(os.path.join(xbmc.translatePath("special://temp"), zfile.namelist()[0]))

    import json
    filme = eval(url)
    print filme['torrent']
    subs = json.loads(abrir_cookie(base_server + 'filme/subs/%s/' % filme['imdb']))
    try:
        sub_url = 'http://www.yifysubtitles.com' + subs['subs'][filme['imdb']]['brazilian-portuguese'][0]['url']
    except:
        sub_url = ''
    # set_sub(sub_url)
    thread.start_new_thread(set_sub, (sub_url,))
    magnect = torrent2magnect(filme['torrent'])

    #thread.start_new_thread(set_sub, (sub_url,))
    xbmcPlayer = xbmc.Player()
    #xbmcPlayer.play('plugin://plugin.video.pulsar/play?uri=' + magnect)
    xbmcPlayer.play('plugin://plugin.video.xbmctorrent/play/' + magnect)


def play_filme_vod(url, sub, server):
    import thread
    def set_sub(url):
        import os.path
        sub_file = os.path.join(xbmc.translatePath("special://temp"), 'sub.srt')
        urllib.urlretrieve(url, sub_file)
        while not xbmc.Player().isPlaying():
            time.sleep(1)
        xbmc.Player().setSubtitles(os.path.join(xbmc.translatePath("special://temp"), 'sub.srt'))
    thread.start_new_thread(set_sub, (sub,))
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(url)

def play_mult_canal(arg, icon, nome):
    try:
        tuple_ = eval(arg)
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        for link in tuple_:
            listitem = xbmcgui.ListItem(nome, thumbnailImage=iconimage)
            listitem.setInfo('video', {'Title': nome})
            playlist.add(url=link, listitem=listitem, index=7)
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)

    except:
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(nome, thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': nome})
        playlist.add(url=arg, listitem=listitem, index=7)
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)

def listar_categorias_filmes(url):
    soup = getSoup(url)
    categorias = soup('categoria')
    import HTMLParser
    pars = HTMLParser.HTMLParser()
    pars.unescape('&copy; &euro;')
    for categoria in categorias:
        addDir(unescape(categoria.nome.text).encode('utf8'), base_server + 'vod/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text, 103, categoria.logo.text)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def listar_filmes_vod(url):

    soup = getSoup(url)
    filmes = soup('filme')
    total = len(filmes)

    for filme in filmes:
        # addDir(name,url,mode,iconimage,total=0,pasta=True)
        addDir('%s [COLOR red]%s[/COLOR] [COLOR green]%s[/COLOR]' % (unescape(filme.nome.text).encode('utf8'), filme.vdr.text.encode('utf8'), filme.server.text.encode('utf8')), str((filme.link.text, filme.sub.text, filme.server.text)), 4, filme.thumbnail.text, total, False, filme.descricao.text, filme.fanart.text)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmc.executebuiltin("Container.SetViewMode(515)")

def listar_series_vod(url):

    soup = getSoup(url)
    series = soup('serie')
    total = len(series)

    for serie in series:
            # addDirM(serie.titulo.text.encode('utf8'),serie.pk.text,604,serie.thumbnail.text,True,total,'',plot=serie.plot.text)
        addDir(serie.titulo.text.encode('utf8'), serie.pk.text, 602, serie.thumbnail.text, total, True, serie.plot.text, serie.fanart.text)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_series_temporadas_vod(url):
    soup = getSoup(base_server + 'vod/xml_s/?action=temporadas&series_pk=' + url)
    temporadas = soup('temporada')
    total = len(temporadas)

    for temporada in temporadas:
        # addDirM(serie.titulo.text.encode('utf8'),serie.pk.text,604,serie.thumbnail.text,True,total,'',plot=serie.plot.text)
        addDir('%s - Temporada %s' % (temporada.serie.text.encode('utf8'), temporada.numero.text.encode('utf8')), temporada.pk.text, 603, temporada.thumbnail.text, total, True)

def listar_serie_episodios_vod(url):
    soup = getSoup(base_server + 'vod/xml_s/?action=episodios&temporada_pk=' + url)
    episodios = soup('episodio')
    total = len(episodios)

    for episodio in episodios:
        #	play_filme_vod(params[0],params[1],server='')
        # addDirM(serie.titulo.text.encode('utf8'),serie.pk.text,604,serie.thumbnail.text,True,total,'',plot=serie.plot.text)
        addDir('%s - %s' % (episodio.numero.text.encode('utf8'), episodio.titulo.text.encode('utf8')), episodio.link.text + '|' + episodio.sub.text + '|', 7004, episodio.thumbnail.text, total, False, episodio.plot.text, episodio.fanart.text)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmc.executebuiltin('Container.SetViewMode(515)')

def listar_categorias(url):
    soup = getSoup(url)
    categorias = soup('categoria')
    for categoria in categorias:
        # print categoria.nome
        if categoria.nome.text == 'XXX':
            addDir(categoria.nome.text, base_server + 'canais/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text, 104, categoria.logo.text)
        else:
            addDir(categoria.nome.text, base_server + 'canais/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text, 102, categoria.logo.text)

    xbmc.executebuiltin("Container.SetViewMode(500)")

def listar_canais_xxx(url):
    keyb = xbmc.Keyboard('', 'XXX')  # Chama o keyboard do XBMC com a frase indicada
    keyb.doModal()  # Espera ate que seja confirmada uma determinada string
    if (keyb.isConfirmed()):
        if keyb.getText() == '0000':
            #epg = eval(abrir_cookie(base_server + 'canais/epg/'))

            soup = getSoup(url)
            canais = soup('canal')
            print epg

            for canal in canais:
                try:
                    canal_programa = epg[canal.epg.text]['programa']
                except:
                    canal_programa = ''
                if canal_programa:
                    addDir(canal.nome.text + ' - [COLOR green](%s)[/COLOR]' % canal_programa, canal.link.text, 105, canal.logo.text, 1, False)
                else:
                    addDir(canal.nome.text, canal.link.text, 105, canal.logo.text, 1, False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

# addDir(name,url,mode,iconimage,total=0,pasta=True)
def listar_canais(url):

    #epg = eval(abrir_cookie(base_server + 'canais/epg/'))

    soup = getSoup(url)
    canais = soup('canal')
    # print epg

    for canal in canais:
        # print canal
        # addDir(canal.nome.text.encode('utf8'),canal.link.text.encode('utf8'),105,canal.logo.text.encode('utf8'),1,False)
        try:
            canal_programa = epg[canal.epg.text]['programa'].encode('utf8')
        except:
            canal_programa = ''
        if canal_programa:
            try:
                addDir(canal.nome.text.decode('utf8') + '  [COLOR red](' + canal_programa + ')[/COLOR]', canal.link.text.decode('utf8'), 105, canal.logo.text.encode('utf8'), 1, False)
            except:
                addDir(canal.nome.text.encode('utf8'), canal.link.text.encode('utf8'), 105, canal.logo.text.encode('utf8'), 1, False)
        else:
            addDir(canal.nome.text.encode('utf8'), canal.link.text.encode('utf8'), 105, canal.logo.text.encode('utf8'), 1, False)

    xbmc.executebuiltin("Container.SetViewMode(500)")


def categorias_filmes2():
    addDir('Ação', 'http://www.filmesonlinegratis.net/acao', 8821, '')
    addDir('Animação', 'http://www.filmesonlinegratis.net/animacao', 8821, '')
    addDir('Aventura', 'http://www.filmesonlinegratis.net/aventura', 8821, '')
    addDir('Comedia', 'http://www.filmesonlinegratis.net/comedia', 8821, '')
    addDir('Comedia Romantica', 'http://www.filmesonlinegratis.net/comedia-romantica', 8821, '')
    addDir('Crime', 'http://www.filmesonlinegratis.net/crime', 8821, '')
    addDir('Documentários', 'http://www.filmesonlinegratis.net/documentario', 8821, '')
    addDir('Drama', 'http://www.filmesonlinegratis.net/drama', 8821, '')
    addDir('Faroeste', 'http://www.filmesonlinegratis.net/faroeste', 8821, '')
    addDir('Ficção', 'http://www.filmesonlinegratis.net/ficcao-cientifica', 8821, '')
    addDir('Guerra', 'http://www.filmesonlinegratis.net/guerra', 8821, '')
    addDir('Musical', 'http://www.filmesonlinegratis.net/musical', 8821, '')
    addDir('Policial', 'http://www.filmesonlinegratis.net/policial', 8821, '')
    addDir('Romance', 'http://www.filmesonlinegratis.net/romance', 8821, '')
    addDir('Suspense', 'http://www.filmesonlinegratis.net/suspense', 8821, '')
    # addDir('Series','http://www.filmesonlinegratis.net/series',8821,'')
    addDir('Terror', 'http://www.filmesonlinegratis.net/terror', 8821, '')
    addDir('Thriller', 'http://www.filmesonlinegratis.net/thriller', 8821, '')

def listar_videos_series2(url):
    codigo_fonte = abrir_url(url)
    soup = BeautifulSoup(abrir_url(url))
    stage = 0
    try:
        try:
            series = soup("ul", {"class": "videos series"})
            temporadas = series[0]('li')
        except:
            series = soup("ul", {"class": "videos"})
            temporadas = series[0]('li')
        temp = []
        for temporada_ in temporadas:
            temporada = html_replace_clean(temporada_.b.text.encode('ascii', 'xmlcharrefreplace'))
            for episodio in temporada_('a'):
                a = [temporada + html_replace_clean(episodio.text.encode('ascii', 'xmlcharrefreplace')), episodio['href'], 8822, '', 0, False]
                if a not in temp:
                    temp.append(a)
        for a in temp:
            addDir(a[0], a[1], a[2], a[3], len(temp), False)
        return
    except:
        pass
        series = soup("ul", {"class": "videos"})
        tables = series[0]('table')
        temp = []
        for table in tables:
            for td in table('td'):
                temporada = html_replace_clean(td.b.text.encode('ascii', 'xmlcharrefreplace'))
                for episodio in td('a', {"class": "bs-episodio"}):
                    a = [temporada + html_replace_clean(episodio.text.encode('ascii', 'xmlcharrefreplace')), episodio['href'], 8822, '', 0, False]
                    if a not in temp:
                        temp.append(a)
        for a in temp:
            addDir(a[0], a[1], a[2], a[3], len(temp), False)
        return   
    
    try:
        temp = []
        temporada = "Temporada ?"
        for b in soup('b'):
            if "Temporada" in b.text:
                temporada = html_replace_clean(b.text.encode('ascii', 'xmlcharrefreplace'))
        for episodio in soup('a', {"class": "bs-episodio"}):
            a = [temporada + html_replace_clean(episodio.text.encode('ascii', 'xmlcharrefreplace')), episodio['href'], 8822, '', 0, False]
            if a not in temp:
                temp.append(a)
        for a in temp:
            addDir(a[0], a[1], a[2], a[3], len(temp), False)
        return
    except:
        pass

def listar_series2(url):
    codigo_fonte = abrir_url(url)
    soup = BeautifulSoup(abrir_url(url))
    lista_filmes = BeautifulSoup(soup.find("div", {"class": "miniaturas"}).prettify())
    filmes = lista_filmes.findAll("article", {"class": "miniatura"})
    a = []
    for filme in filmes:
        plot = ''
        for div in filme('div'):
            if 'Sinopse' in div.text:
                plot = div('p')[len(div('p')) - 1].text.replace('Sinopse:', '')
                break
        if not plot:
            plot = filme('span')[1].text
        temp = [filme('div')[0].a["href"], html_replace_clean(filme('img')[0]["alt"].encode('ascii', 'xmlcharrefreplace')), filme('img')[0]["src"], html_replace_clean(plot.encode('ascii', 'xmlcharrefreplace'))] 
        a.append(temp)
    total = len(a)
    for url2, titulo, img, plot in a:
        titulo = titulo.replace('&#8211;', "-").replace('&#8217;', "'")
        # addDir(name,url,mode,iconimage,total=0,pasta=True,plot='',fanart='')
	titulo = re.sub(r'-.*?$','',titulo)
        addDir(titulo, url2, 8824, img, total, True, plot)

    p_page = soup.find('a', {'class': 'page larger'})
    if p_page:
        addDir('Página Seguinte >>', p_page['href'], 8823, '')

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin('Container.SetViewMode(503)')

def listar_videos_filmes2(url):
    codigo_fonte = abrir_url(url)
    soup = BeautifulSoup(abrir_url(url))
    lista_filmes = BeautifulSoup(soup.find("div", {"class": "miniaturas"}).prettify())
    filmes = lista_filmes.findAll("article", {"class": "miniatura"})
    a = []
    for filme in filmes:
        plot = ''
        for div in filme('div'):
            if 'Sinopse' in div.text:
                plot = div('p')[len(div('p')) - 1].text.replace('Sinopse:', '')
                break
        if not plot:
            plot = filme('span')[1].text
        temp = [filme('div')[0].a["href"], html_replace_clean(filme('img')[0]["alt"].encode('ascii', 'xmlcharrefreplace')), filme('img')[0]["src"], html_replace_clean(plot.encode('ascii', 'xmlcharrefreplace'))] 
        a.append(temp)
    total = len(a)
    for url2, titulo, img, plot in a:
        titulo = titulo.replace('&#8211;', "-").replace('&#8217;', "'")
        # addDir(name,url,mode,iconimage,total=0,pasta=True,plot='',fanart='')
        addDir(titulo, url2, 8822, img, total, False, plot)

    p_page = soup.find('a', {'class': 'page larger'})
    if p_page:
        addDir('Página Seguinte >>', p_page['href'], 8821, '')

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin('Container.SetViewMode(503)')


def player_filmes2(name, url, iconimage):
    google = r'src="(.*?google.*?/preview)"'
    picasa = r'src="(.*?filmesonlinebr.*?/player/.*?)"'
    vk = r'src="(.*?vk.*?/video.*?)"'
    nvideo = r'src="(.*?nowvideo.*?/embed.*?)"'
    dropvideo = r'src="(.*?dropvideo.*?/embed.*?)"'
    vodlocker = r'src="(.*?vodlocker.*?/embed.*?)"'
    firedrive = r'src="(.*?firedrive.*?/embed/.*?)"'
    firedrive2 = r'http://www.armagedomfilmes.biz/player/armage.php.id=(.*?)"'
    dropmega = r'src=".*?drop.*?id=(.*?)"'
    cloudzilla = r'cloudzilla.php.id=(.*?)"'
    cloudzilla_f = r'http://www.cloudzilla.to/share/file/(.*?)"'
    videott = r'value="(http://video.tt/e/.*?)" >'
    videobis = r'<IFRAME SRC="(http://videobis.net/.*?)" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=.*? HEIGHT=.*?></IFRAME>'
    videopw = r'<iframe src="(http://video.pw/e/.*?/)" scrolling="no" frameborder="0" width=".*?" height=".*?"></iframe>'
    vidzi = r'(http://vidzi.tv/.*?.html)'
    videomail = r'(http://videoapi.my.mail.ru/.*?.html)'
    vidig_s = r'vd=(.*?)"'  # http://vidigvideo.com/embed-%s-885x660.html
    vidig = r'(http://vidigvideo.com/.*?.html)'
    dropvideo_s = r'dv=(.*?)"'
    cludzilla_s = r'cz=(.*?)"'  # http://vidigvideo.com/embed-%s-885x660.html
    cloudzilla_e = r'src="(http://www.cloudzilla.to/embed/.*?)"'
    mensagemprogresso = xbmcgui.DialogProgress()
    mensagemprogresso.create('Onsaleuk', 'A resolver link', 'Por favor aguarde...')
    mensagemprogresso.update(33)
    links = []
    hosts = []
    matriz = []
    codigo_fonte = abrir_url(url)
    # try: url_video = re.findall(r'<iframe src="(.*?)" width="738" height="400" frameborder="0"></iframe></li>',codigo_fonte)[0]
    # <iframe src="(.*?)" width="738" height="400" frameborder="0"></iframe></li>
    # except: return
    try:
        links.append(re.findall(cloudzilla_e, codigo_fonte)[0])  # http://www.cloudzilla.to/embed/%s
        hosts.append('CloudZilla')
    except:
        pass

    
    try:
        links.append('http://www.cloudzilla.to/embed/%s' % re.findall(cludzilla_s, codigo_fonte)[0])  # http://www.cloudzilla.to/embed/%s
        hosts.append('CloudZilla')
    except:
        pass


    try:
        links.append('http://dropvideo.com/embed/%s' % re.findall(dropvideo_s, codigo_fonte)[0])  # http://dropvideo.com/embed/%s
        hosts.append('DropVideo')
    except:
        pass


    try:
        links.append('http://vidigvideo.com/embed-%s-885x660.html' % re.findall(vidig_s, codigo_fonte)[0])
        hosts.append('Vidig')
    except:
        pass

    try:
        links.append(re.findall(vidig, codigo_fonte)[0])
        hosts.append('Vidig')
    except:
        pass

    try:
        links.append(re.findall(videomail, codigo_fonte)[0])
        hosts.append('Videomail')
    except:
        pass

    try:
        links.append(re.findall(videopw, codigo_fonte)[0])
        hosts.append('Video.Pw')
    except:
        pass

    try:
        links.append(re.findall(vidzi, codigo_fonte)[0])
        hosts.append('Vidzi')
    except:
        pass

    try:
        links.append(re.findall(videobis, codigo_fonte)[0])
        hosts.append('VideoBis')
    except:
        pass

    try:
        links.append(re.findall(videott, codigo_fonte)[0])
        hosts.append('Video.TT')
    except:
        pass

    try:
        links.append(re.findall(picasa, codigo_fonte)[0])
        hosts.append('Picasa')
    except:
        pass

    try:
        links.append(re.findall(google, codigo_fonte)[0])
        hosts.append('Gdrive')
    except:
        pass

    try:
        links.append(re.findall(vk, codigo_fonte)[0])
        hosts.append('Vk')
    except:
        pass

    try:
        links.append(re.findall(nvideo, codigo_fonte)[0])
        hosts.append('Nowvideo - Sem suporte')
    except:
        pass

    try:
        links.append(re.findall(dropvideo, codigo_fonte)[0])
        hosts.append('Dropvideo')
    except:
        pass

    try:
        links.append('http://www.dropvideo.com/embed/' + re.findall(dropmega, codigo_fonte)[0])
        hosts.append('Dropvideo')
    except:
        pass

    try:
        links.append('http://www.cloudzilla.to/embed/' + re.findall(cloudzilla, codigo_fonte)[0])
        hosts.append('CloudZilla')
    except:
        pass

    try:
        links.append('http://www.cloudzilla.to/embed/' + re.findall(cloudzilla_t, codigo_fonte)[0])
        hosts.append('CloudZilla(Legendado)')
    except:
        pass
    try:
        links.append(re.findall(vodlocker, codigo_fonte)[0])
        hosts.append('Vodlocker')
    except:
        pass

    # eseffair 14/03/2014
    # Vou implementar posteriormente
    try:
        links.append('http://www.firedrive.com/embed/' + re.findall(firedrive2, codigo_fonte)[0])
        hosts.append('Firedrive')
    except:
        pass


    if not hosts:
        mensagemprogresso.update(100)
        mensagemprogresso.close()
        return

    index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)

    if index == -1:
        return

    url_video = links[index]
    mensagemprogresso.update(66)

    if 'google' in url_video:
        matriz = obtem_url_google(url_video)
    elif 'dropvideo.com/embed' in url_video:
        matriz = obtem_url_dropvideo(url_video)   # esta linha está a mais
    elif 'filmesonlinebr.info/player' in url_video:
        matriz = obtem_url_picasa(url_video)
    elif 'vk.com/video_ext' in url_video:
        matriz = obtem_url_vk(url_video)
    elif 'vodlocker.com' in url_video:
        matriz = obtem_url_vodlocker(url_video)
    elif 'firedrive.com/embed' in url_video:
        matriz = obtem_url_firedrive(url_video)
    elif 'cloudzilla' in url_video:
        matriz = obtem_cloudzilla(url_video)
    elif 'http://video.tt' in url_video:
        matriz = obtem_videott(url_video)
    elif 'videobis.net' in url_video:
        matriz = obtem_videobis(url_video)  # video.pw
    elif 'video.pw' in url_video:
        matriz = obtem_videopw(url_video)  # video.pw
    elif 'vidzi.tv' in url_video:
        matriz = obtem_vidig(url_video)
    elif 'mail.ru' in url_video:
        matriz = obtem_videomail(url_video)
    elif 'vidigvideo.com' in url_video:
        matriz = obtem_vidig2(url_video)
    else:
        print "Falha: " + str(url_video)

    url = matriz[0]

    if url == '-':
        mensagemprogresso.update(100)
        mensagemprogresso.close()
        return

    mensagemprogresso.update(100)
    mensagemprogresso.close()

    listitem = xbmcgui.ListItem()  # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
    listitem.setPath(url)
    listitem.setProperty('mimetype', 'video/mp4')
    listitem.setProperty('IsPlayable', 'true')
    # try:
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(url)
    return

def Listar_categorias_series(url=series_base):
    print url
    html = abrir_url(url)
    #html = html.encode('ascii','xmlcharrefreplace')

    soup = BeautifulSoup(html, convertEntities=BeautifulStoneSoup.XML_ENTITIES)

    a = []
    links = soup("a", {"rel": "nofollow"})
    #ow = open('G:\html_list\series.html', 'w')
    # ow.write(str(links))
    # ow.close()
    # print links
    # print menu
    #resultados = content.findAll("td",  { "width" : "1%" })
    for link in links:
        if len(link.text) == 1:
            # print link['href']
            addDir('Séries com a letra: ' + html_replace_clean(link.text.encode('ascii', 'xmlcharrefreplace')).upper(), series_base + link['href'], 5003, 'http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png', len(links), True)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin('Container.SetViewMode(51)')

def Listar_categorias(url=novelas_base):
    print url
    html = abrir_url2(url)
    #html = html.encode('ascii','xmlcharrefreplace')
    soup = BeautifulSoup(html, convertEntities=BeautifulStoneSoup.XML_ENTITIES)

    a = []
    menu = soup("div", {"id": "Menu"})[1]
    # print menu
    links = menu("a")
    #resultados = content.findAll("td",  { "width" : "1%" })
    for link in links:
        if not link['href'] == '#' and not html_replace_clean(link.text.encode('ascii', 'xmlcharrefreplace')) == 'Pagina Inicial':
            # print link['href']
            addDir(html_replace_clean(link.text.encode('ascii', 'xmlcharrefreplace')), link['href'], 4002, 'http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png', len(links), True)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin('Container.SetViewMode(51)')

def Listar_episodios(url):
    print url
    html = abrir_url2(url)
    #html = unicode(html, 'ascii', errors='ignore')
    soup = BeautifulSoup(html)

    a = []
    categorias = soup("div", {"class": "CategoriasLista"})[0]
    # print categorias
    episodios = categorias("div", {"class": "Item"})
    for episodio in episodios:
        img = episodio.img['src']
        titulo = html_replace_clean(episodio.img['alt'].encode('ascii', 'xmlcharrefreplace'))  # episodio.img['alt']
        url = episodio.a['href']
        # addDir(name,url,mode,iconimage,total=0,pasta=True)
        addDir(titulo, url, 4003, img, len(episodios), False)
    try:
        links = soup("div", {"class": "Botaos"})[0]('a')
        for link in links:
            if not link['href'] == url:
                url = link['href']
        if len(episodios) == 11:
            addDir("Proxima Pagina >>", url, 4002, '', len(episodios) + 1)
        else:
            addDir("<< Pagina Anterior", url, 4002, '', len(episodios) + 1)
    except:
        pass
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmc.executebuiltin('Container.SetViewMode(503)')

def listar_series(url):
    print url
    html = abrir_url(url)
    #html = unicode(html, 'ascii', errors='ignore')
    soup = BeautifulSoup(html)

    a = []
    categorias = soup("div", {"id": "Conteudo"})[0]
    # print str(categorias)

    series = categorias("div", {"class": "amazingcarousel-image"})
    for serie in series:
        # print serie
        img = serie.img['src']
        titulo = html_replace_clean(serie.img['alt'].encode('ascii', 'xmlcharrefreplace'))  # episodio.img['alt']
        url = serie.a['href']
        # addDir(name,url,mode,iconimage,total=0,pasta=True)
        addDir(titulo, url, 5004, img, len(series), True)
        #xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        # xbmc.executebuiltin('Container.SetViewMode(503)')

def Listar_episodios_series(url):
    # print url
    html = abrir_url(url)
    #html = unicode(html, 'ascii', errors='ignore')
    soup = BeautifulSoup(html)

    a = []
    categorias = soup("div", {"id": "Conteudo"})[0]
    # print str(categorias)

    episodios = categorias("div", {"class": "Episodio"})

    for episodio in episodios:
        img = episodio.img['src']
        titulo = html_replace_clean(episodio.img['alt'].encode('ascii', 'xmlcharrefreplace'))  # episodio.img['alt']
        url = episodio.a['href']
        # addDir(name,url,mode,iconimage,total=0,pasta=True)
        addDir(titulo, url, 5005, img, len(episodios), False)
    if len(episodios) == 0:
        addDir('Esta temporada não tem episodios ainda...aguarde.', '', 0, '', 0, False)
    links = soup("div", {"class": "Temporadas"})[0]('a')
    ow = open('G:\html_list\series.html', 'w')
    ow.write(str(url))
    ow.close()
    if len(links) > 1:
        addDir('---------------------------', '', 0, '', 0, False)
    for link in links:
        if not link['href'] == '#':
            addDir("Temporada: " + link.string, link['href'], 5004, '', len(episodios) + 1)

    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmc.executebuiltin('Container.SetViewMode(503)')

def Resolve_episodio_serie(url):
        # print url
    pg = 0
    mensagemprogresso = xbmcgui.DialogProgress()
    mensagemprogresso.create('Trabalhando', 'Gerando playlist', 'Por favor aguarde...')
    pg += 10
    mensagemprogresso.update(pg)
    html = abrir_url(url)
    soup = BeautifulSoup(html)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    pg += 10
    mensagemprogresso.update(pg)
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    pg += 10
    mensagemprogresso.update(pg)
    br.open(series_base)
    br.select_form(nr=0)
    br.form['senha'] = base64.b64decode('MTIzNDU2')
    br.form['email'] = base64.b64decode('YXJsZWlyYS5jYXN0cm9AZ21haWwuY29t')
    br.submit()
    pg += 10
    mensagemprogresso.update(pg)
    page = br.open(url).read()

    links = re.findall('src: "(.*?)"', page)
    pg += 10
    mensagemprogresso.update(pg)
    if links:
        for link in links:
            listitem = xbmcgui.ListItem('Epsodio', thumbnailImage='')
            listitem.setInfo('video', {'Title': 'Episodio'})
            playlist.add(url=link, listitem=listitem, index=7)
        mensagemprogresso.update(100)
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
    else:
        mensagemprogresso.update(100)
        dialog = xbmcgui.Dialog()
        dialog.ok("Indisponivel", "Este ainda não esta disponivel, tente novamente em breve.")

def Resolve_episodio(url):
    # print url
    pg = 0
    mensagemprogresso = xbmcgui.DialogProgress()
    mensagemprogresso.create('Trabalhando', 'Gerando playlist', 'Por favor aguarde...')
    pg += 10
    mensagemprogresso.update(pg)
    html = abrir_url(url)
    soup = BeautifulSoup(html)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    pg += 10
    mensagemprogresso.update(pg)
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    pg += 10
    mensagemprogresso.update(pg)
    br.open('https://assistirnovelas.tv')
    form = base64.b64decode('PGZvcm0gYWN0aW9uPSJodHRwczovL2Fzc2lzdGlybm92ZWxhcy50di9Mb2dpblVzdWFyaW8ucGhwIiBpZD0iZm9ybTEiIG1ldGhvZD0icG9zdCI+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT5FLW1haWw8L2xpPg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8bGk+PGlucHV0IHR5cGU9InRleHQiIHZhbHVlPSIiIG5hbWU9ImVtYWlsIiBjbGFzcz0iQ2FtcG9Mb2dpbiIgcGxhY2Vob2xkZXI9IlNldSBlLW1haWwiPjwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT5TZW5oYTwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT48aW5wdXQgdmFsdWU9IiIgbmFtZT0ic2VuaGEiIGNsYXNzPSJDYW1wb0xvZ2luIiBwbGFjZWhvbGRlcj0iU3VhIHNlbmhhIiB0eXBlPSJwYXNzd29yZCI+PC9saT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjxpbnB1dCB0eXBlPSJzdWJtaXQiIGNsYXNzPSJMb2dpbkluaWNpbyIgdmFsdWU9IkVudHJhciI+PC9saT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHBzOi8vYXNzaXN0aXJub3ZlbGFzLnR2L2NhZGFzdHJvLnBocCI+UmVnaXN0cmFyPC9hPjwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwczovL2Fzc2lzdGlybm92ZWxhcy50di9sZW1icmFyX3NlbmhhLnBocCI+TGVtYnJhciBzZW5oYTwvYT48L2xpPg0KICAgICAgICAgICAgICAgICAgPC9mb3JtPg==')
    res = mechanize._form.ParseString(form, "https://assistirnovelas.tv")
    br.form = res[1]
    # br.select_form(nr=0)
    br.form['senha'] = base64.b64decode('MTIzNDU2')
    br.form['email'] = base64.b64decode('YXJsZWlyYS5jYXN0cm9AZ21haWwuY29t')
    br.submit()
    pg += 10
    mensagemprogresso.update(pg)
    page = br.open(url).read()
    links = re.findall("file':.'(.*?mp4.*?)'", page)
    pg += 10
    mensagemprogresso.update(pg)
    if links:
        for link in links:
            listitem = xbmcgui.ListItem('Epsodio', thumbnailImage='')
            listitem.setInfo('video', {'Title': 'Episodio'})
            playlist.add(url=link, listitem=listitem, index=7)
        mensagemprogresso.update(100)
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
    else:
        mensagemprogresso.update(100)
        dialog = xbmcgui.Dialog()
        dialog.ok("Indisponivel", "Este ainda não esta disponivel, tente novamente em breve.")


################################################## PASTAS ################################################################

def addLink(name, url, iconimage):
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('fanart_image', "%s/fanart.jpg" % selfAddon.getAddonInfo("path"))
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)

def addDir(name, url, mode, iconimage, total=0, pasta=True, plot='', fanart=''):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
    contextMenuItems = []
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)

def addDirM(name, url, mode, iconimage, pasta=True, total=1, meta=metagetpt.get_meta('movie', '', ''), plot=''):
    if plot and not meta['plot'] or meta['plot'] == 'N/A':
        meta['plot'] = plot
    if iconimage and not meta['cover_url']:
        meta['cover_url'] = iconimage
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage='http://image.tmdb.org/t/p/original/' + os.path.split(meta['cover_url'])[1], thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels=meta)
    contextMenuItems = []
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
    if not meta['backdrop_url'] == '':
        liz.setProperty('fanart_image', 'http://image.tmdb.org/t/p/original/' + os.path.split(meta['backdrop_url'])[1])
    else:
        try:
            liz.setProperty('fanart_image', fanart)
        except:
            liz.setProperty('fanart_image', '')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
#        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
#	xbmc.executebuiltin('Container.SetViewMode(51)')
    return ok


######################################################## OUTRAS FUNCOES ###############################################

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]                 
    return param

params = get_params()
url = None
name = None
mode = None
tamanhoparavariavel = None
iconimage = None

try: url = urllib.unquote_plus(params["url"])
except: pass
try: tamanhoparavariavel = urllib.unquote_plus(params["tamanhof"])
except: pass
try: iconimage = urllib.unquote_plus(params["iconimage"])
except: pass
try: name = urllib.unquote_plus(params["name"])
except: pass
try: mode = int(params["mode"])
except: pass

# print "Mode: "+str(mode).decode('utf-8')
# print "URL: "+str(url).decode('utf-8')
# print "Name: "+str(name).decode('utf-8')
# print "Icon: "+str(iconimage).decode('utf-8')
# print "Name: "+str(tamanhoparavariavel).decode('utf-8')

if mode == None:
    Menu_inicial()
elif mode == 1001:
    Menu_Inicial_Tv()
elif mode == 1002:
    Menu_Inicial_Filmes()
elif mode == 1:
    listar_categorias(base_server + 'canais/xml?action=categorias')
elif mode == 102:
    listar_canais(url)
elif mode == 103:
    listar_filmes_vod(url)
elif mode == 104:
    listar_canais_xxx(url)
elif mode == 105:
    play_mult_canal(url, iconimage, name)
elif mode == 200:
    menu_filmes()
elif mode == 201:
    listar_categorias_filmes(base_server + 'vod/xml/?action=categorias')
elif mode == 2:
    listar_filmes(url)
elif mode == 3:
    play_filme(url)
elif mode == 4:
    params = eval(url)
    play_filme_vod(params[0], params[1], params[2])
elif mode == 6:
    listar_torrents(url)
elif mode == 1000:
    canais_master()
elif mode == 2000:
    canais_tvzune()
elif mode == 2001:
    play_tvzune(url)
elif mode == 3000:
    canais_playtvfr()
elif mode == 3001:
    play_playtvfr(url)
elif mode == 4001:
    Listar_categorias()
elif mode == 4002:
    Listar_episodios(url)
elif mode == 4003:
    Resolve_episodio(url)
elif mode == 5001:
    Menu_Inicial_Series()
elif mode == 5002:
    Listar_categorias_series()
elif mode == 5003:
    listar_series(url)
elif mode == 5004:
    Listar_episodios_series(url)
elif mode == 5005:
    Resolve_episodio_serie(url)
elif mode == 7001:
    Menu_icial_Melfilme()
elif mode == 7002:
    Categoria(url)
elif mode == 7003:
    melfilme_play(url)
elif mode == 7004:
    params = url.split('|')
    play_filme_vod(params[0], params[1], server='')
elif mode == 601:
    listar_series_vod(base_server + 'vod/xml_s/?action=series')
elif mode == 602:
    listar_series_temporadas_vod(url)
elif mode == 603:
    listar_serie_episodios_vod(url)
elif mode == 8820:
    categorias_filmes2()
elif mode == 8821:
    listar_videos_filmes2(url)
elif mode == 8822:
    player_filmes2(name, url, iconimage)
elif mode == 8823:
    listar_series2(url)
elif mode == 8824:
    listar_videos_series2(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
## -*- coding: utf-8 -*-
#import xbmc, xbmcaddon, xbmcgui, xbmcplugin, urllib, urllib2, os, re, sys, datetime, time
#from BeautifulSoup import BeautifulSoup
#from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
#from metahandlerpt import metahandlerspt
#from tools import *
#from datetime import date
#import mechanize, cookielib, base64
#from resolvers import *
#
#import re, htmlentitydefs
#reload(sys)
#sys.setdefaultencoding('utf-8')
#
#
######################################################## CONSTANTES #####################################################
#
#versao = '0.4.1'
#addon_id = 'plugin.video.onsaleuk'
#selfAddon = xbmcaddon.Addon(id=addon_id)
#addonfolder = selfAddon.getAddonInfo('path')
#art = addonfolder + '/resources/art/'
#metagetpt = metahandlerspt.MetaData(preparezip=False)
#selfAddon = xbmcaddon.Addon(id=addon_id)
#username = urllib.quote(selfAddon.getSetting('username'))
#password = selfAddon.getSetting('password')
#metadata = selfAddon.getSetting('metadata')
#ver_intro = True
#base_server = 'http://178.62.95.238:8008/'
#novelas_base = 'https://assistirnovelas.tv/'
#series_base = 'http://assistirserieshd.com/'
#
#
#################################################### MENUS PLUGIN ######################################################
#
#
#PUBLIC_TRACKERS = [
#    "udp://tracker.publicbt.com:80/announce",
#    "udp://tracker.openbittorrent.com:80/announce",
#    "udp://open.demonii.com:1337/announce",
#    "udp://tracker.istole.it:6969",
#    "udp://tracker.coppersurfer.tk:80",
#    "udp://tracker.ccc.de:80",
#    "udp://tracker.istole.it:80",
#    "udp://tracker.1337x.org:80/announce",
#    "udp://pow7.com:80/announce",
#    "udp://tracker.token.ro:80/announce",
#    "udp://9.rarbg.me:2710/announce",
#    "udp://ipv4.tracker.harry.lu:80/announce",
#    "udp://coppersurfer.tk:6969/announce",
#    "udp://bt.rghost.net:80/announce",
#    "udp://tracker.publichd.eu/announce",
#    "udp://www.eddie4.nl:6969/announce",
#    "http://tracker.ex.ua/announce",
#    "http://mgtracker.org:2710/announce",
#]
#
#def torrent2magnect(url):
#    import base64
#    import bencode
#    import hashlib
#    import urllib
#    #from xbmctorrent.utils import url_get
#    torrent_data = urllib2.urlopen(url).read()
#    try:
#        import zlib
#        torrent_data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(torrent_data)
#    except:
#        pass
#    metadata = bencode.bdecode(torrent_data)
#    hashcontents = bencode.bencode(metadata['info'])
#    digest = hashlib.sha1(hashcontents).digest()
#    b32hash = base64.b32encode(digest)
#    params = {
#        'dn': metadata['info']['name'],
#        'tr': metadata['announce'],
#    }
#    paramstr = urllib.urlencode(params)
#
#    def _boost_magnet(magnet):
#        from urllib import urlencode
#        return "%s&%s" % (magnet, urlencode({"tr": PUBLIC_TRACKERS}, True))
#
#    magnet = 'magnet:?%s&%s' % ('xt=urn:btih:%s' % b32hash, paramstr)
#    return urllib.quote_plus(_boost_magnet(magnet))
#
#def abrir_cookie(url):
#    import mechanize
#    import cookielib
#
#    br = mechanize.Browser()
#    cj = cookielib.LWPCookieJar()
#    br.set_cookiejar(cj)
#    br.set_handle_equiv(True)
#    br.set_handle_gzip(True)
#    br.set_handle_redirect(True)
#    br.set_handle_referer(True)
#    br.set_handle_robots(False)
#    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#    br.open(base_server + 'admin')
#    br.select_form(nr=0)
#    br.form['password'] = password
#    br.form['username'] = username
#    br.submit()
#    br.open(url)
#    return br.response().read()
#
#
#def getSoup(url):
#    data = abrir_cookie(url).decode('utf8')
#    return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
#
#def Ver_intro():
#    if os.path.exists(os.path.join(xbmc.translatePath("special://temp"), "today")):
#        ftoday = open(os.path.join(xbmc.translatePath("special://temp"), "today")).read()
#        today = str(date.today())
#    else:
#        ftoday = ''
#        today = str(date.today())
#    if ftoday != today:
#        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.m4v')
#        while xbmc.Player().isPlaying():
#            ftoday = open(os.path.join(xbmc.translatePath("special://temp"), "today"), 'w')
#            #today = str(date.today())
#            ftoday.write(today)
#            ftoday.close()
#            time.sleep(1)
#        return True
#
#def Menu_inicial():
#        #intro = Ver_intro()
#    try:
#        abrir_cookie(base_server + 'canais/liberar/')
#        addDir("Tv", "", 1, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
#        addDir("Filmes", "1", 1002, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#        addDir("Series", "", 5001, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
#        addDir("Programas de TV", "", 4001, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
#        xbmc.executebuiltin("Container.SetViewMode(51)")
#    except:
#        addDir("Apenas para usuários.", "", "-", "https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
#        addDir("Caso já tenha login/senha, insira na configuração do addon.", "", "-", "https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
#        while xbmc.Player().isPlaying():
#            time.sleep(1)
#        xbmc.executebuiltin("Container.SetViewMode(502)")
#
#
#
#def Menu_Inicial_Tv():
#    addDir("Streams Principais", "", 1, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
#    addDir("Streams do Brasil(Baixa e Media Qualidade)", "", 1000, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
#    #addDir("Opção 3","",2000,"http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
#    addDir("Streams Franceses", "", 3000, "http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
#    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
#    xbmc.executebuiltin("Container.SetViewMode(51)")
#
#def Menu_Inicial_Filmes():
#    addDir("1-FILMES ONSALEUK", "1", 201, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("2-FILMES WEB 1", "1", 7001, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("2-FILMES WEB 2", "1", 8820, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
#    xbmc.executebuiltin("Container.SetViewMode(51)")
#
#def Menu_icial_Melfilme():
#    #base_server = 'http://127.0.0.1:8000/canais/'
#    categorias = eval(abrir_cookie(base_server + 'canais/melfilme?action=0'))
#    for categoria in categorias:
#        addDir(unescape(categoria[0]).encode('utf8'), unescape(categoria[1]).encode('utf8') + '|1', 7002, '')
#
#def Categoria(url):
#    params = url.split('|')
#    print params
#    cat = params[0]
#    pg = params[1]
#    #base_server = 'http://127.0.0.1:8000/canais/'
#    filmes = eval(abrir_cookie(base_server + 'canais/melfilme?action=1&cat=%s&pg=%s' % (cat, pg)))
#    for filme in filmes:
#        addDir(unescape(filme[0]).encode('utf8'), filme[3], 7003, filme[2], pasta=True, total=len(filmes))
#    addDir('Proximos >>', cat + '|' + str(int(pg) + 1), 7002, '')
#    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
#    xbmc.executebuiltin("Container.SetViewMode(50)")
#
#def melfilme_play(url):
#    #base_server = 'http://127.0.0.1:8000/canais/'
#    filme = eval(abrir_cookie(base_server + 'canais/melfilme?action=2&id_=%s' % url))
#    # play_filme_vod(url,sub,server)
#    # addDir(name,url,mode,iconimage,total=0,pasta=True)
#    if filme['arquivo_dublado']:
#        addDir('Dublado', filme['arquivo_dublado'][0] + "|" + filme['legenda'][0], 7004, '', 2, False)
#    if filme['arquivo_legendado']:
#        addDir('Legendado', filme['arquivo_legendado'][0] + "|" + filme['legenda'][0], 7004, '', 2, False)
#
#
#def Menu_Inicial_Series():
#    addDir("Opção 1", "http://www.filmesonlinegratis.net/series", 8823, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Opção 2 [COLOR green][/COLOR][COLOR red][Em Desenvolvimento][/COLOR]", "1", 601, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
#    xbmc.executebuiltin("Container.SetViewMode(51)")
#
#def canais_master():
#    canais = getSoup('https://www.dropbox.com/s/ju2tycbdzwviviy/NovaLista.xml?dl=1')
#    for canal in canais('item'):
#        addLink(canal.title.text, canal.link.text, canal.thumbnail.text)
#    xbmc.executebuiltin("Container.SetViewMode(500)")
#
#
#def canais_playtvfr():
#    canais = eval(abrir_cookie(base_server + 'canais/playtvfr?action=1'))
#    for canal in canais:
#        addDir(canal[0].encode('utf-8', 'ignore'), canal[2], '3001', canal[1], len(canais), False)
#    xbmc.executebuiltin("Container.SetViewMode(500)")
#
#def play_playtvfr(url):
#    m3u8 = abrir_cookie(base_server + 'canais/playtvfr?action=2&ch=%s' % url)
#    xbmcPlayer = xbmc.Player()
#    xbmcPlayer.play(m3u8 + '|User-agent=')
#
#
#def canais_tvzune():
#    canais = eval(abrir_cookie(base_server + 'canais/tvzune?action=1'))
#    for canal in canais:
#        addDir(unescape(canal[0]), unescape(canal[1]), '2001', canal[2], len(canais), False)
#    xbmc.executebuiltin("Container.SetViewMode(500)")
#
#def play_tvzune(url):
#    m3u8 = abrir_cookie(base_server + 'canais/tvzune?action=2&ch=%s' % url)
#    xbmcPlayer = xbmc.Player()
#    xbmcPlayer.play(m3u8 + '|User-agent=')
#
#def menu_filmes():
#    addDir("Pesquisar...", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=mystery|1", 2, "https://www.ibm.com/developerworks/mydeveloperworks/blogs/e8206aad-10e2-4c49-b00c-fee572815374/resource/images/Search-icon.png")
#    addDir("+Populares", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Sci-Fi", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=sci-fi|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Acão", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=action|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Comédia", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=comedy|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Thriller", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=thriller|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Romance", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=romance|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Animação", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=animation|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Documentários", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=documentary|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Horror", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=horror|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Drama", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=drama|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Thriller", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=thriller|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#    addDir("Mistério", "sort=seeds&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=mystery|1", 2, "http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
#
#
#def listar_filmes(request):
#    import json
#    pagina = request.split('|')[1]
#    request = request.split('|')[0]
#    filmes = json.loads(abrir_cookie(base_server + 'filme/filmes?%s' % request))
#    # print filmes
#    for filme in filmes['MovieList']:
#        if not metadata:
#            meta_imdb = metagetpt.get_meta('movie', '', imdb_id=filme['imdb'])
#        total = len(filmes)
#        try:
#            if metadata:
#                addDirM(filme['title'], str({'torrents': filme['items'], 'imdb': filme['imdb'], 'poster': filme['poster_big']}), 6, filme['poster_big'], total, True)
#            else:
#                addDirM(filme['title'], str({'torrents': filme['items'], 'imdb': filme['imdb'], 'poster': filme['poster_big']}), 6, filme['poster_big'], total, True, meta_imdb)
#        except:
#            pass
#    addDir("Proximos >>", request.replace("page=%s" % pagina, "page=%s" % str(int(pagina) + 1)) + "|" + str(int(pagina) + 1), 2, "")
#    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
#    xbmc.executebuiltin('Container.SetViewMode(503)')
#
#def listar_torrents(url):
#    _dict = eval(url)
#    torrents = _dict['torrents']
#    for torrent in torrents:
#        url = torrent['torrent_url']
#        # print torrent
#        addDir('[COLOR green](S:%s)[/COLOR][COLOR red](L:%s)[/COLOR]-%s' % (torrent['torrent_seeds'], torrent['torrent_peers'], torrent['file'].encode('utf-8')), str({'torrent': url, 'imdb': _dict['imdb']}), 3, _dict['poster'], 1, False)
#    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
#    xbmc.executebuiltin("Container.SetViewMode(51)")
#
#def play_filme(url):
#    import thread
#    def set_sub(url):
#        import os.path
#        import glob
#        import zipfile
#        # os.chdir(xbmc.translatePath("special://temp"))
#        # for file_ in glob.glob("*.srt"):
#        #        os.remove(file_)
#        zip_file = os.path.join(xbmc.translatePath("special://temp"), 'sub2.zip')
#        urllib.urlretrieve(url, zip_file)
#        zfile = zipfile.ZipFile(zip_file)
#        print zfile.namelist()
#        #XBMC.Extract(zip_file, xbmc.translatePath("special://temp"))
#        #xbmc.executebuiltin("XBMC.Extract(%s, %s)" % (zip_file, xbmc.translatePath("special://temp")))
#        print "Sub: " + os.path.join(xbmc.translatePath("special://temp"), zfile.namelist()[0])
#        zfile.extract(zfile.namelist()[0], xbmc.translatePath("special://temp"))
#        while not xbmc.Player().isPlaying():
#            time.sleep(1)
#        xbmc.Player().setSubtitles(os.path.join(xbmc.translatePath("special://temp"), zfile.namelist()[0]))
#
#    import json
#    filme = eval(url)
#    print filme['torrent']
#    subs = json.loads(abrir_cookie(base_server + 'filme/subs/%s/' % filme['imdb']))
#    try:
#        sub_url = 'http://www.yifysubtitles.com' + subs['subs'][filme['imdb']]['brazilian-portuguese'][0]['url']
#    except:
#        sub_url = ''
#    # set_sub(sub_url)
#    thread.start_new_thread(set_sub, (sub_url,))
#    magnect = torrent2magnect(filme['torrent'])
#
#    #thread.start_new_thread(set_sub, (sub_url,))
#    xbmcPlayer = xbmc.Player()
#    #xbmcPlayer.play('plugin://plugin.video.pulsar/play?uri=' + magnect)
#    xbmcPlayer.play('plugin://plugin.video.xbmctorrent/play/' + magnect)
#
#
#def play_filme_vod(url, sub, server):
#    import thread
#    def set_sub(url):
#        import os.path
#        sub_file = os.path.join(xbmc.translatePath("special://temp"), 'sub.srt')
#        urllib.urlretrieve(url, sub_file)
#        while not xbmc.Player().isPlaying():
#            time.sleep(1)
#        xbmc.Player().setSubtitles(os.path.join(xbmc.translatePath("special://temp"), 'sub.srt'))
#    thread.start_new_thread(set_sub, (sub,))
#    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
#    xbmcPlayer.play(url)
#
#def play_mult_canal(arg, icon, nome):
#    try:
#        tuple_ = eval(arg)
#        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
#        playlist.clear()
#        for link in tuple_:
#            listitem = xbmcgui.ListItem(nome, thumbnailImage=iconimage)
#            listitem.setInfo('video', {'Title': nome})
#            playlist.add(url=link, listitem=listitem, index=7)
#        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
#
#    except:
#        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
#        playlist.clear()
#        listitem = xbmcgui.ListItem(nome, thumbnailImage=iconimage)
#        listitem.setInfo('video', {'Title': nome})
#        playlist.add(url=arg, listitem=listitem, index=7)
#        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
#
#def listar_categorias_filmes(url):
#    soup = getSoup(url)
#    categorias = soup('categoria')
#    import HTMLParser
#    pars = HTMLParser.HTMLParser()
#    pars.unescape('&copy; &euro;')
#    for categoria in categorias:
#        addDir(unescape(categoria.nome.text).encode('utf8'), base_server + 'vod/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text, 103, categoria.logo.text)
#    xbmc.executebuiltin("Container.SetViewMode(500)")
#
#def listar_filmes_vod(url):
#
#    soup = getSoup(url)
#    filmes = soup('filme')
#    total = len(filmes)
#
#    for filme in filmes:
#        # addDir(name,url,mode,iconimage,total=0,pasta=True)
#        addDir('%s [COLOR red]%s[/COLOR] [COLOR green]%s[/COLOR]' % (unescape(filme.nome.text).encode('utf8'), filme.vdr.text.encode('utf8'), filme.server.text.encode('utf8')), str((filme.link.text, filme.sub.text, filme.server.text)), 4, filme.thumbnail.text, total, False, filme.descricao.text, filme.fanart.text)
#    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#    xbmc.executebuiltin("Container.SetViewMode(515)")
#
#def listar_series_vod(url):
#
#    soup = getSoup(url)
#    series = soup('serie')
#    total = len(series)
#
#    for serie in series:
#            # addDirM(serie.titulo.text.encode('utf8'),serie.pk.text,604,serie.thumbnail.text,True,total,'',plot=serie.plot.text)
#        addDir(serie.titulo.text.encode('utf8'), serie.pk.text, 602, serie.thumbnail.text, total, True, serie.plot.text, serie.fanart.text)
#        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#        xbmc.executebuiltin('Container.SetViewMode(515)')
#
#def listar_series_temporadas_vod(url):
#    soup = getSoup(base_server + 'vod/xml_s/?action=temporadas&series_pk=' + url)
#    temporadas = soup('temporada')
#    total = len(temporadas)
#
#    for temporada in temporadas:
#        # addDirM(serie.titulo.text.encode('utf8'),serie.pk.text,604,serie.thumbnail.text,True,total,'',plot=serie.plot.text)
#        addDir('%s - Temporada %s' % (temporada.serie.text.encode('utf8'), temporada.numero.text.encode('utf8')), temporada.pk.text, 603, temporada.thumbnail.text, total, True)
#
#def listar_serie_episodios_vod(url):
#    soup = getSoup(base_server + 'vod/xml_s/?action=episodios&temporada_pk=' + url)
#    episodios = soup('episodio')
#    total = len(episodios)
#
#    for episodio in episodios:
#        #	play_filme_vod(params[0],params[1],server='')
#        # addDirM(serie.titulo.text.encode('utf8'),serie.pk.text,604,serie.thumbnail.text,True,total,'',plot=serie.plot.text)
#        addDir('%s - %s' % (episodio.numero.text.encode('utf8'), episodio.titulo.text.encode('utf8')), episodio.link.text + '|' + episodio.sub.text + '|', 7004, episodio.thumbnail.text, total, False, episodio.plot.text, episodio.fanart.text)
#        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#        xbmc.executebuiltin('Container.SetViewMode(515)')
#
#def listar_categorias(url):
#    soup = getSoup(url)
#    categorias = soup('categoria')
#    for categoria in categorias:
#        # print categoria.nome
#        if categoria.nome.text == 'XXX':
#            addDir(categoria.nome.text, base_server + 'canais/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text, 104, categoria.logo.text)
#        else:
#            addDir(categoria.nome.text, base_server + 'canais/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text, 102, categoria.logo.text)
#
#    xbmc.executebuiltin("Container.SetViewMode(500)")
#
#def listar_canais_xxx(url):
#    keyb = xbmc.Keyboard('', 'XXX')  # Chama o keyboard do XBMC com a frase indicada
#    keyb.doModal()  # Espera ate que seja confirmada uma determinada string
#    if (keyb.isConfirmed()):
#        if keyb.getText() == '0000':
#            epg = eval(abrir_cookie(base_server + 'canais/epg/'))
#
#            soup = getSoup(url)
#            canais = soup('canal')
#            print epg
#
#            for canal in canais:
#                try:
#                    canal_programa = epg[canal.epg.text]['programa']
#                except:
#                    canal_programa = ''
#                if canal_programa:
#                    addDir(canal.nome.text + ' - [COLOR green](%s)[/COLOR]' % canal_programa, canal.link.text, 105, canal.logo.text, 1, False)
#                else:
#                    addDir(canal.nome.text, canal.link.text, 105, canal.logo.text, 1, False)
#    xbmc.executebuiltin("Container.SetViewMode(500)")
#
## addDir(name,url,mode,iconimage,total=0,pasta=True)
#def listar_canais(url):
#
#    epg = eval(abrir_cookie(base_server + 'canais/epg/'))
#
#    soup = getSoup(url)
#    canais = soup('canal')
#    # print epg
#
#    for canal in canais:
#        # print canal
#        # addDir(canal.nome.text.encode('utf8'),canal.link.text.encode('utf8'),105,canal.logo.text.encode('utf8'),1,False)
#        try:
#            canal_programa = epg[canal.epg.text]['programa'].encode('utf8')
#        except:
#            canal_programa = ''
#        if canal_programa:
#            try:
#                addDir(canal.nome.text.decode('utf8') + '  [COLOR red](' + canal_programa + ')[/COLOR]', canal.link.text.decode('utf8'), 105, canal.logo.text.encode('utf8'), 1, False)
#            except:
#                addDir(canal.nome.text.encode('utf8'), canal.link.text.encode('utf8'), 105, canal.logo.text.encode('utf8'), 1, False)
#        else:
#            addDir(canal.nome.text.encode('utf8'), canal.link.text.encode('utf8'), 105, canal.logo.text.encode('utf8'), 1, False)
#
#    xbmc.executebuiltin("Container.SetViewMode(500)")
#
#
#def categorias_filmes2():
#    addDir('Ação', 'http://www.filmesonlinegratis.net/acao', 8821, '')
#    addDir('Animação', 'http://www.filmesonlinegratis.net/animacao', 8821, '')
#    addDir('Aventura', 'http://www.filmesonlinegratis.net/aventura', 8821, '')
#    addDir('Comedia', 'http://www.filmesonlinegratis.net/comedia', 8821, '')
#    addDir('Comedia Romantica', 'http://www.filmesonlinegratis.net/comedia-romantica', 8821, '')
#    addDir('Crime', 'http://www.filmesonlinegratis.net/crime', 8821, '')
#    addDir('Documentários', 'http://www.filmesonlinegratis.net/documentario', 8821, '')
#    addDir('Drama', 'http://www.filmesonlinegratis.net/drama', 8821, '')
#    addDir('Faroeste', 'http://www.filmesonlinegratis.net/faroeste', 8821, '')
#    addDir('Ficção', 'http://www.filmesonlinegratis.net/ficcao-cientifica', 8821, '')
#    addDir('Guerra', 'http://www.filmesonlinegratis.net/guerra', 8821, '')
#    addDir('Musical', 'http://www.filmesonlinegratis.net/musical', 8821, '')
#    addDir('Policial', 'http://www.filmesonlinegratis.net/policial', 8821, '')
#    addDir('Romance', 'http://www.filmesonlinegratis.net/romance', 8821, '')
#    addDir('Suspense', 'http://www.filmesonlinegratis.net/suspense', 8821, '')
#    # addDir('Series','http://www.filmesonlinegratis.net/series',8821,'')
#    addDir('Terror', 'http://www.filmesonlinegratis.net/terror', 8821, '')
#    addDir('Thriller', 'http://www.filmesonlinegratis.net/thriller', 8821, '')
#
#def listar_videos_series2(url):
#    codigo_fonte = abrir_url(url)
#    soup = BeautifulSoup(abrir_url(url))
#    try:
#        series = soup("ul", {"class": "videos series"})
#        tables = series[0]('table')
#        temp = []
#        for table in tables:
#            for td in table('td'):
#                temporada = html_replace_clean(td.b.text.encode('ascii', 'xmlcharrefreplace'))
#                for episodio in td('a', {"class": "bs-episodio"}):
#                    a = [temporada + html_replace_clean(episodio.text.encode('ascii', 'xmlcharrefreplace')), episodio['href'], 8822, '', 0, False]
#                    if a not in temp:
#                        temp.append(a)
#        for a in temp:
#            addDir(a[0], a[1], a[2], a[3], len(temp), False)
#    except:
#        pass
#
#    try:
#        series = soup("ul", {"class": "videos"})
#        li = series[0]('li', {"class": "video1-code"})[0]
#        temp = []
#        temporada = html_replace_clean(li.b.text.encode('ascii', 'xmlcharrefreplace'))
#        for episodio in li('a'):
#            a = [temporada + html_replace_clean(episodio.text.encode('ascii', 'xmlcharrefreplace')), episodio['href'], 8822, '', 0, False]
#            if a not in temp:
#                temp.append(a)
#        for a in temp:
#            addDir(a[0], a[1], a[2], a[3], len(temp), False)
#    except:
#        temp = []
#        temporada = "Temporada ?"
#        for b in soup('b'):
#            if "Temporada" in b.text:
#                temporada = html_replace_clean(b.text.encode('ascii', 'xmlcharrefreplace'))
#        for episodio in soup('a', {"class": "bs-episodio"}):
#            a = [temporada + html_replace_clean(episodio.text.encode('ascii', 'xmlcharrefreplace')), episodio['href'], 8822, '', 0, False]
#            if a not in temp:
#                temp.append(a)
#        for a in temp:
#            addDir(a[0], a[1], a[2], a[3], len(temp), False)
#
#def listar_series2(url):
#    codigo_fonte = abrir_url(url)
#    soup = BeautifulSoup(abrir_url(url))
#    lista_filmes = BeautifulSoup(soup.find("div", {"class": "miniaturas"}).prettify())
#    filmes = lista_filmes.findAll("article", {"class": "miniatura"})
#    a = []
#    for filme in filmes:
#        plot = ''
#        for div in filme('div'):
#            if 'Sinopse' in div.text:
#                plot = div('p')[len(div('p')) - 1].text.replace('Sinopse:', '')
#                break
#        if not plot:
#            plot = filme('span')[1].text
#        temp = [filme('div')[0].a["href"], html_replace_clean(filme('img')[0]["alt"].encode('ascii', 'xmlcharrefreplace')), filme('img')[0]["src"], html_replace_clean(plot.encode('ascii', 'xmlcharrefreplace'))] 
#        a.append(temp)
#    total = len(a)
#    for url2, titulo, img, plot in a:
#        titulo = titulo.replace('&#8211;', "-").replace('&#8217;', "'")
#        # addDir(name,url,mode,iconimage,total=0,pasta=True,plot='',fanart='')
#        addDir(titulo, url2, 8824, img, total, True, plot)
#
#    p_page = soup.find('a', {'class': 'page larger'})
#    if p_page:
#        addDir('Página Seguinte >>', p_page['href'], 8823, '')
#
#    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
#    xbmc.executebuiltin('Container.SetViewMode(503)')
#
#def listar_videos_filmes2(url):
#    codigo_fonte = abrir_url(url)
#    soup = BeautifulSoup(abrir_url(url))
#    lista_filmes = BeautifulSoup(soup.find("div", {"class": "miniaturas"}).prettify())
#    filmes = lista_filmes.findAll("article", {"class": "miniatura"})
#    a = []
#    for filme in filmes:
#        plot = ''
#        for div in filme('div'):
#            if 'Sinopse' in div.text:
#                plot = div('p')[len(div('p')) - 1].text.replace('Sinopse:', '')
#                break
#        if not plot:
#            plot = filme('span')[1].text
#        temp = [filme('div')[0].a["href"], html_replace_clean(filme('img')[0]["alt"].encode('ascii', 'xmlcharrefreplace')), filme('img')[0]["src"], html_replace_clean(plot.encode('ascii', 'xmlcharrefreplace'))] 
#        a.append(temp)
#    total = len(a)
#    for url2, titulo, img, plot in a:
#        titulo = titulo.replace('&#8211;', "-").replace('&#8217;', "'")
#        # addDir(name,url,mode,iconimage,total=0,pasta=True,plot='',fanart='')
#        addDir(titulo, url2, 8822, img, total, False, plot)
#
#    p_page = soup.find('a', {'class': 'page larger'})
#    if p_page:
#        addDir('Página Seguinte >>', p_page['href'], 8821, '')
#
#    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
#    xbmc.executebuiltin('Container.SetViewMode(503)')
#
#
#def player_filmes2(name, url, iconimage):
#    google = r'src="(.*?google.*?/preview)"'
#    picasa = r'src="(.*?filmesonlinebr.*?/player/.*?)"'
#    vk = r'src="(.*?vk.*?/video.*?)"'
#    nvideo = r'src="(.*?nowvideo.*?/embed.*?)"'
#    dropvideo = r'src="(.*?dropvideo.*?/embed.*?)"'
#    vodlocker = r'src="(.*?vodlocker.*?/embed.*?)"'
#    firedrive = r'src="(.*?firedrive.*?/embed/.*?)"'
#    firedrive2 = r'http://www.armagedomfilmes.biz/player/armage.php.id=(.*?)"'
#    dropmega = r'src=".*?drop.*?id=(.*?)"'
#    cloudzilla = r'cloudzilla.php.id=(.*?)"'
#    cloudzilla_f = r'http://www.cloudzilla.to/share/file/(.*?)"'
#    videott = r'value="(http://video.tt/e/.*?)" >'
#    videobis = r'<IFRAME SRC="(http://videobis.net/.*?)" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=.*? HEIGHT=.*?></IFRAME>'
#    videopw = r'<iframe src="(http://video.pw/e/.*?/)" scrolling="no" frameborder="0" width=".*?" height=".*?"></iframe>'
#    vidzi = r'(http://vidzi.tv/.*?.html)'
#    videomail = r'(http://videoapi.my.mail.ru/.*?.html)'
#    vidig_s = r'vd=(.*?)"'  # http://vidigvideo.com/embed-%s-885x660.html
#    vidig = r'(http://vidigvideo.com/.*?.html)'
#    dropvideo_s = r'dv=(.*?)"'
#    cludzilla_s = r'cz=(.*?)"'  # http://vidigvideo.com/embed-%s-885x660.html
#    mensagemprogresso = xbmcgui.DialogProgress()
#    mensagemprogresso.create('Onsaleuk', 'A resolver link', 'Por favor aguarde...')
#    mensagemprogresso.update(33)
#    links = []
#    hosts = []
#    matriz = []
#    codigo_fonte = abrir_url(url)
#    # try: url_video = re.findall(r'<iframe src="(.*?)" width="738" height="400" frameborder="0"></iframe></li>',codigo_fonte)[0]
#    # <iframe src="(.*?)" width="738" height="400" frameborder="0"></iframe></li>
#    # except: return
#    try:
#        links.append('http://www.cloudzilla.to/embed/%s' % re.findall(cludzilla_s, codigo_fonte)[0])  # http://www.cloudzilla.to/embed/%s
#        hosts.append('CloudZilla')
#    except:
#        pass
#
#
#    try:
#        links.append('http://dropvideo.com/embed/%s' % re.findall(dropvideo_s, codigo_fonte)[0])  # http://dropvideo.com/embed/%s
#        hosts.append('DropVideo')
#    except:
#        pass
#
#
#    try:
#        links.append('http://vidigvideo.com/embed-%s-885x660.html' % re.findall(vidig_s, codigo_fonte)[0])
#        hosts.append('Vidig')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(vidig, codigo_fonte)[0])
#        hosts.append('Vidig')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(videomail, codigo_fonte)[0])
#        hosts.append('Videomail')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(videopw, codigo_fonte)[0])
#        hosts.append('Video.Pw')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(vidzi, codigo_fonte)[0])
#        hosts.append('Vidzi')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(videobis, codigo_fonte)[0])
#        hosts.append('VideoBis')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(videott, codigo_fonte)[0])
#        hosts.append('Video.TT')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(picasa, codigo_fonte)[0])
#        hosts.append('Picasa')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(google, codigo_fonte)[0])
#        hosts.append('Gdrive')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(vk, codigo_fonte)[0])
#        hosts.append('Vk')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(nvideo, codigo_fonte)[0])
#        hosts.append('Nowvideo - Sem suporte')
#    except:
#        pass
#
#    try:
#        links.append(re.findall(dropvideo, codigo_fonte)[0])
#        hosts.append('Dropvideo')
#    except:
#        pass
#
#    try:
#        links.append('http://www.dropvideo.com/embed/' + re.findall(dropmega, codigo_fonte)[0])
#        hosts.append('Dropvideo')
#    except:
#        pass
#
#    try:
#        links.append('http://www.cloudzilla.to/embed/' + re.findall(cloudzilla, codigo_fonte)[0])
#        hosts.append('CloudZilla')
#    except:
#        pass
#
#    try:
#        links.append('http://www.cloudzilla.to/embed/' + re.findall(cloudzilla_t, codigo_fonte)[0])
#        hosts.append('CloudZilla(Legendado)')
#    except:
#        pass
#    try:
#        links.append(re.findall(vodlocker, codigo_fonte)[0])
#        hosts.append('Vodlocker')
#    except:
#        pass
#
#    # eseffair 14/03/2014
#    # Vou implementar posteriormente
#    try:
#        links.append('http://www.firedrive.com/embed/' + re.findall(firedrive2, codigo_fonte)[0])
#        hosts.append('Firedrive')
#    except:
#        pass
#
#
#    if not hosts:
#        return
#
#    index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)
#
#    if index == -1:
#        return
#
#    url_video = links[index]
#    mensagemprogresso.update(66)
#
#    if 'google' in url_video:
#        matriz = obtem_url_google(url_video)
#    elif 'dropvideo.com/embed' in url_video:
#        matriz = obtem_url_dropvideo(url_video)   # esta linha está a mais
#    elif 'filmesonlinebr.info/player' in url_video:
#        matriz = obtem_url_picasa(url_video)
#    elif 'vk.com/video_ext' in url_video:
#        matriz = obtem_url_vk(url_video)
#    elif 'vodlocker.com' in url_video:
#        matriz = obtem_url_vodlocker(url_video)
#    elif 'firedrive.com/embed' in url_video:
#        matriz = obtem_url_firedrive(url_video)
#    elif 'cloudzilla' in url_video:
#        matriz = obtem_cloudzilla(url_video)
#    elif 'http://video.tt' in url_video:
#        matriz = obtem_videott(url_video)
#    elif 'videobis.net' in url_video:
#        matriz = obtem_videobis(url_video)  # video.pw
#    elif 'video.pw' in url_video:
#        matriz = obtem_videopw(url_video)  # video.pw
#    elif 'vidzi.tv' in url_video:
#        matriz = obtem_vidig(url_video)
#    elif 'mail.ru' in url_video:
#        matriz = obtem_videomail(url_video)
#    elif 'vidigvideo.com' in url_video:
#        matriz = obtem_vidig2(url_video)
#    else:
#        print "Falha: " + str(url_video)
#
#    url = matriz[0]
#
#    if url == '-': return
#
#    mensagemprogresso.update(100)
#    mensagemprogresso.close()
#
#    listitem = xbmcgui.ListItem()  # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
#    listitem.setPath(url)
#    listitem.setProperty('mimetype', 'video/mp4')
#    listitem.setProperty('IsPlayable', 'true')
#    # try:
#    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
#    xbmcPlayer.play(url)
#
#def Listar_categorias_series(url=series_base):
#    print url
#    html = abrir_url(url)
#    #html = html.encode('ascii','xmlcharrefreplace')
#
#    soup = BeautifulSoup(html, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
#
#    a = []
#    links = soup("a", {"rel": "nofollow"})
#    #ow = open('G:\html_list\series.html', 'w')
#    # ow.write(str(links))
#    # ow.close()
#    # print links
#    # print menu
#    #resultados = content.findAll("td",  { "width" : "1%" })
#    for link in links:
#        if len(link.text) == 1:
#            # print link['href']
#            addDir('Séries com a letra: ' + html_replace_clean(link.text.encode('ascii', 'xmlcharrefreplace')).upper(), series_base + link['href'], 5003, 'http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png', len(links), True)
#    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
#    xbmc.executebuiltin('Container.SetViewMode(51)')
#
#def Listar_categorias(url=novelas_base):
#    print url
#    html = abrir_url2(url)
#    #html = html.encode('ascii','xmlcharrefreplace')
#    soup = BeautifulSoup(html, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
#
#    a = []
#    menu = soup("div", {"id": "Menu"})[1]
#    # print menu
#    links = menu("a")
#    #resultados = content.findAll("td",  { "width" : "1%" })
#    for link in links:
#        if not link['href'] == '#' and not html_replace_clean(link.text.encode('ascii', 'xmlcharrefreplace')) == 'Pagina Inicial':
#            # print link['href']
#            addDir(html_replace_clean(link.text.encode('ascii', 'xmlcharrefreplace')), link['href'], 4002, 'http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png', len(links), True)
#    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
#    xbmc.executebuiltin('Container.SetViewMode(51)')
#
#def Listar_episodios(url):
#    print url
#    html = abrir_url2(url)
#    #html = unicode(html, 'ascii', errors='ignore')
#    soup = BeautifulSoup(html)
#
#    a = []
#    categorias = soup("div", {"class": "CategoriasLista"})[0]
#    # print categorias
#    episodios = categorias("div", {"class": "Item"})
#    for episodio in episodios:
#        img = episodio.img['src']
#        titulo = html_replace_clean(episodio.img['alt'].encode('ascii', 'xmlcharrefreplace'))  # episodio.img['alt']
#        url = episodio.a['href']
#        # addDir(name,url,mode,iconimage,total=0,pasta=True)
#        addDir(titulo, url, 4003, img, len(episodios), False)
#    try:
#        links = soup("div", {"class": "Botaos"})[0]('a')
#        for link in links:
#            if not link['href'] == url:
#                url = link['href']
#        if len(episodios) == 11:
#            addDir("Proxima Pagina >>", url, 4002, '', len(episodios) + 1)
#        else:
#            addDir("<< Pagina Anterior", url, 4002, '', len(episodios) + 1)
#    except:
#        pass
#    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#    xbmc.executebuiltin('Container.SetViewMode(503)')
#
#def listar_series(url):
#    print url
#    html = abrir_url(url)
#    #html = unicode(html, 'ascii', errors='ignore')
#    soup = BeautifulSoup(html)
#
#    a = []
#    categorias = soup("div", {"id": "Conteudo"})[0]
#    # print str(categorias)
#
#    series = categorias("div", {"class": "amazingcarousel-image"})
#    for serie in series:
#        # print serie
#        img = serie.img['src']
#        titulo = html_replace_clean(serie.img['alt'].encode('ascii', 'xmlcharrefreplace'))  # episodio.img['alt']
#        url = serie.a['href']
#        # addDir(name,url,mode,iconimage,total=0,pasta=True)
#        addDir(titulo, url, 5004, img, len(series), True)
#        #xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#        # xbmc.executebuiltin('Container.SetViewMode(503)')
#
#def Listar_episodios_series(url):
#    # print url
#    html = abrir_url(url)
#    #html = unicode(html, 'ascii', errors='ignore')
#    soup = BeautifulSoup(html)
#
#    a = []
#    categorias = soup("div", {"id": "Conteudo"})[0]
#    # print str(categorias)
#
#    episodios = categorias("div", {"class": "Episodio"})
#
#    for episodio in episodios:
#        img = episodio.img['src']
#        titulo = html_replace_clean(episodio.img['alt'].encode('ascii', 'xmlcharrefreplace'))  # episodio.img['alt']
#        url = episodio.a['href']
#        # addDir(name,url,mode,iconimage,total=0,pasta=True)
#        addDir(titulo, url, 5005, img, len(episodios), False)
#    if len(episodios) == 0:
#        addDir('Esta temporada não tem episodios ainda...aguarde.', '', 0, '', 0, False)
#    links = soup("div", {"class": "Temporadas"})[0]('a')
#    ow = open('G:\html_list\series.html', 'w')
#    ow.write(str(url))
#    ow.close()
#    if len(links) > 1:
#        addDir('---------------------------', '', 0, '', 0, False)
#    for link in links:
#        if not link['href'] == '#':
#            addDir("Temporada: " + link.string, link['href'], 5004, '', len(episodios) + 1)
#
#    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#    xbmc.executebuiltin('Container.SetViewMode(503)')
#
#def Resolve_episodio_serie(url):
#        # print url
#    pg = 0
#    mensagemprogresso = xbmcgui.DialogProgress()
#    mensagemprogresso.create('Trabalhando', 'Gerando playlist', 'Por favor aguarde...')
#    pg += 10
#    mensagemprogresso.update(pg)
#    html = abrir_url(url)
#    soup = BeautifulSoup(html)
#    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
#    playlist.clear()
#    pg += 10
#    mensagemprogresso.update(pg)
#    br = mechanize.Browser()
#    cj = cookielib.LWPCookieJar()
#    br.set_cookiejar(cj)
#    br.set_handle_equiv(True)
#    br.set_handle_gzip(True)
#    br.set_handle_redirect(True)
#    br.set_handle_referer(True)
#    br.set_handle_robots(False)
#    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#    pg += 10
#    mensagemprogresso.update(pg)
#    br.open(series_base)
#    br.select_form(nr=0)
#    br.form['senha'] = base64.b64decode('MTIzNDU2')
#    br.form['email'] = base64.b64decode('YXJsZWlyYS5jYXN0cm9AZ21haWwuY29t')
#    br.submit()
#    pg += 10
#    mensagemprogresso.update(pg)
#    page = br.open(url).read()
#
#    links = re.findall('src: "(.*?)"', page)
#    pg += 10
#    mensagemprogresso.update(pg)
#    if links:
#        for link in links:
#            listitem = xbmcgui.ListItem('Epsodio', thumbnailImage='')
#            listitem.setInfo('video', {'Title': 'Episodio'})
#            playlist.add(url=link, listitem=listitem, index=7)
#        mensagemprogresso.update(100)
#        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
#    else:
#        mensagemprogresso.update(100)
#        dialog = xbmcgui.Dialog()
#        dialog.ok("Indisponivel", "Este ainda não esta disponivel, tente novamente em breve.")
#
#def Resolve_episodio(url):
#    # print url
#    pg = 0
#    mensagemprogresso = xbmcgui.DialogProgress()
#    mensagemprogresso.create('Trabalhando', 'Gerando playlist', 'Por favor aguarde...')
#    pg += 10
#    mensagemprogresso.update(pg)
#    html = abrir_url(url)
#    soup = BeautifulSoup(html)
#    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
#    playlist.clear()
#    pg += 10
#    mensagemprogresso.update(pg)
#    br = mechanize.Browser()
#    cj = cookielib.LWPCookieJar()
#    br.set_cookiejar(cj)
#    br.set_handle_equiv(True)
#    br.set_handle_gzip(True)
#    br.set_handle_redirect(True)
#    br.set_handle_referer(True)
#    br.set_handle_robots(False)
#    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#    pg += 10
#    mensagemprogresso.update(pg)
#    br.open('https://assistirnovelas.tv')
#    form = base64.b64decode('PGZvcm0gYWN0aW9uPSJodHRwczovL2Fzc2lzdGlybm92ZWxhcy50di9Mb2dpblVzdWFyaW8ucGhwIiBpZD0iZm9ybTEiIG1ldGhvZD0icG9zdCI+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT5FLW1haWw8L2xpPg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8bGk+PGlucHV0IHR5cGU9InRleHQiIHZhbHVlPSIiIG5hbWU9ImVtYWlsIiBjbGFzcz0iQ2FtcG9Mb2dpbiIgcGxhY2Vob2xkZXI9IlNldSBlLW1haWwiPjwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT5TZW5oYTwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT48aW5wdXQgdmFsdWU9IiIgbmFtZT0ic2VuaGEiIGNsYXNzPSJDYW1wb0xvZ2luIiBwbGFjZWhvbGRlcj0iU3VhIHNlbmhhIiB0eXBlPSJwYXNzd29yZCI+PC9saT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjxpbnB1dCB0eXBlPSJzdWJtaXQiIGNsYXNzPSJMb2dpbkluaWNpbyIgdmFsdWU9IkVudHJhciI+PC9saT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHBzOi8vYXNzaXN0aXJub3ZlbGFzLnR2L2NhZGFzdHJvLnBocCI+UmVnaXN0cmFyPC9hPjwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwczovL2Fzc2lzdGlybm92ZWxhcy50di9sZW1icmFyX3NlbmhhLnBocCI+TGVtYnJhciBzZW5oYTwvYT48L2xpPg0KICAgICAgICAgICAgICAgICAgPC9mb3JtPg==')
#    res = mechanize._form.ParseString(form, "https://assistirnovelas.tv")
#    br.form = res[1]
#    # br.select_form(nr=0)
#    br.form['senha'] = base64.b64decode('MTIzNDU2')
#    br.form['email'] = base64.b64decode('YXJsZWlyYS5jYXN0cm9AZ21haWwuY29t')
#    br.submit()
#    pg += 10
#    mensagemprogresso.update(pg)
#    page = br.open(url).read()
#    links = re.findall("file':.'(.*?mp4.*?)'", page)
#    pg += 10
#    mensagemprogresso.update(pg)
#    if links:
#        for link in links:
#            listitem = xbmcgui.ListItem('Epsodio', thumbnailImage='')
#            listitem.setInfo('video', {'Title': 'Episodio'})
#            playlist.add(url=link, listitem=listitem, index=7)
#        mensagemprogresso.update(100)
#        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
#    else:
#        mensagemprogresso.update(100)
#        dialog = xbmcgui.Dialog()
#        dialog.ok("Indisponivel", "Este ainda não esta disponivel, tente novamente em breve.")
#
#
################################################### PASTAS ################################################################
#
#def addLink(name, url, iconimage):
#    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
#    liz.setInfo(type="Video", infoLabels={"Title": name})
#    liz.setProperty('fanart_image', "%s/fanart.jpg" % selfAddon.getAddonInfo("path"))
#    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
#
#def addDir(name, url, mode, iconimage, total=0, pasta=True, plot='', fanart=''):
#    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
#    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
#    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
#    contextMenuItems = []
#    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
#    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
#    liz.setProperty('fanart_image', fanart)
#    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
#
#def addDirM(name, url, mode, iconimage, pasta=True, total=1, meta=metagetpt.get_meta('movie', '', ''), plot=''):
#    if plot and not meta['plot'] or meta['plot'] == 'N/A':
#        meta['plot'] = plot
#    if iconimage and not meta['cover_url']:
#        meta['cover_url'] = iconimage
#    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
#    ok = True
#    liz = xbmcgui.ListItem(name, iconImage='http://image.tmdb.org/t/p/original/' + os.path.split(meta['cover_url'])[1], thumbnailImage=iconimage)
#    liz.setInfo(type="Video", infoLabels=meta)
#    contextMenuItems = []
#    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
#    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
#    if not meta['backdrop_url'] == '':
#        liz.setProperty('fanart_image', 'http://image.tmdb.org/t/p/original/' + os.path.split(meta['backdrop_url'])[1])
#    else:
#        try:
#            liz.setProperty('fanart_image', fanart)
#        except:
#            liz.setProperty('fanart_image', '')
#    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
##        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
##	xbmc.executebuiltin('Container.SetViewMode(51)')
#    return ok
#
#
######################################################### OUTRAS FUNCOES ###############################################
#
#def get_params():
#    param = []
#    paramstring = sys.argv[2]
#    if len(paramstring) >= 2:
#        params = sys.argv[2]
#        cleanedparams = params.replace('?', '')
#        if (params[len(params) - 1] == '/'):
#            params = params[0:len(params) - 2]
#        pairsofparams = cleanedparams.split('&')
#        param = {}
#        for i in range(len(pairsofparams)):
#            splitparams = {}
#            splitparams = pairsofparams[i].split('=')
#            if (len(splitparams)) == 2:
#                param[splitparams[0]] = splitparams[1]                 
#    return param
#
#params = get_params()
#url = None
#name = None
#mode = None
#tamanhoparavariavel = None
#iconimage = None
#
#try: url = urllib.unquote_plus(params["url"])
#except: pass
#try: tamanhoparavariavel = urllib.unquote_plus(params["tamanhof"])
#except: pass
#try: iconimage = urllib.unquote_plus(params["iconimage"])
#except: pass
#try: name = urllib.unquote_plus(params["name"])
#except: pass
#try: mode = int(params["mode"])
#except: pass
#
## print "Mode: "+str(mode).decode('utf-8')
## print "URL: "+str(url).decode('utf-8')
## print "Name: "+str(name).decode('utf-8')
## print "Icon: "+str(iconimage).decode('utf-8')
## print "Name: "+str(tamanhoparavariavel).decode('utf-8')
#
#if mode == None:
#    Menu_inicial()
#elif mode == 1001:
#    Menu_Inicial_Tv()
#elif mode == 1002:
#    Menu_Inicial_Filmes()
#elif mode == 1:
#    listar_categorias(base_server + 'canais/xml?action=categorias')
#elif mode == 102:
#    listar_canais(url)
#elif mode == 103:
#    listar_filmes_vod(url)
#elif mode == 104:
#    listar_canais_xxx(url)
#elif mode == 105:
#    play_mult_canal(url, iconimage, name)
#elif mode == 200:
#    menu_filmes()
#elif mode == 201:
#    listar_categorias_filmes(base_server + 'vod/xml/?action=categorias')
#elif mode == 2:
#    listar_filmes(url)
#elif mode == 3:
#    play_filme(url)
#elif mode == 4:
#    params = eval(url)
#    play_filme_vod(params[0], params[1], params[2])
#elif mode == 6:
#    listar_torrents(url)
#elif mode == 1000:
#    canais_master()
#elif mode == 2000:
#    canais_tvzune()
#elif mode == 2001:
#    play_tvzune(url)
#elif mode == 3000:
#    canais_playtvfr()
#elif mode == 3001:
#    play_playtvfr(url)
#elif mode == 4001:
#    Listar_categorias()
#elif mode == 4002:
#    Listar_episodios(url)
#elif mode == 4003:
#    Resolve_episodio(url)
#elif mode == 5001:
#    Menu_Inicial_Series()
#elif mode == 5002:
#    Listar_categorias_series()
#elif mode == 5003:
#    listar_series(url)
#elif mode == 5004:
#    Listar_episodios_series(url)
#elif mode == 5005:
#    Resolve_episodio_serie(url)
#elif mode == 7001:
#    Menu_icial_Melfilme()
#elif mode == 7002:
#    Categoria(url)
#elif mode == 7003:
#    melfilme_play(url)
#elif mode == 7004:
#    params = url.split('|')
#    play_filme_vod(params[0], params[1], server='')
#elif mode == 601:
#    listar_series_vod(base_server + 'vod/xml_s/?action=series')
#elif mode == 602:
#    listar_series_temporadas_vod(url)
#elif mode == 603:
#    listar_serie_episodios_vod(url)
#elif mode == 8820:
#    categorias_filmes2()
#elif mode == 8821:
#    listar_videos_filmes2(url)
#elif mode == 8822:
#    play_filme(url)
#    #player_filmes2(name, url, iconimage)
#elif mode == 8823:
#    listar_series2(url)
#elif mode == 8824:
#    listar_videos_series2(url)
#
#
#xbmcplugin.endOfDirectory(int(sys.argv[1]))

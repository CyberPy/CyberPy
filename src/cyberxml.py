# coding=utf-8

from __future__ import division
from __future__ import unicode_literals
from builtins import str
from past.utils import old_div
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class XML(HyperText):
    def __init__(self):
        super(
			XML, 
			self
			).__init__()
        self.doctype = '''
		<?xml version="1.0" encoding="UTF-8"?>
		'''

class SiteMap(XML):
    change_frequency = 'weekly'
    def __init__(self):
        super(
			SiteMap, 
			self
			).__init__()

        self.index = '''
		<sitemapindex 
		xmlns="http://
		www.sitemaps.org/
		schemas/sitemap/
		0.9">%s</sitemapindex>'''

        self.sitemap = '''
		<sitemap>%s</sitemap>'''

        self.urlset = '''
		<urlset xmlns="
		http://www.
		sitemaps.org/
		schemas/sitemap/
		0.9">%s</urlset>'''

        self.url = '''
		<url>%s</url>'''

        self.loc = '''
		<loc>%s</loc>'''

        self.lastmod = '''
		<lastmod>%s</lastmod>'''

        self.priority = '''
		<priority>%s</priority>'''

        self.changefreq = '''
		<changefreq>%s
		</changefreq>'''

        self.mainMap = []
        self.timeStamp = TimeStamp()
        utc = self.timeStamp.load()
        self.lastmoddate = utc.split()[0]
    def add_url(
		self, 
		path, 
		name, 
		position):
        page = PyGod()
        page.url = Path.home_url(*path)
        page.name = name
        page.position = position
        self.mainMap.append(page)
    @classmethod
    def set_mode(cls):
        C.MODES.case('sitemap.xml', cls)
    @staticmethod
    def __name(page):
        index = page.position * -1
        page_list = page.url.split(
			'/')[index:-1]
        if not page_list:
            page_list.append('Home')
        title = [C.NAME, ' - ']
        title.extend(page_list)
        return ' '.join(
			reversed(title)
			).title()
    @classmethod
    def __page(cls, item):
        page = PyGod()
        page.url = item['PAGE']
        page.position = page.url.count('/') - 2
        page.name = cls.__name(page)
        return page
    def cms_import(self, item):
        return self.mainMap.append(
			self.__page(item))
    @staticmethod
    def same_origin(item):
        item['PAGE'] = decode_uri(item['PAGE'])
        return DOMAIN in item['PAGE']
    def cms(self):
        pages = Page().list_all()
        for item in pages:
            if self.same_origin(item):
                self.cms_import(item)
    def map(self):
        urls = Snippet()
        for page in self.mainMap:
            page.priority = str(
				old_div(1.00, float(
					page.position
					))
				)
            url = self.entry(page)
            urls.add(url)
        urlset = UI.tag(
			self.urlset, 
			urls.string()
			)
        return Snippet(
			self.doctype,
			urlset
			).string()
    def clean(self, url):
        url = url.replace(
			'&', 
			'&amp;')
        url = url.replace(
			"'", 
			'&apos;')
        url = url.replace(
			'"', 
			'&quot;')
        url = url.replace(
			'>', 
			'&gt;')
        url = url.replace(
			'<', 
			'&lt;')
        return url
    def entry(self, page):
        url = self.clean(
			page.url)
        loc = UI.tag(
			self.loc, 
			url)
        lastmod = UI.tag(
			self.lastmod, 
			self.lastmoddate)
        changefreq = UI.tag(
			self.changefreq, 
			self.change_frequency
			)
        priority = UI.tag(
			self.priority, 
			page.priority
			)
        return UI.tag(
			self.url, 
			Snippet(
				loc,
				lastmod,
				changefreq,
				priority
				).string()
			)
    def load(self):
        file = ContentFactory()
        file.content = self.map()
        file.contenttype(
			'text', 
			'xml'
			)
        file.min_HTML()
        file.gzip()
        return file

class RSS(XML):
    def __init__(self):
        super(
			RSS, 
			self
			).__init__()
        self.namespace = '''
		<rss version="2.0" 
		xmlns:content="
		http://purl.org/
		rss/1.0/FILEs/
		content/" xmlns:
		wfw="http://
		wellformedweb.org/
		CommentAPI/" 
		xmlns:dc="http://
		purl.org/dc/elements/
		1.1/" xmlns:atom="
		http://www.w3.org/
		2005/Atom" xmlns:
		sy="http://purl.org/
		rss/1.0/FILEs/
		syndication/" xmlns:
		slash="http://
		purl.org/rss/1.0/
		FILEs/slash/">
		%s</rss>'''

        self.channel = '''
		<channel>%s</channel>'''
        self.title = '''
		<title>%s</title>'''

        self.atomlink = '''
		<atom:link 
		href="https://
		clinicdrbita.com/
		feed/" rel="self" 
		type="application/
		rss+xml"/>'''

        self.link = '''
		<link>%s</link>'''
        self.descr = '''
		<descr>%s
		</descr>'''

        self.last_build_date = '''
		<lastuildDate>%s
		</lastBuildDate>'''

        self.lang = '''
		<language>%s
		</language>'''

        self.updateperiod = '''
		<sy:updatePeriod>%s
		</sy:updatePeriod>'''

        self.updatefrequency = '''
		<sy:updateFrequency>%s
		</sy:updateFrequency>'''

        self.generator = '''
		<generator>%s
		</generator>'''

        self.item = '''
		<item>%s</item>'''

        self.pubdate = '''
		<pubDate>%s
		</pubDate>'''

        self.creator = '''
		<dc:creator>%s
		</dc:creator>'''

        self.guid = '''
		<guid isPermaLink="
		false">%s</guid>'''

        self.category = '''
		<category>%s
		</category>'''

        self.descr = '''
		<descr>%s
		</descr>'''

        self.content = '''
		<content:encoded>%s
		</content:encoded>'''
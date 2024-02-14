# coding=utf-8

from __future__ import unicode_literals
from builtins import str
from builtins import range
from sys import modules

C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class Schema(Snippet):
    skip = None
    def __init__(self):
        super(
			Schema,
			self
			).__init__()
        self.scope = '''
	    itemscope
		itemtype="%s"'''

        self.prop = '''
	    itemprop="%s"'''
    def __json(self, object):
        return C.UI.create_element(
			'script',
			object,
			type='''
			application/
			ld+json''')
    def __article_meta(self):
        return C.UI.create_element(
			'meta',
			**{
				' itemscope itemprop="%s"':
				'mainEntityOfPage',
				'  itemType="%s"':
				'https://schema.org/WebPage',
				' itemid="%s"': self.path.__add__(
					self.article_dict['TITLE']
					).replace(' ', '-')
				})
    def __article_h2(self):
        return C.UI.create_element(
			'h2',
			self.article_dict['TITLE'],
			**{
				' itemprop="%s"':
				'headline'
				}
			)
    def __author(self):
        author_isset = 'AUTHOR' in self.article_dict
        condition = IfElse(
			lambda: self.article_dict['AUTHOR'],
			lambda: NAME
			)
        return C.UI.create_element(
			'span',
			condition.value(
				author_isset
				),
			**{' itemprop="%s"': 'name'}
			)
    def __article_h3(self):
        return C.UI.create_element(
			'h3',
			self.__author(),
			**{
				' itemprop="%s"':
				'author',
				' itemscope itemtype="%s"':
				'https://schema.org/Organization'
				}
			)
    def __descr(self):
        return C.UI.create_element(
			'span',
			self.article_dict['DESCRIPTION'],
			**{
				' item="%s"':
				'description'
				}
			)
    def __thumbnail(self):
        return C.UI.rel_imagelink(
			self.article_dict['IMGURL'],
			'article thumbnail',
			self.path,
			self.article_dict[
				'TITLE'
				].replace(' ', '-')
			)
    def __thumbnail_meta(self):
        return C.UI.create_element(
			'meta',
			**{
				' itemprop="%s"':
				'url',
				' content="%s"':
				self.article_dict['IMGURL']
				}
			)
    def __image_width(self):
        return C.UI.create_element(
			'meta',
			**{
				' itemprop="%s"':
				'width',
				' content="%s"':
				self.article_dict['WIDTH']
				}
			)
    def __image_height(self):
        return C.UI.create_element(
			'meta',
			**{
				' itemprop="%s"':
				'height',
				' content="%s"':
				self.article_dict['HEIGHT']
				}
			)
    def __image_object(self):
        return C.UI.addprop(
			C.UI.box(
				'articlethumbnail',
				Snippet(
					self.__thumbnail(),
					self.__thumbnail_meta(),
					self.__image_width(),
					self.__image_height()
					).string()
				),
			''' itemprop=
			"image"
			itemscope itemtype="
			https://
			schema.org/
			ImageObject"''')
    def __article_utc(self):
        return C.UI.create_element(
			'meta',
			**{
				' itemprop="%s"':
				'datePublished',
				' content="%s+00:00"':
				self.article_dict['UTC'].replace(
					' ',
					'T')
				}
			)
    def __publisher(self):
        img_path = Path.home_url('image', 'logo.png')
        return Snippet(
			'''<div style="width:150px;
			display:inline-block;"
			itemprop="publisher"
			itemscope itemtype="
			https://schema.org/Organization">''',
			'''<div id="authorimg" itemprop="logo"
			itemscope itemtype="
			https://schema.org/ImageObject">''',
			UI.image(
				img_path,
				'Clinic Dr. Bita Logo'),
			UI.tag(
				'<meta itemprop="url" content="%s">',
				img_path),
			UI.tag(
				'<meta itemprop="width" content="%s">',
				DATA.address('logo')['width']),
			UI.tag(
				'<meta itemprop="height" content="%s">',
				DATA.address('logo')['height']),
			'</div>',
			UI.tag(
				'<meta itemprop="name" content="%s">',
				NAME),
			'</div>'
			).string()
    def __article_box(self):
        return C.UI.box(
			'articlebox',
			Snippet(
				self.__article_meta(),
				self.__article_h2(),
				self.__publisher(),
				self.__article_h3(),
				C.UI.br,
				self.__descr(),
				self.__image_object(),
				self.__article_utc()
				).string()
			)
    def article(
		self,
		path,
		article):
        self.article_dict = article
        self.path = path
        return C.UI.addprop(
			self.__article_box(),
			''' itemscope itemtype=
			"http://schema.org/
			NewsArticle"'''
			)
    def search(self):
        return self.__json(
			Snippet(
				'''{"@context":
				"http://schema.org",
				"@type":
				"WebSite",''',
				C.UI.tag(
					'"url": "%s",',
					C.DOMAIN),
				'''"potentialAction":
				{"@type":
				"SearchAction",
				"target": "''',
				Path.home_url(
					'api',
					'search',
					'{search_term_string}'),
				'''","query-input":
				"required name=
				search_term_string"}}'''
				).string())
    def __add_altname(self):
        return C.UI.tag(
			'''"alternateName":
			"%s",''',
			C.ALTNAME)
    def site_name(self):
        has_altname = C.ALTNAME != None
        condition = IfElse(
		    self.__add_altname,
			lambda: '')
        return self.__json(
			Snippet(
				'''{"@context":
				"http://schema.org",
				"@type":
				"WebSite",''',
				C.UI.tag(
					'"name": "%s",',
					C.NAME),
				condition.value(has_altname),
				C.UI.tag(
					'''"url":
					"%s"}''',
					C.DOMAIN)
				).string())
    def __logo(self):
        split_logo = LOGO_URL.split('/')
        split_logo.pop(0)
        logo_url = Path.home_url(
			*split_logo)
        self.js_obj.insert(
			'"logo": "%s",',
			logo_url)
    def __add_type(self):
        self.js_obj.insert(
			'''"additionalType":
		    "%s",''',
			Snippet(
				'''http://www.
				productontology
				.org/id/''',
				C.DATA.address(
					'WIKITYPE'
					)
				).string()
			)
    def __image(self):
        self.js_obj.insert(
			'"image": "%s",',
			Path.home_url(
				C.DATA.address(
					'image')))
    def __hasmap(self):
        maplist = Snippet('"hasMap": [')
        for gmap in DATA.options['hasMap']:
            map_item = Snippet(
				'''{"@type":
				"Map",''')
            map_item.insert(
				'"mapType": "%s",',
				gmap['mapType'])
            map_item.insert(
				'"url": "%s"',
				gmap['hasMap'])
            map_item.add('},')
            maplist.add(map_item.element)
        maplist.add('],')
        self.js_obj.add(maplist.element)
    def __addresses(self):
        a_list = Snippet()
        for address in C.DATA.options['addresses']:
            addr = Snippet(
				'''"@type":
				"PostalAddress",''')
            addr.insert(
				'"addressLocality": "%s",',
				address['city'])
            addr.insert(
				'"addressRegion": "%s",',
				address['region'])
            addr.insert(
				'"streetAddress": "%s",',
				address['streetAddress'])
            addr.insert(
				'"postalCode": "%s",',
				address['postalCode'])
            addr.insert(
				'"addressCountry": "%s",',
				DEF_COUNTRY)
            addr.insert(
				'"telephone": "%s",',
				address['telephone'])
            a_list.insert('{%s},', addr.element)
        self.js_obj.insert(
			'"address": [%s],',
			a_list.element)
    def __opening_hours(self):
        self.js_obj.insert(
			'"openingHours": "%s",',
			DATA.address(
				'openingHours'))
    def __contact_point(self):
        c_dict = DATA.address('contactPoint')
        cont = Snippet('"@type": "ContactPoint",')
        cont.insert(
			'"telephone": "%s",',
			c_dict.address('telephone'))
        cont.insert(
			'"contactType": "%s"',
			c_dict.address('contactType'))
        self.js_obj.insert(
			'"contactPoint": {%s},',
			cont.element)
    def __same_as(self):
        same = Snippet('"sameAs": [')
        last_item = DATA.options[
			'sameAs'][
			len(
				DATA.options[
					'sameAs'])
			-1]
        for item in DATA.options['sameAs']:
            same.insert(
				'"%s"',
				item)
            same.add(Delimiter.comma(
				item,
				last_item))
        same.add('],')
        self.js_obj.add(same.element)
    def __price_range(self):
        self.js_obj.add(
			Snippet(
				'"priceRange": "',
				DATA.address(
					'priceRange'),
				'",'
				).string())
    def __extras(self):
        extras = DATA.address('extras')
        if type(extras) is not str:
            extras = json.dumps(extras)
        self.js_obj.add(extras)
    def __data(self):
        self.schema_data = Switch()
        self.schema_data.case(
			'image',
			self.__image)
        self.schema_data.case(
			'addresses',
			self.__addresses)
        self.schema_data.case(
			'openingHours',
			self.__opening_hours)
        self.schema_data.case(
			'contactPoint',
			self.__contact_point)
        self.schema_data.case(
			'sameAs',
			self.__same_as)
        self.schema_data.case(
			'priceRange',
			self.__price_range)
        self.schema_data.case(
			'hasMap',
			self.__hasmap)
        self.schema_data.case(
			'extras',
			self.__extras)
    def __add_data(self):
        self.__data()
        add = self.schema_data.action
        for key in DATA.options:
            if self.schema_data.has(key):
                add(key)
    def __fixorg(self, char):
        self.__fix(
			self.js_obj,
			char
			)
    def __orgcontext(self):
        try:
            self.js_obj = Snippet(
				self.context,
				C.UI.tag(
					'"@type": "%s",',
					DATA.address(
						'type'
						)
					),
				)
        except Exception:
            Errors.log()
    def __orgdata(self):
        if DATA.has('WIKITYPE'):
            self.__add_type()
        self.js_obj.insert(
			'"name": "%s",',
			NAME)
        self.js_obj.insert(
			'"url": "%s",',
			C.DOMAIN)
        self.js_obj.insert(
			'"description": "%s",',
			DATA.address(
				'DESCR')
			)
    def organization(self):
        self.__orgcontext()
        self.__orgdata()
        self.__add_data()
        has_logo = LOGO_URL != None
        is_business = DATA.address(
			'type'
			) == 'LocalBusiness'
        valid_logo = has_logo and is_business
        if valid_logo:
            self.__logo()
        self.js_obj.add('}')
        self.__fixorg('}')
        self.__fixorg(']')
        return self.js_obj.string()
    def __state(self):
        self.js_objs.join(
			'''"areaServed":
			{"@type": "state"
			,"name": ''',
			DATA.address(
				'state'),
			'},')
    def __city(self):
        self.js_objs.join(
			'''"areaServed":
			{"@type": "city"
			,"name": ''',
			DATA.address(
				'city'),
			'},')
    def __catalogs(self):
        catalogs = DATA.address('catalogs')
        if type(catalogs) is not str:
            catalogs = json.dumps(catalogs)
        self.js_objs.add(catalogs)
    def __service_data(self):
        self.schema_data = Switch()
        self.schema_data.case(
			'state',
			self.__state)
        self.schema_data.case(
			'city',
			self.__city)
        self.schema_data.case(
			'catalogs',
			self.__catalogs)
    def __add_service_data(self):
        self.__service_data()
        add = self.schema_data.action
        for key in DATA.options:
            if self.schema_data.has(key):
                add(key)
    def __embed_org(self):
        return C.UI.tag(
			'"provider": {%s,',
			self.organization().replace(
				self.context,
				''))
    def __service_context(self):
        self.js_objs = Snippet()
        self.js_objs.join(
			self.context,
			'''"@type":
			"Service",
			"serviceType": "''',
			DATA.address(
			    'serviceType'
			    ),
			'",',
			self.__embed_org()
			)
    def __fix(self, obj, char):
        obj.setval(
			obj.element.replace(
				''.join(
					[
						',',
						char
						]
					),
				char
				)
			)
    def __fixservice(self, char):
        self.__fix(
			self.js_objs,
			char
			)
    def service(self):
        self.__service_context()
        self.__add_service_data()
        self.js_objs.add('}')
        self.__fixservice('}')
        self.__fixservice(']')
        return self.js_objs.string()
    def entity(self):
        try:
            self.context = '''
	    	{"@context":
		    "http://schema.org/",
		    '''
            is_service = DATA.has(
	    	    'serviceType'
		        )
            condition = IfElse(
			    self.service,
			    self.organization
			    )
            return self.__json(
			    condition.value(
				    is_service
				    )
			    )
        except Exception:
            Errors.log()
    def __bc_template(self):
        return C.UI.create_element(
			'ol', '%s',
			scope='''
			http://schema.org/
			BreadcrumbList''')
    def __item_template(self):
        self.iTemplate = C.UI.create_element(
			'li', '%s',
			itemprop='itemListElement',
			scope='''http://
			schema.org/
			ListItem''')
    def __data_template(self):
        self.iData = C.UI.create_element(
			'meta',
			s=Snippet(
				C.UI.tag(
					self.prop,
					'item'),
				C.UI.tag(
					self.prop,
					'name'),
				C.UI.tag(
					self.prop,
					'position'),
				' %s'
				).string())
    def __createitem(self, item):
        return C.UI.addprop(
	    	self.iTemplate,
		    C.UI.tag(
			    C.UI.clss,
				Snippet(
					'itemposition ',
					item['position']
					).string()))
    def __position(self, item):
        return C.UI.tag(
			self.iData,
			C.UI.tag(
				' position="%s"',
				item['position']))
    def __name(self, item):
        return C.UI.create_element(
	    	'span',
		    item['name'].title(
				).replace(
					'-',
					' '),
			**{
				' itemprop="%s"':
				'name'})
    def __link(self, item):
        return C.UI.create_element(
	    	'a',
		    self.__name(item),
			**{
				'href':
				item['url'],
				' itemprop="%s"':
				'item'})
    def __item_link(self, item):
        link = self.__link(item)
        pos = self.__position(item)
        return C.UI.tag(
	    	self.__createitem(item),
		    Snippet(
			    link,
				pos
				).string()
			)
    def __additem(self, item):
        self.append(
			self.__item_link(
				item))
    def __add_dash(self):
        self.append(
			C.UI.create_element(
				'li',
				'/',
				clss='crumbdash'))
    def __add_items(self):
        last = len(self) - 1
        for item in self.url_list:
            self.__additem(item)
            self.__add_dash()
        self.pop(last)
        self.join()
    def __create_breadcrumb(self):
        return C.UI.tag(
	    	self.__bc_template(),
		    self.string())
    def __set_pathlist(self):
        self.pathlist = C.INFO.tolist('web')
        has_home = lambda: '' in self.pathlist
        while has_home():
            index = self.pathlist.index('')
            self.pathlist.pop(index)
            if not has_home():
                break
        if self.skip:
            self.pathlist.append(
				''.join(['#', self.skip]))
    def __get_urls(self):
        self.__set_pathlist()
        self.__populate_urls()
    def __populate_urls(self):
        path_end = len(self.pathlist)
        for path_index in range(path_end):
            name = self.pathlist[path_index]
            item = {'name': name.replace('#', '')}
            intposition = path_index + 2
            item['position'] = str(intposition)
            if '#' in name:
                item['url'] = name
            else:
                item['url'] = self.__generate_url(
					path_index)
            self.url_list.append(item)
    def __generate_url(self, lastIndex):
        item_url = Snippet(C.DOMAIN)
        lang = lambda: C.INFO.address('LANG')
        not_def = lang() != DEF_LANG
        if not_def:
            item_url.join(
				lang(),
				'/')
        for index in range(lastIndex + 1):
            item_url.join(
			    self.pathlist[index],
				'/')
        return item_url.string()
    def __default_urls(self):
        self.pathlist = []
        lang = lambda: C.INFO.address('LANG')
        url = IfElse(
			lambda: C.DOMAIN,
			lambda: C.DOMAIN.__add__(lang())
			)
        is_def = lang() == DEF_LANG
        self.url_list = [
			{'url': url.value(is_def),
			'name': lang().title(),
			'position': '1'}]
    def breadcrumb(self):
        self.__item_template()
        self.__data_template()
        self.__default_urls()
        self.__get_urls()
        self.__add_items()
        return self.__create_breadcrumb()
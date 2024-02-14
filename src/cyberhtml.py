# coding=utf-8

from __future__ import unicode_literals
from builtins import range
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class HTML(HyperText):
    doctype = '<!DOCTYPE html>'
    html = '<html>%s</html>'
    lang = ' lang="%s"'
    scope = ' scope="%s"'
    itemprop = ' itemprop="%s"'
    head = '<head>%s</head>'
    charset = ' charset="%s"'
    prefix = ' prefix="%s"'
    body = '<body>%s</body>'
    method = ' method="%s"'
    script = '<script>%s</script>'
    async = ' async'
    defer = ' defer'
    strong = '<strong>%s</strong>'
    css = '<style>%s</style>'
    iframe = '<iframe>%s</iframe>'
    meta = '<meta>'
    rows = ' rows="%s"'
    cols = ' cols="%s"'
    textarea = '<textarea>%s</textarea>'
    input = '<input>'
    content = ' content="%s"'
    value = ' value="%s"'
    target = ' target="%s"'
    name = ' name="%s"'
    br = '<br>'
    hr = '<hr>'
    button = '<button>%s</button>'
    div = '<div>%s</div>'
    p = '<p>%s</p>'
    ol = '<ol>%s</ol>'
    ul = '<ul>%s</ul>'
    li = '<li>%s</li>'
    a = '<a>%s</a>'
    b = '<b>%s</b>'
    h1 = '<h1>%s</h1>'
    h2 = '<h2>%s</h2>'
    h3 = '<h3>%s</h3>'
    h4 = '<h4>%s</h4>'
    h5 = '<h5>%s</h5>'
    h6 = '<h6>%s</h6>'
    ins = '<ins>%s</ins>'
    deleted = '<del>%s</del>'
    style = ' style="%s"'
    action = ' action="%s"'
    src = ' src="%s"'
    clss = ' class="%s"'
    id = ' id="%s"'
    i = '<i>%s</i>'
    em = '<em>%s</em>'
    form = '<form>%s</form>'
    title = '<title>%s</title>'
    property = ' property="%s"'
    link = '<link>'
    rel = ' rel="%s"'
    type = ' type="%s"'
    href = ' href="%s"'
    img = '<img>'
    audio = '<audio>%s</audio>'
    video = '<video>%s</video>'
    table = '<table>%s</table>'
    th = '<th>%s</th>'
    tr = '<tr>%s</tr>'
    td = '<td>%s</td>'
    span = '<span>%s</span>'
    onclick = ' onclick="%s"'
    onchange = ' onchange="%s"'
    onload = ' onload="%s"'
    onkeydown = ' onkeydown="%s"'
    onmouseover = ' onmouseover="%s"'
    onmouseout = ' onmouseout="%s"'
    alt = ' alt="%s"'
    code = '<code>%s</code>'
    canvas = '''<canvas>Canvas Not
	Supported by Browser.</canvas>'''
    article = '<article>%s</article>'
    aside = '<aside>%s</aside>'
    time = '<time>%s</time>'
    footer = '<footer>%s</footer>'
    details = '<details>%s</details>'
    fig = '<figure>%s</figure>'
    figcaption = '<figcaption>%s</figcaption>'
    header = '<header>%s</header>'
    main = '<main>%s</main>'
    nav = '<nav>%s</nav>'
    section = '<section>%s</section>'
    summary = '<summary>%s</summary>'
    width = ' width="%s"'
    height = ' height="%s"'
    sizes = ' sizes="%s"'
    frameborder = ' frameborder="%s"'
    source = '<source>'
    option = '<option>%s</option>'
    select = '<select>%s</select>'
    s = '%s'

class Href_Lang(HTML):
	urls = {}
	def __init__(self):
		super(Href_Lang, self).__init__()
		self.tags = C.Doc()
	def __add_tag(self, __lang__):
		self.tags.create_element(
			'link',
			rel='alternate',
			clss='langurl',
			href=self.urls[__lang__],
			lang=__lang__ )
	def __add_tags(self):
		for lang in self.urls:
			try:
				self.__add_tag(lang)
			except:
				pass
	def get(self):
		if self.urls:
			self.__add_tags()
			self.tags.merge()
		self.urls.clear()
		return self.tags.element

class Head(HTML):
    data = Snippet()
    markup = Schema()
    img = ''
    @staticmethod
    def reset():
        C.Module.glob(
			'ROBOTS',
			None)
        C.Module.glob(
			'TITLE',
			None)
        C.Module.glob(
			'DESCR',
			None)
    @classmethod
    def metalink(
		cls,
		relVal,
		hrefVal,
		**kwargs):
        props = {
			'rel': relVal,
			'href': hrefVal}
        if kwargs:
            props.update(kwargs)
        return cls.create_element(
			'link',
			**props)
    @classmethod
    def shortlink(cls):
        url = Snippet(C.LIVE_URL)
        if C.INFO.address('embed') == 'true':
            url.add('?embed=true')
        return cls.metalink(
			'shortlink',
			url.string())
    @classmethod
    def canonical(cls):
        url = Snippet(C.LIVE_URL)
        if C.INFO.address('embed') == 'true':
            url.add('?embed=true')
        return cls.metalink(
			'canonical',
			url.string())
    @classmethod
    def shortcut_icon(cls):
        return cls.metalink(
			'shortcut icon',
			'/image/favicon.png')
    @classmethod
    def phoneicon(cls):
        return cls.metalink(
			'apple-touch-icon',
			'/image/iphonefavicon.png',
			type='image/png')
    @classmethod
    def tableticon(cls):
        return cls.metalink(
			'apple-touch-icon',
			'/image/ipadfavicon.png',
			type='image/png',
			sizes='72x72')
    @classmethod
    def metacontent(
		cls,
		content,
		**kwargs):
        props = {'content': content}
        if kwargs:
            props.update(kwargs)
        return cls.create_element(
			'meta',
			**props)
    @classmethod
    def meta_template(
		cls,
		name,
		content,
		**kwargs):
        try:
            props = {
				'name':
				name
				}
            if kwargs:
                props.update(kwargs)
            return cls.metacontent(
			    content,
			    **props
				)
        except Exception:
            Errors.log()
    @classmethod
    def og_meta(
		cls,
		property,
		content,
		**kwargs):
        props = {
			'property':
			property
			}
        if kwargs:
            props.update(kwargs)
        return cls.metacontent(
			content,
			**props
			)
    @classmethod
    def og_locale(cls):
        return cls.og_meta(
			'og:locale',
			C.LANG.options['og'])
    @classmethod
    def og_type(cls):
        return cls.og_meta(
			'og:type',
			C.OGTYPE)
    @classmethod
    def __append_title(cls, key):
        if C.DATA.has(key):
            cls.__setlast(
				C.DATA.address(
					key
					)
				)
    @classmethod
    def __get_words(cls):
        words = []
        key = 'web'
        while C.INFO.has(key):
            key = C.INFO.address(
				key
				)
            words.append(
				Snippet(
					key.title(),
					' '
					).string()
				)
            if not C.INFO.has(key):
                break
        words.reverse()
        return words
    @classmethod
    def __setlast(cls, val):
        cls.words[
			cls.lastindex
			] = val
    @classmethod
    def __appendlast(cls, last):
        if cls.words[
			cls.lastindex
			] == '':
            cls.__append_title(
				last
				)
    @classmethod
    def __set_title(cls):
        C.TITLE = Snippet(
			*cls.words
			).string()
    @classmethod
    def __add_func(cls):
        condition = IfElse(
			lambda val: cls.words.insert(0, val),
			lambda val: cls.words.append(val)
			)
        return condition.address(
			C.KNOWN_BRAND
			)
    @classmethod
    def __create_title(cls):
        try:
            cls.words = cls.__get_words()
            cls.lastindex = len(
			    cls.words
			    ) - 1
            cls.__appendlast(
			    'serviceType'
			    )
            cls.__appendlast(
			    'WIKITYPE'
			    )
            add = cls.__add_func()
            if cls.words[
			    cls.lastindex
			    ] != '':
                add(' - ')
            add(C.NAME)
            cls.__set_title()
        except Exception:
            Errors.log()
    @classmethod
    def og_title(cls):
        if C.TITLE == None:
            cls.__create_title()
        return cls.og_meta(
			'og:title',
			C.TITLE
			)
    @classmethod
    def og_descr(cls, DESCR):
        return cls.og_meta(
			'og:description',
			DESCR)
    @classmethod
    def og_url(cls):
        return cls.og_meta(
			'og:url',
			C.LIVE_URL)
    @classmethod
    def og_site_name(cls):
        return cls.og_meta(
			'og:site_name',
			C.NAME)
    @classmethod
    def og_image(cls):
        return cls.og_meta(
			'og:image',
			cls.img)
    @classmethod
    def contenttype(cls):
        return Snippet(
			cls.create_element(
				'meta',
				charset='UTF-8'
				),
			cls.create_element(
				'meta',
				**{
					' http-equiv="%s"':
					'Content-type',
					' content="%s"':
					'text/html; charset=UTF-8'
					}
				)
			).string()
    @classmethod
    def region(cls):
        return cls.meta_template(
			'geo.region',
			Snippet(
				C.DEF_COUNTRY,
				'-',
				C.DEF_STATE
				).string()
			)
    @classmethod
    def placename(cls):
        return cls.meta_template(
			'geo.placename',
			C.PLACENAME)
    @classmethod
    def position(cls):
        cls.text.join(
			cls.meta_template(
				'geo.position',
				Snippet(
					C.LAT,
					';',
					C.LONG
					).string()
				),
			cls.meta_template(
				'icbm',
				Snippet(
					C.LAT,
					',',
					C.LONG
					).string()
				)
			)
        return cls.text.string()
    @classmethod
    def viewport(cls):
        return cls.meta_template(
			'viewport',
			'''width=device-width,
			initial-scale=1.0''')
    @classmethod
    def hide(cls):
        return cls.meta_template(
			'robots',
			'''noindex,
			nofollow''')
    @classmethod
    def noindex(cls):
        return cls.meta_template(
			'robots',
			'noindex')
    @classmethod
    def nofollow(cls):
        return cls.meta_template(
			'robots',
			'nofollow')
    @classmethod
    def author(cls):
        return cls.meta_template(
			'author',
			C.NAME)
    @classmethod
    def description(cls, content):
        return cls.meta_template(
			'description',
			content)
    @classmethod
    def load_title(cls):
        if C.TITLE == None:
            cls.__create_title()
        return cls.tag(
			cls.title,
			C.TITLE)
    @classmethod
    def CSSlib(cls, css):
        return cls.metalink(
			'stylesheet',
			cls.tag(
				'/text/css/%s.css',
				css
				)
			)
    @classmethod
    def CSS(cls):
        file_name = C.NAME.replace(
			' ',
			'')
        file_name = file_name.replace(
			'.',
			'')
        return cls.CSSlib(
			file_name.lower()
			)
    @classmethod
    def BootStrap(cls):
        return cls.CSSlib(
			'bootstrap.min'
			)
    @classmethod
    def Picnic(cls):
        return cls.CSSlib(
			'picnic.min'
			)
    @classmethod
    def Pure(cls):
        return cls.CSSlib(
			'pure-min'
			)
    @classmethod
    def JSlib(cls, js):
        return cls.addprop(
			cls.create_element(
				'script',
				'',
				src=cls.tag(
					'/text/js/%s.js',
					js
					)
				),
				cls.defer
				)
    @classmethod
    def JS(cls):
        file_name = NAME.replace(
			' ',
			'')
        file_name = file_name.replace(
			'.',
			'')
        return cls.JSlib(
			file_name.lower()
			)
    @classmethod
    def jQuery(cls):
        return cls.JSlib(
			'jquery.min'
			)
    @classmethod
    def ThreeJS(cls):
        return cls.JSlib(
			'three.min'
			)
    @classmethod
    def AngularJS(cls):
        return cls.JSlib(
			'angular.min'
			)
    @classmethod
    def ReactJS(cls):
        return cls.JSlib(
			'react.min'
			)
    @classmethod
    def MeteorJS(cls):
        return cls.JSlib(
			'meteor.min'
			)
    @classmethod
    def gapi(cls):
        return Snippet(
			cls.meta_template(
				'google-signin-scope',
				C.SCOPES
				),
			cls.meta_template(
				'google-signin-client_id',
				C.CLIENTID
				),
			'<script src="https://',
			'apis.google.com/js/',
			'platform.js" defer></script>'
			).string()
    @classmethod
    def add_robots(cls):
        rob = C.ROBOTS.replace(' ', '')
        isif = rob == 'index,follow'
        isfi = rob == 'follow,index'
        if C.DEV_MODE:
            C.ROBOTS = 'hide'
        elif isif or isfi:
            C.ROBOTS = None
        robots = Switch()
        robots.case(
			'hide',
			cls.hide
			)
        robots.case(
			'nofollow',
			cls.nofollow
			)
        robots.case(
			'noindex',
			cls.noindex
			)
        if robots.has(C.ROBOTS):
            cls.data.add(
				robots.value(
					C.ROBOTS
					)
				)
    @classmethod
    def add_description(cls):
        cls.data.join(
			cls.og_descr(
				C.DESCR
				),
			cls.description(
				C.DESCR
				)
			)
    @classmethod
    def add_libs(cls, *args):
        libs = []
        if args:
            meta_options = Switch()
            meta_options.case(
				'search',
				cls.markup.search
				)
            meta_options.case(
				'gapi',
				cls.metaGAPI
				)
            meta_options.case(
				'jQuery',
				cls.jQuery
				)
            meta_options.case(
				'ThreeJS',
				cls.ThreeJS
				)
            meta_options.case(
				'AngularJS',
				cls.AngularJS
				)
            meta_options.case(
				'MeteorJS',
				cls.MeteorJS
				)
            meta_options.case(
				'ReactJS',
				cls.ReactJS
				)
            meta_options.case(
				'Pure',
				cls.Pure
				)
            meta_options.case(
				'Picnic',
				cls.Picnic
				)
            meta_options.case(
				'BootStrap',
				cls.BootStrap
				)
            for arg in args:
                libs.append(
					meta_options.value(
						arg
						)
					)
        cls.data.join(*libs)
    @classmethod
    def default(cls, *args):
        robots_isset = C.ROBOTS != None
        if robots_isset or C.DEV_MODE:
            cls.add_robots()
        descr_isset = C.DESCR != None
        if descr_isset:
            cls.add_description()
        if args:
            cls.add_libs(*args)
        cls.data.join(
			cls.contenttype(),
			cls.author(),
			cls.viewport(),
			Href_Lang().get(),
			cls.og_locale(),
			cls.og_type(),
			cls.og_title(),
			cls.og_url(),
			cls.og_site_name(),
			cls.og_image(),
			cls.region(),
			cls.position(),
			cls.placename(),
			cls.markup.site_name(),
			cls.markup.entity(),
			cls.CSS(),
			cls.JS(),
			cls.shortlink(),
			cls.canonical(),
			cls.shortcut_icon(),
			cls.phoneicon(),
			cls.tableticon(),
			cls.load_title())
        cls.reset()
        return cls.data.string(
			).replace(
				'\n',
				'')
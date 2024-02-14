# coding=utf-8

from __future__ import unicode_literals
from builtins import str
from builtins import range
from builtins import object
from sys import modules
C = modules['MAIN'].C
C.Module.module_access(
	__name__
	)

class UI(HTML):
    @classmethod
    def gapi(cls):
        return cls.create_element(
			'div',
			'',
			**{
				'clss': 'g-signin2',
				' data-onsuccess="%s"': C.SIGNIN,
				' data-theme="%s"': 'dark'
				}
			)
    @classmethod
    def container(cls, className):
        return cls.create_element(
			'div',
			'%s',
			clss=className
			)
    @classmethod
    def input(cls, _name, _type):
        return cls.create_element(
			'input',
			name=_name,
			type=_type)
    @classmethod
    def submit_input(cls, name):
        return cls.input(
			name,
			'submit')
    @classmethod
    def hidden_input(cls, name):
        return cls.input(
			name,
			'hidden')
    @classmethod
    def text_input(cls, name):
        return cls.input(
			name,
			'text')
    @classmethod
    def textarea_input(
		cls,
		**kwargs):
        if 'innertext' in kwargs:
            text = kwargs['innertext']
            del kwargs['innertext']
        else:
            text = ''
        return cls.create_element(
			'textarea',
			text,
			**kwargs
			)
    @classmethod
    def radio_input(cls, name):
        return cls.input(
			name,
			'radio'
			)
    @classmethod
    def password_input(cls, name):
        return cls.input(
			name,
			'password')
    @classmethod
    def checkbox_input(cls, name):
        return cls.input(
			name,
			'checkbox')
    @classmethod
    def number_input(cls, name):
        return cls.input(
			name,
			'number')
    @classmethod
    def date_input(cls, name):
        return cls.input(
			name,
			'date')
    @classmethod
    def color_input(cls, name):
        return cls.input(
			name,
			'color')
    @classmethod
    def range_input(cls, name):
        return cls.input(
			name,
			'range')
    @classmethod
    def time_input(cls, name):
        return cls.input(
			name,
			'time')
    @classmethod
    def search_input(cls, name):
        return cls.input(
			name,
			'search')
    @classmethod
    def url_input(cls, name):
        return cls.input(
			name,
			'url')
    @classmethod
    def box(cls, classname, elements):
        return cls.tag(
			cls.container(classname),
			elements)
    @classmethod
    def image(cls, imgurl, alttext):
        return cls.create_element(
			'img',
			src=imgurl,
			alt=alttext)
    @classmethod
    def imagelink(cls,
				  imgurl,
				  alttext,
				  *args,
				  **kwargs):
        return Path.link(
			cls.image(
				imgurl,
				alttext),
			*args,
			**kwargs)
    @classmethod
    def rel_imagelink(cls,
					 imgurl,
					 alttext,
					 *args,
					 **kwargs):
        return Path.rellink(
			cls.image(
				imgurl,
				alttext),
			*args,
			**kwargs)
    @classmethod
    def logo(cls):
        return cls.image(
			C.LOGO_URL,
			NAME.__add__(
				' Logo'))
    @classmethod
    def logolink(cls, *args, **kwargs):
        return Path.rellink(
			cls.logo(),
			*args,
			**kwargs)
    @classmethod
    def __caption(cls, *caption):
        condition = IfElse(
			lambda: cls.tag(cls.figcaption, caption[0]),
			lambda: '')
        return condition.value(
			len(caption) > 0
			)
    @classmethod
    def figure(
		cls,
		imgurl,
		alttext,
		*caption):
        return cls.create_element(
			'fig',
			cls.image(
				imgurl,
				alttext),
			cls.__caption(*caption)
			)
    @classmethod
    def __fig_url(cls, url):
        condition = IfElse(
			lambda: (url),
			lambda: ())
        return condition.value(
			len(url) > 0
			)
    @classmethod
    def figurelink(
		cls,
		imgurl,
		alttext,
		linkurl,
		*caption):
        if caption:
            return cls.create_element(
	    		'fig',
		    	cls.imagelink(
			    	imgurl,
				    alttext,
				    *cls.__fig_url(
					    linkurl
					    )
				    ),
			    cls.__caption(*caption)
			    )
        else:
            return cls.create_element(
	    		'fig',
		    	cls.imagelink(
			    	imgurl,
				    alttext,
				    *cls.__fig_url(
					    linkurl
					    )
				    )
			    )
    @classmethod
    def rel_figurelink(
		cls,
		imgurl,
		alttext,
		linkurl,
		*caption):
        if caption:
            return cls.create_element(
	    		'fig',
		    	cls.rel_imagelink(
			    	imgurl,
				    alttext,
				    *cls.__fig_url(
					    linkurl
					    )
				    ),
			    cls.__caption(*caption)
			    )
        else:
            return cls.create_element(
	    		'fig',
		    	cls.rel_imagelink(
			    	imgurl,
				    alttext,
				    *cls.__fig_url(
					    linkurl
					    )
				    )
			    )
    @classmethod
    def video(cls, vidurl, alt):
        return cls.create_element(
			'video',
			alt,
			src=vidurl,
			s=' controls autoplay')
    @classmethod
    def vidslider(cls, vidurl, alt):
        return cls.addprop(
			cls.video(
				vidurl,
				alt),
			' loop muted')
    @classmethod
    def img_box(
		cls,
		clss,
		imgurl,
		text):
        return cls.addprops(
			cls.box(
				clss,
				text),
			cls.tags(
				cls.style,
				"background-image: url('",
				imgurl,
				"');"))
    @classmethod
    def img_slider(cls, imgurl, text):
        return cls.img_box(
			'imageslider',
			imgurl,
			text)
    @classmethod
    def button_box(cls, imgurl, text):
        return cls.img_box(
			'button',
			imgurl,
			text)
    @classmethod
    def __wrap(cls, parags, paragraph):
        parags.append(cls.tag(cls.p, paragraph))
    @classmethod
    def __par(cls):
        par = CyberObject()
        par.set('pars', [])
        par.set('add', par.pars.append)
        par.set(
			'wrap',
			lambda val: cls.__wrap(par.pars, val)
			)
        par.set(
			'cond',
			IfElse(par.add, par.wrap)
			)
        return par
    @classmethod
    def text_box(cls, paragraphs):
        par = cls.__par()
        for paragraph in paragraphs:
            has_p = '<p>' in paragraph
            func = par.cond.address(has_p)
            func(paragraph)
        return cls.box(
			'textbox',
			Snippet(*par.pars).element)

class Doc(Snippet):
	def __init__(self, *args):
		super(Doc, self).__init__(*args)
		self.snips = Switch()
		self.snips.case(
			str, lambda index: None)
		self.snips.case(
			str, lambda index: None)
		self.snips.case(
			Element,
			self.__replace_element)
		self.snips.setdefault(
			self.__element_error)
	def create_element(self, tag, *args, **kwargs):
		self.affix(
			UI.create_element(tag, *args, **kwargs)
			)
	def wrap(self, tag, **kwargs):
		self.merge()
		self.setval(
			UI.create_element(
				tag, self.element, **kwargs
				)
			)
	def __replace_element(self, index):
		self[index] = self[index].element
	def __element_error(self, index):
		raise TypeError(''.join([
			'Invalid element at index ',
			str(index)]))
	def __snipstr(self, snip, index):
		self.snips.defaddress(type(snip))(index)
	def merge(self):
		for index in range(len(self)):
			self.__snipstr(self[index], index)
		self.join()
	def affix(self, element):
		self.append(Element(element))
	def gapi(self):
		self.affix(UI.gapi())
	def input(self, _name, _type):
		self.affix(UI.input(_name, _type))
	def submit_input(self, name):
		self.affix(UI.submit_input(name))
	def hidden_input(self, name):
		self.affix(UI.hidden_input(name))
	def text_input(self, name):
		self.affix(UI.text_input(name))
	def textarea_input(self, **kwargs):
		self.affix(UI.textarea_input(**kwargs))
	def radio_input(self, name):
		self.affix(UI.radio_input(name))
	def password_input(self, name):
		self.affix(UI.password_input(name))
	def checkbox_input(self, name):
		self.affix(UI.checkbox_input(name))
	def number_input(self, name):
		self.affix(UI.number_input(name))
	def date_input(self, name):
		self.affix(UI.date_input(name))
	def color_input(self, name):
		self.affix(UI.color_input(name))
	def range_input(self, name):
		self.affix(UI.range_input(name))
	def time_input(self, name):
		self.affix(UI.time_input(name))
	def search_input(self, name):
		self.affix(UI.search_input(name))
	def url_input(self, name):
		self.affix(UI.url_input(name))
	def box(self, classname, elements):
		self.affix(UI.box(classname, elements))
	def image(self, imgurl, alttext):
		self.affix(UI.image(imgurl, alttext))
	def imagelink(
		self,
		imgurl,
		alttext,
		*args,
		**kwargs):
		self.affix(
			UI.imagelink(
				imgurl,
				alttext,
				*args,
				**kwargs
				)
			)
	def rel_imagelink(
		self,
		imgurl,
		alttext,
		*args,
		**kwargs):
		self.affix(
			UI.rel_imagelink(
				imgurl,
				alttext,
				*args,
				**kwargs
				)
			)
	def logo(self):
		self.affix(UI.logo())
	def logolink(self, *args, **kwargs):
		self.affix(UI.logolink(*args, **kwargs))
	def figure(self, imgurl, alttext, *caption):
		self.affix(
			UI.figure(
				imgurl,
				alttext,
				*caption
				)
			)
	def figurelink(
		self,
		imgurl,
		alttext,
		linkurl,
		*caption):
		self.affix(
			UI.figurelink(
				imgurl,
				alttext,
				linkurl,
				*caption
				)
			)
	def rel_figurelink(
		self,
		imgurl,
		alttext,
		linkurl,
		*caption):
		self.affix(
			UI.rel_figurelink(
				imgurl,
				alttext,
				linkurl,
				*caption
				)
			)
	def video(self, vidurl, alt):
		self.affix(
			UI.video(vidurl, alt)
			)
	def vidslider(self, vidurl, alt):
		self.affix(
			UI.vidslider(vidurl, alt)
			)
	def img_box(self, clss, imgurl, text):
		self.affix(
			UI.img_box(clss, imgurl, text)
			)
	def img_slider(self, imgurl, text):
		self.affix(
			UI.img_slider(imgurl, text)
			)
	def button_box(self, imgurl, text):
		self.affix(
			UI.button_box(imgurl, text)
			)
	def text_box(self, paragraphs):
		self.affix(UI.text_box(paragraphs))
	def __repr__(self):
		rep = Snippet(
			'Doc(', self.element, ') '
			)
		for element in self:
			rep.append(element.__repr__())
		rep.add(str(rep[:]))
		return rep.element

class GooglePlace(object):
    api = 'https://www.google.com/maps/embed/v1/'

    query = Switch(
		**{
			'place': '&q=',
			'search': '&q=',
			'directions': '&origin=',
			'streetview': '&location=',
			'view': '&center='
			}
		)

    def __init__(self):
        self.mode = 'place'
        self.width = '250'
        self.height = '250'
        self.border = '0'

    def src(self):
        return Snippet(
			self.api, self.mode,
			'?key=', self.key,
			self.query.address(self.mode),
			self.place.replace(
				' ', '+'
				)
			).element

    def generate(self):
        return UI.create_element(
			'iframe',
			''.join([self.place, ' - Google Map']),
			**{
				'width': self.width,
				'height': self.height,
				' frameborder="%s"': self.border,
				' style="border:%s"': self.border,
				'clss': 'googleplace',
				'src': self.src()
				}
			)

class Accordion(
	Snippet,
	CursorSwitch):
	def __init__(self):
		super(
			Accordion,
			self
			).__init__()
		self.options = OrderedDict()
	def create_bookmark(self, bookmark):
		self.case(
			bookmark,
			UI.tag(
				UI.id,
				bookmark))
	def store_bookmarks(self, *bookmarks):
		for bookmark in bookmarks:
			self.create_bookmark(bookmark)
	def get_bookmark(self, bookmark):
		return self.address(bookmark)
	def add_bookmark(self, element, bookmark):
		return UI.addprop(
			element,
			bookmark)
	def create_anchor(self, bookmark):
		self.append(
			UI.create_element(
				'li',
				Path.linkify(
					bookmark.title(),
					UI.tag(
						'#%s',
						bookmark)),
				clss='anchor'))
	def create_table(self):
		for bookmark in self.options:
			self.create_anchor(bookmark)
		for anchor in self:
			self.add(anchor)
		del self[:]
		self.table = UI.create_element(
			'ul',
			self.string(),
			clss='tableofcontents')
	def create_subtitle(self, subtitle):
		self.append(
			UI.tag(
				UI.img_box(
					'subtitlebox',
					'''/image/
					subtitlebox.png''',
					'%s'),
				UI.create_element(
					'h2',
					subtitle.title(),
					id=subtitle)))
	def store_subtitles(self):
		for bookmark in self.options:
			self.create_subtitle(bookmark)
	def create_textbox(self, index, *text):
		self[index] = Snippet(
			self[index],
			UI.text_box(
				text)
			).string()
	def store_text(self, *text_list):
		index = 0
		for text in text_list:
			self.create_textbox(
				index,
				*text)
			index += 1
	def merge(self):
		self.add(self.table)
		length = len(self)
		hascontent = lambda: length > 0
		while hascontent():
			self.add(self[0])
			self.pop(0)
			length -= 1
			if not hascontent():
				break
		self.setval(
			UI.box(
				'accordion',
				self.string()
				)
			)
	def create(self, *text_list):
		try:
			self.create_table()
			self.store_subtitles()
			self.store_text(*text_list)
			self.merge()
		except Exception:
			Errors.log()
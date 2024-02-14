/*//-
ClassicQuery 1.1//-
(c) 2023 CyberPy//-
https://github.com/CyberPy/ClassicQuery//-
License: MIT//-
*///-//-

/*import { Parents, Classic } from '/pythonmyadmin/min/cls.js';*/

var GLOBALS = [Parents, Classic];

console.logs = function (...args) {
    args.forEach(this.log);
};
String.prototype.toTitleCase = function()
{
    var chars = this.toLowerCase().split('');
    chars[0] = chars[0].toUpperCase();
    return chars.join('');
};

function params(vars) {
    var data = [];
    for (var key in vars) {
        var dataList = [key, "=", vars[key], "&"];
        for (var i in dataList) {
            data.push(dataList[i]);
        }
    }
    data.pop();
    return data.join("");
}
GLOBALS.push(params);

function cyberpyEncode(url) {
    var reg = new RegExp("/", "g");
    return encodeURIComponent(url.replace(reg, "-d-"));
}
GLOBALS.push(cyberpyEncode);

function cyberpyDecode(url) {
    var reg = new RegExp("-d-", "g");
    return decodeURIComponent(url.replace(reg, "/"));
}
GLOBALS.push(cyberpyDecode);

class ClassicQuery extends Classic {
    constructor(query, node, debug) {
        super();
        this.C = this.constructor.C;
        this.debug = debug;
        this.nodes = Array.from(node.querySelectorAll(query));
        this.init();
    }
    self_init(self) {
        if (self.nodes.length > 0) {
            self.bindNodes();
            self.createAnimations();
        } else if (self.debug) {
            throw "querySelector Error: No ".concat(query, " tags found");
        }
        self.styleMap();
    }
    self_indexOf(self, node) {
        var element;
        if (node.constructor === self.constructor) {
            element = node.nodes[0];
        } else {
            element = node;
        }
        return self.nodes.indexOf(node);
    }
    self_children(self, flatten = !0) {
        var children = [];
        for (var i in self.nodes) {
            children.push(Array.from(self.nodes[0].children));
        }
        if (children.length === 1 && flatten) {
            children = children[0];
        }
        return children;
    }
    self_flatChildren(self) {
        var children = self.children(!1);
        return [].concat.apply([], children);
    }
    self_childNode(self) {
        return self.C.node(self.flatChildren());
    }
    self_childNodes(self) {
        var children = self.flatChildren();
        for (var i in children) {
            children[i] = self.C.node(children[i]);
        }
        return children;
    }
    static cls_styleMap(cls) {
        cls.getter = { true: cls.computedStyle, false: cls.style };
        cls.setter = {
            true: cls.zero,
            false: function (vars) {
                return vars.oldVal - vars.quanta;
            },
        };
    }
    static stc_computedStyle(element) {
        return window.getComputedStyle(element);
    }
    static stc_style(element) {
        return element.style;
    }
    static cls_elementStyle(cls, element, computedStyle) {
        return function () {
            return cls.getter[computedStyle](element);
        };
    }
    static stc_element(element) {
        return function () {
            return element;
        };
    }
    static cls_propOwners(cls, element, computedStyle) {
        return { true: cls.element(element), false: cls.elementStyle(element, computedStyle) };
    }
    static cls_mutableProp(cls, element) {
        return cls.propOwners(element, !1)[element.style === undefined]();
    }
    static cls_prop(cls, element) {
        return cls.propOwners(element, !0)[element.style === undefined]();
    }
    static cls_attrValue(cls, vars) {
        var strAttr = cls.prop(vars.element)[vars.attr];
        if (typeof strAttr === "string") {
            strAttr = strAttr.replace("px", "");
            strAttr = strAttr.replace("%", "");
            strAttr = Number(strAttr);
        }
        return strAttr;
    }
    static cls_attrUnit(cls, vars) {
        var attrValue = cls.prop(vars.element)[vars.attr];
        if (typeof attrValue !== "string") {
            attrValue = attrValue.toString();
        }
        var unit;
        if (attrValue.includes("px")) {
            unit = "px";
        } else if (attrValue.includes("%")) {
            unit = "%";
        } else if (attrValue.includes("em")) {
            unit = "em";
        } else {
            unit = "";
        }
        return unit;
    }
    static stc_increment(vars) {
        return vars.oldVal + vars.quanta;
    }
    static cls_decrement(cls, vars) {
        return cls.setter[vars.quanta > vars.oldVal](vars);
    }
    static stc_zero(vars) {
        return 0;
    }
    static stc_greaterStop(vars) {
        return vars.attr >= vars.value;
    }
    static stc_lesserStop(vars) {
        return vars.attr <= vars.value;
    }
    static cls_animation(cls, vars) {
        var actions = { true: cls.increment, false: cls.decrement };
        var conditions = { true: cls.greaterStop, false: cls.lesserStop };
        var attr = cls.attrValue(vars);
        var unit = cls.attrUnit(vars);
        var action = actions[vars.value > attr];
        var condition = conditions[vars.value > attr];
        var speed = Math.abs(attr - vars.value) / vars.time;
        var value;
        if (vars.value > attr) {
            value = vars.value;
        } else {
            value = attr;
        }
        var quanta = value / vars.time;
        if (quanta === 0) {
            quanta = 0.1;
        }
        var interval = setInterval(function () {
            var stop = condition({ attr: attr, value: vars.value });
            if (stop) {
                clearInterval(interval);
                cls.mutableProp(vars.element)[vars.attr] = vars.value.toString().concat(unit);
                if (vars.callback) {
                    return vars.callback();
                }
            } else {
                var newVal = action({ oldVal: attr, quanta: quanta });
                cls.mutableProp(vars.element)[vars.attr] = newVal.toString().concat(unit);
                attr = cls.attrValue(vars);
            }
        }, speed);
    }
    self_animate(self, vars) {
        self.apply(function (e) {
            self.animation(Object.assign({ element: e }, vars));
        });
    }
    self_createAnimation(self, style) {
        var styleName = style[0].toUpperCase().concat(style.slice(1));
        var name = "animate".concat(styleName);
        self[name] = function (value, msecs, callback) {
            self.animate({ value: value, attr: style, time: msecs, callback: callback });
        };
    }
    self_createAnimations(self) {
        for (var i in self.nodes[0].style) {
            self.createAnimation(i);
        }
    }
    self_bindCalls(self, i) {
        self[i] = function (args) {
            var arr = args instanceof Array;
            if (!arr) {
                args = [args];
            }
            var res = [];
            self.nodes.forEach(function (e) {
                res.push(e[i](...args));
            });
            return res;
        };
    }
    static stc_attrPath(args) {
        return 'self.nodes[i]["'.concat(args.join('"]["'), '"]');
    }
    static cls_setAttrPath(cls, args) {
        return cls.attrPath(args).concat("=val");
    }
    self_wrapPath(self, path) {
        var arr = path instanceof Array;
        if (!arr) {
            path = [path];
        }
        return path;
    }
    self_set(self, path, val) {
        path = self.wrapPath(path);
        for (var i in self.nodes) {
            eval(self.setAttrPath(path));
        }
    }
    static cls_getComputedPath(cls, path) {
        return "window.getComputedStyle(self.nodes[i], null).getPropertyValue(".concat('"', path[0], '")');
    }
    static cls_getPath(cls, path) {
        var attrPath;
        if (path[0] === "style") {
            attrPath = cls.getComputedPath(path);
        } else {
            attrPath = cls.attrPath(path);
        }
        return attrPath;
    }
    self_get(self, path) {
        var val = [];
        path = self.wrapPath(path);
        for (var i in self.nodes) {
            eval("val.push(".concat(self.getPath(path), ")"));
        }
        if (val.length === 1) {
            val = val[0];
        }
        return val;
    }
    self_bindNodes(self) {
        for (var i in self.nodes[0]) {
            var isset = Boolean(self.nodes[0][i]);
            var isfunc = typeof self.nodes[0][i] === "function";
            if (!isset && isfunc) {
                self.bindCalls(i);
            }
        }
    }
    self_apply(self, func) {
        self.nodes.forEach(func);
    }
    self_event(self, event, func) {
        var eventHandler = function (element) {
            element.addEventListener(event, () => {
                func(element);
            });
        };
        self.apply(eventHandler);
    }
    self_html(self, responseText) {
        self.set("innerHTML", responseText);
    }
    self_from(self, uri, data, method, contentType, onfail) {
        self.C.request(uri, self.html, data, method, contentType, onfail);
    }
    self_getNode(self, index) {
        if (index >= self.nodes.length) {
            throw "Error: No node at index ".concat(index.toString());
        }
        return self.C.node(self.nodes[index]);
    }
    self_length(self) {
        return self.nodes.length;
    }
}
GLOBALS.push(ClassicQuery);

function C(query, node = document, debug = !1) {
    return new ClassicQuery(query, node, debug);
}
GLOBALS.push(C);

C.node = function (...node) {
    var cNode = this();
    for (var i in node) {
        cNode.nodes.push(node[i]);
    }
    cNode.init();
    return cNode;
}.bind(C);
C.create = function (tag) {
    var e = document.createElement(tag);
    return this.node(e);
}.bind(C);
C.request = function (uri, onsuccess, data = {}, method = "GET", contentType = "application/json", onfail = function () {}) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () {
        onsuccess(this.responseText);
    };
    xhr.onerror = function () {
        onfail(this.response);
    };
    try {
        xhr.open(method, uri, !0);
        xhr.setRequestHeader("Content-Type", contentType);
        xhr.send(params(data));
    } catch (e) {
        throw "Error: request received invalid arguments";
    }
};
ClassicQuery.C = C;
C.noConflict = function () {
    window.cQuery = ClassicQuery.C;
};
Classic.initStatic(ClassicQuery);
class RequestPromise extends Classic {
    constructor(
        uri,
        onsuccess,
        data = {},
        method = "GET",
        contentType = "application/json",
        onfail = function (status) {
            return status;
        }
    ) {
        super();
        this.xhr = new XMLHttpRequest();
        this.data = data;
        this.xhr.open(method, uri, !0);
        this.xhr.setRequestHeader("Content-Type", contentType);
        this.handle = function (res, rej) {
            this.xhr.onload = function () {
                res(onsuccess(this.responseText, this.val));
            };
            this.xhr.onerror = function () {
                rej(onfail(this.statusText, this.val));
            };
        }.bind(this);
    }
    self_send(self) {
        self.xhr.send(params(self.data));
    }
    self_create(self, val) {
        self.val = val;
        try {
            return new Promise(function (res, rej) {
                self.handle(res, rej);
                self.send();
            });
        } catch (e) {
            console.warn(e.message);
        }
    }
}
GLOBALS.push(RequestPromise);

class BundleRequest extends Classic
{
    constructor(basePoint='/api/')
    {
        super();
        this.basePoint = basePoint;
        this.endPoint = basePoint.concat('bundle');
        this.reqs = [];
        this.callBacks = [];
    }

    self_addEndPoint(self, uri, onsuccess, data={}, method='POST', userCache='1')
    {
        var req = {
            'method': method,
            'data': data,
            'uri': uri.replace(self.basePoint, ''),
            'user_cache': userCache
        };
        self.reqs.push(req);
        self.callBacks.push(onsuccess);
    }

    self_loopCallBacks(self, resp)
    {
        try
        {
            var resps = JSON.parse(resp).query;
            if( resps.constructor !== Array )
            {
                throw "BundleRequest Response Error: expected array";
            }
            self.callBacks.forEach((callBack, idx)=>{
                callBack(resps[idx]);
            });
        }
        catch(e)
        {
            console.warn(e.message);
        }
    }

    self_create(self)
    {
        var bundle = new RequestPromise(
            self.endPoint,
            self.loopCallBacks,
            {REQS: JSON.stringify(self.reqs)},
            'POST' );
        return bundle.create();
    }
}

class AnimationPromise extends Classic {
    constructor(animation, val, time) {
        super();
        this.animation = animation;
        this.val = val;
        this.time = time;
        this.check();
    }
    self_handle(self, res, rej) {
        var callback = () => {
            res("success");
        };
        var fail = (msg) => {
            rej(msg);
        };
        try {
            self.animation(self.val, self.time, callback);
        } catch (e) {
            console.log(e.message);
            fail(e.message);
        }
    }
    self_check(self) {
        var atype = typeof self.animation;
        var vtype = typeof self.val;
        var ttype = typeof self.time;
        if (atype !== "function") {
            throw "Error: animation must be a function, got ".concat(atype, " instead");
        }
        if (vtype !== "number") {
            throw "Error: value must be a number, got ".concat(vtype, " instead");
        }
        if (ttype !== "number") {
            throw "Error: time must be a number, got ".concat(ttype, " instead");
        }
    }
    self_create(self) {
        return new Promise(self.handle);
    }
}
GLOBALS.push(AnimationPromise);

class Chain extends Classic {
    constructor(name) {
        super();
        this.name = name;
        this.reset();
        this.proceed = { true: this.next, false: this.err };
        this.last = null;
    }
    self_append(self, prom) {
        self.proms.push(prom);
    }
    self_extend(self, proms) {
        for (var i in proms) {
            self.append(proms[i]);
        }
    }
    self_next(self, i) {
        self.last = self.last.then(self.proms[i], () => {
            return self.err(i);
        });
    }
    self_err(self, i) {
        var err = "Error: ";
        if (typeof self.name === "string") {
            err = err.concat(' in chain "', self.name, '"');
        }
        i++;
        err = err.concat(" at index ", i.toString(), ", ", self.proms[i - 1].method);
        console.warn(err);
        return Promise.reject();
    }
    self_setLast(self) {
        if (!self.proms.length) {
            var err = "Error: empty chain";
            if (typeof self.name === "string") {
                err = err.concat(' "', self.name, '"');
            }
            throw err;
        }
        if (!self.last) {
            self.last = self.proms[0]();
            self.proms.splice(0, 1);
        }
    }
    self_loop(self) {
        for (var i in self.proms) {
            self.proceed[Boolean(self.last)](i);
        }
    }
    self_exe(self) {
        self.setLast();
        self.loop();
        return self.last;
    }
    self_reset(self) {
        self.proms = [];
    }
    static stc_prom(func) {
        return new Promise(function (res, rej) {
            try {
                func(() => {
                    res("success");
                });
            } catch (e) {
                console.warn(e.message);
                rej(e.message);
            }
        });
    }
    static cls_promify(cls, func) {
        return () => {
            return cls.prom(func);
        };
    }
}
GLOBALS.push(Chain);
Classic.initStatic(Chain);

class API extends Classic {
    static cls_result(cls, vars) {
        var rep = MySQL.rep;
        MySQL.rep = new Rep(vars.responseText, vars.href);
        MySQL.lower();
        MySQL.dcount(rep);
    }
    static cls_setVars(cls, vars) {
        if (!vars.data) {
            vars.data = {};
        }
        if (!vars.onsuccess) {
            vars.onsuccess = function (obj) {
                cls.result(obj);
                return "success";
            };
        }
    }
    static cls_request(cls, vars) {
        var req = new RequestPromise(
            vars.href,
            function (text, val) {
                return vars.onsuccess({ responseText: text, href: vars.href, value: val, method: vars.method });
            },
            vars.data,
            vars.method
        );
        return req;
    }
    static cls_get(cls, vars) {
        cls.setVars(vars);
        vars.method = "GET";
        return cls.request(vars);
    }
    static cls_post(cls, vars) {
        cls.setVars(vars);
        vars.method = "POST";
        vars.data.new = vars.value;
        return cls.request(vars);
    }
    static cls_put(cls, vars) {
        cls.setVars(vars);
        vars.method = "PUT";
        vars.data.new = vars.value;
        return cls.request(vars);
    }
    static cls_delete(cls, vars) {
        cls.setVars(vars);
        vars.method = "DELETE";
        return cls.request(vars);
    }
}
GLOBALS.push(API);
Classic.initStatic(API);

class Resource extends Classic {
    constructor(links) {
        if (!links) {
            throw "Err: Invalid resource parameters";
        }
        super();
        this.links = links;
        this.addLinks();
    }
    self_shorten(self, link) {
        var pathList = link.href.split("/");
        var secLast = pathList[pathList.length - 3];
        link.href = link.href.replace(secLast.concat("/", self.value), secLast);
        link.data = {};
        link.data[secLast] = self.value;
    }
    self_shortenLinks(self) {
        for (var key in self.links) {
            self.shorten(self.links[key]);
        }
    }
    self_addLinks(self) {
        for (var key in self.links) {
            self.addLink(self.links[key]);
        }
    }
    self_addLink(self, link) {
        var method = link.method.toLowerCase();
        self[method] = function (...path) {
            return API[method]({ onsuccess: self.onsuccess, href: link.href.concat(path.join("/")), value: self.value, data: link.data });
        };
    }
}
GLOBALS.push(Resource);

class Rep extends Classic {
    constructor(json, parent = "/api/query/") {
        var obj = JSON.parse(json);
        super();
        this.parent = parent;
        this.resources = {};
        for (var query in obj) {
            this.toSelf(obj[query]);
        }
    }
    self_cyberpyEncode(self) {
        for (var key in self.resources) {
            var newKey = cyberpyEncode(key);
            if (newKey !== key) {
                self.resources[newKey] = self.resources[key];
                delete self.resources[key];
            }
        }
    }
    self_imp(self, vars) {
        if (!self[vars.new]) {
            try {
                self.resources[vars.new] = new Resource(vars.links);
            } catch (e) {
                console.log(e.message);
            }
        }
    }
    self_impArr(self, arr) {
        for (var key in arr) {
            self.imp(arr[key]);
        }
    }
    self_import(self, arr) {
        if (arr instanceof Array) {
            self.impArr(arr);
        } else if (arr instanceof Object) {
            self.imp(arr);
        }
    }
    self_toSelf(self, arr) {
        if (Boolean(arr)) {
            self.import(arr);
        }
    }
    static cls_state(cls, json) {
        return new cls(json);
    }
}
GLOBALS.push(Rep);

class MySQL extends Classic {
    static cls_last(cls) {
        return cls.reps.length - 1;
    }
    static cls_isLast(cls) {
        return cls.last() === cls.index;
    }
    static cls_toLast(cls) {
        cls.rep = cls.reps[cls.last()];
    }
    static cls_toTop(cls) {
        cls.rep = cls.reps[0];
    }
    static cls_toIndex(cls, index) {
        if (!index) {
            index = cls.index;
        }
        cls.rep = cls.reps[index];
    }
    static cls_next(cls) {
        cls.index++;
        cls.toIndex();
    }
    static cls_up(cls) {
        cls.index--;
        cls.toIndex();
    }
    static cls_toReps(cls) {
        var isLast = cls.isLast();
        cls.index++;
        if (isLast) {
            cls.reps.push(cls.rep);
        } else {
            cls.reps[cls.index] = cls.rep;
            cls.reps.length = cls.index + 1;
        }
    }
    static cls_dcount(cls, rep) {
        if (rep !== cls.rep) {
            cls.toReps();
        }
    }
    static cls_top(cls) {
        return API.get({ href: "/api/query/" });
    }
    static cls_lower(cls) {
        if (cls.rep) {
            var resources = {};
            for (var i in cls.rep.resources) {
                cls.rep.resources[i].value = i;
                resources[i.toLowerCase()] = cls.rep.resources[i];
            }
            cls.rep.resources = resources;
        }
    }
    static cls_init(cls) {
        cls.rep = null;
        cls.reps = [];
        cls.index = -1;
        return cls.top().create();
    }
    static cls_propsLength(cls) {
        var index = 0;
        for (var i in cls.rep.resources) {
            index++;
        }
        return index;
    }
    static cls_down(cls, resKey, ...path) {
        var res = cls.rep.resources[resKey.toLowerCase()];
        return res.get(...path).create();
    }
}
GLOBALS.push(MySQL);
Classic.initStatic(MySQL);

class Model extends Classic {
    constructor(dbname, tbname, model, baseURI='/api/query/') {
        super();
        this.baseURI = baseURI;
        this.dbname = dbname;
        this.tbname = tbname;
        this.model = model;
        this.chain = new Chain("ClassicQuery.Model");
        this.check();
        this.props = {};
    }
    self_set(self, prop, value, encode) {
        if (encode) {
            value = cyberpyEncode(value);
        }
        self.props[prop] = value;
    }
    self_get(self, prop) {
        return self.props[prop];
    }
    self_getVal(self, prop) {
        return cyberpyDecode(String(self.props[prop]));
    }
    self_setVal(self, prop, value)
    {
        return self.set(prop, value, true);
    }
    self_uri(self, isNew)
    {
        return [
            self.baseURI, self.dbname,
            '/', self.tbname, '/',
            (isNew) ? '': self.model
            ].join('').toLowerCase();
    }
    self_length(self)
    {
        return Object.keys(self.props).length;
    }
    self_addProps(self, resp) {
        try
        {
            var res = JSON.parse(resp).query;
            if( res.constructor !== Object )
            {
                throw "Error: invalid response";
            }
            for(var key in res)
            {
                self.props[ key.toLowerCase() ] = res[key];
            }
        }
        catch(e)
        {
            var msg = [
                'Failed GET: ', self.uri(),
                '/*\n', e.message || e ];
            console.warn(msg.join(''));
        }
    }
    self_addExtra(self, extra) {
        if (extra) {
            self.chain.extend(extra);
        }
    }
    self_exe(self, extra) {
        return new Promise(function (res, rej) {
            try {
                self.addExtra(extra);
                self.chain.append(() => {
                    self.chain.reset();
                    res("success");
                });
                self.chain.exe();
            } catch (e) {
                rej(e.message);
            }
        });
    }
    self_check(self) {
        if (!self.dbname) {
            throw "Error: No database specified";
        }
        if (!self.tbname) {
            throw "Error: No table specified";
        }
    }
    self_create(self, then) {
        var req = new RequestPromise(
            self.uri(true), (resp)=>{
                try{
                    var models = JSON.parse(resp)[self.tbname];
                    if( models.constructor !== Array )
                    {
                        throw "Error: expected array";
                    }
                    if(!then){return;}
                    then(models);
                } catch(e) {
                    var msg = [
                        "Failed POST: ".concat(self.uri()),
                        '\n', e.message || e ];
                    console.warn(msg.join(''));
                    self.props = {};
                }
            },
            {'new': self.model}, 'POST' );
        return req.create();
    }
    self_read(self) {
        var req = new RequestPromise(
            self.uri().concat('/*'),
            self.addProps );
        return req.create();
    }

    self_update(self, prop, value, then) {
        var uri = self.uri().concat('/', prop);
        var data = {};
        data[prop] = 'none';
        self.setVal(prop, value);
        data['new'] = self.get(prop);
        var req = new RequestPromise(
            uri, (resp)=>{
                try{
                    if( JSON.parse(resp)[prop].id !== 0 )
                    {
                        throw "Error: invalid data";
                    }
                    if(!then){return;}
                    then(self);
                } catch(e) {
                    var msg = [
                        "Failed PUT: ".concat(uri),
                        '\n', e.message || e ];
                    console.warn(msg.join(''));
                }
            },
            data, 'PUT' );
        return req.create();
    }
    self_delete(self, then) {
        var req = new RequestPromise(
            self.uri(), (resp)=>{
                try{
                    var models = JSON.parse(resp)[self.tbname];
                    if( models.constructor !== Array )
                    {
                        throw "Error: expected array";
                    }
                    if(!then){return;}
                    then(models);
                } catch(e) {
                    var msg = [
                        "Failed DELETE: ".concat(self.uri()),
                        '\n', e.message || e ];
                    console.warn(msg.join(''));
                }
            },
            self.props, 'DELETE' );
        return req.create();
    }
    self_crud(self, commands) {
        var chain = new Chain("ClassicQuery.Model.crud");
        chain.extend(commands);
        return chain.exe();
    }
}
GLOBALS.push(Model);

/*function uniScope(scope, global)
{
    scope[ global.name ] = global;
}

function scopeFactory(scope)
{
    return (global)=>{
        uniScope(scope, global);
    };
}

export default function init(scope=window)
{
    var toScope = scopeFactory(scope);
    GLOBALS.forEach(toScope);
    return GLOBALS;
};

GLOBALS.add = function(global, scope=window)
{
    this.push(global);
    uniScope(scope, global);
};*/

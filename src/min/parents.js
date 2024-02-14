/*

ParentsJS V1.1
(c) 2023 AristoTech*
https://aristotech.vip/wp-content/parents-1.1.js
License:MIT

* V1.0 published under "CyberPy"

*/

export default class Parents {
    constructor(a = null) {
        null !== a && Parents.inherit(this, a);
    }
    static checkConstructor(a) {
        for (var b in a) {
            var c = "constructor" === a[b];
            if (c) return !0;
        }
    }
    static getMethods(a) {
        var b = Object.getOwnPropertyNames(a),
            c = Parents.checkConstructor(b);
        if (c) {
            	var d = b.indexOf('constructor');
              b.splice(d, 1);
        }
        return b;
    }
    static set(a, b, c) {
        for (var d in b) {
            var e = b[d];
            if(a[e]){continue;}
            a[e] = c[e];
        }
    }
    static inherit(a, b) {
        for (var c = 0; c < b.length; c++) {
            var d = b[c],
                e = new d(),
                f = Object.getOwnPropertyNames(e),
                g = Parents.getStaticMethods(d),
                h = Parents.getMethods(d.prototype);
            ['name',...g].forEach((i)=>{
            	var j = i.replace('stc_','').replace('cls_',''),
              	k = f.indexOf(j);
              if(k === -1){return;}
              f.splice(k, 1);
            });
            Parents.set(a.constructor, g, d);
            Parents.set(a, f, e);
            Parents.set(a.constructor.prototype, h, d.prototype);
        }
    }
    static getStaticMethods(a) {
        var b = Object.getOwnPropertyNames(a),
            c = Parents.checkConstructor(b),
            d = [];
        b.forEach((e)=>{
        	if(e.startsWith('cls_') || e.startsWith('stc_'))
          {
          	d.push(e);
          }
        });
        return d;
    }
		static staticInherit(a, b) {
        for (var c = 0; c < b.length; c++) {
            var d = b[c],
                e = Parents.getStaticMethods(d);
            Parents.set(a, e, d);
        }
    }
}
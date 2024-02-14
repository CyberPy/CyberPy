/*

ClassicJS V1.1
(c) 2023 AristoTech*
https://aristotech.vip/wp-content/classic-1.1.js
License:MIT

* V1.0 published under "CyberPy"

*/

import Parents from '/pythonmyadmin/min/parents.js';

export{Parents};

export class Classic extends Parents {
    constructor(a = null) {
        super(a), Classic.instanceImport(this);
    }
    static instanceImport(a) {
        Classic.clsMethod(a), Classic.stcMethod(a), a.selfMethod(a), Classic.initStatic(a.constructor);
    }
    static init(a, b = null) {
        Parents.inherit(a), Classic.instanceImport(b);
    }
    static setMethods(a, b, c, d) {
        var e = Parents.getMethods(a);
        for (var f in e) {
            var g = e[f];
            var h = g.replace(c, "");
            g !== h && (!b.name && (b.name = b.constructor.name), (b[h] = d(b, a[g])), a[g].constructor === Function && (b[h].method = b.name.concat(".", h)));
        }
    }
    static initStatic(a, b = []) {
        Parents.staticInherit(a, b);
        Classic.setMethods(a, a, "cls_", Classic.template), Classic.setMethods(a, a, "stc_", Classic.stcTemplate);
    }
    static template(a, b) {
        return function() {
            var c = Array.from(arguments);
            return c.splice(0, 0, a), b(...c);
        };
    }
    static stcTemplate(a, b) {
        if (b.constructor !== Function) {
            return b;
        }
        return function() {
            var c = Array.from(arguments);
            return b(...c);
        };
    }
    selfMethod(a) {
        Classic.setMethods(a.constructor.prototype, a, "self_", Classic.template);
    }
    static clsMethod(a) {
        Classic.setMethods(a.constructor, a, "cls_", Classic.template);
    }
    static stcMethod(a) {
        Classic.setMethods(a.constructor, a, "stc_", Classic.stcTemplate);
    }
}
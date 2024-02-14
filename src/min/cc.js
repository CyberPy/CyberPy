/*//-
CreditCardJS V1.0//-
(c) 2023 AristoTech* //-
https://aristotech.vip/wp-content/cc.js//-
License: MIT//-

* Original release under "CyberPy"
*///-//-

import { Classic } from '/pythonmyadmin/min/cls.js';

export default class CreditCard extends Classic{constructor(a){super(),this.cc=a}self_reduce(a,b){return 9<b&&(b-=9),b}self_double(a,b){0!=b%2&&(a.cc[b]=a.reduce(2*a.cc[b]))}self_iterate(a){for(var b in a.cc)a.double(b)}self_add(a){a.cc=a.cc.reduce((b,c)=>b+c,0)}self_validate(a){return a.iterate(),a.add(),0==a.cc%10}self_filter(a){for(var b in a.cc=a.cc.replace(' ',''),a.cc=a.cc.replace('-',''),a.cc=a.cc.split(''),a.cc)a.cc[b]=+a.cc[b];a.cc.reverse()}self_check(a){var b;return'string'==typeof a.cc?(a.filter(),b=a.validate()):b=!1,b}}

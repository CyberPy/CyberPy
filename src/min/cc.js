/*//-
CreditCardJS V1.1//-
(c) 2023 AristoTech* //-
https://aristotech.vip/wp-content/cc-1.1.js//-
License: MIT//-

* Original release under "CyberPy"
*///-//-

import { Classic } from '/pythonmyadmin/min/cls.js';

export default class CreditCard extends Classic{constructor(a){super(),this.cc=a}static stc_reduce(a){return 9<a&&(a-=9),a}self_double(a,b){0!=b%2&&(a.cc[b]=a.reduce(2*a.cc[b]))}self_iterate(a){for(var b in a.cc)a.double(b)}self_add(a){a.cc=a.cc.reduce((b,c)=>b+c,0)}self_validate(a){return a.iterate(),a.add(),0==a.cc%10}self_filter(a){for(var b in a.cc=a.cc.replace(' ',''),a.cc=a.cc.replace('-',''),a.cc=a.cc.split(''),a.cc)a.cc[b]=+a.cc[b];a.cc.reverse()}self_check(a){var b;return'string'==typeof a.cc?(a.filter(),b=a.validate()):b=!1,b}}

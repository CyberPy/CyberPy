/*
//-
pythonMyAdmin V1.0//-
(c) 2023 CyberPy//-
https://github.com/CyberPy//-
License: MIT//-
*/

//-//-

import init from '/pythonmyadmin/min/cquery.js';
import CreditCard from '/pythonmyadmin/min/cc.js';
var GLOBALS = init();

//-//-

var session;

class Accordion extends Classic
{
    constructor()
    {
        super();
        this.acc = C('.accordion');
        if(this.has())
        {
            this.init();
        }
    }

    self_has(self)
    {
        return self.acc.length() > 0;
    }

    self_init(self)
    {
        self.imgBoxes = C('.subtitlebox');
        self.textBoxes = C('.textbox');
        self.imgBoxes.apply(self.hide);
        self.addImgBoxEvent();
        self.imgBox = C();
        self.textBox = C();
        self.last = Promise.resolve();
    }

    self_fadeOut(self)
    {
        var ani = new AnimationPromise(
            self.textBox.animateOpacity,
            0, 50);
        self.last = self.last
            .then(ani.create)
            .then(self.collapse);
    }

    self_fadeIn(self)
    {
        var ani = new AnimationPromise(
            self.textBox.animateOpacity,
            1, 50);
        self.last = self.last.then(ani.create);
    }

    self_textBoxHeight(self)
    {
        return self.textBox.get('offsetHeight')
        || self.textBox.get(['style', 'pixelHeight']);
    }

    self_animateHeight(self, value, callback)
    {
        self.textBox.set(
                ['style', 'height'],
                Number(value)
                .toString().concat('px'));
            if(callback)
            {
                callback();
            }
            self.last = Promise.resolve();
    }

    self_collapse(self)
    {
        self.animateHeight(0, self.hideTextBox);
    }

    self_expand(self)
    {
        self.showTextBox();
        self.animateHeight(self.textBox.get(
            ['dataset', 'height']));
        self.last.then(self.fadeIn);
    }

    self_hide(self, element)
    {
        self.imgBox = C.node(element);
        self.textBox = self.textBoxes.getNode(
            self.imgBoxes.indexOf(element));
        self.textBox.set(
            ['dataset', 'height'],
            self.textBoxHeight());
        self.textBox.set(['style', 'height'], '0px');
        self.hideTextBox();
    }

    self_hideTextBox(self)
    {
        self.textBox.set(['style', 'display'], 'none');
    }

    self_showTextBox(self)
    {
        self.textBox.set(['style', 'display'], 'block');
    }

    self_moveBack(self)
    {
        self.fadeOut();
        self.imgBox = C();
    }

    self_moveNew(self, node)
    {
        self.imgBox = node;
        self.textBox = self.textBoxes.getNode(
            self.imgBoxes.indexOf(node.nodes[0]));
        self.expand();
    }

    self_switch(self, node)
    {
        self.moveBack();
        setTimeout
        (
            function()
            {
                self.last.then(()=>{self.moveNew(node)});
            },
            400
        );
    }

    self_moveImgBox(self, element)
    {
        var node = C.node(element);
        switch (self.imgBox.nodes[0])
        {
            case (undefined):
                self.moveNew(node);
                break;
            case (element):
                self.moveBack();
                break;
            default:
                self.switch(node);
                break;
        }
    }

    self_addImgBoxEvent(self, element)
    {
        self.imgBoxes.event('click', self.moveImgBox);
    }
}

class HeightManager extends Classic
{
    constructor()
    {
        super();
    }

    self_lines(self, result)
    {
        var lines = Number
        (
            (
                result.length / 800
            ).toFixed(0)
        );
        if (window.innerWidth < 410)
        {
            lines *= 1.3;
        }
        if (lines === 0)
        {
            lines++;
        }
        return lines;
    }

    self_addHeight(self, result)
    {
        session.pma.addHeight
        (
            100 * self.lines(result)
        );
    }
}

class Interpreter extends Classic
{
    constructor()
    {
        super([HeightManager]);
        this.init();
        this.setClickEvents();
    }

    self_init(self)
    {
        self.scriptBox = C('#scriptbox');
        self.execButton = C('#execbutton');
        self.clearButton = C('#execclear');
        self.scriptResult = C('.scriptresult');
        self.container = C.node(
            self.scriptResult.get('parentNode'));
        self.initialHeight = self.container
            .get(['dataset', 'height']);
    }

    self_setClickEvents(self)
    {
        self.execClick();
        self.clearClick();
    }

    self_clearClick(self)
    {
        self.clearButton.event('click', self.clear);
    }

    self_clear(self)
    {
        self.scriptResult.set('innerHTML', '<br>');
        var height = self.initialHeight.concat('px');
        self.container.set(['style', 'height'], height);
        self.container.set(
            ['dataset', 'height'],
            self.initialHeight);
    }

    self_execClick(self)
    {
        self.execButton.event('click', self.evaluate);
    }

    self_evaluate(self)
    {
        C.request(
            '/pythonMyAdmin/evaluate',
            self.result,
            {
                code: cyberpyEncode(
                    self.scriptBox.get('value')
                )
            },
            'POST', 'text/html');
    }

    self_updateHeight(self, result)
    {
        session.pma.currentBox = self.container;
        self.addHeight(result);
    }

    self_insertResult(self, result)
    {
        var p = C.create('p');
        p.set('innerHTML', result);
        self.scriptResult.nodes[0]
            .appendChild(p.nodes[0]);
    }

    self_result(self, result)
    {
        self.updateHeight(result);
        self.insertResult(result);
    }

}

class ID extends Classic
{
    constructor()
    {
        super();
        this.noCancel = false;
    }

    self_promptType(self)
    {
        self.coltype = prompt('Enter column type: ');
        if(self.coltype)
        {
            self.coltype = self.coltype.toUpperCase();
            self.noCancel = true;
        }
    }

    self_promptCol(self)
    {
        self.col = prompt('Enter primary column: ');
        if(self.col)
        {
            self.col = self.col.toUpperCase();
            self.promptType();
        }
    }

    self_promptTB(self)
    {
        self.tb = prompt('Enter table: ');
        if(self.tb)
        {
            self.promptCol();
        }
    }

    self_promptDB(self)
    {
        self.db = prompt('Enter database: ');
        if(self.db)
        {
            self.promptTB();
        }
    }

    self_promptRefTB(self)
    {
        self.reftb = prompt('Enter reference table: ');
        if(self.reftb)
        {
            self.promptDB();
        }
    }

    self_promptRefDB(self)
    {
        self.refdb = prompt('Enter reference database: ');
        if(self.refdb)
        {
            self.promptRefTB();
        }
    }

    self_autoIncrement(self)
    {
        var inc;
        if(confirm('Auto-increment?'))
        {
            inc = 'AUTO_INCREMENT ';
        }
        else
        {
            inc = '';
        }
        return inc;
    }

    self_primID(self)
    {
        var alter = 'ALTER TABLE ';
        var tb = self.db.concat('.', self.tb);
        return [
        alter, tb, ' DROP PRIMARY KEY;\n',
        alter, tb, ' MODIFY ', self.col,
        ' ', self.coltype, ';\n', alter,
        tb, ' ADD ID INT NOT NULL ',
        self.autoIncrement(),
        'PRIMARY KEY FIRST;'
        ].join('');
    }

    self_getNull(self)
    {
        var nul;
        if(confirm('Prevent null value?'))
        {
            nul = 'NOT NULL ';
        }
        else
        {
            nul = '';
        }
        return nul;
    }

    self_colID(self)
    {
        return [
        'ALTER TABLE ', self.db, '.',
        self.tb, ' ADD ID INT ',
        self.getNull(), ';'].join('');
    }

    self_setIdSQL(self)
    {
        var id;
        if(confirm('Primary?'))
        {
            id = self.primID();
        }
        else
        {
            id = self.colID();
        }
        return id;
    }

    self_setRefIdSQL(self)
    {
        var alter = 'ALTER TABLE ';
        var tb = self.db.concat('.', self.tb);
        return [
        alter, tb, ' DROP PRIMARY KEY;\n',
        alter, tb, ' MODIFY ', self.col,
        ' ', self.coltype, ';\n', alter,
        tb, ' ADD ID INT NOT NULL;\n',
        alter, tb, ' ADD FOREIGN KEY(ID) REFERENCES ',
        self.refdb, '.', self.reftb, '(ID);\n',
        alter, tb, ' ADD PRIMARY KEY(', self.col, ');'
        ].join('');
    }

    static stc_btn(html)
    {
        var btn = C.create('button');
        btn.set(
            ['style', 'display'],
            'inline-block');
        btn.set('innerHTML', html);
        return btn;
    }

    static cls_setRefIdBtn(cls, onclick)
    {
        var btn = cls.btn('Set Reference ID');
        btn.event('click', onclick);
        return btn;
    }

    static cls_setIdBtn(cls, onclick)
    {
        var btn = cls.btn('Set ID');
        btn.event('click', onclick);
        return btn;
    }
}

class Progress extends Classic
{
    constructor()
    {
        super();
        this.total = 0;
        this.val = 0;
        this.progBox = C('#progbox');
        this.textBox = C.node(
            this.progBox.get('parentNode')
            );
        this.res = C('#sqlres');
        this.loadbox = C('#dbloadbox');
        this.setNodes();
        this.progPercent = C('#progpercent');
        this.progBar = C('#progbar');
        this.visible = false;
    }

    self_setNodes(self)
    {
        self.nodes = self.textBox.childNodes();
        self.nodes.forEach((e)=>{
            e.initial = e.get(['style', 'display']);
        });
        self.nodes.undo = (e)=>{
            e.set(['style', 'display'], e.initial);
        };
        self.nodes.revert = ()=>{
            self.nodes.forEach(self.nodes.undo);
        };
    }

    self_addHeight(self, i)
    {
        if(self.visible)
        {
            var height = Number(self.textBox.get(
            ['dataset', 'height'])) + 150 * i;
            self.textBox.set(
                ['style', 'height'],
                height.toString().concat('px'));
        }
    }

    self_show(self)
    {
        self.addHeight(1);
        self.nodes.forEach((e)=>{
            e.set(['style', 'display'], 'none');
        });
        self.progBox.set(
            ['style', 'display'],
            'block');
        self.res.set(
            ['style', 'display'],
            'block');
        self.loadbox.set(
            ['style', 'display'],
            'block');
        self.visible = true;
        return Promise.resolve();
    }

    self_reset(self, res)
    {
        self.val = -1;
        self.update();
        self.total = 0;
        self.nodes.revert();
        var height = self.textBox.get(
            ['dataset', 'height'])
            .concat('px');
        self.textBox.set(
            ['style', 'height'],
            height);
        self.visible = false;
        res();
    }

    self_percent(self)
    {
        var perc = self.val / self.total * 100;
        return perc.toString().concat('%');
    }

    self_setBar(self, perc)
    {
        self.progBar.set(
            ['style', 'width'],
            perc);
    }

    self_setPerc(self, perc)
    {
        self.progPercent.set('innerHTML', perc);
    }

    self_update(self)
    {
        if(self.visible)
        {
            self.val++;
            var perc = self.percent();
            self.setBar(perc);
            self.setPerc(perc);
        }
        return Promise.resolve();
    }

}

class LoadIcons extends Classic
{
    constructor(boxid)
    {
        super();
        this.last = Promise.resolve();
        this.box = C(boxid);
        this.animations = [];
        this.createAnimation();
    }

    self_createAnimation(self)
    {
        self.addFadeIn(self.box);
        var btns = self.box.childNodes();
        btns.forEach(self.addFadeIn);
        btns.forEach(self.addFadeOut);
        self.addFadeOut(self.box);
    }

    self_addAnimation(self, btn, val)
    {
        self.animations.push(
            new AnimationPromise(
            btn.animateOpacity, val, 30));
    }

    self_addFadeIn(self, btn)
    {
        self.addAnimation(btn, 1);
    }

    self_addFadeOut(self, btn)
    {
        self.addAnimation(btn, 0);
    }

    self_fade(self, ani)
    {
        self.last = self.last.then(ani.create);
    }

    self_animate(self)
    {
        self.animations.forEach(self.fade);
    }

    self_cycle(self, n)
    {
        for(var i = 0; i < n; i++)
        {
            self.animate();
        }
    }
}

class Database extends Classic
{
    constructor(csl)
    {
        super();
        this.csl = csl;
        this.reset();
        this.prog = new Progress();
    }

    self_reset(self, res)
    {
        self.tbNames = [];
        self.tbStructs = {};
        self.mdlNames = [];
        self.models = [];
        self.sql = [];
        if(res){res();}
    }

    self_successMsg(self, res)
    {
        self.csl.insertResult('- Export Complete');
        res();
    }

    self_download(self, res)
    {
        var e = document.createElement('a');
        e.href = 'data:text/plain;charset=utf-8,'
            .concat(cyberpyEncode(
            self.sql.join('')));
        e.download = self.db
            .toLowerCase()
            .concat('.sql');
        e.click();
        res();
    }

    self_getdb(self)
    {
        return MySQL.down(self.db);
    }

    self_gettb(self, tb)
    {
        return MySQL.down(tb);
    }

    self_toList(self, list)
    {
        for (var key in MySQL.rep.resources)
        {
            list.push(key);
        }
    }

    self_toTbNames(self, res)
    {
        self.toList(self.tbNames);
        for(var i in self.tbNames)
        {
            self.tbNames[i] = self.tbNames[i].toUpperCase();
        }
        self.prog.total += self.tbNames.length;
        res();
    }

    self_checkdb(self, res)
    {
        if(!MySQL.rep.resources[
            self.db.toLowerCase()])
        {
            self.csl.clear();
            self.csl.insertResult([
                '- Database "',
                self.db,
                ,'" not found'
            ].join(''));
            self.reset();
            self.prog.reset();
            throw 'Database not found';
        }
        else
        {
            res();
        }
    }

    self_tbChain(self, res)
    {
        var chain = new Chain('tbChain');
        chain.extend([
            MySQL.init,
            Chain.promify(self.checkdb),
            self.getdb,
            Chain.promify(self.toTbNames),
            res
        ]);
        chain.exe();
    }

    self_tbList(self, res)
    {
        self.sql.push(
            'CREATE DATABASE IF NOT EXISTS '
            .concat(self.db, ';'));
        self.tbChain(res);
    }

    self_toMdlNames(self, res)
    {
        self.toList(self.mdlNames);
        self.prog.total += self.mdlNames.length;
        res();
    }

    self_toModels(self, tb)
    {
        for(var i in self.mdlNames)
        {
            self.models.push(
                new Model(
                self.db, tb,
                self.mdlNames[i]));
        }
        self.mdlNames = [];
    }

    self_cycle(self)
    {
        self.csl.loadIcons.cycle(1);
        return Promise.resolve();
    }

    self_readModels(self, res)
    {
        var chain = new Chain('readModels');
        self.csl.insertResult('- Fetching Models...');
        self.prog.addHeight(self.csl.resLength());
        for (var i in self.models)
        {
            chain.extend([
                self.cycle,
                self.models[i].read,
                self.prog.update
            ]);
        }
        chain.append(res);
        chain.exe();
    }

    self_mdlChain(self, tb)
    {
        var chain = new Chain('mdlChain');
        chain.extend([
            self.cycle,
            MySQL.init,
            self.getdb,
            ()=>{return self.gettb(tb);},
            Chain.promify(self.toMdlNames),
            Chain.promify((res)=>{
                self.toModels(tb);res();}),

        ]);
        return chain;
    }

    self_mdlChainProm(self, chain)
    {
        return (res)=>{
            chain.append(res);
            chain.exe();
        };
    }

    self_fromTbNames(self, res)
    {
        var chain = new Chain('fromTbNames');
        for (var i in self.tbNames)
        {
            var mdlChain = self.mdlChain(self.tbNames[i]);
            var prom = self.mdlChainProm(mdlChain);
            chain.append(Chain.promify(prom));
        }
        chain.extend([
            Chain.promify(self.readModels),
            res
        ]);
        chain.exe();
    }

    self_filterStruct(self, struct)
    {
        return struct
            .replace('- ', '')
            .replace(/"/g, '""')
            .replace(/'/g, '"')
            .replace(/None/g, '""')
            .toUpperCase();
    }

    self_addStruct(self, tb)
    {
        self.prog.addHeight(self.csl.resLength());
        var struct = self.filterStruct(self.csl.lastResult());
        var obj = JSON.parse(struct);
        if (obj.constructor !== Array)
        {
            obj = [obj];
        }
        self.tbStructs[tb] = obj;
        return Promise.resolve();
    }

    self_describe(self, tb)
    {
        self.csl.loadIcons.cycle(1);
        var sql = 'DESCRIBE '
            .concat(self.db, '.', tb);
        return self.csl.fetchID(sql)
            .then(()=>{
                return self.addStruct(tb);
            });
    }

    self_createDescribe(self, i)
    {
        return ()=>{return self.describe(
            self.tbNames[i]);};
    }

    self_filterSession(self)
    {
        var cyberpy = /CYBERPY/.test(self.db);
        var sessions = self.tbNames.indexOf('sessions');
        if(cyberpy && sessions !== -1)
        {
            self.tbNames.splice(sessions, 1);
        }
    }

    self_toTbStructs(self, res)
    {
        self.filterSession();
        self.csl.insertResult('- Fetching Tables...');
        self.prog.addHeight(self.csl.resLength());
        var chain = new Chain('tbStructs');
        for (var i in self.tbNames)
        {
            chain.extend([
                self.createDescribe(i),
                self.prog.update
            ]);
        }
        chain.append(res);
        chain.exe();
    }

    static stc_null(col)
    {
        var sql;
        if(col.NULL === 'NO')
        {
            sql = 'NOT NULL ';
        }
        else
        {
            sql = '';
        }
        return sql;
    }

    static stc_default(col)
    {
        var def;
        if(col.DEFAULT)
        {
            def = 'DEFAULT '.concat(
                '"', col.DEFAULT, '" '
                );
        }
        else
        {
            def = '';
        }
        return def;
    }

    static stc_extra(col)
    {
        var extra;
        if(col.EXTRA)
        {
            extra = col.EXTRA.concat(' ');
        }
        else
        {
            extra = '';
        }
        return extra;
    }

    static stc_key(col)
    {
        var key;
        switch(col.KEY)
        {
            case 'UNI':
                key = 'UNIQUE ';
                break;
            case 'PRI':
                key = ', PRIMARY KEY('
                    .concat(col.FIELD, ')');
                break;
            default:
                key = '';
                break;
        }
        return key;
    }

    self_addCol(self, col)
    {
        self.sql = self.sql.concat([
            col.FIELD, ' ', col.TYPE, ' ',
            self.null(col), self.default(col),
            self.extra(col), self.key(col), ','
        ]);
    }

    self_tbSql(self, tb)
    {
        self.sql = self.sql.concat([
            'CREATE TABLE IF NOT EXISTS ',
            self.db, '.', tb, ' ('
        ]);
        for (var i in self.tbStructs[tb])
        {
            self.addCol(self.tbStructs[tb][i]);
        }
        self.sql.pop();
        self.sql.push(');');
    }

    self_createTables(self, res)
    {

        for(var i in self.tbNames)
        {
            self.tbSql(self.tbNames[i]);
        }
        res();
    }

    self_addProps(self, mdl)
    {
        for (var prop in mdl.props)
        {
            self.sql = self.sql.concat([prop, ',']);
        }
        self.sql.pop();
    }

    self_addVals(self, mdl)
    {
        for (var prop in mdl.props)
        {
            self.sql = self.sql.concat(
                ["'", mdl.props[prop].value,
                    "'", ',']
                );
        }
        self.sql.pop();
    }

    self_insert(self, mdl)
    {
        self.sql = self.sql.concat([
            'INSERT INTO ', mdl.dbname,
            '.', mdl.tbname, ' ('
        ]);
        self.addProps(mdl);
        self.sql.push(') VALUES (');
        self.addVals(mdl);
        self.sql.push(');');
    }

    self_insertModels(self, res)
    {
        for(var mdl in self.models)
        {
            self.insert(self.models[mdl]);
        }
        res();
    }

    self_promptdb(self)
    {
        self.db = prompt('Enter Database:');
        if(self.db)
        {
            self.db = self.db.toUpperCase();
        }
        else
        {
            throw 'Error: No database selected';
        }
    }

    self_export(self)
    {
        self.promptdb();
        var chain = new Chain('export');
        chain.extend([
            self.cycle,
            self.prog.show,
            Chain.promify(self.tbList),
            Chain.promify(self.toTbStructs),
            Chain.promify(self.createTables),
            Chain.promify(self.fromTbNames),
            Chain.promify(self.insertModels),
            Chain.promify(self.download),
            Chain.promify(self.reset),
            Chain.promify(self.prog.reset),
            Chain.promify(
                (res)=>{self.csl.clear(); res();}
                ),
            Chain.promify(self.successMsg)
        ]);
        chain.exe();
    }
}

class Script extends Classic
{
    constructor(csl)
    {
        super();
        this.csl = csl;
        this.input = C('#upload');
    }

    self_setVal(self, file)
    {
        self.csl.loadIcons.cycle(1);
        self.csl.sqlBox.set('value', file.target.result);
        self.csl.clear();
        self.csl.insertResult('- Upload Complete');
    }

    self_getVal(self)
    {
        var fileReader = new FileReader();
        fileReader.onload = self.setVal;
        fileReader.readAsText(
            self.input.get('files')[0]);
    }

    self_getFile(self)
    {
        self.csl.loadIcons.cycle(1);
        if('files' in self.input.nodes[0])
        {
            self.getVal();
        }
    }
}

class Console extends Classic
{
    constructor()
    {
        super([HeightManager]);
        Classic.initStatic(ID);
        this.init();
    }

    self_init(self)
    {
        self.sqlBox = C('#sqlbox');
        self.sqlres = C('#sqlres');
        self.loadIcons = new LoadIcons('#dbloadbox');
        self.db = new Database(self);
        self.script = new Script(self);
        self.container = C.node(
            self.sqlres.get('parentNode'));
        self.initialHeight = self.container
            .get(['dataset', 'height']);
        self.addIdBtn();
        self.addRefIdBtn();
    }

    self_addIdBtn(self)
    {
        self.sqlres.get('parentNode').insertBefore
        (
            ID.setIdBtn(self.setID).nodes[0],
            self.sqlres.nodes[0]
        );
    }

    self_addRefIdBtn(self)
    {
        self.sqlres.get('parentNode').insertBefore
        (
            ID.setRefIdBtn(self.setRefID).nodes[0],
            self.sqlres.nodes[0]
        );
    }

    self_execID(self, sql)
    {
        if(sql)
        {
            var val = self.sqlBox.get('value');
            self.sqlBox.set('value', sql);
            self.execSQL();
            self.sqlBox.set('value', val);
        }
    }

    self_fetchID(self, sql)
    {
        if(sql)
        {
            var val = self.sqlBox.get('value');
            self.sqlBox.set('value', sql);
            var prom = self.fetchSQL();
            self.sqlBox.set('value', val);
            return prom;
        }
    }

    self_setRefID(self)
    {
        var id = new ID();
        id.promptRefDB();
        if(id.noCancel)
        {
            var sql;
            try
            {
                sql = id.setRefIdSQL();
            }
            catch (e)
            {
                console.log(e.message);
            }
            finally
            {
                self.execID(sql);
            }
        }
    }

    self_setID(self)
    {
        var id = new ID();
        id.promptDB();
        if(id.noCancel)
        {
            var sql;
            try
            {
                sql = id.setIdSQL();
            }
            catch (e)
            {
                console.log(e.message);
            }
            finally
            {
                self.execID(sql);
            }
        }
    }

    self_clear(self)
    {
        self.loadIcons.cycle(1);
        self.sqlres.set('innerHTML', '<br>');
        var height = self.initialHeight.concat('px');
        self.container.set(
            ['style', 'height'], height);
        self.container.set(
            ['dataset', 'height'],
            self.initialHeight);
    }

    self_updateHeight(self, result)
    {
        session.pma.currentBox = self.container;
        self.addHeight(result);
    }

    self_insertResult(self, result)
    {
        var p = C.create('p');
        p.set('innerHTML', result);
        self.sqlres.nodes[0].appendChild(p.nodes[0]);
    }

    self_resList(self)
    {
        return Array.from(self.sqlres.nodes[0].children);
    }

    self_lastResult(self)
    {
        var resList = self.resList();
        return resList[resList.length - 1].innerHTML;
    }

    self_resLength(self)
    {
        return self.resList().length;
    }

    self_result(self, result)
    {
        self.updateHeight(result);
        self.insertResult(result);
        return 'success';
    }

    self_sql(self, action)
    {
        self.loadIcons.cycle(2);
        var req = new RequestPromise(
            '/pythonMyAdmin/console/'.concat(action),
            self.result,
            {
                code: cyberpyEncode(
                    self.sqlBox.get('value')
                )
            },
            'POST', 'text/html');
        return req.create();
    }

    self_execSQL(self)
    {
        return self.sql('exec');
    }

    self_fetchSQL(self)
    {
        return self.sql('fetch');
    }
}

class SandBox extends Classic
{
    constructor()
    {
        super([HeightManager]);
        this.init();
    }

    self_init(self)
    {
        self.sandbox = C('#sandbox');
        self.execsandbox = C('#execsandbox');
        self.sandboxres = C('.sandboxres');
        self.container = C.node(
            self.sandboxres
            .get('parentNode'));
        self.initialHeight = self.container
            .get(['dataset', 'height']);
    }

    self_clear(self)
    {
        self.sandboxres.set('innerHTML', '<br>');
        var height = self.initialHeight.concat('px');
        self.container.set(['style', 'height'], height);
        self.container.set(
            ['dataset', 'height'],
            self.initialHeight);
    }

    self_updateHeight(self, result)
    {
        session.pma.currentBox = self.container;
        self.addHeight(result);
    }

    self_insertResult(self, result)
    {
        var p = C.create('p');
        p.set('innerHTML', '-'
            .concat(' ', result));
        self.sandboxres.nodes[0]
            .appendChild(p.nodes[0]);
    }

    self_result(self, result)
    {
        self.updateHeight(result);
        self.insertResult(result);
    }

    self_attempt(self, scriptstr)
    {
        var result;
        try
        {
            result = eval(scriptstr);
        }
        catch(err)
        {
            result = err.message;
        }
        return String(result);
    }

    self_execJS(self)
    {
        var scriptstr = 'function script(){'.concat
        (
            self.sandbox.get('value'),
            '}; script()'
        );
        var att = self.attempt(scriptstr);
        self.result(att);
    }

}

class CMS extends Classic
{
    constructor()
    {
        super();
        MySQL.init().then(this.finddb);
        this.loadIcons = new LoadIcons('#cmsloadbox');
        this.gobtn = C('#cmsgo');
        this.resetbtn = C('#cmsreset');
        this.cmsBox = C('#cmsbox');
        this.cmsTables = C('#cmstables');
        this.btns();
        this.prom = Promise.resolve();
    }

    self_createName(self, name)
    {
        var modelName = prompt(
                name[0].toUpperCase().concat(
                    name.substring(1, name.length),
                    ': ')).replace(///_/g, '-');
        if(modelName[modelName.length - 1] !== '/')
        {
            modelName = modelName.concat('/');
        }
        return cyberpyEncode(modelName);
    }

    self_create(self)
    {
        var name = self.cmsTables.get('value');
        var mdl = new Model(
            self.dbname,
            name,
            self.createName(name));
        self.loadIcons.cycle(4);
        mdl.crud([
            mdl.create,
            Chain.promify(self.reset)
        ]);
    }

    self_delete(self)
    {
        self.pageMdl();
        var chain = new Chain('Chain.delete');
        self.loadIcons.cycle(1);
        chain.extend([
            self.model.delete,
            Chain.promify(self.reset)
        ]);
        chain.exe();
    }

    self_update(self)
    {
        var chain = new Chain('Chain.update');
        chain.extend([
            Chain.promify(self.updating),
            self.updatePage,
            Chain.promify(self.updated)]);
        self.chain(chain.exe);
    }

    self_updatePage(self)
    {
        self.loadIcons.cycle(1);
        var prop = self.props.get('value');
        var val = self.textBox.get('value');
        var isPage = prop.toLowerCase() === 'page';
        var noTrail = val[val.length - 1] !== '/';
        if(isPage && noTrail)
        {
            val = val.concat('/');
        }
        else if(val === '')
        {
            val = 'NULL';
        }
        return self.model.update(prop, val);
    }

    self_updated(self, res)
    {
        var val = self.textBox.get('value');
        if(val.length > 20)
        {
            val = val.substring(0, 20).concat(' ...');
        }
        self.setStatus(
            'Updated property "'.concat(
                self.props.get('value'),
                '" to "', val, '"'));
        res();
    }

    self_updating(self, res)
    {
        self.setStatus('Updating...');
        res();
    }

    self_setStatus(self, html)
    {
        self.status.set(
            'innerHTML',
            html);
        return Promise.resolve();
    }

    self_del(self, node)
    {
        node.get('parentNode')
            .removeChild(
            node.nodes[0]);
    }

    self_val(self)
    {
        return self.model.getVal(
            self.props.get('value'));
    }

    self_addTextBox(self)
    {
        self.textBox = C.create('textarea');
        self.textBox.set('spellcheck', 'false');
        self.textBox.set('id', 'cmstextbox');
        self.textBox.set('value', self.val());
        self.valBox.nodes[0].appendChild(
            self.textBox.nodes[0]);
    }

    self_isSure(self)
    {
        return confirm('Are you sure?');
    }

    self_ifSure(self, func)
    {
        return ()=>{
            if(self.isSure())
            {
                func();
            }
        };
    }

    self_cmsBtn(self, func)
    {
        var btn = C.create('button');
        btn.set('className', 'cmsbtn');
        btn.event('click', self.ifSure(func));
        return btn;
    }

    self_createDelBtn(self)
    {
        self.delBtn = self.cmsBtn(self.delete);
        self.delBtn.set('innerHTML', 'Delete');
    }

    self_createCreateBtn(self)
    {
        self.createBtn = self.cmsBtn(self.create);
        self.createBtn.set('innerHTML', 'Create');
    }

    self_createUpdateBtn(self)
    {
        self.updateBtn = self.cmsBtn(self.update);
        self.updateBtn.set('innerHTML', 'Update');
    }

    self_createPropsBtn(self)
    {
        self.propsBtn = self.cmsBtn(self.loadProps);
        self.propsBtn.set('innerHTML', 'Properties');
    }

    self_createLoadBtn(self)
    {
        self.loadBtn = self.cmsBtn(self.load);
        self.loadBtn.set('innerHTML', 'Load');
    }

    self_createCloneBtn(self)
    {
        self.cloneBtn = self.cmsBtn(self.clone);
        self.cloneBtn.set('innerHTML', 'Clone');
    }

    self_btns(self)
    {
        self.createDelBtn();
        self.createCreateBtn();
        self.createUpdateBtn();
        self.createPropsBtn();
        self.createLoadBtn();
        self.createCloneBtn();
    }

    self_addUpdateBtn(self)
    {
        self.valBox.nodes[0].appendChild(
            self.updateBtn.nodes[0]);
    }

    self_addStatus(self)
    {
        self.status = C.create('p');
        self.valBox.nodes[0].appendChild(
            self.status.nodes[0]);
    }

    self_load(self)
    {
        var isset;
        if (self.valBox)
        {
            isset = self.pageBox.nodes[0]
            .contains(self.valBox.nodes[0]);
        }
        if(isset)
        {
            self.del(self.valBox);
        }
        self.valBox = C.create('div');
        self.valBox.set('id', 'cmsval');
        self.addUpdateBtn();
        self.addStatus();
        self.addTextBox();
        self.pageBox.nodes[0].appendChild(
            self.valBox.nodes[0]);
    }

    self_properties(self)
    {
        self.props = C.create('select');
        self.props.set('className', 'cmslist');
        self.props.event('change', self.load);
    }

    self_page(self)
    {
        return self.sel.get('value');
    }

    self_pageMdl(self)
    {
        self.model = new Model(
            self.dbname,
            self.cmsTables.get('value'),
            self.page());
    }

    self_createProps(self)
    {
        for (var prop in self.model.props)
        {
            self.props.nodes[0].appendChild(
                self.option(prop));
        }
        return Promise.resolve();
    }

    self_addProps(self)
    {
        self.pageBox.set('innerHTML', '');
        self.pageBox.nodes[0].appendChild(
            self.loadBtn.nodes[0]);
        self.pageBox.nodes[0].appendChild(
            self.props.nodes[0]);
        return Promise.resolve();
    }

    self_cloneUpdate(self, mdl, key)
    {
        return function()
        {
            return mdl.update(key,
                self.model.getVal(key));
        };
    }

    self_cloneProps(self, mdl)
    {
        var cycles = 0;
        var last = Promise.resolve();
        for (var key in self.model.props)
        {
            if(key !== 'page')
            {
                last = last.then(
                    self.cloneUpdate(
                    mdl, key));
            }
            cycles++;
        }
        self.loadIcons.cycle(cycles / 3);
        return last;
    }

    self_cloneMdl(self)
    {
        return new Model(
            self.model.dbname,
            self.model.tbname,
            self.createName(
                self.model.tbname
            ));
    }

    self_clone(self)
    {
        self.pageMdl();
        var chain = new Chain('CMS.clone');
        self.loadIcons.cycle(3);
        var mdl = self.cloneMdl();
        chain.extend([
            self.model.read,
            mdl.create,
            ()=>{return self.cloneProps(mdl);},
            Chain.promify(self.reset)
        ]);
        chain.exe();
    }

    self_loadProps(self)
    {
        self.properties();
        self.pageMdl();
        var chain = new Chain();
        self.loadIcons.cycle(3);
        chain.extend([
            self.model.read,
            self.createProps,
            self.addProps
        ]);
        chain.exe();
    }

    self_select(self)
    {
        self.sel = C.create('select');
        self.sel.set('className', 'cmslist');
        self.sel.event('change', self.loadProps);
    }

    static stc_option(val)
    {
        var opt = C.create('option');
        opt.set('className', 'cmsoption');
        opt.set('value', val);
        opt.set('innerHTML', cyberpyDecode(val));
        return opt.nodes[0];
    }

    self_addOptions(self)
    {
        for (var page in self.pages)
        {
            self.sel.nodes[0].appendChild(
                self.option(page)
            );
        }
    }

    self_createPageList(self)
    {
        self.select();
        self.addOptions();
        var box = self.cmsBox.nodes[0];
        box.appendChild(self.createBtn.nodes[0]);
        box.appendChild(self.cloneBtn.nodes[0]);
        box.appendChild(self.delBtn.nodes[0]);
        box.appendChild(self.propsBtn.nodes[0]);
        box.appendChild(self.sel.nodes[0]);
    }

    self_createPageBox(self)
    {
        self.pageBox = C.create('div');
        self.pageBox.set('id', 'pagebox');
        self.cmsBox.nodes[0].appendChild(
            self.pageBox.nodes[0]);
    }

    self_launch(self, res)
    {
        self.pages = MySQL.rep.resources;
        self.cmsBox.set(['style', 'display'], 'block');
        self.createPageList();
        self.gobtn.set(['style', 'display'], 'none');
        self.resetbtn.set(['style', 'display'], 'block');
        self.createPageBox();
        res();
    }

    self_reset(self, res)
    {
        self.cmsBox.set('innerHTML', '');
        self.getPages(res);
    }

    self_chain(self, func)
    {
        self.prom = self.prom.then(func);
    }

    self_finddb(self)
    {
        for(var db in MySQL.rep.resources)
        {
            if(/cyberpy/.test(db))
            {
                self.dbname = db;
            }
        }
    }

    self_getdb(self)
    {
        return MySQL.down(self.dbname);
    }

    self_gettb(self)
    {
        return MySQL.down(self.cmsTables.get('value'));
    }

    self_setHeight(self)
    {
        var box = self.cmsBox.get('parentNode');
        box.dataset.height = '1500';
        box.style.height = '1500px';
    }

    self_getPages(self, res)
    {
        self.setHeight();
        var chain = new Chain('cms.getPages');
        self.loadIcons.cycle(2);
        chain.extend([
            MySQL.init,
            self.getdb,
            self.gettb,
            Chain.promify(self.launch)]);
        if(res)
        {
            chain.append(()=>{
                res();
                return Promise.resolve();
            });
        }
        if(self.dbname)
        {
            self.chain(chain.exe);
        }
    }
}

class PythonMyAdmin extends Classic
{
    constructor()
    {
        super([Accordion]);
        this.http = new XMLHttpRequest();
        if (this.has())
        {
            this.initPMA();
        }
    }

    self_initPMA(self)
    {
        self.console = new Console();
        self.cms = new CMS(self.console.db);
        self.interpreter = new Interpreter();
        self.sandbox = new SandBox();
        self.currentBox = C();
    }

    self_getNextBox(self)
    {
        var index = self.textBoxes.indexOf
        (
            self.currentBox.nodes[0]
        );
        index++;
        self.nextBox = self.textBoxes.getNode(index);
    }

    self_getCurrentBox(self, item)
    {
        if(eval(item.get(['dataset', 'callback'])) === self.create)
        {
            self.currentBox = C.node(item.get('parentNode'));
        }
        else
        {
            var li = item.get('parentNode');
            var ul = li.parentNode;
            self.currentBox = C.node(ul.parentNode);
        }
    }

    self_updateHeight(self)
    {
        var repr = self.nextBox.children()[2];
        var total = 2;
        if (repr)
        {
            total += C.node(repr).children().length;
        }
        var height = 150 * total;
        if(window.innerWidth < 410)
        {
            height *= 1.8;
        }
        self.nextBox.set(
            ['dataset', 'height'],
            height.toString());
    }

    self_addHeight(self, pixels)
    {

        var height = Number(
            self.currentBox.get(
            ['dataset', 'height']));
        if(window.innerWidth < 410)
        {
            pixels *= 1.8;
        }
        height += pixels;
        self.currentBox.set(
            ['dataset', 'height'],
            height.toString());
        self.currentBox.set(
            ['style', 'height'],
            height.toString().concat('px'));
    }

    self_checkResponse(self, html)
    {
        return self.currentBox.get('innerHTML') !== html;
    }

    self_itemType(self, decrement)
    {
        var index = self.textBoxes.indexOf(
            self.currentBox.nodes[0]);
        if(decrement)
        {
            index--;
        }
        var item;
        switch(index)
        {
            case 0:
                item = 'database';
                break;
            case 1:
                item = 'table';
                break;
            case 2:
                item = 'model';
                break;
            case 3:
                item = 'property';
                break;
            case 4:
                item = 'value';
                break;
        }
        return item;
    }

    self_create(self, html)
    {
        if(self.checkResponse(html))
        {
            self.addHeight(150);
            self.currentBox.set('innerHTML', html);
        }
        else
        {
            var itemType = self.itemType();
            alert('Error: Duplicate '.concat(itemType));
        }
    }

    self_read(self, html)
    {
        if(html)
        {
            self.getNextBox();
            self.nextBox.set('innerHTML', html);
            self.updateHeight();
            self.nextBox.get('previousSibling').click();
        }
        else
        {
            var itemType = self.itemType();
            alert('Error: check '.concat
                (itemType, 's in console'));
        }
    }

    self_update(self, html)
    {
        if(self.checkResponse(html))
        {
            self.currentBox.set('innerHTML', html);
        }
        else
        {
            var itemType = self.itemType(true);
            alert('Error: check '.concat
                (itemType, 's in console'));
        }
    }

    self_delete(self, html)
    {
        if(self.checkResponse(html))
        {
            self.addHeight(-150);
            self.currentBox.set('innerHTML', html);
        }
        else
        {
            var itemType = self.itemType();
            alert('Error: Duplicate '.concat(itemType));
        }
    }

    self_itemClick(self, item)
    {
        var node = C.node(item);
        self.getCurrentBox(node);
        self.request
        (
            self.requestData(node)
        );
    }

    self_requestData(self, item)
    {
        var req = {
            'uri': item.get(['dataset', 'uri']),
            'callback': eval(item.get(
                ['dataset', 'callback'])),
            'data': JSON.parse(item.get(
                ['dataset', 'data']))
        };
        if(req.data.action === 'update')
        {
            var uri = req.uri.split('/');
            var parent = uri[uri.length - 3];
            var current = uri[uri.length - 2];
            req.data[parent.toLowerCase()] = current;
            uri.splice(uri.length - 2, 1);
            req.uri = uri.join('/');
        }
        return req;
    }

    self_commandConfirmed(self, vars)
    {
        var confirmed;
        var set = function(condition)
        {
            if(condition)
            {
                confirmed = true;
            }
            else
            {
                confirmed = false;
            }
        };
        switch(vars.callback)
        {
            case(self.delete):
                var okdel = confirm('Confirm "Delete"');
                var repr = self.currentBox.children()[2];
                var items = Array.from(repr.children);
                var candel = items.length > 1;
                set(okdel && candel);
                if(!confirmed)
                {
                    alert('Empty parent not allowed. \
                    Either delete parent, or create a \
                    child before deleting this one.');
                }
                break;
            case(self.update):
                vars.data.new = cyberpyEncode(
                    prompt('Enter New: ')
                    );
                set(vars.data.new);
                break;
            case(self.create):
                var index = self.textBoxes.indexOf(
                    self.currentBox.nodes[0]);
                var isProp = index === 3;
                if (isProp)
                {
                    vars.data.new = prompt
                    (
                        'Enter [col_name,col_type,value]: '
                    );
                }
                else
                {
                    vars.data.new = prompt
                    (
                        'Enter New: '
                    );
                }
                set(vars.data.new);
                if(confirmed && isProp)
                {
                    var commaCheck = (
                    vars.data.new.match(/,/g)
                    || []).length === 2;
                    if(commaCheck)
                    {
                        var data = vars.data.new.split(',');
                        data[0] = data[0].toUpperCase();
                        data[1] = data[1].toUpperCase();
                        vars.data.new = data.join(',');
                    }
                    else
                    {
                        confirmed = false;
                        alert('Invalid. Try again.');
                    }
                }
                break;
            default:
                confirmed = true;
        }
        return confirmed;
    }

    self_noTemplate(self, uri)
    {
        var pathList = uri.split('/');
        var notDuplicate = true;
        for (var i in pathList)
        {
            var reg = new RegExp(
                pathList[i]
                .replace(
                /[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g,
                "\\$&"
                ), 'g');
            if (pathList[i] !== '' &&
                (uri.match(reg) || []).length > 1)
            {
                notDuplicate = false;
            }
        }
        return notDuplicate;
    }

    self_sendRequest(self, vars)
    {
        if (self.commandConfirmed(vars))
        {
            var uri = vars.uri;
            delete vars.uri;
            C.request(
                uri, vars.callback,
                vars.data, 'POST',
                'text/plain');
        }
    }

    self_request(self, vars)
    {
        if(vars.data.action === 'read'
            || self.noTemplate(vars.uri))
        {
            self.sendRequest(vars);
        }
        else
        {
            alert("Error: cannot modify a template's values");
        }
    }
}

class $ extends Classic
{
    constructor()
    {
        super();
        this.pma = new PythonMyAdmin();
        if(/session=ok/.test(document.cookie))
        {
            this.init();
            document.cookie = 'max-age=0';
        }
    }

    self_panic(self)
    {
        for(var key in session)
        {
            delete session[key];
        }
        location.replace(
            '/pythonMyAdmin?logout=true'
            );
    }

    self_check(self, resp)
    {
        var obj = JSON.parse(resp);
        if(obj.query !== 'true')
        {
           self.panic;
        }
    }

    self_init(self)
    {
        var req = new RequestPromise(
            '/api/ok_session',
            self.check);
        self.prom = req.create();
    }
}

export default function main()
{
    session = new $();
    return session;
}

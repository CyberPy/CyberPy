var session;
( async ()=>{
    var main = await import('/pythonmyadmin/min/main.js');
    session = main.default();
})();
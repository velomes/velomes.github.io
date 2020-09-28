/* Init minified.js */
var MINI = require('minified');
var _=MINI._, $=MINI.$, $$=MINI.$$, EE=MINI.EE, HTML=MINI.HTML;


var App = {};


window.onhashchange = function() {
    App.Change();
};


$(function() {
    App.Change();
});


(function(app) {
    'use strict';

    app.Change = function() {
        var stage = "1";
        if (location.hash.length > 0) {
            stage = location.hash.split('#')[1];
        }
        
        $('#image-cont').set('@src', 'timeline_' + stage + '.svg');
        $('.select-btn').set('$', '-selected');
        $('#btn-' + stage).set('$', '+selected');
    };

})(App);

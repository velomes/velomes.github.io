/* Init minified.js */
var MINI = require('minified');
var _=MINI._, $=MINI.$, $$=MINI.$$, EE=MINI.EE, HTML=MINI.HTML;

var App = {};

var compose = 'https://www.reddit.com/message/compose?';

(function(app) {
    'use strict';

    app.Show = function() {
    	var spam = $('#spamlist');
    	spam.fill();

    	var messageTitle = $('#message-title').get('value');
    	var messageContent = $('#message-content').get('value');
    	var users = $('#users').get('value');

    	users = users.split('\n');

    	for (var i=0; i<users.length; i++) {
    		var username = users[i].trim();

    		if (i > 0 && i % 10 === 0) {
    			console.log(i);
    			spam.add(EE('br'));
    		}

    		var to = 'to=' + escape(username);
    		var subject = 'subject=' + escape(messageTitle);
    		var message = 'message=' + escape(messageContent);
    		var href = compose + to + '&' + subject + '&' + message;
    		spam.add(EE('div', [
    				EE('span', (i + 1) + '. '),
    				EE('a', {'href': href, 'target': '_blank'}, username)
    			]));


    	}

    };

})(App);
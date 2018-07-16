/* Init minified.js */
var MINI = require('minified');
var _=MINI._, $=MINI.$, $$=MINI.$$, EE=MINI.EE, HTML=MINI.HTML;

var parser = new DOMParser();

window.onhashchange = function() {
    App.Route();
};


function loadData(uri, callback) {
    $.request('get', uri)
    .then(function(response) {
            console.log('Loaded (' + uri + ')');
            callback(response);
    })
    .error(function(status, statusText, responseText) {
            App.Error('Error[' + status +']: (' + uri + ')');
            callback(null);
    });
}

function getKeyOr(data, key, defaultValue) {
    return key in data ? data[key] : defaultValue;
}

function fixStr(str) {
    return decodeURIComponent(escape(unescape(str)));
}

var App = {
    scoreKeys: ['Stg', 'GC', 'PC', 'KOM', 'Spr', 'Sum', 'Bky', 'Ass'],
    riders: null,
    scores: null,
    league: null,
};


$(function() {
    App.Init();
});


(function(app) {
    'use strict';

    app.Init = function() {
        loadData('scores.json', function(response) {
            app.scores = $.parseJSON(response);
        });
        loadData('riders.json', function(response) {
            app.riders = $.parseJSON(response);
        });
        app.Route();
    };

    app.Route = function() {
    if (location.hash.length > 0) {
        var splitHash = location.hash.split(':');
        switch (splitHash[0]) {
            case '#league':
                app.Loading();
                app.League(splitHash[1]);
                break;
            case '#rider':
                app.Loading();
                app.Ready(function() {
                    app.DisplayRider(fixStr(splitHash[1]));
                });
                break;
            case '#riders':
                app.Loading();
                app.Ready(app.DisplayRiders);
                break;
            default:
                break;
        }
    }
    };

    app.Loading = function() {
        $('#app').fill(EE('div', {$: 'sp-circle'}));
    };

    app.League = function(league) {
        if (league !== null && league['shortname'] == league) {
            app.Ready(app.DisplayLeague);
        }

        loadData('leagues/' + league +'.json', function(response) {
            var err = 'League "' + league + '"" not found.';
            if (response === null) {
                $('#app').fill(EE('div', err));
            } else {
                app.league = $.parseJSON(response);
                app.Ready(app.DisplayLeague);
            }
        });
        

    };

    app.Main = function() {

    };

    app.Error = function(error) {
        console.error(error);
    };

    app.Ready = function(callback) {
        if (app.scores === null || app.riders === null) {
            setTimeout(function() { app.Ready(callback); }, 100);
            return;
        }
        callback();
    };

    app.DisplayLeague = function() {
        console.log('displaying league: ' + app.league['name']);
    };

    app.DisplayRiders = function() {
        app.Ready(app.DisplayRiders);

        console.log('displaying riders');
    };

    app.stageScoreRow = function(stage, scores) {
        var tr = EE('tr');
        tr.add(EE('td', stage));

        return app.riderScores(tr, scores);
    };

    app.riderScoreRow = function(rider, team, scores) {

    };

    app.riderScores = function(tr, scores) {
        var total = 0;
        app.scoreKeys.forEach(function(key) {
            var score = getKeyOr(scores, key, 0);
            total += score;
            tr.add(EE('td', score));
        });

        tr.add(EE('td', {$: 'score-total'}, total));

        return tr;
    };

    app.DisplayRider = function(rider) {
        if (!(rider in app.riders)) {
            app.Error('Unknown rider: ' + rider);
            $('#app').fill(EE('div', {$: 'error'}, 'Unknown rider: ' + rider));
            return;
        }

        $('#app').fill(EE('div', rider));
        var table = EE('table', [EE('thead', EE('tr')), EE('tbody'), EE('tfoot', EE('tr'))]);

        /* header */
        $('thead tr', table).add(EE('th', 'Stage'));
        app.scoreKeys.forEach(function(key) {
            $('thead tr', table).add(EE('th', key));
        });
        $('thead tr', table).add(EE('th', 'Total'));

        /* stages */
        for (var i = 1; i <= 21; i++) {
            var stage = getKeyOr(app.scores['stages'], i, {'riders': {}});
            var stageScores = getKeyOr(stage['riders'], rider, {});
            $('tbody', table).add(app.stageScoreRow('Stage ' + i, stageScores));
        }

        /* final */
        var finalScore = getKeyOr(getKeyOr(app.scores, 'final', {}), rider, {});
         $('tbody', table).add(app.stageScoreRow('Final', finalScore));

        /* totals */
        var totalScore = getKeyOr(app.scores['totals'], rider, {});
        $('tfoot', table).add(app.stageScoreRow('Total', totalScore));

        $('#app').add(table);
    };

})(App);
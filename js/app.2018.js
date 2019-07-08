/* Init minified.js */
var MINI = require('minified');
var _=MINI._, $=MINI.$, $$=MINI.$$, EE=MINI.EE, HTML=MINI.HTML;

var parser = new DOMParser();

var LEAGUE_STEP_LIMIT = 350;

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

function sumKeys(data) {
    var total = 0;
    Object.keys(data).forEach(function(key) {
        total += data[key];
    });
    return total;
}

var App = {
    scoreKeys: ['Stg', 'GC', 'PC', 'KOM', 'Spr', 'Sum', 'Bky', 'Ass'],
    riders: null,
    scores: null,
    league: null,
    home: null,
};


$(function() {
    App.Init();
});


(function(app) {
    'use strict';

    app.Init = function() {
        app.home = $('.intro');
        loadData('scores.2018.json', function(response) {
            app.scores = $.parseJSON(response);
        });
        loadData('riders.2018.json', function(response) {
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
                    app.League(splitHash[1], splitHash.length>2?splitHash[2]:'total');
                    break;
                case '#rider':
                    app.Loading();
                    app.Ready(function() {
                        app.DisplayRider(fixStr(splitHash[1]));
                    });
                    break;
                case '#riders':
                    app.Loading();
                    app.Ready(function() {
                        app.DisplayRiders(splitHash.length>1?splitHash[1]:'total');
                    });
                    break;
                case '#home':
                    app.Home();
                    break;
            }
        } else {
            location.hash = '#home';
        }
    };

    app.Loading = function() {
        $('#app').fill(EE('div', {$: 'sp-circle'}));
    };

    app.Home = function() {
        $('#app').fill(app.home);
    };

    app.League = function(league, stage) {
        if (app.league !== null && app.league['shortname'] == league) {
                app.Ready(function() {
                    app.DisplayLeague(stage);
                });
            return;
        }

        loadData('leagues/2018/' + league +'.json', function(response) {
            if (response === null) {
                var err = 'League "' + league + '" not found.';
                $('#app').fill(EE('div', err));
            } else {
                app.league = $.parseJSON(response);
                app.Ready(function() {
                    app.DisplayLeague(stage);
                });
            }
        });
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

    app.stageButton = function(value, target, selected, counted) {
        return EE('a', {'href': target, $: 'select-btn' + (selected?' selected':'') + (counted?'':' invalid')}, value);
    };

    app.StageToggle = function(hash, stage) {
        var hsh = function(v) {
            return hash + ':' + v;
        };

        var div = EE('div', {$: 'stage-select'});
        div.add(app.stageButton('Total', hsh('total'), stage=='total', true));
        for (var i = 1; i <= 21; i++) {
            div.add(app.stageButton(i, hsh(i), stage==i.toString(), i in app.scores['stages']));
        }
        var f = EE('span', {$: 'select-btn' + (stage=='final'?' selected':'')}, 'F');
        div.add(app.stageButton('F', hsh('final'), stage=='final', 'final' in app.scores['stages']));

        return EE('div', {$: 'middle-list'}, div);
    };

    app.ToggleTeam = function(team, scores, elmnt) {
        if (elmnt.next().length === 0 || !elmnt.next().is('.details')) {
            elmnt.addAfter(app.TeamDetails(team, scores));
        }

        elmnt.set('$', 'hl');
        elmnt.next().set('$', 'hidden');
    };

    app.TeamDetails = function(team, scores) {
        /* table */
        var table = EE('table', {$: 'results middle-list'}, [EE('thead', EE('tr')), EE('tbody')]);

        /* header */
        $('thead tr', table).add(EE('th', 'Name'));
        $('thead tr', table).add(EE('th', 'Team'));
        app.scoreKeys.forEach(function(key) {
            $('thead tr', table).add(EE('th', key));
        });
        $('thead tr', table).add(EE('th', 'Total'));

        team.forEach(function(rider) {
            var tr = app.riderScoreRow(rider, getKeyOr(app.riders, rider, {'team': '-'})['team'], getKeyOr(scores, rider, {}));
            $('tbody', table).add(tr);
        });

        return EE('div', {$: 'details hidden'}, table);
    };

    app.teamDiv = function(position, team, odd) {
        var div = EE('div', {$: 'teams middle-list' + (odd?' odd':'')});
        div.add(EE('div', {$: 'team position'}, position));
        div.add(EE('div', {$: 'team info'}, [
            EE('div', {$: 'name'}, team['name']),
            EE('div', {$: 'owner'}, team['user']),
        ]));
        div.add(EE('div', {$: 'team score'}, team['total']));

        return div;
    };

    app.DisplayLeague = function(stage, from) {
        if (from === undefined) { from = 0; } else { $('.more').remove(); }
        if (from === 0) {
            $('#app').fill([
                EE('div', {$: 'title'}, app.league['name']),
            ]);

            $('#app').add(app.StageToggle('#league:' + app.league['shortname'], stage));
        }

        var scores = stage == 'total' ?
            app.scores['totals'] :
            getKeyOr(app.scores['stages'], stage, {'riders': {}})['riders'];

        /* helpers */
        var total = function(rider) {
            return sumKeys(getKeyOr(scores, rider, {}));
        };
        var sumTeam = function(riders) {
            var sum = 0;
            riders.forEach(function(rider) {
                sum += total(rider);
            });
            return sum;
        };

        /* add totals and sort */
        var teams = app.league['teams'];
        teams.forEach(function(team) {
            team['total'] = sumTeam(team['team']);
        });
        teams.sort(function(a, b) {
            return  a['total'] - b['total'];
        });
        teams.reverse();

        /* list */
        if (from === 0) {
            $('#app').add(EE('div', {'id': 'team-list', $: 'middle-list'}));
        }
        for(var n = from; n < teams.length; n++) {
            if (n >= from + LEAGUE_STEP_LIMIT) {
                var more = EE('div', {$: 'teams more'}, 'Load more...');
                more.onClick(app.DisplayLeague, [stage, n]);
                $('#team-list').add(more);
                break;
            }

            var div = app.teamDiv(n + 1, teams[n], n % 2);
            div.onClick(app.ToggleTeam, [teams[n]['team'], scores, div]);
            $('#team-list').add(div);
        }
    };

    app.riderScores = function(tr, scores) {
        var total = 0;
        app.scoreKeys.forEach(function(key) {
            var score = getKeyOr(scores, key, 0);
            total += score;
            tr.add(EE('td', score>0?score:'-'));
        });

        tr.add(EE('td', {$: 'score-total'}, total));

        return tr;
    };

    app.riderScoreRow = function(rider, team, scores) {
        var tr = EE('tr');
        tr.add(EE('td', {$: 'rider-name'}, EE('a', {'href': '#rider:' + rider}, rider)));
        tr.add(EE('td', {$: 'team-name'}, team));

        return app.riderScores(tr, scores);
    };

    app.DisplayRiders = function(stage) {
        console.log(stage);
        $('#app').fill(EE('div', {$: 'title'}, 'Scores'));

        var scores = stage == 'total' ?
            app.scores['totals'] :
            getKeyOr(app.scores['stages'], stage, {'riders': {}})['riders'];

        $('#app').add(app.StageToggle('#riders', stage));

        /* get riders ordered by scores */
        var sorter = Object.keys(app.riders).map(function(rider) {
            return [rider, sumKeys(getKeyOr(scores, rider, {}))];
        });
        sorter.sort(function(a, b) {
            return a[1] - b[1];
        });
        sorter.reverse();
        sorter = sorter.map(function(pair) { return pair[0]; });

        /* table */
        var table = EE('table', {$: 'middle-list riders-list'}, [EE('thead', EE('tr')), EE('tbody')]);

        /* header */
        $('thead tr', table).add(EE('th', 'Name'));
        $('thead tr', table).add(EE('th', 'Team'));
        app.scoreKeys.forEach(function(key) {
            $('thead tr', table).add(EE('th', key));
        });
        $('thead tr', table).add(EE('th', 'Total'));

        /* list */
        sorter.forEach(function(rider) {
            var tr = app.riderScoreRow(rider, getKeyOr(app.riders, rider, {'team': '-'})['team'], getKeyOr(scores, rider, {}));
            $('tbody', table).add(tr);
        });

        $('#app').add(table);
    };

    app.stageScoreRow = function(stage, scores) {
        var tr = EE('tr');
        tr.add(EE('td', {$: 'stage'}, stage));

        return app.riderScores(tr, scores);
    };

    app.DisplayRider = function(rider) {
        if (!(rider in app.riders)) {
            app.Error('Unknown rider: ' + rider);
            $('#app').fill(EE('div', {$: 'error'}, 'Unknown rider: ' + rider));
            return;
        }

        $('#app').fill(EE('div', {$: 'title'}, rider));
        var table = EE('table', {$: 'middle-list rider-list'}, [EE('thead', EE('tr')), EE('tbody'), EE('tfoot')]);

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
            $('tbody', table).add(app.stageScoreRow(i, stageScores));
        }

        /* final */
        console.log(app.scores['stages']['final']);
        var finalStage = getKeyOr(app.scores['stages'], 'final', {'riders': {}});
        var finalScore = getKeyOr(finalStage['riders'], rider, {});
        $('tbody', table).add(app.stageScoreRow('Final', finalScore));

        /* totals */
        var totalScore = getKeyOr(app.scores['totals'], rider, {});
        $('tfoot', table).add(app.stageScoreRow('Total', totalScore));

        $('#app').add(table);

        $('#app').add(
            EE('div', {$: 'intro'},
                EE('p',
                    EE('a', {'href': '/#riders'}, 'See all riders')
                )
            )
        );
    };

})(App);

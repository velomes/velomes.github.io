/* Init minified.js */
var MINI = require('minified');
var _=MINI._, $=MINI.$, $$=MINI.$$, EE=MINI.EE, HTML=MINI.HTML;


var App = {};


window.onhashchange = function() {
    App.Change();
};

var comments = {
  "21": {
    "race": 1489,
    "results": 614,
    "top": [
      {
        "author": "bjcuk_14",
        "body": "Good result for Bennett, hopefully he can avoid the time cut and make it to Paris",
        "score": 181
      }
    ]
  },
  "20": {
    "race": 4115,
    "results": 2113,
    "top": [
      {
        "author": "ser-seaworth",
        "body": "Don't let the Slovenian Switcharoo and the general hyping of young riders distract you from the fact that at age 35, Richie Porte just rode his best ever result in a Grand Tour; his first podium.",
        "score": 594
      }
    ]
  },
  "19": {
    "race": 1229,
    "results": 397,
    "top": [
      {
        "author": "PeterSagansLaundry",
        "body": "Green jersey update: Bennett followed Sagan to the BORA team bus, then sprinted in front of him to get through the door first.",
        "score": 182
      }
    ]
  },
  "18": {
    "race": 2878,
    "results": 835,
    "top": [
      {
        "author": "well_do_ya_punk",
        "body": "This is probably the most likable Sky/Ineos moment in memory. lol.",
        "score": 254
      }
    ]
  },
  "17": {
    "race": 2990,
    "results": 926,
    "top": [
      {
        "author": "jackendrick",
        "body": "Bahrain following Bora's tried and tested method of teammates destroying themselves for the leader to disappoint",
        "score": 139
      }
    ]
  },
  "16": {
    "race": 1540,
    "results": 367,
    "top": [
      {
        "author": "juleslovesprog",
        "body": "Lanterne Rouge headline: Kamna BAMBOOZLES Carapaz with THERMONUCLEAR attack.",
        "score": 145
      }
    ]
  },
  "15": {
    "race": 2869,
    "results": 1265,
    "top": [
      {
        "author": "SadeasThePantsless",
        "body": "The best climber in the world, Cosnefroy, retains his Polka Dot jersey.",
        "score": 227
      }
    ]
  },
  "14": {
    "race": 1406,
    "results": 567,
    "top": [
      {
        "author": "bomber84e1",
        "body": "Sunweb communism strikes again, if one rider wins, they all have to win",
        "score": 157
      }
    ]
  },
  "13": {
    "race": 1964,
    "results": 963,
    "top": [
      {
        "author": "pabloneruda69",
        "body": "Who knew that the Slovenian National Championship in June was gonna be the real Grand Tour of the season...",
        "score": 198
      }
    ]
  },
  "12": {
    "race": 1358,
    "results": 309,
    "top": [
      {
        "author": "Pups3000",
        "body": "HIRSCHI, ROLLAND - THIS IS THE STAGE r/PELOTON WAS WAITING FOR",
        "score": 161
      }
    ]
  },
  "11": {
    "race": 916,
    "results": 1108,
    "top": [
      {
        "author": "Franticalmond2",
        "body": "LMAO I just saw the slow-mo after the finish and WvA gave Sagan the middle finger.",
        "score": 118
      }
    ]
  },
  "10": {
    "race": 1180,
    "results": 454,
    "top": [
      {
        "author": "GeniuslyMoronic",
        "body": "Mads Pedersen finishing 5th after saving Richie's ass and closing huge gaps in the echelons. <br />Amazing strength he has this Tour.",
        "score": 93
      }
    ]
  },
  "9": {
    "race": 2309,
    "results": 683,
    "top": [
      {
        "author": "cjmpol",
        "body": "Can we just give Hirschi the overall combatively prize now? You could breakaway every day from now until the end of the Tour and not show as much bravery as that. Unbelievable.",
        "score": 273
      }
    ]
  },
  "8": {
    "race": 2818,
    "results": 938,
    "top": [
      {
        "author": "paulindy2000",
        "body": "Friendship ended with Thibaut, Guillaume new best French GC Hope",
        "score": 117
      }
    ]
  },
  "7": {
    "race": 2303,
    "results": 705,
    "top": [
      {
        "author": "RdJNL",
        "body": "Mollema just said Trek didn't expect the echelons. Amateur hour...",
        "score": 126
      }
    ]
  },
  "6": {
    "race": 1640,
    "results": 454,
    "top": [
      {
        "author": "ser-seaworth",
        "body": "Shoutout to the eight dudes in the breakaway for making the stage more interesting <br />Shoutout to Fabio Aru for whatever the hell that was",
        "score": 178
      }
    ]
  },
  "5": {
    "race": 1271,
    "results": 882,
    "top": [
      {
        "author": "BHarrop3079",
        "body": "It's not often you see somebody tear the peleton to shreds on a mountain one day and then win a bunch sprint the following day. <br />Wout Van Aert take a bow",
        "score": 214
      }
    ]
  },
  "4": {
    "race": 1329,
    "results": 641,
    "top": [
      {
        "author": "dexter311",
        "body": "I lived to see the great r/olland breakaway of 2020.",
        "score": 210
      }
    ]
  },
  "3": {
    "race": 1393,
    "results": 410,
    "top": [
      {
        "author": "hauntedlasagna",
        "body": "peter back in green, nature is healing",
        "score": 83
      }
    ]
  },
  "2": {
    "race": 2191,
    "results": 510,
    "top": [
      {
        "author": "slyfox1908",
        "body": "Alaphilippe, like Sagan, has that rare quality of being totally inevitable on some stages but engrossing to watch anyway.",
        "score": 109
      }
    ]
  },
  "1": {
    "race": 2742,
    "results": 698,
    "top": [
      {
        "author": "sulfuratus",
        "body": "Nice of Astana to demonstrate both that the rider-imposed neutralisation wasn't compulsory, but also immediately after that maybe it wasn't such a bad idea.",
        "score": 179
      }
    ]
  }
}

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
        
        $('#summary-race').set('innerHTML', comments[stage]['race']);
        $('#summary-results').set('innerHTML', comments[stage]['results']);
        $('#best-comment').set('innerHTML', comments[stage]['top'][0]['body']);
        $('#best-comment-author').set('innerHTML', '/u/' + comments[stage]['top'][0]['author']);
        $('#image-cont').set('@src', 'timeline_' + stage + '.svg');
        $('.select-btn').set('$', '-selected');
        $('#btn-' + stage).set('$', '+selected');
    };

})(App);

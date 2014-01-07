require.config({
    paths: {
        angular: '../static/components/angular/angular',
        angularRoute: '../static/components/angular-route/angular-route',
        angularMocks: '../static/components/angular-mocks/angular-mocks',
        text: '../static/components/requirejs-text/text'
    },
    shim: {
        'angular': {'exports': 'angular'},
        'angularRoute': ['angular'],
        'angularMocks': {
            deps: ['angular'],
            'exports': 'angular.mock'
        }
    },
    priority: [
        'angular'
    ]
});


/**
 * http://code.angularjs.org/1.2.1/docs/guide/bootstrap#overview_deferred-bootstrap
 * @type {string}
 */
window.name = 'NG_DEFER_BOOTSTRAP!';

require([
    'angular',
    'app',
    'routes'
], function (angular, app, routes) {
    'use strict';
    var $html = angular.element(document.getElementsByTagName('html')[0]);

    angular.element().ready(function () {
        angular.resumeBootstrap([app['name']]);
    });
});

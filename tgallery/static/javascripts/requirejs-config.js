require.config({
    'baseUrl': 'components',
    'paths': {
        'tgallery': 'javascripts',
        'jquery': 'jquery/jquery',
        'lodash': 'lodash/dist/lodash'
    },
    'shim': {
        'backbone': {
            'deps': [
                'lodash',
                'jquery'
            ],
            'exports': 'Backbone'
        }
    },
    'packages': [
        {
            'name': 'lodash',
            'main': 'lodash',
            'location': 'lodash'
        },
        {
            'name': 'backbone',
            'main': 'backbone',
            'location': 'backbone'
        },
        {
            'name': 'bootstrap',
            'main': 'bootstrap',
            'location': 'bootstrap/js'
        }
    ]
});

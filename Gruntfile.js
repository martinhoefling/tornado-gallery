/**
 * @param {Object} grunt
 */
module.exports = function (grunt) {
    grunt.initConfig({
        nose: {
            options: {
                verbose: true,
                virtualenv: 'virtualenv',
                tests: ['tgallery_tests'],
                with_coverage: true,
                cover_package: ['tgallery'],
                cover_erase: true
            },
            main: { }
        },
        pylint: {
            options: {
                rcfile: '.pylintrc',
                virtualenv: 'virtualenv',
            },
            source: {
                src: 'tgallery',
            },
            tests: {
                src: 'tgallery_tests',
            },
        },
        less: {
            development: {
                options: {
                    dumpLineNumbers: 'all',
                    ieCompat: false
                },
                files: {
                    'tgallery/static/stylesheet/style.css': 'tgallery/static/stylesheet/style.less',
                }
            },
        },
        gjslint: {
            options: {
                flags: ['--flagfile .gjslintrc']
            },
            source: {
                src: ['tgallery/static/javascript/**/*.js'],
                options: {
                    reporter: { name: 'console' }
                }
            },
        },
        jshint: {
            source: {
                src: ['tgallery/static/javascript/**/*.js'],
                options: {
                    jshintrc: '.jshintrc'
                }
            },
        },
        concurrent: {
            tasks: ['pylint', 'jshint', 'gjslint', 'less', 'nose'],
        }
    });

    grunt.loadNpmTasks('grunt-nose');
    grunt.loadNpmTasks('grunt-pylint');
    grunt.loadNpmTasks('grunt-gjslint');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-concurrent');

    grunt.registerTask(
        'lint',
        'Lint project',
        ['pylint', 'jshint', 'gjslint']
    );
    grunt.registerTask(
        'test',
        'Test project',
        ['nose']
    );
    grunt.registerTask(
        'default',
        'Do all',
        ['concurrent:tasks']
    );
};

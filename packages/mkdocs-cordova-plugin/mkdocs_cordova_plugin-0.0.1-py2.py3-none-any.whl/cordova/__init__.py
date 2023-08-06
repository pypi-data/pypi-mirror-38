# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os
import logging
import shutil
from mkdocs import utils
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

log = logging.getLogger(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))

class PlatformOption(config_options.OptionallyRequired):
    """ Validate Platform(s) provided in config are supported platforms. """

    def external_dependencies_found(self, platform):
        if platform == 'android':
            if os.system("npm list -g --depth 0 | grep cordova"):
                print("cordova not installed.\nUse `npm install -g cordova`.")
                return False
            for env_var in ['ANDROID_HOME', 'JAVA_HOME']:
                if os.environ.get(env_var) is None:
                    print(env_var + " is not set." + \
                            "\nPlease install Android Studio:" + \
                            "\n\thttps://developer.android.com/studio/")
                    return False
            return True
        else:
            return False

    def run_validation(self, value):
        if isinstance(value, utils.string_types):
            value = [value]
        elif not isinstance(value, (list, tuple)):
            raise config_options.ValidationError('Expected a list of platforms.')
        for platform in value:
            if not self.external_dependencies_found(platform):
                raise config_options.ValidationError(
                        '"{}" is not a supported platform or ' + \
                        'external dependencies have not been met.'.format(platform)
                        )
                return value

class CordovaPlugin(BasePlugin):
    """ Deploy documentation to any mobile device via Apache Cordova. """

    config_scheme = (
            ('platform', PlatformOption(default=['android'])),
    )

    def on_config(self, config, **kwargs):
        "Add plugin templates and scripts to config."
        config['theme'].static_templates.add('head.html')
        path = os.path.join(base_path, 'templates')
        config['theme'].dirs.append(path)
        if 'package.json' not in config['extra_templates']:
            config['extra_templates'].append('package.json')
        if 'config.xml' not in config['extra_templates']:
            config['extra_templates'].append('config.xml')
        if 'js/index.js' not in config['extra_javascript']:
            config['extra_javascript'].append('js/index.js')
        return config

    def on_post_build(self, config, **kwargs):
        "Generate app from site directory."
        project_dir = os.getcwd()
        app_dir = os.path.join(project_dir, 'app')
        www_dir = os.path.join(app_dir, 'www')
        try:
            os.mkdir(app_dir)
            shutil.copytree(config['site_dir'], www_dir)
            os.chdir(app_dir)
            shutil.move(os.path.join(www_dir, 'package.json'), app_dir)
            shutil.move(os.path.join(www_dir, 'config.xml'), app_dir)
            os.remove(os.path.join(www_dir, 'sitemap.xml.gz'))
            for platform in config['extra']['platform']:
                os.system("cordova platform add " + platform)
            os.system("cordova build --no-telemetry")
            shutil.move(os.path.join(app_dir, 'platforms', 'android', 'app', 
			'build', 'outputs', 'apk', 'debug', 'app-debug.apk'),
			app_dir)
            print('Moved to:\n\t' + app_dir + '/app-debug.apk')
        finally:
            os.chdir(project_dir)

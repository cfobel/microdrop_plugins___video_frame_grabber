import re
import os
import sys

import yaml

from git_util import GitUtil
from path import path


def get_plugin_version():
    version = GitUtil(None).describe()
    m = re.search('^v(?P<major>\d+)\.(?P<minor>\d+)(-(?P<micro>\d+))?', version)
    if m.group('micro'):
        micro = m.group('micro')
    else:
        micro = '0'
    version_string = "%s.%s.%s" % (m.group('major'),
            m.group('minor'), micro)
    return version_string


SOFTWARE_VERSION = get_plugin_version()
env = Environment(tools = ["default", "disttar"],
        DISTTAR_EXCLUDEDIRS=['.git'],
        DISTTAR_EXCLUDERES=[r'\.sconsign\.dblite'],
        DISTTAR_EXCLUDEEXTS=['.gz', '.pyc', '.tgz', '.swp'])

plugin_root = path('.').abspath()
properties_target = plugin_root.joinpath('properties.yml')
properties = {'name': str(plugin_root.name), 'version': SOFTWARE_VERSION}
properties_target.write_bytes(yaml.dump(properties))
archive_name = '%s-%s.tar.gz' % (properties['name'], SOFTWARE_VERSION)

# This will build an archive using what ever DISTTAR_FORMAT that is set.
tar = env.DistTar('%s' % properties['name'], [env.Dir('#')])
renamed_tar = env.Command(env.File(archive_name), None,
        Move(archive_name, tar[0]))
Depends(renamed_tar, tar)
Clean(renamed_tar, tar)

if 'PLUGIN_ARCHIVE_DIR' in os.environ:
    target_archive_dir = os.environ['PLUGIN_ARCHIVE_DIR']
    Install(target_archive_dir, renamed_tar)

import json
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from msmexplorer import version

if not version.release:
    print("This is not a release.")
    exit(0)

URL = 'http://www.msmbuilder.org/msmexplorer'
res = urlopen(URL + '/versions.json').read().decode('utf-8')
versions = json.loads(res)

# new release so all the others are now old
for i in range(len(versions)):
    versions[i]['latest'] = False

versions.append({
    'version': version.short_version,
    'url': "{base}/{version}".format(base=URL, version=version.short_version),
    'latest': True})

with open("docs/_deploy/versions.json", 'w') as versionf:
    json.dump(versions, versionf)


import json

version_json = '''
{"date": "2018-11-03T21:25:18.662639", "dirty": false, "error": null, "full-revisionid": "5ebdd893d622f68740cae288691747ef5d05a924", "version": "0.17.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)


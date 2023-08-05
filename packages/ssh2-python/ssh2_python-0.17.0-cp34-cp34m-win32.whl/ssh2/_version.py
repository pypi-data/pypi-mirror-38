
import json

version_json = '''
{"version": "0.17.0", "error": null, "full-revisionid": "5ebdd893d622f68740cae288691747ef5d05a924", "date": "2018-11-03T19:59:40.194968", "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)


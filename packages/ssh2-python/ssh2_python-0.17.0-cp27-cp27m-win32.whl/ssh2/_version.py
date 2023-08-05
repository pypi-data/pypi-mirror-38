
import json

version_json = '''
{"date": "2018-11-03T19:55:52.015000", "full-revisionid": "5ebdd893d622f68740cae288691747ef5d05a924", "dirty": false, "version": "0.17.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)


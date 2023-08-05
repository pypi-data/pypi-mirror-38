
import json

version_json = '''
{"dirty": false, "full-revisionid": "5ebdd893d622f68740cae288691747ef5d05a924", "version": "0.17.0", "date": "2018-11-03T20:04:24.672794", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)


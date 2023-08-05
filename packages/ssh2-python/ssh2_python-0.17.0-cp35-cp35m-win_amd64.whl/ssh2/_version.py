
import json

version_json = '''
{"full-revisionid": "5ebdd893d622f68740cae288691747ef5d05a924", "dirty": false, "date": "2018-11-03T20:15:43.156403", "version": "0.17.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)


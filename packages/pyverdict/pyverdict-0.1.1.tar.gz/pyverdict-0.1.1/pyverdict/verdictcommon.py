import json
import pkg_resources
from email import message_from_string

def get_verdictdb_version():
    '''
    Relies on the package metadata. See below for how to read metadata.
    https://stackoverflow.com/questions/10567174/how-can-i-get-the-author-name-project-description-etc-from-a-distribution-objec
    '''
    pkgInfo = pkg_resources.get_distribution('pyverdict').get_metadata('PKG-INFO')
    msg = message_from_string(pkgInfo)
    metadata = json.loads(msg['Description'])
    verdictdb_version = metadata['Internal VerdictDB version']
    return verdictdb_version

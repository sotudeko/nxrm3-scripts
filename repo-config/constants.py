base_url = 'service/rest/v1'

endpoints = {}
endpoints['role'] = 'security/roles'
endpoints['user'] = 'security/users?source=default'
endpoints['priv'] = 'security/privileges'
endpoints['blob'] = 'blobstores'
endpoints['repo'] = 'repositorySettings'
endpoints['contentselector'] = 'security/content-selectors'
blobpath_api = 'blobstores/file'

output_dir = './output'

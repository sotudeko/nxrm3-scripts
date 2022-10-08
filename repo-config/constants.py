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

ootb_blobstore = 'default'
ootb_roles = ['nx-admin', 'nx-anonymous', 'replication-role']
ootb_priv = 'nx-'
ootb_repositories = ['nuget-group', 'nuget.org-proxy', 'nuget-hosted', 'maven-central', 'maven-public', 'maven-releases', 'maven-snapshots']
ootb_users = ['admin', 'anonymous']

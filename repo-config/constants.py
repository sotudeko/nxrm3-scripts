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

privilege_endpoints = {}
privilege_endpoints['application'] = 'security/privileges/application'
privilege_endpoints['repository-content-selector'] = 'security/privileges/repository-content-selector'
privilege_endpoints['repository-view'] = 'security/privileges/repository-view'
privilege_endpoints['repository-admin'] = 'security/privileges/repository-admin'
privilege_endpoints['wildcard'] = "security/privileges/wildcard"
privilege_endpoints['script'] = "security/privileges/script"


import org.sonatype.nexus.blobstore.api.BlobStoreManager
import org.sonatype.nexus.repository.storage.WritePolicy
import org.sonatype.nexus.repository.maven.VersionPolicy
import org.sonatype.nexus.repository.maven.LayoutPolicy

repository.createMavenProxy('proxy1', 'https://www.example.com/', 'default', true, VersionPolicy.RELEASE, LayoutPolicy.PERMISSIVE)

repository.createMavenHosted("private", BlobStoreManager.DEFAULT_BLOBSTORE_NAME, true, VersionPolicy.RELEASE, WritePolicy.ALLOW_ONCE, LayoutPolicy.STRICT)


def creds = [:].withDefault { 0 }
creds.put('type','username')
creds.put('username','admin')
creds.put('password','admin123')

repository.getRepositoryManager().get('proxy1').getConfiguration().getAttributes().'httpclient'.'authentication' = creds

2022-09-19 18:39:00,977+0100 INFO  [quartz-12-thread-20]  *SYSTEM org.sonatype.nexus.repository.manager.internal.RepositoryManagerImpl - 
Creating repository in memory: proxy-one -> OrientConfiguration{
    repositoryName='proxy-one', 
    recipeName='maven2-proxy', 
    attributes={
        httpclient={
            connection={
                blocked=false, 
                autoBlock=true
                }
            }, 
            proxy={
                remoteUrl=https://www.example.com/, 
                contentMaxAge=1440, 
                metadataMaxAge=1440}, 
                negativeCache={
                    enabled=true, 
                    timeToLive=1440
                }, 
                storage={
                    blobStoreName=default, 
                    strictContentTypeValidation=true
                }, 
                maven={
                    versionPolicy=RELEASE, 
                    layoutPolicy=STRICT
                }
            }
        }

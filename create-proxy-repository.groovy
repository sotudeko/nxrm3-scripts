import org.sonatype.nexus.repository.Repository
import org.sonatype.nexus.blobstore.api.BlobStoreManager
import org.sonatype.nexus.repository.maven.VersionPolicy
import org.sonatype.nexus.repository.maven.LayoutPolicy
import groovy.json.JsonSlurper
 
//expects json string with appropriate content to be passed in
def repodetails = new JsonSlurper().parseText(args)

log.info("Create repository")

repository.createMavenProxy(
  repodetails.repositoryName, 
  repodetails.remoteUrl, 
  repodetails.blobStoreName, 
  true, 
  VersionPolicy.RELEASE, 
  LayoutPolicy.PERMISSIVE
)


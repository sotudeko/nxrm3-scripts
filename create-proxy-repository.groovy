import org.sonatype.nexus.repository.Repository
import org.sonatype.nexus.blobstore.api.BlobStoreManager
//import org.sonatype.nexus.repository.storage.WritePolicy
import org.sonatype.nexus.repository.maven.VersionPolicy
import org.sonatype.nexus.repository.maven.LayoutPolicy

log.info("Create repository")
repository.createMavenProxy('my-proxy-repo-3', 'https://www.proxythis-take2.com/', 'default', true, VersionPolicy.RELEASE, LayoutPolicy.PERMISSIVE)


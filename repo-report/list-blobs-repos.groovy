/*
 * Sonatype Nexus (TM) Open Source Version
 * Copyright (c) 2008-present Sonatype, Inc.
 * All rights reserved. Includes the third-party code listed at http://links.sonatype.com/products/nexus/oss/attributions.
 *
 * This program and the accompanying materials are made available under the terms of the Eclipse Public License Version 1.0,
 * which accompanies this distribution and is available at http://www.eclipse.org/legal/epl-v10.html.
 *
 * Sonatype Nexus (TM) Professional Version is available from Sonatype, Inc. "Sonatype" and "Sonatype Nexus" are trademarks
 * of Sonatype, Inc. Apache Maven is a trademark of the Apache Software Foundation. M2eclipse is a trademark of the
 * Eclipse Foundation. All other trademarks are the property of their respective owners.
*/

/*
 * Utility script that scans blobstores and reads the properties files to summarize which repositories
 * are using the blob store, and how much space each is consuming.
 *
 * The script tabulates both the total size, and the size that could be reclaimed by performing a compact blob store
 * task.
 *
 * Script was developed to run as an 'Execute Script' task within Nexus Repository Manager.
 */
import groovy.json.JsonOutput
import java.text.SimpleDateFormat
import org.sonatype.nexus.internal.app.ApplicationDirectoriesImpl

def applicationDirectories = container.lookup(ApplicationDirectoriesImpl.class.name)

//Be default the root blobs directory is in the Nexus work directory
def nexusBlobRootDirectory = new File(applicationDirectories.getWorkDirectory(), 'blobs')

//Default location of results is the Nexus temporary directory
def resultsFileLocation = applicationDirectories.getTemporaryDirectory() as File

def blobStatCollection = [:].withDefault { 0 }

class BlobStatistics
{
  def repositories = [:].withDefault { 0 }

  long totalBlobStoreBytes = 0

  long totalReclaimableBytes = 0

  def collectMetrics(final Properties properties) {
    def repo = properties.'@Bucket.repo-name'
    if (!repositories.containsKey(repo)) {
      addRepo(properties.'@Bucket.repo-name' as String)
    }
    repositories."$repo".totalBytes += (properties.size as long)
    totalBlobStoreBytes += (properties.size as long)

    if (properties.'deleted') {
      repositories."$repo".reclaimableBytes += (properties.size as long)
      totalReclaimableBytes += (properties.size as long)
    }
  }

  def addRepo(final String repoName) {
    repositories.put(repoName, new RepoStatistics())
  }

  class RepoStatistics {
    long totalBytes = 0
    long reclaimableBytes = 0
  }
}

def getScanner(final File baseDirectory) {
  def ant = new AntBuilder()
  def scanner = ant.fileScanner {
    fileset(dir: baseDirectory) {
      include(name: '**/*.properties')
      exclude(name: '**/metadata.properties')
      exclude(name: '**/*metrics.properties')
      exclude(name: '**/tmp')
    }
  }
  return scanner
}

log.info('Starting Blob Storage Summary scan for ' + nexusBlobRootDirectory.getName() + ' directory')

log.info(nexusBlobRootDirectory.toString())

nexusBlobRootDirectory.eachFile { blobStore ->
  log.debug('Collecting storage metrics for ' + blobStore.getName())
  BlobStatistics blobStat = new BlobStatistics()

  getScanner(blobStore).each { propertiesFile ->
    def properties = new Properties()
    propertiesFile.withInputStream { is ->
      properties.load(is)
    }
    blobStat.collectMetrics(properties)
  }
  blobStatCollection.put(blobStore.getName(), blobStat)
}

// new File(resultsFileLocation,
//     "/tmp/repoSizes-${new SimpleDateFormat("yyyyMMdd-HHmmss").format(new Date())}.json").withWriter { Writer writer ->
//   writer << JsonOutput.prettyPrint(JsonOutput.toJson(
//       blobStatCollection.toSorted {a, b -> b.value.totalBlobStoreBytes <=> a.value.totalBlobStoreBytes}))
// }

log.info('Blob Storage Summary scan for ' + nexusBlobRootDirectory.getName() + ' directory has completed')
// https://github.com/sonatype-nexus-community/nexus-scripting-examples/blob/master/complex-script/core.groovy

// https://issues.sonatype.org/browse/NEXUS-30813

// https://javadoc.io/static/org.sonatype.nexus/nexus-core/3.1.0-04/org/sonatype/nexus/CoreApi.html
// httpProxyWithBasicAuth(String host, int port, String username, String password)
// httpsProxyWithBasicAuth(String host, int port, String username, String password)

core.httpProxyWithBasicAuth('basic-webproxy', 9901, 'repomgr1', 'letmethrough1')
core.httpsProxyWithBasicAuth('secure-webproxy', 9902, 'repomgr2', 'letmethrough2')

log.info('Script core completed successfully')



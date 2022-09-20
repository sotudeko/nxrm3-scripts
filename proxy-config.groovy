// https://github.com/sonatype-nexus-community/nexus-scripting-examples/blob/master/complex-script/core.groovy

// https://issues.sonatype.org/browse/NEXUS-30813

// https://javadoc.io/static/org.sonatype.nexus/nexus-core/3.1.0-04/org/sonatype/nexus/CoreApi.html
// httpProxyWithBasicAuth(String host, int port, String username, String password)
// httpsProxyWithBasicAuth(String host, int port, String username, String password)

core.httpProxyWithBasicAuth('basic-http-proxy', 7771, 'buser', 'buserletmethrough1')
core.httpsProxyWithBasicAuth('secure-https-proxy', 7772, 'suser', 'suserletmethrough2')

log.info('Script core completed successfully')



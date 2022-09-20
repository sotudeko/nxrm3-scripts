import groovy.json.JsonSlurper

//expects json string with appropriate content to be passed in
def details = new JsonSlurper().parseText(args)

log.info("Basic http proxy - Running config http proxy")

core.httpProxyWithBasicAuth(details.host, details.port, details.username, details.password)

log.info('Script core completed successfully')



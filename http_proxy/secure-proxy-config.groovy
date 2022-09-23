import groovy.json.JsonSlurper

//expects json string with appropriate content to be passed in
def details = new JsonSlurper().parseText(args)

log.info("Secure https proxy - Running config https proxy")

core.httpsProxyWithBasicAuth(details.host, details.port, details.username, details.password)

log.info('Script core completed successfully')



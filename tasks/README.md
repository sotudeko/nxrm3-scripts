# nxrm3-scripts


## Create export and import tasks

### Add the script to NXRM3
sh 1_add_ei_script.sh host username password

### Create an export task
2_create_ei_task.sh export maven-releases target-dir-root host username password

### Create an import task
2_create_ei_task.sh import maven-releases source-dir-root host username password


# References

- [Nexus 3 Groovy Script development environment setup](https://support.sonatype.com/hc/en-us/articles/115015812727)






import groovy.json.JsonSlurper
import org.sonatype.nexus.scheduling.TaskConfiguration
import org.sonatype.nexus.scheduling.TaskInfo
import org.sonatype.nexus.scheduling.TaskScheduler
import org.sonatype.nexus.scheduling.schedule.Monthly
import org.sonatype.nexus.scheduling.schedule.Schedule
import org.sonatype.nexus.scheduling.schedule.Weekly
import java.text.SimpleDateFormat

parsed_args = new JsonSlurper().parseText(args)

TaskScheduler taskScheduler = container.lookup(TaskScheduler.class.getName())

TaskInfo existingTask = taskScheduler.listsTasks().find { TaskInfo taskInfo ->
    taskInfo.name == parsed_args.name
}

if (existingTask && existingTask.getCurrentState().getRunState() != null) {
    log.info("Could not update currently running task : " + parsed_args.name)
    return
}

TaskConfiguration taskConfiguration = taskScheduler.createTaskConfigurationInstance(parsed_args.typeId)

if (existingTask) {
    taskConfiguration.setId(existingTask.getId())
}

taskConfiguration.setName(parsed_args.name)

taskConfiguration.setAlertEmail(parsed_args.get('task_alert_email', '') as String)

taskConfiguration.setEnabled(Boolean.valueOf(parsed_args.get('enabled', 'true') as String))

// parsed_args.taskProperties.each { key, value ->
//     taskConfiguration.setString(key, value)
// }

// parsed_args.booleanTaskProperties.each { key, value ->
//     taskConfiguration.setBoolean(key, Boolean.valueOf(value))
// }

schedule = taskScheduler.scheduleFactory.manual()

taskScheduler.scheduleTask(taskConfiguration, schedule)





from com.icrossing.floatdotcom.FloatDotComDetails import FloatDotCom
from com.icrossing.mondaydotcom.MondayDotComDetails import MondayDotCom
import time
def starFloatToMonday(event,context):
    print('Starting application ............')
    mondayDotCom = MondayDotCom()
    boards_details = mondayDotCom.fetchMondayDotComDetsils()

    floatDotCom = FloatDotCom()
    projects = floatDotCom.getAllProjects()
    monday_task_owner_details = mondayDotCom.getTask_ownerDeatilsByName(boards_details)

    for p in projects:
        print('project Name', p['name'])
        mondayDotComDashBoard = mondayDotCom.getMondayDotComDashBoardByName(p['name'],boards_details)
        # dashBaordItem = mondayDotCom.getMondayDotComDashBaordItemByBoardIdAndItemName(mondayDotComDashBoard['id'])
        if mondayDotComDashBoard is not None:
            tasks = floatDotCom.getTaskByProject(p['project_id'])
            for task in tasks:
                print('task', task)
                task_start_date = task['start_date']
                task_end_date = task['end_date']
                task_hours_per_day = task['hours']
                task_name = task['name']
                task_notes = task['notes']
                task_people_id = task['people_id']
                task_people_name = [
                    floatDotCom.getPersonById(task_people_id)['name']] if task_people_id is not None else []
                task_people_ids = task['people_ids']
                task_peoples_name = []  # TODO Check for multiple people names
                for each_people_id in task_people_ids or []:
                    task_peoples_name.append(floatDotCom.getPersonById(each_people_id)['name'])

                item_start_date = None
                item_end_date = None
                timeRange_id=None
                item_hours_per_day = None
                item_hours_per_day_id=None
                item_name = None
                item_notes = None
                item_notes_id=None
                item_people_name = None
                item_Task_owner_name = None
                item_status = None
                item_integration_status = None
                item_integration_status_id = None

                dashBoardItem = mondayDotCom.getMondayDotComDashBoardItemByBoardIdAndItemName(
                    mondayDotComDashBoard['id'], task['name'],boards_details)
                # print('dashBaordItem+++',dashBoardItem)
                for item_column_values in dashBoardItem['column_values']:
                    # print(item_column_values)
                    if item_column_values['title'] == 'Task Owner':
                        # item_peoples_name=item_column_values['text']
                        splitter = ', '
                        item_Task_owner_name = item_column_values['text'].split(splitter) if splitter in \
                                                                                          item_column_values[
                                                                                              'text'] else [
                            item_column_values['text']]
                        item_Task_owner_id=item_column_values['id']
                        # item_peoples_id=eval(item_column_values['value'])['personsAndTeams']
                        # item_peoples_name_id={item_peoples_name[i]: item_peoples_id[i] for i in range(len(item_peoples_name))}
                    if item_column_values['id'] == 'status':
                        item_status = item_column_values['text']

                    if item_column_values['title'] == 'Timeline':
                        timeRange = item_column_values['value']
                        item_start_date = eval(timeRange)['from']
                        item_end_date = eval(timeRange)['to']
                        timeRange_id=item_column_values['id']

                    if item_column_values['title'] == 'Notes':
                        item_notes = item_column_values['text']
                        item_notes_id=item_column_values['id']

                    # if item_column_values['id']=='numbers':
                    #    item_hours_per_day=int(item_column_values['text'])

                    if item_column_values['id'] == 'button':
                        pass
                    if item_column_values['title'] == 'Integration Status':
                        item_integration_status = item_column_values['text']
                        item_integration_status_id = item_column_values['id']

                    if item_column_values['title'] == 'Hours per Day':
                        item_hours_per_day = float(item_column_values['text'])
                        item_hours_per_day_id=item_column_values['id']

                # Find change item in monday dot com
                if bool((task_people_name if len(
                        task_people_name) != 0 else task_peoples_name) != item_Task_owner_name) or task_start_date != item_start_date or task_end_date != item_end_date or task_hours_per_day != item_hours_per_day or task_notes != item_notes:
                    print('task Name', dashBoardItem['name'], 'has some changes in Float dot com task details',
                          dashBoardItem)
                    # print('peoples_name++++', task_peoples_name,'++++',monday_task_owner_details)
                    personsAndTeams = [monday_task_owner_details[x] for x in
                                       (task_peoples_name if len(task_peoples_name) != 0 else task_people_name) if
                                       x in monday_task_owner_details]
                    # mondayDotCom.updateMondayDotcomItemColumn(mondayDotComDashBoard['id'], dashBoardItem['id'], 'person',{"personsAndTeams":[{"id":17824317,"kind":"person"},{"id":17844822,"kind":"person"}]})
                    mondayDotCom.updateMondayDotcomItemColumn(mondayDotComDashBoard['id'], dashBoardItem['id'],
                                                              item_Task_owner_id, {"personsAndTeams": personsAndTeams})
                    mondayDotCom.updateMondayDotcomItemColumn(mondayDotComDashBoard['id'], dashBoardItem['id'],
                                                              timeRange_id,
                                                              {"from": task_start_date, "to": task_end_date})
                    mondayDotCom.updateMondayDotcomItemColumn(mondayDotComDashBoard['id'], dashBoardItem['id'], item_notes_id,
                                                              task_notes)
                    # mondayDotCom.updateMondayDotcomItemColumn(mondayDotComDashBoard['id'], dashBoardItem['id'], 'date', {'date':task_end_date})
                    mondayDotCom.updateMondayDotcomItemColumn(mondayDotComDashBoard['id'], dashBoardItem['id'],
                                                              item_hours_per_day_id, task_hours_per_day)

                    time.sleep(10)
                    mondayDotCom.updateMondayDotcomItemColumn(mondayDotComDashBoard['id'], dashBoardItem['id'],
                                                              item_integration_status_id, {"label": "UpdatedfromFloat"})
                    print('Updated MondayDotcom item name', dashBoardItem['name'])








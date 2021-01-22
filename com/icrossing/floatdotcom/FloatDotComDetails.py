#!/usr/bin/env python3

import os
from datetime import date
from datetime import timedelta

# Import the API
from float_api import FloatAPI

# Get access token from environment variable
FLOAT_ACCESS_TOKEN ='3902a174fc4f2eabsj+OAjz/Gy9Ww6WGHWV0xVZFYFmd0VKDNpAqlKk2Ya0='

# Create an API object
api = FloatAPI(FLOAT_ACCESS_TOKEN, 'my_api_demo', 'me@example.org')


# Today
start_date_float = date.today().isoformat()

# 30 days in the future
end_date_float = (date.today() + timedelta(days=30)).isoformat()

class FloatDotCom:
  "This is a FloatDotCom class"
  def createProject(self,projectName):
    return api.create_project(name=projectName)

  def getAllProjects(self):
      return api.get_all_projects()

  def getAllTask(self):
    return api.get_all_tasks()

  def deleteTask(self,task_id):
      return api.delete_task(task_id)

  def deleteProject(self,project_id):
      return api.delete_project(project_id)

  def updateTaskNotes(self,taskId,notes):
      return api.update_task(task_id = taskId,notes = notes)

  def getPersonById(self,people_id):
      return api.get_person(people_id)


  def creatTaskForProject(self,project_id, hours, assignee, task_name,start_date,end_date,notes):
    try:
        person = api.create_person(name=assignee)
        # Create a test task
        task = api.create_task(project_id=project_id,
                               start_date=start_date,
                               end_date=end_date,
                               hours=hours,
                               people_id=person['people_id'],
                               name=task_name
                               )
        self.updateTaskNotes(task['task_id'],notes)
        print('task created')
        return task
    except Exception as ex:
        print('ERROR',ex)
        r = api.delete_person(person['people_id'])
        print('ERROR','Creating task for the Project deleting person created',r)


  def getProject(self,name):
      f = set(['name', 'project_id'])
      projects = api.get_all_projects(fields=','.join(f))
      for p in projects:
          if p['name']==name:
              return p;


  def getTaskByProject(self,project_id):
      project=api.get_project(project_id)
      tasks = api.get_all_tasks()
      project_and_task = []
      for t in tasks:
        if project['project_id'] == t['project_id']:
           project_and_task.append(t)
      return project_and_task





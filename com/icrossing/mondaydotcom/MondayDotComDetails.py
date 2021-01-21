import requests
import json
from com.icrossing.floatdotcom.FloatDotComDetails import FloatDotCom
from datetime import date
from datetime import timedelta
from monday import MondayClient

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjk0Mzk1MTU1LCJ1aWQiOjE3ODI0MzE3LCJpYWQiOiIyMDIwLTEyLTI5VDAzOjE4OjI3LjAwMFoiLCJwZXIiOiJtZTp3cml0ZSIsImFjdGlkIjo3ODE1NzM5LCJyZ24iOiJ1c2UxIn0.cN8GBBYH4tJupyyzI5DFWsKbsnB84WxAmdiIxEyN9Cg"
monday = MondayClient(apiKey)


# print('updatwd item 3',monday.items.change_item_value('915436835', '915446079', 'status_13',  {"label":"Updated by Float"}))
class MondayDotCom:
    # query = '{boards  { name id  items { name id column_values{title id type text } } } }'
    def getMondayDotComDashBoard(self):
        return monday.boards.fetch_boards()

    def getMondayDotComDashBoardItem(self, board_id):
        dashBoardItems = monday.boards.fetch_items_by_board_id(board_id)
        for board in dashBoardItems['data']['boards']:
            return board['items']

    def getMondayDotComDashBoardItemByBoardIdAndItemName(self, board_id, item_name):
        items = self.getMondayDotComDashBoardItem(board_id)
        for item in items:
            # print('item',item)
            if item['name'] == item_name:
                return item

    def getMondayDotComDashBoardByName(self, board_name):
        mondayDashBoards = self.getMondayDotComDashBoard()
        for dashBoard in mondayDashBoards['data']['boards']:
            if dashBoard['name'] == board_name:
                return dashBoard

    def updateMondayDotcomItemColumn(self, board_id, item_id, column_id, column_value):
        # print('board_id',board_id,'item_id',item_id,'column_id ',column_id,'column_value ',column_value)
        r = monday.items.change_item_value(board_id, item_id, column_id, column_value)
        print(f'Updated board_id {board_id} item_id {item_id} column_id {column_id} column_value {column_value}')

    def updateMondayDotComDashBoardItemColumn(self):
        pass

    def getAssigneeDeatilsByName(self):
        item_peoples_name_id = {}
        boards_details=monday.boards.fetch_boards()
        #print('boards+++',boards_details)
        if boards_details is not None:
            boards=boards_details['data']['boards']
        for each_board in boards:
            mon_items = self.getMondayDotComDashBoardItem(each_board['id'])
            for each_mon_item in mon_items:
                for each_column_values in each_mon_item['column_values']:
                    if each_column_values['id'] == 'person':
                        splitter = ', '
                        item_peoples_name = each_column_values['text'].split(splitter) if splitter in each_column_values[
                            'text'] else [each_column_values['text']]
                        item_peoples_id = eval(each_column_values['value'])['personsAndTeams']
                        item_peoples_name_id.update(
                            {item_peoples_name[i]: item_peoples_id[i] for i in range(len(item_peoples_name))})
            # print('users++++',item_peoples_name_id)
        return item_peoples_name_id

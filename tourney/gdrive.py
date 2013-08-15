import gdata.spreadsheet.service

google_id = 'phoenix@dartoo.com'
password = '3355dartoO'

class Sheet():
    def __init__(__, book_name, sheet_name):
        __.book_name = book_name
        __.sheet_name = sheet_name

        __.client = gdata.spreadsheet.service.SpreadsheetsService()
        __.client.email = google_id
        __.client.password = password
        __.client.ProgrammaticLogin()

        __.workbooks = __.client.GetSpreadsheetsFeed()
        __.workbook = dict(map(lambda e: (e.title.text, e.id.text.rsplit('/', 1)[1]), __.workbooks.entry))
        __.key = __.workbook[ book_name ]

        __.sheets = __.client.GetWorksheetsFeed( __.key )
        __.sheet = dict(map(lambda e: (e.title.text, e.id.text.rsplit('/', 1)[1]), __.sheets.entry))
        __.sheet_id = __.sheet[ sheet_name ]

        __.listfeed = __.client.GetListFeed( __.key, __.sheet_id )

    def insert(__, row_data={}):
        __.client.InsertRow( row_data=row_data, key=__.key, wksht_id=__.sheet_id)

    def delete(__, row=0):
        __.client.DeleteRow( __.listfeed.entry[ row ])

    def delete_all(__):
        map( lambda x: __.delete( x ), range(len(__.listfeed.entry) - 1, -1, -1))

    def update(__, row=0, row_data={}):
        __.client.UpdateRow( __.listfeed.entry[ row ], row_data)

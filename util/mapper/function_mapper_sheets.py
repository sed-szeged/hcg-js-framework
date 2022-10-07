from util.sheets import Sheets, SheetException


def sheet_repos_data():
    try:
        global sheets
        sheets = Sheets('keys.json', '1eS2sJBlqjJbugbETjsD3oTYmMwLaUmJ6Y7VXxluxfVE', 'Mapping', 'Mapping')
    except SheetException as e:
        sheets = None
        print(f"[SHEETS] {e}")

    return sheets.mapping_data()


def sheet_row_format(sheet_data):
    result = [
        sheet_data['tick'], sheet_data['repo'], sheet_data['hash'], sheet_data['testing-framework'],
        sheet_data['completed'], sheet_data['time'], sheet_data['SCG'], sheet_data['DCG'], sheet_data['SM'],
        sheet_data['DM'], sheet_data['Map'], sheet_data['Generated'], sheet_data['Note']
    ]
    return result


def update_note(sheet_data, note):
    sheet_data['Note'] = note


def push_to_sheets(sheet_data, map_coverage, current_date):
    sheet_data['Map'] = map_coverage
    sheet_data['Generated'] = current_date
    sheets.push([sheet_row_format(sheet_data)], sheet_data['line'])

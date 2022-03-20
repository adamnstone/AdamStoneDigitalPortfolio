import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import date, timedelta
from zoho_sheets_api import Zoho

def get_column_title_at_certain_row(column_header, row, data):
    head = None
    for header in data[row - 1]:
        if header.strip().lower() == column_header.strip().lower():
            head = header
    if row != 0:
        return data[row - 1][head]
    else:
        return head

def get_todays_column(data, date_header="Date", use_zoho=True):
    if use_zoho:
        zoho = Zoho()
        found_today = False
        i = 0
        dates = zoho.get_dates()
        while not found_today:
            date_string = dates[i]["content"]
            yesterday_date_spl = [str(int(x)) for x in str(date.today() - timedelta(days = 1)).split("-")]
            year = yesterday_date_spl[0]
            month = yesterday_date_spl[1]
            day = yesterday_date_spl[2]
            formatted_yesterday_date_full_year = f"{month}/{day}/{year}"
            formatted_yesterday_date_last_two_digits_year = f"{month}/{day}/{year[2:]}"
            if date_string.strip() == formatted_yesterday_date_full_year or date_string.strip() == formatted_yesterday_date_last_two_digits_year:
                found_today = True
                continue
            i += 1
        yesterdays_index = i + 1
        print("Yesterday's Row: " + str(yesterdays_index))
        row = []
        row_values = zoho.get_row(yesterdays_index)
        filled_columns = []
        for r in row_values:
            filled_columns.append(int(r["column_index"]) - 1)
        for title in zoho.get_headers():
            if int(title["column_index"] - 1) in filled_columns:
                row.append({title["content"]: row_values[filled_columns.index(int(title["column_index"]) - 1)]["content"]})
        return row, yesterdays_index
    else:
        found_today = False
        i = 0
        while not found_today:
            date_string = get_column_title_at_certain_row(date_header, i, data)
            yesterday_date_spl = [str(int(x)) for x in str(date.today() - timedelta(days = 1)).split("-")]
            year = yesterday_date_spl[0]
            month = yesterday_date_spl[1]
            day = yesterday_date_spl[2]
            formatted_yesterday_date_full_year = f"{month}/{day}/{year}"
            formatted_yesterday_date_last_two_digits_year = f"{month}/{day}/{year[2:]}"
            if date_string.strip() == formatted_yesterday_date_full_year or date_string.strip() == formatted_yesterday_date_last_two_digits_year:
                found_today = True
                continue
            i += 1
        yesterdays_index = i - 1
        print("Yesterday's Row: " + str(yesterdays_index))
        row = data[yesterdays_index]
        print(row)
        return row, yesterdays_index

def write_data_to_sheet(places_to_put, things_to_put, use_zoho=True):
    if use_zoho:
        row, yesterdays_row = get_todays_column(None, use_zoho=True)
        zoho = Zoho()
        header_row = zoho.get_headers()
        for x in range(len(places_to_put)):
            place = places_to_put[x]
            for i in range(len(header_row)):
                dict = header_row[i]
                if dict["content"] == place:
                    print(f"Writing {things_to_put[x]} to Zoho Sheet at {i+1}, {yesterdays_row}!")
                    zoho.set_value(i+1, yesterdays_row, things_to_put[x] if things_to_put[x] is not None else "0")
        print("Data Written Successfully")
    else:
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

        client = gspread.authorize(creds)

        sheet = client.open("Weekly performance by day").worksheet("Daily")

        data = sheet.get_all_records()

        row, row_index = get_todays_column(data, use_zoho=use_zoho)
        titles_list = []
        for title in row:
            titles_list.append(title.strip().lower())

        for i in range(len(places_to_put)):
            place_to_put = places_to_put[i]
            thing_to_put = things_to_put[i]
            r = row_index + 2
            c = titles_list.index(place_to_put.strip().lower()) + 1
            print(f"Writing to Spreadsheet; Row: {r}, Column: {c}, Putting: {thing_to_put}")
            sheet.update_cell(r, c, thing_to_put)


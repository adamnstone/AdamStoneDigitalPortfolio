import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import date, timedelta

zoho_client_id = "1000.K1JFHHKEHJNKA98U9PDUKVCHLSGMKT"
zoho_client_secret = "d0d7bc1edf36783e52d05c8c1290121ab06dcba9c4"

def get_column_title_at_certain_row(column_header, row, data, zoho=True):
    if zoho:
        pass
    else:
        head = None
        for header in data[row - 1]:
            if header.strip().lower() == column_header.strip().lower():
                head = header
        if row != 0:
            return data[row - 1][head]
        else:
            return head

def get_todays_column(data, date_header="Date", zoho=True):
    if zoho:
        pass
    else:
        found_today = False
        i = 0
        while not found_today:
            date_string = get_column_title_at_certain_row(date_header, i, data, zoho=zoho)
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
        return row, yesterdays_index

def write_data_to_sheet(places_to_put, things_to_put, zoho=True):
    if zoho:
        pass
    else:
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

        client = gspread.authorize(creds)

        sheet = client.open("Weekly performance by day").worksheet("Daily")

        data = sheet.get_all_records()

        row, row_index = get_todays_column(data, zoho=zoho)
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

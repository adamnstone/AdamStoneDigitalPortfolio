send_email = True
run_periodically = True
use_zoho = False

# imports
import send_mail, read_inbox, write_to_sheet, time
from bs4 import BeautifulSoup
from datetime import date, timedelta
import datetime as dt

data_email = "data@charlottelaundry.com"
data_email_password = "Adamstone00@"
email_host = 'mail.charlottelaundry.com'

# months list used for finding email with correct subject
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def get_data_from_store(all_data, store_name, metric_name):
    for store in all_data:
        if store["Store"] == store_name:
            return store[metric_name]
    raise Exception(f"Metric {metric_name} from Store {store_name} not Found")

def put_data_in_spreadsheet(data_list):
    places_to_put = ["Washer", "Dryer", "Retail 5609", "Retail 3001", "Retail 5935"]
    store_names = ["Washland", "Washland", "5609 South", "Sunrise", "5935 South"]
    metric_names = ["Washers", "Dryers", "Net Sales", "Net Sales", "Net Sales"]
    if len(store_names) != len(metric_names):
        raise Exception("List Store Names Not Same Length As List Metric Names:", store_names, metric_names)
    things_to_put = [get_data_from_store(data_list, store_names[i], metric_names[i]) for i in range(len(store_names))]
    write_to_sheet.write_data_to_sheet(places_to_put, things_to_put, zoho=use_zoho)
    print("Data Written to Spreadsheet Successfully!")

# this function is used for finding the store in the subject of an email; for example, [Sunrise]
def get_first_word_in_brackets(s):
    # string to return
    s_to_return = ""
    # boolean that keeps track of whether the opening square bracket has been found
    first_found = False
    # for every char in string
    for c in s:
        # if the char is a [
        if c == "[":
            # set the boolean first_found to True
            first_found = True
        # otherwise, if it is a ]
        elif c == "]":
            # return the string that keeps track of the store name
            return s_to_return
        # otherwise, if the [ has been seen
        elif first_found:
            # add the current char to the string to return
            s_to_return += c


def subject_matches_date(subject, previous_day = True, amount_before = 0):
    date_string = str(date.today() - timedelta(days = 1 + amount_before))
    date_string_list = [str(int(x)) for x in date_string.split("-")]
    if f"{date_string_list[1]}-{str(int(date_string_list[2]))}-{date_string_list[0]}" in subject:
        return True
    date_string_list[1] = months[int(date_string_list[1]) - 1]
    if previous_day:
        date_string_list[2] = str(int(date_string_list[2]))
    return f"{date_string_list[1]} {date_string_list[2]}, {date_string_list[0]}" in subject

headers_email = ["Store", "Gross Sales1", "Net Sales", "Top-Selling Category", "Top-Selling Category Sales"]
headers_attachment = ["Store", "Washers", "Dryers", "Total"]

def get_data_from_email(email):

    soup = BeautifulSoup(email["html_body"], "html.parser")

    tables = soup.find_all("table", { "class" : "column" })

    data = {}

    data["Store"] = get_first_word_in_brackets(email["subject"])

    for table in tables:
        tds = table.find_all("td")
        td_texts = [x.text.strip() for x in tds]
        for i in range(0, len(td_texts)):
            text = td_texts[i]
            if text.strip():
                if text in headers_email:
                    data[text] = td_texts[i + 1]

        trs = table.find_all("tr")
        for i in range(0, len(trs)):
            tr = trs[i]
            if tr in headers_email:
                data[tr] = trs[i + 1].text

    return data


def format_data(data):
        s = None
        try:
            s = ""
            for header in headers_email:
                s += f"{header}: {data[header]}\n"
        except:
            s = ""
            for header in headers_attachment:
                s += f"{header}: {data[header]}\n"
        return s

def get_signature():
    return "This is brought to you by Adam Stone Analytical Services"

def format_all_data(all_data):
    formatted_strings = [format_data(x) for x in all_data]
    s = ""
    for formatted in formatted_strings:
        s += "-" * 10
        s += "\n"
        s += formatted
    s += "-" * 10
    s += "\n\n\n"
    s += get_signature()
    return s

def get_data_from_attachment_string(attachment):
    to_return = {}
    spl = attachment.split()
    has_seen_list = [False for x in range(0, len(headers_attachment))]
    for i in range(0, len(spl)):
        def get_info(flag, key, add):
            if spl[i] == flag:
                ind = headers_attachment.index(key)
                if not has_seen_list[ind]:
                    has_seen_list[ind] = True
                    to_return[key] = spl[i + add]
        get_info("Location", "Store", 2)
        get_info("Washers", "Washers", 4)
        get_info("Dryers", "Dryers", 1)
    to_return["Total"] = f"${str(float(to_return['Washers'][1:]) + float(to_return['Dryers'][1:]))}"
    return to_return

def main_func():
    try:
        # print the date
        print("DATE: " + str(date.today()))
        # get yesterday's date
        yesterday = date.today() - timedelta(days = 1)
        # convert yesterday's date to a string
        date_string = str(yesterday)
        # create the subject of the email that will be sent with the collected data
        final_email_subject = f"Data Collected For {date_string}"
    
        # list that hold all of the data dictionaries from each store/email
        all_data = []
    
        # index
        i = 1
    
        # while the data from 4 emails has not been collected
        while len(all_data) < 4:
            # e is the email dictionary and attachment_data is the data from the attachment of that email if there is any
            e, attachment_data = read_inbox.get_inbox("data@charlottelaundry.com", "Adamstone00@", host="mail.charlottelaundry.com", amount_of_emails_func = lambda x : [x[-i]])
            # e is a list that contains a single element, the email; set e equal to the first item in itself
            e = e[0]
            # logging to console
            print(f"Checking if \"{e['subject']}\" matches date")
            # if the subject matches yesterday's date and it is not an email that has already been sent by this program for today
            if subject_matches_date(e["subject"], amount_before=1):
                break
            elif subject_matches_date(e["subject"]) and e["subject"] != final_email_subject:
                # logging to the console
                print("Matches")
                print(f"Checking if \"{e['subject']}\" includes \"Scheduled report\"")
                # if the subject of e has the string "Scheduled report" (all emails that include this string have their data in an attachment
                if "Scheduled report" in e["subject"]:
                    # logging to the console
                    print("Includes")
                    # append the data from the attachment to the list that contains the data from each email/store
                    if attachment_data != None:
                        all_data.append(get_data_from_attachment_string(attachment_data))
                # otherwise
                else:
                    # logging to the console
                    print("Does not include")
                    # add the data from the html body of this email to the list that contains the data from each email/store
                    all_data.append(get_data_from_email(e))
            # otherwise
            else:
                # logging to the console
                print("Does not match")
            # increment the index of the email
            i += 1
    
        # log all of the data to the console
        print(all_data)
    
        # send the email with all of the data formatted
        if send_email:
            send_mail.send_mail(data_email, data_email_password,
                                    text=format_all_data(all_data),
                                    subject=final_email_subject,
                                    from_email=f"Adam Stone Analytical Services <{data_email}>",
                                    to_emails=["dan@charlottelaundry.com",
                                               "hardik.shah@charlottelaundry.com",
                                               "paul@charlottelaundry.com"],
                                    port=2525,
                                    host=email_host)
            print("Email Sent")
        else:
            print("No Email Sent")
    
        put_data_in_spreadsheet(all_data)
    
        # press enter to exit the program
        print("Exiting...\n\n\n")
    except Exception as error:
        error_string = str(error)
        send_mail.send_mail(data_email, data_email_password,
                            text=f"An Error Occurred:\n\n{error_string}",
                            subject="An Error Occurred",
                            from_email=f"Adam Stone Analytical Services <{data_email}>",
                            to_emails=["dan@charlottelaundry.com",
                                       "hardik.shah@charlottelaundry.com",
                                       "paul@charlottelaundry.com"],
                            port=2525,
                            host=email_host)

def hour_is(hour):
    return int(dt.datetime.now().hour) == hour

def minute_is(minute):
    return int(dt.datetime.now().minute) == minute

# if this file is being run, not imported
def main_autorun():
    if run_periodically:
        print("WAITING FOR 7:00am")
        while not minute_is(0) and not minute_is(60):
            print(f"Checking if current minute {dt.datetime.now().minute} is 0 or 60")
            time.sleep(60)
        while True:
            if hour_is(7):
                main_func()
            time.sleep(3600) # seconds
    else:
        main_func()

if __name__ == "__main__":
    main_autorun()

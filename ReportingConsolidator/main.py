send_email = True
run_periodically = True
use_zoho = True
write_to_spreadsheet = True

# imports
import send_mail, read_inbox, write_to_sheet, time, sys
from bs4 import BeautifulSoup
from datetime import date, timedelta
import datetime as dt

data_email = "data@charlottelaundry.com"
data_email_password = "XXXXXXXXXX"
email_host = 'mail.charlottelaundry.com'

# months list used for finding email with correct subject
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

column_id_values = ["Tran #", "Date", "Card Type", "Amount", "AP Code", "Details"]

extra_seed_live_headers = ["Device", "Serial Number"]

seed_live_csv_file_name = "seed_live_csv.csv"

vending_machine_serial_number_to_name_dict = {"VJ300345030": "Drink Machine",
                                              "VJ300389415": "Sunrise",
                                              "VJ300389365": "Monroe Rd. Laundry - Laundry Products Machine",
                                              "VJ300389359": "Monroe Rd. Laundry - DN 2145",
                                              "VJ300389416": "Missing Machine Name for VJ300389416"}

def get_data_from_store(all_data, store_name, metric_name):
    for store in all_data:
            if store["Store"] == store_name:
                return store[metric_name]
    print(f"Error: Metric {metric_name} from Store {store_name} not Found - Skipping...")

def put_data_in_spreadsheet(data_list):
    places_to_put = ["Washer", "Dryer", "Retail 5609", "Retail 3001", "Retail 5935"]
    store_names = ["Washland", "Washland", "5609 South", "Sunrise", "5935 South"]
    metric_names = ["Washers", "Dryers", "Net Sales", "Net Sales", "Net Sales"]
    if len(store_names) != len(metric_names):
        raise Exception("List Store Names Not Same Length As List Metric Names:", store_names, metric_names)
    things_to_put = [get_data_from_store([x for x in data_list if type(x) != list], store_names[i], metric_names[i]) for i in range(len(store_names))]
    write_to_sheet.write_data_to_sheet(places_to_put, things_to_put, use_zoho=use_zoho)
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


def compile_vending_machine_data(data):
    machines = []
    for vending in data:
        found = False
        for machine_list in machines:
            if machine_list[0]["Device"] == vending["Device"]:
                machine_list.append(vending)
                found = True
                break
        if not found:
            machines.append([vending])

    new_machines = []

    for machine_list in machines:
        new_machines.append({})
        new_machines[-1]["Device"] = machine_list[0]["Device"]
        new_machines[-1]["Card Type"] = ""
        new_machines[-1]["Amount"] = ""
        for machine in machine_list:
            if not machine["Card Type"] in new_machines[-1]["Card Type"]:
                new_machines[-1]["Card Type"] += f"/{machine['Card Type']}" if new_machines[-1]["Card Type"] != "" else f"{machine['Card Type']}"
                new_machines[-1]["Amount"] += "/0" if new_machines[-1]["Amount"] != "" else "0"
            spl = new_machines[-1]["Amount"].split("/")
            spl[new_machines[-1]["Card Type"].split("/").index(machine["Card Type"])] = str(float(spl[new_machines[-1]["Card Type"].split("/").index(machine["Card Type"])]) + float(machine["Amount"][1:] if machine["Amount"][0] == "$" else machine["Amount"]))
            new_machines[-1]["Amount"] = "/".join(spl)

        new_machines[-1]["Amount"] = "/".join([f"${x}" for x in new_machines[-1]["Amount"].split("/")])

    return new_machines



def format_data(data):
    s = None
    try:
        s = ""
        for header in headers_email:
            s += f"{header}: {data[header]}\n"
    except:
        try:
            s = ""
            for header in headers_attachment:
                s += f"{header}: {data[header]}\n"
        except:
            s += "Vending Machine Data:\n\n"
            compiled = compile_vending_machine_data(data)
            for vending in compiled:
                s += f"Device: {vending_machine_serial_number_to_name_dict[vending['Device']]}:\n"
                s += f"\tSerial Number - {vending['Device']};\n"
                for key in vending:
                    if key != "Device":
                        s += f"\t{key} - {vending[key]};\n"
                s += "\n"
    return s

def get_signature():
    return "This is brought to you by Adam Stone Analytical Services"

def format_all_data(all_data):
    for i in range(len(all_data)):
        if type(all_data[i]) == list:
            all_data.append(all_data[i])
            all_data.pop(i)
    # previous just to put vending data at the end of the email
    print(f"ALL DATA: {all_data}")
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

def make_csv(data):
    r_str = ""
    for header in column_id_values + extra_seed_live_headers:
        r_str += header + ("," if header != (column_id_values+extra_seed_live_headers)[-1] else "\n")
    for dict in data:
        for header in column_id_values + extra_seed_live_headers:
            r_str += ((dict[header] if header != "Serial Number" else dict["Device"]) if header != "Device" else vending_machine_serial_number_to_name_dict[dict["Device"]]) + ("," if header != (column_id_values+extra_seed_live_headers)[-1] else "\n")
    with open(seed_live_csv_file_name, "w") as file:
        file.write(r_str)

def get_data_from_seed_live(attachment_data):
    information = []
    # tbody -> tr -> tds with classes column_ids
    device_id = "colId_5"
    column_ids = {"colId_4": column_id_values[0], "colId_8": column_id_values[1], "colId_9": column_id_values[2], "colId_10": column_id_values[3], "colId_11": column_id_values[4], "colId_12": column_id_values[5]}
    soup = BeautifulSoup(attachment_data, "html.parser")
    its = soup.find_all(True, {"class": [device_id, "headerRow"]})
    device_ns = []
    LOOK_DEVICE = "**device**"
    LOOK_HEAD = "**head**"
    looking_for = LOOK_DEVICE
    for tag in its:
        if tag['class'][0] == "headerRow" and tag.text.split()[0] != "Tran":
            print(f"Found non-header with split text {tag.text.split()} skipping...")
            continue
        else:
            if tag['class'][0] == device_id:
                print(tag.text.split())
                if tag.text.split()[0] == "Device:":
                    device_ns.append(tag.text.split()[1])
                    looking_for = LOOK_HEAD
            elif tag['class'][0] == "headerRow":
                if looking_for == LOOK_DEVICE:
                    device_ns.append(device_ns[-1])
                else:
                    looking_for = LOOK_DEVICE
    print(device_ns)
    tbodies = soup.find_all("tbody")
    next_tbody = False
    device_counter = 0
    for tbody in tbodies:
        if not next_tbody:
            for child in tbody.findChildren():
                if child.has_attr('class'):
                    if 'headerRow' in child['class']:
                        next_tbody = True
                        print("Header Row Located\n")
        else:
            next_tbody = False
            tbs = []
            for item_navstring in tbody.children:
                item = str(item_navstring)
                if item.strip() != "":
                    tbs.append(BeautifulSoup(item, "html.parser"))
            for tr in [x.find("tr") for x in tbs]:
                info = {}
                for td in [x.find("td") for x in [(BeautifulSoup(str(x), "html.parser")) for x in tr.children if str(x).strip() != ""]]:
                    info[column_ids[td['class'][0]]] = td.text.strip()
                    info["Device"] = device_ns[device_counter]
                information.append(info)
            device_counter += 1
    make_csv(information)
    return information

def is_seed_live(subject):
    return "SeedLive Generated Report - Sales Activity By Batch" in subject

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

        seen_seed_live = False

        while True:
            try:
                # e is the email dictionary and attachment_data is the data from the attachment of that email if there is any
                e, attachment_data = read_inbox.get_inbox("data@charlottelaundry.com", "Adamstone00@", host="mail.charlottelaundry.com", amount_of_emails_func = lambda x : [x[-i]])                # e is a list that contains a single element, the email; set e equal to the first item in itself
                e = e[0]
                # logging to console
                print(f"Checking if \"{e['subject']}\" matches date")
                # if the subject matches yesterday's date and it is not an email that has already been sent by this program for today
                if subject_matches_date(e["subject"], amount_before=1) or (is_seed_live(e["subject"])) and seen_seed_live:
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
                    print("Checking if is SeedLive Generated Report")
                    if is_seed_live(e['subject']):
                        print("Matches")
                        seen_seed_live = True
                        try:
                            all_data.append(get_data_from_seed_live(attachment_data))
                        except Exception as e:
                            print(f"Error with SeedLive: {e}")
                    else:
                        # logging to the console
                        print("Does not match")
                # increment the index of the email
                i += 1
            except Exception as e:
                print(f"Error with email: {str(e)}\n\nSkipping...")
    
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
            print(format_all_data(all_data))
            print("No Email Sent")

        if write_to_spreadsheet:
            put_data_in_spreadsheet(all_data)
        else:
            print("Not Written to Spreadsheet")
    
        # press enter to exit the program
        print("Exiting...\n\n\n")
    except Exception as error:
        error_string = str(error)
        print(f"ERROR: {error_string}")
        if send_email:
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
    print(f"Checking if hour {dt.datetime.now().hour} is 7")
    return int(dt.datetime.now().hour) == hour

def minute_is(minute):
    return int(dt.datetime.now().minute) == minute

# if this file is being run, not imported
def main_autorun():
    global run_periodically
    if len(sys.argv) > 1:
        if sys.argv[1] == "-i":
            run_periodically = False
    if run_periodically:
        print("WAITING FOR 7:00am")
        while not minute_is(0) and not minute_is(60):
            print(f"Checking if current minute {dt.datetime.now().minute} is 0 or 60")
            time.sleep(60)
        print("Correct Minute Found")
        while True:
            if hour_is(7):
                main_func()
            time.sleep(3600) # seconds
    else:
        main_func()

if __name__ == "__main__":
    main_autorun()

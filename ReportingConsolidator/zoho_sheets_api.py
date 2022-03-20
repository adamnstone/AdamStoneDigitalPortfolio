import requests

#one_time = requests.post(f"https://accounts.zoho.com/oauth/v2/token?grant_type=authorization_code&client_id={zoho_client_id}&client_secret={zoho_client_secret}&redirect_uri=https://www.charlottelaundry.com/&code={code}")

class Zoho:
    def __init__(self):
        self.zoho_client_id = "1000.B37CPDNABB4NLBOP2SQPQHG3CGZ4II"
        self.zoho_client_secret = "f1ffc2d8c3d09d4673f28b79360c64059d07d18b76"
        self.resource_id = "7ve7je5f64d242a544fceb7694baff1301ab0"
        self.oauthtoken = "1000.10ed7d411d5ee5743dcee418128af8f9.c7b2d6dd8b200db06088e0c6a96ff3ce"
        self.scope = "ZohoSheet.dataAPI.UPDATE,ZohoSheet.dataAPI.READ"
        self.redirect_uri = "https://www.charlottelaundry.com/webmail/"
        self.code = "1000.7368061e28281405b744cedfcdd31920.2dc280ff5904b5d1841b3fb610c10e59"
        self.refresh_token_generated_once = "1000.1b0f00123c0550d64bf708c03683c699.69419476798aa92c892203d29bd311ee"
        self.base_url = f"https://sheet.zoho.com/api/v2/{self.resource_id}"

        self.date_title = "Date"

        self.authorization_headers = {"Authorization": f"Zoho-oauthtoken {self.generate_new_access_token()}"}

    def get_column_of_header(self, title):
        titles = self.get_headers()
        for dict in titles:
            if dict["content"].strip() == title.strip():
                col = dict["column_index"]
                return self.get_full_column(col)

    def get_full_column(self, column):
        return requests.get(f"{self.base_url}?method=range.content.get&worksheet_name=Daily&worksheet_id=&start_row=1&start_column={column}&end_row=65535&end_column={column}", headers=self.authorization_headers).json()

    def generate_new_access_token(self):

        response = requests.post(f"https://accounts.zoho.com/oauth/v2/token?refresh_token={self.refresh_token_generated_once}&client_id={self.zoho_client_id}&client_secret={self.zoho_client_secret}&grant_type=refresh_token")

        access_token = response.json()["access_token"]

        return access_token

    def get_headers(self):
        return self.get_row(1)

    def get_row(self, row, stripped=True):
        response = requests.get(f"{self.base_url}?method=range.content.get&worksheet_name=Daily&worksheet_id=&start_row={row}&start_column=1&end_row={row}&end_column=1024", headers=self.authorization_headers)

        lst = response.json()["range_details"][0]["row_details"]

        if stripped:
            for dict in lst:
                dict["content"] = dict["content"].strip()

        return lst

    def get_dates(self):
        date_column_index = None
        title_row = self.get_headers()
        for dict in title_row:
            title = dict["content"]
            if title == self.date_title:
                date_column_index = int(dict["column_index"])
                break
        print(f"Date Column Index: {date_column_index}")
        date_column = [{"row_index": x["row_index"], "content": x["row_details"][0]["content"]} for x in self.get_full_column(date_column_index)["range_details"]]
        return date_column

    def set_value(self, x, y, content):
        response = requests.post(f"{self.base_url}?method=cell.content.set&worksheet_name=Daily&worksheet_id=&row={y}&column={x}&content={content}", headers=self.authorization_headers)

        response_json = response.json()

        if response_json["status"].lower().strip() != "success":
            print(f"Setting cell {x}, {y} to {content} failed... Response:\n{response_json}")
        else:
            print(f"\"{content}\" successfully written to {x}, {y} in Zoho Sheets!")

        return response_json


if __name__ == "__main__":
    zoho = Zoho()
    print(zoho.get_headers())
    print(zoho.get_dates())

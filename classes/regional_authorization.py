from data.marketplace_dict import marketplace_dictionary
auth_url_string = "/apps/authorize/consent?application_id="


class Authorization:
    def __init__(self, mp):
        self.mp = marketplace_dictionary[mp]
        self.mp_url = marketplace_dictionary[mp]["seller_central_url"]
        self.auth_url = self.mp_url+auth_url_string

    def authorize(self):
        app_id = input("Type in your application ID: ")
        print(f"Copy this url to browser and start authorization flow: {self.auth_url}{app_id}")


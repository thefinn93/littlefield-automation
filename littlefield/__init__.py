import requests
from bs4 import BeautifulSoup

BASE_URL = "http://sim.responsive.net/Littlefield"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"}


class Littlefield(object):

    def __init__(self, user, password, institution="bothell3"):
        self.user = user
        self.password = password
        self.cookies = self.login(user, password, institution)

    def login(self, user, password, institution):
        """Logs into responsive.net and returns the cookie dict returned"""
        postdata = {
            "institution": institution,
            "ismobile": "false",
            "id": user,
            "password": password
        }

        response = requests.post("%s/CheckAccess" % BASE_URL, data=postdata)
        return response.cookies

    def post(self, path, postdata):
        return requests.post("%s/%s" % (BASE_URL, path), postdata, headers=HEADERS,
                             cookies=self.cookies)

    def get(self, path):
        return requests.get("%s/%s" % (BASE_URL, path), headers=HEADERS, cookies=self.cookies)

    def get_status(self):
        statuspage = self.get("/LTStatus")
        center = BeautifulSoup(statuspage.content, "html.parser").find("center")
        if center is None:
            raise Exceptipon("center is none!")
        soup = center.text.split("\n")
        status = {}
        for item in soup:
            if ":" in item:
                key, value = item.split(":")
                key = key.strip().lower()
                value = value.strip()
                if "," in value:
                    value = int("".join(value.split(",")))
                try:
                    value = int(value)
                except ValueError:
                    pass
                status[key] = value
        return status

    def get_data(self, datatype):
        """Retreives and parses a dataset"""
        data = self.post('Plot1', {'download': 'download', 'data': datatype}).content
        if data == b"You do not have permission to view this data.\n":
            raise Exception('You do not have permission to view this data.')
        data = data.decode('utf-8').split("\n")
        out = {}
        keys = ["day", "average"]
        for key in keys:
            out[key] = []
        for line in data[1:]:
            l = line.split("\t")
            for i in range(0, len(keys)):
                if len(l) > i and l[i] != "":
                    try:
                        out[keys[i]].append(float(l[i]))
                    except ValueError:
                        value = "".join(l[i].split(","))
                        out[keys[i]].append(float(value))
        return out

    def get_station(self, station):
        req = self.get("StationMenu?id=%s" % station)
        text = BeautifulSoup(req.content, "html.parser").text
        fields = {}
        for line in text.split("\n"):
            if ":" in line:
                key, value = line.split(":")
                key = key.strip().lower()
                value = value.strip()
                try:
                    value = int("".join(value.split(",")))
                except ValueError:
                    pass
                fields[key] = value
        return fields

    def update_machine_count(self, station, count=None, scheduling=None):
        res = self.post('StationForm', {
            "pwd": self.password,
            "submit": "confirm",
            "trans": "S%sCOUNT,%s" % (station, count),
            "id": station,
            "cancel": "cancel"
        })

    def get_standings(self):
        standings = self.get('Standing')
        soup = BeautifulSoup(standings.content, "html.parser").text.split("\n\n")
        out = []
        for row in soup[4:]:
            if "\n" in row:
                standing, team, cash = row.split("\n")
                cash = "".join(cash.strip().split(","))
                out.append({
                    "name": team.strip(),
                    "cash": int(cash)
                })
        return out

    def get_cash(self):
        lines = BeautifulSoup(self.get('CashStatus').content, "html.parser").text.split("\n")
        out = {}
        out['revenue'] = self.getamount(lines[13])
        out['interest'] = self.getamount(lines[15])
        out['machines'] = self.getamount(lines[19])*-1
        out['inventory'] = self.getamount(lines[21])*-1
        return out

    def getamount(self, amount, t=int):
        return t("".join(amount.split(",")))

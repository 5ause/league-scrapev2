import RequestSender
import time


def test_requests():
    RequestSender.add_keys(["RGAPI-2e562809-efb3-4116-aaeb-b44da21b77a1",
                            "RGAPI-1a6e7073-d658-4461-a0ad-256d0585f865",
                            "RGAPI-b3e61abb-f9a4-42e9-8cfd-07c05a8e1553"])

    codes = dict()

    def add_code(code, cdodes):
        if code not in cdodes:
            cdodes[code] = 1
        else:
            cdodes[code] += 1

    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/PlatypusOfCanada?api_key=<API_KEY>"

    start_time = int(time.time())
    count = 0
    while int(time.time()) < (start_time + 120):
        count += 1
        resp = RequestSender.send_request(url, variables={"API_KEY": ""})
        add_code(resp.status_code, codes)
        print("count=" + str(count), ", code=" + str(resp.status_code))

    print("sent " + str(count) + " requests in " + str(int(time.time()) - start_time) + " seconds.")
    print(codes)


def test_process_url():
    assert RequestSender.process_url("www.google.ca/<A>/<B><C>", {"A": "hello", "B": "MY", "C": "man"}) == \
           "www.google.ca/hello/MYman"


test_requests()

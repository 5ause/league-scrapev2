from typing import List

import bs4.element
from bs4 import BeautifulSoup
import RequestSender

LOG_URL_1 = "https://www.leagueofgraphs.com/summoner/na/<NAME>"
LOG_URL_CHAMPIONS = "https://www.leagueofgraphs.com/summoner/champions/na/<NAME>"


def get_response(name: str, url):
    name = name.replace(" ", "+")
    variables = {"NAME": name}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/96.0.4664.110 Safari/537.36"}
    response = RequestSender.send_request(url, variables=variables, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def find_role_wr(soup: BeautifulSoup, role):
    role_list = ["Jungler", "Top", "AD Carry", "Mid", "Support"]
    element1 = soup.find("div", attrs={"id": "profileRoles"})
    element2 = element1.findAll("tr")
    for i in range(0, len(element2)):
        element2[i] = element2[i].findAll("td")
    wr_dict = get_role_wr_dict(element2, role_list)
    if role in role_list and role in wr_dict:
        return {"role": role, "played": wr_dict[role][1], "winrate": wr_dict[role][2]}


# HELPER
def populate_role_wr_dict(list_of_tuples, role_list: List[str]):
    ret_dict = dict()
    for tpl in list_of_tuples:
        if tpl is None or len(tpl) < 3:
            continue
        tpl_role = tpl[0]
        for role in role_list:
            if role == tpl_role and role not in ret_dict:
                ret_dict[role] = tpl
    return ret_dict


# HELPER
def get_role_wr_info(tr: List[bs4.element.Tag]):
    if len(tr) < 3:
        return
    name_div = tr[0].find("div", attrs={"class": "txt name"})
    role_name = name_div.contents[0].strip()

    total_played = tr[1].attrs["data-sort-value"]

    wr = tr[2].attrs["data-sort-value"]

    return role_name, total_played, wr


# HELPER
def get_role_wr_dict(element2: List[bs4.element.Tag], role_list):
    list_of_tuples = []
    for a in element2:
        list_of_tuples.append(get_role_wr_info(a))

    return populate_role_wr_dict(list_of_tuples, role_list)


# UTILITY
def get_name_match_score(input_name: str, compare_to_name: str):
    assert len(input_name) > 0 and len(compare_to_name) > 0
    # match score btwn 0 and 1
    # if name is equal or in, 1
    input_name = input_name.lower().strip()
    compare_to_name = compare_to_name.lower().strip()
    input_name = input_name.replace(" ", "")
    compare_to_name = compare_to_name.replace(" ", "")
    if input_name == "monkeyking":
        input_name = "wukong"
    if compare_to_name == "monkeyking":
        compare_to_name = "wukong"
    if input_name == compare_to_name or input_name in compare_to_name:
        return 1
    return 0

    # We could do like you start at the beginning and check each character index is good, but like bruh
    # there's no way a champ name would be that far off...


# IMPORTANT
def get_champ_wr_played(soup: BeautifulSoup, champion_name: str):
    datas = get_champ_datas(soup)
    for key in datas:
        if get_name_match_score(champion_name, key) > 0.99:
            champ_data = datas[key]
            champ_data["champion"] = key
            return champ_data
    return None


# Semi-important HELPER
def get_champ_datas(soup: BeautifulSoup):
    all_rows = soup.findAll("tr")

    # print(all_rows[1])

    champ_dict = dict()

    # gets games played and winrate
    for row in all_rows:
        data = get_champ_data(row)
        name = get_champ_name(row)
        if data is not None and name is not None:
            champ_dict[name] = data
    return champ_dict


def get_champ_name(row: bs4.element.Tag):
    name_span = row.find("span", attrs={"class": "name"})
    if name_span is not None:
        return name_span.contents[0].strip()
    return None


def get_champ_data(row: bs4.element.Tag):
    all_progress_bars = row.findAll("progressbar")
    ret_dict = dict()
    if len(all_progress_bars) == 2:
        ret_dict = {"gamesPlayed": all_progress_bars[0].attrs["data-value"],
                    "winrate": all_progress_bars[1].attrs["data-value"]}
    return ret_dict

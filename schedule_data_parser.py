import requests
import lxml.html


def json_schedule_data_generator(response: str) -> tuple:
    """
    This function gets the raw html schedule data from urfu website
    and generates json and student's group data with it.
    """
    tree = lxml.html.document_fromstring(response)
    text_original = tree.xpath("/html//text()")

    # removing incorrect values in data
    no_spaces_text = [i.strip() for i in text_original if i.strip() != ""]

    # removing new lines in data
    prepared_text = [i.replace('\n', '').replace('   ', '') for i in
                     no_spaces_text]
    group = prepared_text[1]
    schedule = prepared_text[2::]

    # making schedule json
    schedule_dict = dict()
    current_slice = 0
    for _ in range(13):
        current = schedule[current_slice::]
        if "июня" in current[2]:
            if not schedule_dict.get(current[1]):
                schedule_dict[current[1]] = {}
            schedule_dict[current[1]][current[0]] = "Сегодня экзаменов нет"
            current_slice += 2
        else:
            schedule_join = " ".join(current[1:7:])
            if not schedule_dict.get(current[1]):
                schedule_dict[current[1]] = {}
            schedule_dict[current[1]][current[0]] = schedule_join
            current_slice += 7
    return schedule_dict, group


def json_schedule_data() -> tuple:
    """
    This function send a request to urfu website,
    and returns generated json schedule and student's group data.
    """
    url = "https://urfu.ru/api/schedule/groups/lessons/46278/20220613/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers).text
    return json_schedule_data_generator(response)


if __name__ == '__main__':
    print(json_schedule_data())

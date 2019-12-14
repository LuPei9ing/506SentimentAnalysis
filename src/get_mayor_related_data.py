import pandas as pd
import json
import os
import re


def load_department():
    department = []
    with open('mainstream/department.json') as json_file:
        data = json.load(json_file)
        for d in data['department']:
            department.append(d)
    return department


def load_districts():
    districts = []
    with open('mainstream/districts.json') as json_file:
        data = json.load(json_file)
        for d in data['districts']:
            districts.append(d)
    return districts


def load_data(input_filename, key_word, output_filename, department):
    data = pd.read_csv(input_filename)
    header = list(data.columns)
    print(header)
    title_column = -1
    summary_column = -1
    tags_column = -1
    body_column = -1
    for i in range(len(header)):
        if header[i] == 'title':
            title_column = i
        elif header[i] == 'summary':
            summary_column = i
        elif header[i] == 'tags':
            tags_column = i
        elif header[i] == 'body':
            body_column = i
    data = data.values.tolist()

    arts_data = []
    for item in data:
        title = str(item[title_column]).lower()
        summary = str(item[summary_column]).lower()
        tags = str(item[tags_column]).lower()
        body = str(item[body_column]).lower()
        if 'boston' in title and key_word in title\
                or 'boston' in summary and key_word in summary\
                or 'boston' in tags and key_word in tags\
                or 'boston' in body and key_word in body:
            for dep in department:
                dep = dep.lower()
                if dep in title or dep in summary or dep in tags or dep in body:
                    item.remove(item[0])
                    arts_data.append(item)
                    break
    header.remove(header[0])
    df = pd.DataFrame(arts_data, columns=header)
    df.to_csv(output_filename, index=False)


def remove_urls(text):
    # remove urls start with http or https
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', ' ', text)
    # remove urls contains certain domainS
    text = re.sub(r'(\w|\.|\/|\?|\=|\&|\%)*'
                   r'(\.com|\.net|\.xyz|\.top|\.tech|\.org|\.gov|\.edu|\.ink|\.red|\.int|\.mil|\.pub|\.me|\.TV|\.info|\.mobi|\.travel|\.cn)'
                   r'(\w|\.|\/|\?|\=|\&|\%)*\b', ' ', text)
    return text


def load_all_data(input_filename, output_filename, department, districts):
    data = pd.read_csv(input_filename)
    header = list(data.columns)
    print(header)
    title_column = -1
    summary_column = -1
    tags_column = -1
    body_column = -1
    for i in range(len(header)):
        if header[i] == 'title':
            title_column = i
        elif header[i] == 'summary':
            summary_column = i
        elif header[i] == 'tags':
            tags_column = i
        elif header[i] == 'body':
            body_column = i
    data = data.values.tolist()
    print(len(data))

    new_data = []
    count = 0
    for item in data:
        title = str(item[title_column]).replace('bostonherald',' ').replace('Boston Herald', ' ').lower()
        summary = str(item[summary_column]).replace('bostonherald',' ').replace('Boston Herald', ' ').lower()
        tags = str(item[tags_column]).replace('bostonherald',' ').replace('Boston Herald', ' ').lower()
        # body = remove_urls(str(item[body_column])).lower()
        body = (str(item[body_column])).replace('bostonherald',' ').replace('Boston Herald', ' ').lower()
        find_dep = False
        find_dis = False
        for dep in department:
            dep = dep.lower()
            if dep in title or dep in summary or dep in tags or dep in body:
                find_dep = True
                break
        for dis in districts:
            dis = dis.lower()
            if dis in title or dis in summary or dis in tags or dis in body:
                find_dis = True
                break
        if find_dep and find_dis:
            item.remove(item[0])
            if input_filename != 'mainstream/boston_globe.csv':
                item.remove(item[0])
            item.insert(0, count)
            new_data.append(item)
            count = count + 1

    if input_filename != 'mainstream/boston_globe.csv':
        header.remove(header[0])
    header.remove(header[0])
    header.insert(0, "ID")
    df = pd.DataFrame(new_data, columns=header)
    df.to_csv(output_filename, index=False)
    print(len(new_data))


def load_social_data(input_filename, output_filename, department):
    with open(input_filename) as f:
        data = json.loads(f.read())

    print(len(data))
    new_data = []
    count = 0
    for d in data:
        text = str(d['text']).lower()

        find_dep = False
        # find_dis = False

        find_dis = True
        for dep in department:
            dep = dep.lower()
            if dep in text:
                find_dep = True
                break
            else:
                for tag in d['hashtags']:
                    if dep.replace(' ', '').lower() in str(tag).lower():
                        find_dep = True
                        break
        if find_dep and find_dis:
            t = d['timestamp'].split('T')[0]
            item = [count, t, d['likes'], d['retweets'], d['replies'], d['hashtags'], d['text']]
            new_data.append(item)
            count = count + 1
            # print(item)
    print(len(new_data))
    print(input_filename)
    header = ['tweet_id', 'Timestamp', 'likes', 'retweets', 'replies', 'hashtag', 'text']
    df = pd.DataFrame(new_data, columns=header)
    df.to_csv(output_filename, index=False)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def main():
    department = load_department()
    districts = load_districts()
    topics = ["arts", "community", "housing", "library", "program", "resident", "school", "service", "street", "youth"]

    # -------------------------------------mainstream media data-------------------------------------
    input_filenames = ["boston_globe", "boston_herald", "wbur", "wgbh"]

    # split data(mayor related) by topics + website
    # for input_filename in input_filenames:
    #     for topic in topics:
    #         load_data("mainstream/" + input_filename + ".csv", topic, "mainstream_topic/" + input_filename + "_" + topic + ".csv", department)

    # split data(mayor related) by website
    for input_filename in input_filenames:
        load_all_data("mainstream/" + input_filename + ".csv", "mainstream_mayor/" + input_filename + ".csv", department, districts)

    # -----------------------------------------social media data--------------------------------------
    for topic in topics:
        input_filename = 'twitter/' + topic + '.json'
        output_filename = 'twitter_mayor/' + topic + '.csv'
        load_social_data(input_filename, output_filename, department)


main()

import json


def get_rastless_dates():
    with open("rastless_layer_dates.json") as fobj:
        data = json.load(fobj)

    return [x["datetime"].replace(" ", "T") for x in data]


def get_rasdaman_dates():
    with open("rasdaman_layer_dates.json") as fobj:
        data = json.load(fobj)

    return data[0]["datetime_steps"]


def date_intersection(dates_rastless, dates_rasdaman):
    return list(set(dates_rastless).intersection(dates_rasdaman))


if __name__ == '__main__':
    dates_rastless = get_rastless_dates()
    dates_rasdaman = get_rasdaman_dates()

    dates_in_both_systems = date_intersection(dates_rastless, dates_rasdaman)

    print("test")
import csv
from collections import namedtuple

def get_unique_recommendations(csv_file_path):
    unique_recommendations = set()

    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            unique_recommendations.add(row['Recommendation'])

    return unique_recommendations

Recommendation = namedtuple('Recommendation', ['code','name','url','party'])
Constituency = namedtuple('Constituency', ['code','name'])

def read_recommendations(csv_file_path):
    recs = {}
    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row['Code']
            name = row['Constituency name']
            url = row['Source URL']
            party = row['Recommendation']
            recs[name] = Recommendation(code, name, url, party)
    return recs

def compare_recommendations():
    constituencies = read_constituencies()

    stopthetories = read_recommendations("data/stopthetories.csv")
    tacticaldotvote = read_recommendations("data/tactical.vote.csv")
    tacticalvotecouk = read_recommendations("data/tacticalvote.co.uk.csv")

    for con in constituencies:
        stt_party = stopthetories[con.name].party
        tdv_party = tacticaldotvote[con.name].party
        tvuk_party = tacticalvotecouk[con.name].party

        parties = [stt_party, tdv_party, tvuk_party]
        filtered_parties = [party for party in parties if party not in {"Any", "TBC"}]
        unique_parties = list(set(filtered_parties))
        if len(unique_parties) > 1:
            print(f"{con.name} ({con.code}): Stop the Tories has {stt_party} at {stopthetories[con.name].url}, tactical.vote has {tdv_party} at {tacticaldotvote[con.name].url}, tacticalvote.co.uk has {tvuk_party} at {tacticalvotecouk[con.name].url}")

def read_constituencies():
    constituencies = []
    with open("data/constituencies.csv", mode='r', newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            code = row['Code']
            name = row['Constituency name']
            constituencies.append(Constituency(code, name))
    return constituencies


if __name__ == '__main__':
    # print("From stopthetories")
    # print(get_unique_recommendations('data/stopthetories.csv'))
    # print("From tactical.vote")
    # print(get_unique_recommendations('data/tactical.vote.csv'))
    # print("From tacticalvote.co.uk")
    # print(get_unique_recommendations('data/tacticalvote.co.uk.csv'))

    compare_recommendations()
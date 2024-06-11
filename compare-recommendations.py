import csv


def get_unique_recommendations(csv_file_path):
    unique_recommendations = set()

    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            unique_recommendations.add(row['Recommendation'])

    return unique_recommendations


if __name__ == '__main__':
    print("From stopthetories")
    print(get_unique_recommendations('data/stopthetories.csv'))
    print("From tactical.vote")
    print(get_unique_recommendations('data/tactical.vote.csv'))
    print("From tacticalvote.co.uk")
    print(get_unique_recommendations('data/tacticalvote.co.uk.csv'))

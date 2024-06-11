import csv
import requests
import time
from bs4 import BeautifulSoup
import unicodedata
import re

user_agent = 'tacticalvoting-consistency-checker (https://github.com/inigo/tacticalvoting-consistency-checker)'

"""
Checks recommendations from https://tactical.vote
"""
class TacticalDotVoteChecker:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.headers = { 'User-Agent': user_agent }

        with open(self.output_file, mode='w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Code', 'Constituency name', 'Source URL', 'Recommendation'])

    @staticmethod
    def normalize_name(name):
        # Normalize accents and lowercase
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
        name = name.lower()
        # Replace spaces with hyphens and remove other characters
        name = re.sub(r'\s+', '-', name)
        name = re.sub(r'[^a-z0-9\-]', '', name)
        return name

    @staticmethod
    def normalize_recommendation(name):
        mapping = {
            'Plaid cymru': 'Plaid Cymru',
            'Liberal democrat': 'Lib Dem',
            'Social democratic and labour party': 'SDLP',
            'Scottish national party': 'SNP',
            'Sinn fein': 'Sinn Féin',
            'No recommendation': 'Any',
            'Not sure': 'TBC',
        }
        return mapping.get(name, name)

    def get_recommendation(self, normalized_name):
        url = f'https://tactical.vote/{normalized_name}/'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            recommendation_div = soup.find('div', class_='recommendation')

            if recommendation_div:
                classes = recommendation_div.get('class', [])
                # Exclude the 'recommendation' class itself
                for cls in classes:
                    if cls != 'recommendation':
                        return cls.capitalize().replace('-', ' ')

            return "No recommendation"
        else:
            return "HTTP error"

    def process_constituencies(self):
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as input_file:
            reader = csv.DictReader(input_file)

            for row in reader:
                code = row['Code']
                constituency_name = row['Constituency name']
                normalized_name = self.normalize_name(constituency_name)

                recommendation = self.get_recommendation(normalized_name)
                source_url = f'https://tactical.vote/{normalized_name}/'
                print(f"Retrieved {recommendation} from {source_url} for {constituency_name}")
                self.write_result([code, constituency_name, source_url, recommendation])

                # Wait for 2 seconds to respect the server
                time.sleep(2)

    def write_result(self, result):
        with open(self.output_file, mode='a', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(result)

"""
Checks recommendations from https://tacticalvote.co.uk/
"""
class TacticalVoteCoUkDownloader:
    def __init__(self, output_file):
        self.output_file = output_file
        self.headers = { 'User-Agent': user_agent }

    def execute(self):
        csv_data = self.download_csv()
        processed_data = self.process_csv(csv_data)
        self.write_csv(processed_data)
        print(f"Process completed. Results saved to {self.output_file}")

    def download_csv(self):
        response = requests.get('https://tacticalvote.co.uk/data/recommendations.csv', headers=self.headers)
        response.raise_for_status()
        return response.text

    @staticmethod
    def normalize_name(name):
        # Remove accented characters entirely
        name = re.sub(r'[^\x00-\x7F]+', '', name)
        # Remove the word "and"
        name = re.sub(r'\band\b', '', name, flags=re.IGNORECASE)
        # Remove spaces and punctuation
        name = re.sub(r'[\s\W_]+', '', name)
        return name

    @staticmethod
    def normalize_recommendation(name):
        mapping = {
            'LD': 'Lib Dem',
        }
        return mapping.get(name, name)

    @staticmethod
    def process_csv(csv_data):
        results = []
        reader = csv.DictReader(csv_data.splitlines())

        for row in reader:
            code = row['id']
            constituency_name = row['Constituency']
            normalized_name = TacticalVoteCoUkDownloader.normalize_name(row['Constituency'])
            source_url = f'https://tacticalvote.co.uk/#{normalized_name}'
            recommendation = TacticalVoteCoUkDownloader.normalize_recommendation(row['Vote For'])
            results.append([code, constituency_name, source_url, recommendation])

        return results

    def write_csv(self, data):
        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Code', 'Constituency name', 'Source URL', 'Recommendation'])
            writer.writerows(data)

"""
Checks recommendations from https://stopthetories.vote/
"""
class StopTheToriesVoteChecker:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.headers = { 'User-Agent': user_agent }

        with open(self.output_file, mode='w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Code', 'Constituency name', 'Source URL', 'Recommendation'])

    @staticmethod
    def normalize_name(name):
        # Remove accents, lowercase, replace spaces with hyphens
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
        name = name.lower()
        name = re.sub(r'\s+', '-', name)
        name = re.sub(r"'", '-', name) # Queen's Park and Maida Vale
        name = re.sub(r'[^a-z0-9\-]', '', name)
        return name

    @staticmethod
    def normalize_recommendation(name):
        mapping = {
            'plaid': 'Plaid Cymru',
            'libdem': 'Lib Dem',
            'green': 'Green',
            'snp': 'SNP',
            'No recommendation': 'TBC',
            'labour': 'Labour',
        }
        return mapping.get(name, name)

    def get_recommendation(self, normalized_name):
        url = f'https://stopthetories.vote/parl/{normalized_name}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.find('div', class_='party-heart'):
                return "Any"

            party_none_div = soup.find('div', class_='party-none')
            if party_none_div:
                descendants = party_none_div.find_all('span', class_=lambda c: c and c.startswith('party-'))
                if descendants:
                    return ' or '.join([self.normalize_recommendation(desc.get('class')[0].split('-')[1]) for desc in descendants])
                return "TBC"

            recommendation_div = soup.find('div', class_='party')
            if recommendation_div:
                classes = recommendation_div.get('class', [])
                # Find the class that starts with 'party-'
                for cls in classes:
                    if cls.startswith('party-'):
                        return cls.split('-')[1]

            return "No recommendation"
        else:
            return "HTTP error"

    def process_constituencies(self):
        with open(self.input_file, mode='r', newline='', encoding='utf-8-sig') as input_file:
            reader = csv.DictReader(input_file)

            for row in reader:
                code = row['Code']
                constituency_name = row['Constituency name']
                normalized_name = self.normalize_name(constituency_name)

                recommendation = self.normalize_recommendation(self.get_recommendation(normalized_name))
                source_url = f'https://stopthetories.vote/parl/{normalized_name}'
                print(f"Retrieved {recommendation} from {source_url} for {constituency_name}")
                self.write_result([code, constituency_name, source_url, recommendation])

                # Wait for 2 seconds to respect the server
                time.sleep(1)


    def write_result(self, result):
        with open(self.output_file, mode='a', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(result)

if __name__ == '__main__':

    constituencies_file_path = 'data/constituencies.csv'

    # checker1 = TacticalDotVoteChecker(constituencies_file_path, 'data/tactical.vote.csv')
    # checker1.process_constituencies()
    #
    # checker2 = TacticalVoteCoUkDownloader('data/tacticalvote.co.uk.csv')
    # checker2.execute()

    checker3 = StopTheToriesVoteChecker(constituencies_file_path, 'data/stopthetories.csv')
    checker3.process_constituencies()



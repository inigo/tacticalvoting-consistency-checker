import csv
import requests
import time

input_file_path = 'data/UK constituency postcodes 2024.csv'
output_file_path = 'data/constituencies.csv'

def retrieve_sample_postcodes():
    results = []

    # Read the initial CSV file
    with open(input_file_path, mode='r', newline='', encoding='utf-8-sig') as input_file:
        constituencies_reader = csv.DictReader(input_file)

        for row in constituencies_reader:
            code = row['Code']
            constituency = row['Constituency']

            # Make the HTTP request
            url = f'https://www.doogal.co.uk/Constituency24CSV/{code}'
            response = requests.get(url)
            response.raise_for_status()  # Note this will abort the whole process for one error - that's intentional, since we expect this to be rare

            # Read the additional CSV content
            postcode_lines = response.text.splitlines()
            postcodes_reader = csv.DictReader(postcode_lines)

            # Find the first active postcode - there are "not in use" postcodes in the CSVs that have been withdrawn
            first_active_postcode = None
            for line in postcodes_reader:
                if line['In Use?'].strip().lower() == 'yes':
                    first_active_postcode = line['Postcode']
                    break
            if first_active_postcode:
                results.append([code, constituency, first_active_postcode])
                print(f"Retrieved {code}, {constituency} and {first_active_postcode}")

            # Be polite to doogal
            time.sleep(2)

    # Write the results to a new CSV file
    with open(output_file_path, mode='w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Code', 'Constituency name', 'Sample postcode'])
        writer.writerows(results)

if __name__ == '__main__':
    retrieve_sample_postcodes()
    print(f"Process completed. Results saved to {output_file_path}")

import csv
import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

    return text

# Function to split the combined data into fields using regex
def split_combined_data(combined_data):    
    # Define the regex pattern to match individual data items
    pattern = re.compile(r'\s{2,}')

    # Split the combined data using the regex pattern
    split_data = re.split(pattern, combined_data.strip())

    # Filter out empty elements
    split_data = [item for item in split_data if item]

    # return the split data
    return split_data

# trim unnecessary data out of the lines
def trim_lines(list):
    # initiate a new list
    clean_list = []

    # iterate through each item in the list
    for item in list:
        # filter out entries that don't start with a number or have length 11
        item = [entry for entry in item if (entry[0].isdigit() or len(entry) == 11) and entry]

        # split CRED LIM and NAME fields if necessary, strip off BILL CD suffix
        if len(item) > 5:
            # CRED LIM and NAME
            part1, part2 = item[4].split(' ', 1)
            item[4] = part1
            item.insert(5, part2)

            # BILL CD
            # loop through this item to find the BILL CD, it varies slightly
            for index, element in enumerate(item):
                if element.startswith('B'):
                    item[index] = item[index][:-3]       
        
        # add this line to the new list
        clean_list.append(item)

    # return the new list
    return clean_list[:-3]

def convert_text(text):
    # split up the given text by newline
    text_lines = text.split("\n")

    # create a list to store each line
    pdf_list = []

    # add all of the lines to the list
    for line in text_lines:
        pdf_list.append(line)

    # remove all entries from the list that aren't 16 characters long or contain a decimal point
    # every line of relevant data fits these criteria - we want to delete unnecessary headers and footers
    pdf_list = [entry for entry in pdf_list if not entry.isspace() and (len(entry.split()[0]) == 16 or '.' in entry)]

    # create the headings of the report that Brittany cares about
    headers = ["ACCT NUMBER", "CURR BAL", "CRED LIM", "NAME", "OPN DT",
               "LST AC", "PAY DT", "LAST PAY AMT", "AMT DUE", "EXP DT", "BILL CD",
                "BILL DAY"]
    
    # initiate the official list of data
    csv_list = []    

    # Iterate through the list, combining every other element
    for i in range(0, len(pdf_list), 2):
        # Combine the current element and the next element (if it exists)
        combined_data = pdf_list[i]
        
        # make sure we aren't at the end of the PDF list
        if i + 1 < len(pdf_list):
            combined_data += ' ' + pdf_list[i + 1]
        
        # Split the combined data into individual pieces of data
        split_data = split_combined_data(combined_data)

        # Append the cleaned list of data to the final result list
        csv_list.append(split_data)

    # keep only the items in this list that start with a number or are length 8
    # this filters out unnecessary data
    csv_list = trim_lines(csv_list)

    # append the headers
    csv_list.insert(0, headers)
    
    # return the list
    return csv_list

def write_text_to_csv(csv_list, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # transpose data to align rows with columns
        transposed_data = zip(csv_list)

        for line in csv_list:
            writer.writerow(line)

def main():
    pdf_file_path = '20240531-CHJournal-VG-P1C.pdf'
    csv_file_path = 'output.csv'

    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # convert the text
    csv_list = convert_text(pdf_text)

    # Write text to CSV
    write_text_to_csv(csv_list, csv_file_path)

if __name__ == "__main__":
    main()
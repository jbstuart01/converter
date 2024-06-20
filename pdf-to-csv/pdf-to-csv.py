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

def convert_text(text):
    # split up the given text by newline
    text_lines = text.split("\n")

    # create a list to store each line
    pdf_list = []

    # add all of the lines to the list
    for line in text_lines:
        pdf_list.append(line)

    # remove all entries from the list that don't start with a number
    # this ensures we remove all unnecessary headers and footers
    pdf_list = [entry for entry in pdf_list if not re.match(r'^\s*[a-zA-Z]', entry) and not entry.isspace()]

    # Function to split the combined data into fields using regex
    def split_combined_data(combined_data):
        # Define the regex pattern to match individual data items
        pattern = re.compile(r'\s+')
        # Split the combined data using the regex pattern
        split_data = re.split(pattern, combined_data.strip())
        # Filter out empty elements
        split_data = [item for item in split_data if item]
        return split_data

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
        csv_list.extend(split_data)

    # create the headings of the report that Brittany cares about
    heading = ["ACCT NUMBER", "CURR BAL", "CRED LIM", "NAME", "OPN DT",
               "LST AC", "PAY DT", "LAST PAY AMT", "AMT DUE", "EXP DT", "BILL CD",
                "BILL DAY"]
  
    # combine the stripped list and the heading using slice notation
    csv_list[:0] = [heading]

    print(csv_list[:10])
    return


def write_text_to_csv(text, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # split text into lines and write each line as a row in the CSV
        for line in text.split('\n'):
            writer.writerow([line])

def main():
    pdf_file_path = '20240531-CHJournal-VG-P1C.pdf'
    csv_file_path = 'output.csv'

    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # convert the text
    convert_text(pdf_text)

    # Write text to CSV
    #write_text_to_csv(pdf_text, csv_file_path)

if __name__ == "__main__":
    main()
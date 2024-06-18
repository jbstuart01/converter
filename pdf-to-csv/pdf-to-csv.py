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
    line_list = []

    # add all of the lines to the list
    for line in text_lines:
        line_list.append(line)

    # remove all entries from the list that don't start with a 4
    # this ensures we remove all unnecessary headers and footers
    line_list = [entry for entry in line_list if (entry.strip() and str(entry).startswith('4'))]

    # add the headings of the report that Brittany cares about
    heading = ["ACCT NUMBER", "CURR BAL", "CRED LIM", "NAME", "OPN DT",
               "LST AC", "PAY DT", "LAST PAY AMT", "AMT DUE", "EXP DT", "BILL CD",
                "BILL DAY"]
    
    # combine the stripped list and the heading using slice notation
    line_list[:0] = [heading]


    print(line_list[:10])    
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
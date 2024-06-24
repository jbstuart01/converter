import csv
import PyPDF2
import re

# extract the raw text from the PDF
def extract_text_from_pdf(pdf_path):
    # open a PDF object and call it file
    with open(pdf_path, 'rb') as file:
        # initialize a PDF reader object
        reader = PyPDF2.PdfReader(file)

        # iterate through all the text in the PDF and add it to a string variable
        text = ''.join([page.extract_text() for page in reader.pages])
    
    # return this string
    return text

# take in one line of data separated by varying amounts of whitespace and return a list of those items
def split_combined_data(combined_data):
    # the pattern is two or more consecutive whitespaces
    # we don't want only one whitespace because this splits up the name
    pattern = re.compile(r'\s{2,}')

    # create the list
    split_data = re.split(pattern, combined_data.strip())
    
    # return every item in this list as long as it exists
    return [item for item in split_data if item]

# clean and filter the list of data lines
def trim_lines(lines):
    # initialize a new list to store the cleaned data
    clean_list = []

    # iterate through each item in the data list
    for item in lines:
        # only keep entries that start with a digit or have exactly 11 characters
        # the only entry we care about that starts with a letter is known to be 11 chars
        item = [entry for entry in item if (entry[0].isdigit() or len(entry) == 11)]
        
        # only perform this on list items that are long enough
        if len(item) > 5:
            # we care about both these data fields, but they're only separated by one space so they are combined
            # split them up along that one space
            part1, part2 = item[4].split(' ', 1)
            item[4] = part1
            item.insert(5, part2)

            # this happens on another occasion in the item, but we don't care about the second of the two
            # just strip off the last 3 characters since we don't care about it
            # unfortunately the location varies slightly from item to item, so we have to search through the item to find it
            for index, element in enumerate(item):
                # the element we care about starts with a B
                if element.startswith('B'):
                    # strip off the last 3 characters
                    item[index] = element[:-3]
        
        # add this item to the cleaned list
        clean_list.append(item)
    
    # return the cleaned list, stripping off the last 3 garbage entries
    return clean_list[:-3]

# convert a string to a two-dimensional list
def convert_text(text):
    # use newline characters to build the list
    # combine every other line since the original PDF had each line of data wrap to one new line
    # use a check to exclude garbage (headers/footers/other formatting)
    text_lines = [line for line in text.split("\n") if line and len(line.split()) > 0 and (len(line.split()[0]) == 16 or '.' in line)]
    
    # the headers of the data we care about
    headers = ["ACCT NUMBER", "CURR BAL", "CRED LIM", "NAME", "OPN DT",
               "LST AC", "PAY DT", "LAST PAY AMT", "AMT DUE", "EXP DT", "BILL CD",
               "BILL DAY"]
    
    # make each line of the list a combination of every other line from the original list
    csv_list = [split_combined_data(text_lines[i] + ' ' + text_lines[i + 1]) for i in range(0, len(text_lines), 2)]
    
    # trim the unnecessary data out of this list
    csv_list = trim_lines(csv_list)

    # add the headers
    csv_list.insert(0, headers)
    
    # return the cleaned list
    return csv_list

# write a given list to a CSV
def write_text_to_csv(csv_list, csv_path):
    # open the CSV with write priviliges and call it file
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        # initialize a CSV writer object
        writer = csv.writer(file)

        # write each row of the given list
        writer.writerows(csv_list)

def main():
    # path of our original PDF
    pdf_file_path = '20240531-CHJournal-VG-P1C.pdf'
    
    # path of the final CSV to write to 
    csv_file_path = 'output.csv'
    
    # get the text from the original PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # convert the text to a two-dimensional list
    csv_list = convert_text(pdf_text)

    # write this list to the final CSV
    write_text_to_csv(csv_list, csv_file_path)

if __name__ == "__main__":
    main()

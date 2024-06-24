# PDF to CSV Converter
## Overview

This Python program extracts text from a PDF file and converts it into a structured CSV file. The program is designed to process a PDF file that contains sensitive financial data. The original PDF is horribly formatted, so the mission of this program is to convert it into a much more helpful CSV that can then be used in a traditional spreadsheet.

>Note: Due to the extremely specific formatting of this particular PDF, this program was only designed to work for this specific use case, and will not work as-is on any other file. However, the methodology can be repeated for a variety of similar use cases.

## Features

Extracts text from a multi-page PDF files.
Cleans and structures the extracted data.
Converts the cleaned data into a CSV file with appropriate headers.
Handles specific formatting issues in the data, such as splitting combined fields and trimming unnecessary suffixes.

## Requirements

- Python 3.6 or higher
- PyPDF2
- re (regular expressions)
- csv (standard library module)

## Installation

Clone the Repository:

    git clone https://github.com/yourusername/pdf-to-csv.git
    cd pdf-to-csv

Install Dependencies

    pip install PyPDF2

## Usage

1. Ensure your PDF file is located in the same directory as the script or provide the correct path.

2. Execute the script by running:

       python pdf-to-csv.py

3. The script will generate a file named `output.csv` in the same directory, containing the structured data extracted from the PDF.

## Code Explanation

### Functions

    extract_text_from_pdf(pdf_path)
Loads the entire contents of the PDF file into a string variable.

    convert_text(text)
Converts the raw extracted text into a structured list suitable for CSV output.

    split_combined_data(combined_data)
Splits the combined data from a massive string into elements of a list using regular expressions to handle multiple variations of separators.

    trim_lines(data_list)
Cleans and filters the list of data lines. Removes garbage and splits elements that were still joined by default.
    
    

    write_text_to_csv(csv_list, csv_path)
Writes the structured data to a CSV file.


### Main Script

The main script ties together the functions.

1. Extracts text from the PDF.
2. Converts the text into structured data.
3. Writes the data to a CSV file.

## Challenges
A number of challenges arose when creating this program. Here are a few:
- **Exception Cases:** There were a lot of specific exclusions that were required to ensure only relevant lines of data were included in the final output. Every page had a header and footer that needed to be ignored, and there were totals scattered throughout the document as well.
- **Inconsistent Data:** Not every entry in the data had the same amount of fields, making it challenging to get all the columns to end up matching. For the sake of time, most of these were solved by making adjustments to the final CSV in Excel.
- **Efficient Garbage Dumping:** An optimization to the program would be to have all the unnecessary data dumped out in the same step. Due to the complicated nature of the formatting, there are filters and slices at various points of the program. This is not ideal, but the primary objective of the project was to get a working CSV file as fast as possible.

## Contribution
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any issues or suggestions, please open an issue on the GitHub repository or contact [jacob.stuart@gtkycu.com].

import pandas as pd

# Read the Excel file
excel_file = pd.read_excel('sheets.xlsx', sheet_name=None)

# Get the word or characters to search for
search_word = input("Enter the word or characters to search for: ")

# Search for the word or characters in each sheet
for sheet_name, sheet_data in excel_file.items():
    # Convert all cells to strings and search for the word or characters
    search_results = sheet_data.applymap(str).apply(lambda x: x.str.contains(search_word, case=False))

    # Check if the search word or characters were found in the sheet
    if search_results.any().any():
        print(f'"{sheet_name}" 시트에서 입력하신 "{search_word}"이 확인됩니다. 셀의 위치 :')

        # Loop through the rows and columns to find the cell locations of the search results
        for i, row in search_results.iterrows():
            for j, value in enumerate(row):
                if value:
                    # Convert the column index to a letter using ASCII code, and concatenate with the row index to create the cell location string
                    col_letter = chr(j+65)
                    cell_location = f'{col_letter}{i+1}'
                    print(f'    {cell_location}')

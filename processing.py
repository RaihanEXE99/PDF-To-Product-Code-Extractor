import textract
import re
from datetime import datetime

def get_numbers(file_path):
    # Get The PDF content and filter for 8 digit numbers
    output, out_string = [], ''
    try:
        pdf_content = textract.process(file_path)
    except UnicodeDecodeError:
        pdf_content = textract.process(file_path, method='pdfminer')
    text = str(pdf_content)
    numbers_list = re.sub('\D', ' ', text).split()
    for x in numbers_list:
        if len(x) == 8 and x not in output:
            output.append(x)
    numbs_amnt = len(output)
    # Formatting of output string
    out_string += f'{numbs_amnt} product numbers found:\\n'
    for i, x in enumerate(output):
        if (i+1) % 10 == 0:
            out_string += f'{x}\\n'
        else:
            out_string += f'{x} '
    out_string.rstrip()

    # Get date, amount of processed PDF files and extracted numbers
    # and write to record.txt
    now = datetime.now()
    dt_string = now.strftime('%d/%m/%Y %H:%M:%S')
    with open('record.txt', 'r') as f:
        lines = f.readlines()
        amnt = int(''.join(re.sub('\D', ' ', lines[0]).split()))
        amnt += 1
        curr_numbs = int(''.join(re.sub('\D', ' ', lines[1]).split()))
        curr_numbs += numbs_amnt
    with open('record.txt', 'w') as f:
        f.write(f'PDF files processed: {amnt}\n'
                f'Product numbers extracted: {curr_numbs}\n'
                f'Last time used: {dt_string}')
    return out_string

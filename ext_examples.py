from openpyxl import load_workbook

# Load the Excel file
file_path = "/mnt/data/sample.xlsx"

def extract_alt_text_examples(file_path, num_examples=5):
    wb = load_workbook(file_path)
    sheet = wb.active  # Select the first sheet
 
    # Extract the first `num_examples` rows for context
    examples = []
    for i in range(num_examples):
        caption, alt_text = sheet[f'D{i+3}'].value, sheet[f'G{i+3}'].value
        if caption and alt_text:
            examples.append(f"Caption: {caption}\nAlt Text: {alt_text}")
    wb.close()

    return "\n\n".join(examples)

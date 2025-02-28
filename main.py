import io
from pdf2image import convert_from_path
from openpyxl import load_workbook, Workbook
from openpyxl.drawing.image import Image as ExcelImage
import app
import base64
import re
import os
import ext_examples
from dotenv import load_dotenv


load_dotenv()
prompt = os.getenv("prompt")
caption_prompt = os.getenv("caption_prompt")
poppler_path = os.getenv("poppler_path")

file_prompt = """
This is file is for your training purpose.
"""


def check_uploaded():
    pass


def pdf_images_to_excel(pdf_path, excel_path, completed_pages, row_number, sample_file):
    sample = ext_examples.extract_alt_text_examples(sample_file,num_examples=5)

    # Convert PDF pages to images
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    # Create a new Excel workbook and sheet
    if os.path.exists(excel_path):
        wb = load_workbook(excel_path)
    else:
        wb = Workbook()

    ws = wb.active
    ws.title = "PDF Images"
    ws[f'A1'] = "Page No."
    ws[f'C1'] = "Figure"
    ws[f'E1'] = "Caption"
    ws[f'G1'] = "ALT-Text"

    try:
        i=row_number
        for j, image in enumerate(images):
            if j<completed_pages:
                continue 
            # Convert image to bytes
            img_buffer = io.BytesIO()
            image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Convert to Base64
            img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
            caption = app.get_response(img_base64,caption_prompt)
            if len(caption) <=2 : 
                print(f"page: {j} skipped because no diagrams found")
                continue
            print(caption)
            caption = caption.split("\n\n")
    
            for item in caption: 
                fig = re.match(r'(Fig\.\s*\d+\.\d+)', item)
                if fig:
                    fig = fig.group(0)
                else:
                    fig = "N/A"

                alt_text = app.generate_alt_text(sample, img_base64, prompt+item)                         
                ws[f'A{i+2}'] = f"Page no. {j}"
                ws[f'C{i+2}'] = fig
                text = item[len(fig):].strip()
                ws[f'E{i+2}'] = text+'\n'
                ws[f'G{i+2}'] = alt_text
                i+=1
            print(f"page {j} completed")
        wb.save(excel_path)
        print(f"Excel saved at: {excel_path}")       
    except:
        wb.save(excel_path)
        print(f"Some error occured")
        print(f"Excel saved at: {excel_path}")


     
def main():
    completed_pages = int(input("Enter the number of completed pages: "))
    sapmle_path = "sample.xlsx"
    row_number = int(input("Enter the number of rows completed: "))
    pdf_images_to_excel("input.pdf", "output.xlsx", completed_pages, row_number, sapmle_path)


if __name__ == "__main__":
    main()
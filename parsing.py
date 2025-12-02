import os
import pdfplumber
pdf_folder = r"C:\Users\malik\OneDrive\Desktop\YCG 1"
output_folder = r"C:\Users\malik\OneDrive\Desktop\YCG 1\parsed_text"
os.makedirs(output_folder, exist_ok=True)
def pdf_to_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Parsing page {i+1} of {len(pdf.pages)}...")
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf") and not filename.startswith("._"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Parsing {filename}...")
        text = pdf_to_text(pdf_path)
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_output_path = os.path.join(output_folder, txt_filename)
        with open(txt_output_path, "w", encoding="utf-8") as f_out:
            f_out.write(text)
print(f"\nParsing complete! All PDF texts saved in {output_folder}")
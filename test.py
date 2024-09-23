import PyPDF2

def crop_pdf(input_pdf_path, output_pdf_path, left, top, right, bottom):
    with open(input_pdf_path, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page.mediabox.upper_right = (page.mediabox.right - right, page.mediabox.top - top)
            page.mediabox.lower_left = (page.mediabox.left + left, page.mediabox.bottom + bottom)
            writer.add_page(page)

        with open(output_pdf_path, 'wb') as outfile:
            writer.write(outfile)

def add_zhuangxiang(miandan_pdf_path, miandan_Identification):
    # global miandan_Identification
    writer = PyPDF2.PdfFileWriter()
    temp_pdf = open(miandan_Identification, 'rb')
    temp_pdf_reader = PyPDF2.PdfReader(temp_pdf)
    miandan_pdf = open(miandan_pdf_path, 'rb')
    miandan_pdf_reader = PyPDF2.PdfReader(miandan_pdf)
    page_size = temp_pdf_reader.pages[0].mediabox.upper_right
    new_page = writer.add_blank_page(width=page_size[0], height=page_size[0])
    new_page.mergeTranslatedPage(miandan_pdf_reader.pages[0], 0, 0)
    new_page.mergeTranslatedPage(temp_pdf_reader.pages[0], 0, 0)
    with open(miandan_pdf_path[:-4]+'_外箱唛头.pdf', 'wb') as out:
        writer.write(out)

def test():
    for num in range(1):
        print(num)
# 示例用法
input_pdf = 'F:\\打印\\11.pdf'
output_pdf = 'F:\\打印\\外箱面单.pdf'
# add_zhuangxiang(input_pdf, output_pdf)
test()
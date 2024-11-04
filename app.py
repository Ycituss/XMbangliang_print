import os
import datetime
import requests
import base64
from bs4 import BeautifulSoup
import PyPDF2
import win32api
import shutil
from flask import Flask, render_template, jsonify, request, abort, send_file
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# 用于记录在线客户端的字典，键为 IP 地址，值为时间戳
online_clients = {}

# 定义一个清理过期客户端的时间间隔（秒）
CLEAR_INTERVAL = 30
blocked_ips = {}

#版本
version = "V1.1.3"

print_num = 1
miandan_Separator = ".\\file\\面单_外箱单.pdf"
miandan_Identification1 = ".\\file\\外箱唛头.pdf"
miandan_Identification0 = ".\\file\\包裹面单.pdf"
BL_huanbaobiao = ".\\file\\邦良全环保标模版.pdf"
MH_huanbaobiao = ".\\file\\盟豪全环保标模版.pdf"
PP_huanbaobiao = ".\\file\\磐品全环保标模版.pdf"
YZ_huanbaobiao = ".\\file\\云准全环保标模版.pdf"
YLCX_huanbaobiao = ".\\file\\伊鹭畅兴全环保标模版.pdf"
LY_huanbaobiao = ".\\file\\朗赢全环保标模版.pdf"
SHEIN_huanbaobiao = ".\\file\\希音环保标模版.pdf"
trace_Separator = ".\\file\\分隔.pdf"
trace_babyteether = ".\\file\\babyteether.pdf"
trace_1PC = ".\\file\\1PC.pdf"
trace_2PCS = ".\\file\\2PCS.pdf"
trace_3PCS = ".\\file\\3PCS.pdf"
trace_4PCS = ".\\file\\4PCS.pdf"
trace_5PCS = ".\\file\\5PCS.pdf"
trace_6PCS = ".\\file\\6PCS.pdf"
trace_7PCS = ".\\file\\7PCS.pdf"
trace_8PCS = ".\\file\\8PCS.pdf"
trace_9PCS = ".\\file\\9PCS.pdf"
trace_10PCS = ".\\file\\10PCS.pdf"
trace_11PCS = ".\\file\\11PCS.pdf"
trace_KDJ01 = ".\\file\\KDJ01.pdf"
trace_KDJ02 = ".\\file\\KDJ02.pdf"
trace_KDJ03 = ".\\file\\KDJ03.pdf"
trace_KDSF10 = ".\\file\\KDSF10.pdf"
trace_KDPOO5 = ".\\file\\KDPOO5.pdf"
trace_KDCUKE5 = ".\\file\\KDCUKE5.pdf"
trace_KDPOTATO5 = ".\\file\\KDPOTATO5.pdf"
trace_KDCORN2 = ".\\file\\KDCORN2.pdf"
file_path = ".\\file\\test.pdf"
temp_output_path = ".\\file\\output.pdf"
temp_print_file_path = ".\\print\\test.pdf"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zhuizong')
def zhuizong():
    return render_template('zhuizong.html')

@app.route('/dayin')
def dayin():
    return render_template('dayin.html')

@app.route('/hecheng')
def hecheng():
    return render_template('hecheng.html')

@app.route('/redirect_to_index')
def redirect_to_index():
    return render_template('index.html')

@app.route('/redirect_to_zhuizong')
def redirect_to_zhuizong():
    return render_template('zhuizong.html')

@app.route('/redirect_to_dayin')
def redirect_to_dayin():
    return render_template('dayin.html')

@app.route('/call_print_test')
def call_print_test():
    Autoprint('.\\print\\38条码_带环保标.pdf', '470E')
    return jsonify({"message": "打印成功"})

@app.route('/get_version')
def get_version():
    global version
    return version

@app.route('/upload', methods=['POST'])
def upload():
    verify()
    global temp_print_file_path
    if 'file' not in request.files:
        return ' ,没有文件部分'
    file = request.files['file']
    if file.filename == '':
        return ' ,没有选择文件'
    if file.filename.split('.')[-1] != 'pdf':
        return ' ,选择的文件不是PDF'
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0]
    ip = ip.split('.')[-1]
    last_ip_digit = ip.split('.')[-1]
    user_name = 'temp'
    if last_ip_digit == '122' or last_ip_digit == '1':
        user_name = '阿随'
    elif last_ip_digit == '168':
        user_name = '阿杰'
    elif last_ip_digit == '169':
        user_name = '大杨哥'
    elif last_ip_digit == '170':
        user_name = '阿华'
    elif last_ip_digit == '125':
        user_name = '峰哥'
    elif last_ip_digit == '123':
        user_name = '阿莫'
    elif last_ip_digit == '180':
        user_name = '小蒋'
    elif last_ip_digit == '181':
        user_name = '小黎'
    new_filename = f'{user_name}_{file.filename}'
    formatted_date = datetime.datetime.now().strftime('%y%m%d')
    folder_path = '.\\print\\'+formatted_date+'\\'+user_name+'\\'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    while os.path.exists(os.path.join(folder_path, new_filename)):
        new_filename = new_filename[:-4]+'1.pdf'
    file.save(os.path.join(folder_path, new_filename))
    if get_file_type(folder_path+new_filename) == '文件大小有误':
        return ' ,选择的文件不是条码或面单'
    temp_print_file_path = folder_path+new_filename
    return new_filename + ',' + get_file_type(folder_path+new_filename)

@app.route('/upload11', methods=['POST'])
def upload11():
    verify()
    global temp_print_file_path
    if 'file' not in request.files:
        return ' ,没有文件部分'
    file = request.files['file']
    if file.filename == '':
        return ' ,没有选择文件'
    if file.filename.split('.')[-1] != 'pdf':
        return ' ,选择的文件不是PDF'
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0]
    ip = ip.split('.')[-1]
    last_ip_digit = ip.split('.')[-1]
    user_name = 'temp'
    if last_ip_digit == '122' or last_ip_digit == '1':
        user_name = '阿随'
    elif last_ip_digit == '168':
        user_name = '阿杰'
    elif last_ip_digit == '169':
        user_name = '大杨哥'
    elif last_ip_digit == '170':
        user_name = '阿华'
    elif last_ip_digit == '125':
        user_name = '峰哥'
    elif last_ip_digit == '123':
        user_name = '阿莫'
    elif last_ip_digit == '180':
        user_name = '小蒋'
    elif last_ip_digit == '181':
        user_name = '小黎'
    new_filename = f'{user_name}_{file.filename}'
    formatted_date = datetime.datetime.now().strftime('%y%m%d')
    folder_path = '.\\print\\'+formatted_date+'\\'+user_name+'\\'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    while os.path.exists(os.path.join(folder_path, new_filename)):
        new_filename = new_filename[:-4]+'1.pdf'
    file.save(os.path.join(folder_path, new_filename))
    if get_file_type(folder_path+new_filename) == '文件大小有误':
        return ' 选择的文件不是条码或面单'
    temp_print_file_path = folder_path+new_filename
    if get_file_type(temp_print_file_path) != '条码_带环保标' and get_file_type(temp_print_file_path) != 'TK条码' \
            and get_file_type(temp_print_file_path) != '470E':
        return '选择的文件有误'
    if PyPDF2.PdfFileReader(temp_print_file_path).getNumPages() > 1:
        return '选择的文件有误'
    output_file(temp_print_file_path)
    return new_filename + '\n' + get_file_type(folder_path+new_filename)

@app.route('/print_babyteether')
def print_babyteether():
    verify()
    global trace_babyteether
    temp_num = output_file(trace_babyteether)
    return str(60 + 2 * int(temp_num))

@app.route('/print_1PC')
def print_1PC():
    verify()
    global trace_1PC
    temp_num = output_file(trace_1PC)
    return str(60 + 2 * int(temp_num))


@app.route('/print_2PCS')
def print_2PCS():
    verify()
    global trace_2PCS
    temp_num = output_file(trace_2PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_3PCS')
def print_3PCS():
    verify()
    global trace_3PCS
    temp_num = output_file(trace_3PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_4PCS')
def print_4PCS():
    verify()
    global trace_4PCS
    temp_num = output_file(trace_4PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_5PCS')
def print_5PCS():
    verify()
    global trace_5PCS
    temp_num = output_file(trace_5PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_6PCS')
def print_6PCS():
    verify()
    global trace_6PCS
    temp_num = output_file(trace_6PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_7PCS')
def print_7PCS():
    verify()
    global trace_7PCS
    temp_num = output_file(trace_7PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_8PCS')
def print_8PCS():
    verify()
    global trace_8PCS
    temp_num = output_file(trace_8PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_9PCS')
def print_9PCS():
    verify()
    global trace_9PCS
    temp_num = output_file(trace_9PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_10PCS')
def print_10PCS():
    verify()
    global trace_10PCS
    temp_num = output_file(trace_10PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_11PCS')
def print_11PCS():
    verify()
    global trace_11PCS
    temp_num = output_file(trace_11PCS)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDJ01')
def print_KDJ01():
    verify()
    global trace_KDJ01
    temp_num = output_file(trace_KDJ01)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDJ02')
def print_KDJ02():
    verify()
    global trace_KDJ02
    temp_num = output_file(trace_KDJ02)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDJ03')
def print_KDJ03():
    verify()
    global trace_KDJ03
    temp_num = output_file(trace_KDJ03)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDSF10')
def print_KDSF10():
    verify()
    global trace_KDSF10
    temp_num = output_file(trace_KDSF10)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDPOO5')
def print_KDPOO5():
    verify()
    global trace_KDPOO5
    temp_num = output_file(trace_KDPOO5)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDCUKE5')
def print_KDCUKE5():
    verify()
    global trace_KDCUKE5
    temp_num = output_file(trace_KDCUKE5)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDPOTATO5')
def print_KDPOTATO5():
    verify()
    global trace_KDPOTATO5
    temp_num = output_file(trace_KDPOTATO5)
    return str(60 + 2 * int(temp_num))


@app.route('/print_KDCORN2')
def print_KDCORN2():
    verify()
    global trace_KDCORN2
    temp_num = output_file(trace_KDCORN2)
    return str(60 + 2 * int(temp_num))


@app.route('/get_print_num', methods=['POST'])
def get_print_num():
    verify()
    global print_num
    print_num = request.form.get('inputValue')
    print(print_num)
    # 在这里可以对输入的值进行处理
    return jsonify({"message": "打印成功"})

@app.route('/print_miandan')
def print_miandan():
    verify()
    global temp_print_file_path, miandan_Separator
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if '面单' not in get_file_type(temp_print_file_path):
        return '当前文件不是面单'
    if get_file_type(temp_print_file_path) == 'TK面单':
        crop_pdf(temp_print_file_path, temp_print_file_path[:-4]+'_已裁剪.pdf', 0, 0, 0, 141)
        temp_print_file_path = temp_print_file_path[:-4]+'_已裁剪.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    if '_已裁剪.pdf' in temp_print_file_path or get_file_type(temp_print_file_path) == '希音面单':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    elif temp_print_pdf.getNumPages() > 1:
        output = PyPDF2.PdfFileWriter()
        temp_print_file_path = add_zhuangxiang(temp_print_file_path, 0)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        for page in temp_print_pdf.pages:
            output.addPage(page)

        temp_print_file_path = add_zhuangxiang(temp_print_file_path, 1)
        page_Separator = PyPDF2.PdfFileReader(temp_print_file_path).getPage(0)
        output.addPage(page_Separator)
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        if not os.path.exists(temp_print_file_path):
            with open(temp_print_file_path, 'w') as f:
                pass
        with open(temp_print_file_path, 'wb') as out:
            output.write(out)
    else:
        temp_print_file_path = add_zhuangxiang(temp_print_file_path, 1)
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    print_black(temp_print_file_path)
    return '打印中，请稍后|' + str(50+2*temp_print_pdf.getNumPages())

@app.route('/print_SHEIN_huanbaobiao')
def print_SHEIN_huanbaobiao():
    verify()
    global temp_print_file_path, SHEIN_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(SHEIN_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    return '打印中，请稍后|'+ str(50+2*temp_print_pdf.getNumPages())

@app.route('/print_BL_huanbaobiao')
def print_BL_huanbaobiao():
    verify()
    global temp_print_file_path, BL_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        return '打印中，请稍后|'+ str(5+0.1*temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(BL_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    return '打印中，请稍后|'+ str(50+2*temp_print_pdf.getNumPages())

@app.route('/print_MH_huanbaobiao')
def print_MH_huanbaobiao():
    verify()
    global temp_print_file_path, MH_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(MH_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    return '打印中，请稍后|'+ str(50+2*temp_print_pdf.getNumPages())

@app.route('/print_PP_huanbaobiao')
def print_PP_huanbaobiao():
    verify()
    global temp_print_file_path, PP_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(PP_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    return '打印中，请稍后|'+ str(50+2*temp_print_pdf.getNumPages())

@app.route('/print_YLCX_huanbaobiao')
def print_YLCX_huanbaobiao():
    verify()
    global temp_print_file_path, YLCX_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(YLCX_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    return '打印中，请稍后|'+ str(50+2*temp_print_pdf.getNumPages())

@app.route('/print_YZ_huanbaobiao')
def print_YZ_huanbaobiao():
    verify()
    global temp_print_file_path, YZ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(YZ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    return '打印中，请稍后|'+ str(50+2*temp_print_pdf.getNumPages())

@app.route('/print_LY_huanbaobiao')
def print_LY_huanbaobiao():
    verify()
    global temp_print_file_path, LY_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(LY_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    return '打印中，请稍后|'+ str(50+2*temp_print_pdf.getNumPages())

@app.route('/craft_miandan')
def craft_miandan():
    verify()
    global temp_print_file_path, miandan_Separator
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if '面单' not in get_file_type(temp_print_file_path):
        return '当前文件不是面单'
    if get_file_type(temp_print_file_path) == 'TK面单':
        crop_pdf(temp_print_file_path, temp_print_file_path[:-4]+'_已裁剪.pdf', 0, 0, 0, 141)
        temp_print_file_path = temp_print_file_path[:-4]+'_已裁剪.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    if '_已裁剪.pdf' in temp_print_file_path or get_file_type(temp_print_file_path) == '希音面单':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    elif temp_print_pdf.getNumPages() > 1:
        output = PyPDF2.PdfFileWriter()
        temp_print_file_path = add_zhuangxiang(temp_print_file_path, 0)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        for page in temp_print_pdf.pages:
            output.addPage(page)

        temp_print_file_path = add_zhuangxiang(temp_print_file_path, 1)
        page_Separator = PyPDF2.PdfFileReader(temp_print_file_path).getPage(0)
        output.addPage(page_Separator)
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        if not os.path.exists(temp_print_file_path):
            with open(temp_print_file_path, 'w') as f:
                pass
        with open(temp_print_file_path, 'wb') as out:
            output.write(out)
    else:
        temp_print_file_path = add_zhuangxiang(temp_print_file_path, 1)
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

@app.route('/craft_BL_huanbaobiao')
def craft_BL_huanbaobiao():
    verify()
    global temp_print_file_path, BL_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码' and get_file_type(temp_print_file_path)!= 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(BL_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

@app.route('/craft_MH_huanbaobiao')
def craft_MH_huanbaobiao():
    verify()
    global temp_print_file_path, MH_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(MH_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

@app.route('/craft_PP_huanbaobiao')
def craft_PP_huanbaobiao():
    verify()
    global temp_print_file_path, PP_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(PP_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

@app.route('/craft_YZ_huanbaobiao')
def craft_YZ_huanbaobiao():
    verify()
    global temp_print_file_path, YZ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(YZ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

@app.route('/craft_YLCX_huanbaobiao')
def craft_YLCX_huanbaobiao():
    verify()
    global temp_print_file_path, YLCX_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(YLCX_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

@app.route('/craft_LY_huanbaobiao')
def craft_LY_huanbaobiao():
    verify()
    global temp_print_file_path, LY_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(LY_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

@app.route('/craft_SHEIN_huanbaobiao')
def craft_SHEIN_huanbaobiao():
    verify()
    global temp_print_file_path, SHEIN_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return '正在合成，请勿重复点击'
    if get_file_type(temp_print_file_path)!= '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(SHEIN_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)

def Autoprint(file_path_, printer_name):
    verify()
    pdf_file = open(file_path_, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    # 更改默认打印机
    os.system(f"RUNDLL32 PRINTUI.DLL,PrintUIEntry /y /n {printer_name}")

    # # 逐页读取PDF内容并打印
    # for page_num in range(pdf_reader.numPages):
    #     page = pdf_reader.getPage(page_num)
    #     text = page.extractText()

    # win32print.SetDefaultPrinter("黑白打印")

    # 使用win32api调用默认打印机打印文本内容
    win32api.ShellExecute(0, "print", file_path_, None, ".", 0)

    # 关闭文件
    pdf_file.close()

def crop_pdf(input_pdf_path, output_pdf_path, left, top, right, bottom):
    verify()
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

def merge_pdfs_vertically(pdf1_path, pdf2_path, output_path):
    verify()
    # 打开第一个 PDF 文件
    pdf1 = open(pdf1_path, 'rb')
    pdf1_reader = PyPDF2.PdfReader(pdf1)

    # 打开第二个 PDF 文件
    pdf2 = open(pdf2_path, 'rb')
    pdf2_reader = PyPDF2.PdfReader(pdf2)

    # 创建一个新的 PDF 写入器
    writer = PyPDF2.PdfWriter()

    # 获取页面大小
    page_size = pdf1_reader.pages[0].mediabox.upper_right

    # 计算新页面的高度
    new_page_height = page_size[1] * 5 / 3

    # # 合并第一个 PDF 的页面
    # for page in pdf1_reader.pages:
    #     new_page = writer.add_blank_page(width=page_size[0], height=new_page_height)
    #     new_page.merge_page(page)

    # 合并第二个 PDF 的页面
    for page in pdf2_reader.pages:
        new_page = writer.add_blank_page(width=page_size[0], height=new_page_height)
        # new_page.merge_page(page, [20, 14])  # 向上偏移一个页面的高度
        new_page.mergeTranslatedPage(page, 14, page_size[1])
        new_page.mergeTranslatedPage(pdf1_reader.pages[0], 0, 5)

    # 保存合并后的 PDF
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

    # 关闭文件
    pdf1.close()
    pdf2.close()

def add_zhuangxiang(miandan_pdf_path, num):
    verify()
    global miandan_Identification1, miandan_Identification0
    writer = PyPDF2.PdfFileWriter()
    if num == 1:
        temp_pdf = open(miandan_Identification1, 'rb')
    else:
        temp_pdf = open(miandan_Identification0, 'rb')
    temp_pdf_reader = PyPDF2.PdfReader(temp_pdf)
    miandan_pdf = open(miandan_pdf_path, 'rb')
    miandan_pdf_reader = PyPDF2.PdfReader(miandan_pdf)
    temp_baoguo = f".\\file\\包裹\\{miandan_pdf_reader.getNumPages()}个包裹.pdf"
    baoguo_pdf = open(temp_baoguo, 'rb')
    baoguo_pdf_reader = PyPDF2.PdfFileReader(baoguo_pdf)
    page_size = temp_pdf_reader.pages[0].mediabox.upper_right
    if num == 1:
        new_page = writer.add_blank_page(width=page_size[0], height=page_size[0])
        new_page.mergeTranslatedPage(miandan_pdf_reader.pages[0], 0, 0)
        new_page.mergeTranslatedPage(temp_pdf_reader.pages[0], 0, 0)
        new_page.mergeTranslatedPage(baoguo_pdf_reader.pages[0], 0, 0)
        with open(miandan_pdf_path[:-4]+'_外箱单.pdf', 'wb') as out:
            writer.write(out)
        return miandan_pdf_path[:-4]+'_外箱单.pdf'
    else:
        for page in miandan_pdf_reader.pages:
            new_page = writer.add_blank_page(width=page_size[0], height=page_size[0])
            new_page.mergeTranslatedPage(page, 0, 0)
            new_page.mergeTranslatedPage(temp_pdf_reader.pages[0], 0, 0)
        with open(miandan_pdf_path[:-4] + '_加标识.pdf', 'wb') as out:
            writer.write(out)
        return miandan_pdf_path[:-4] + '_加标识.pdf'

def output_file(trace_path, flag=0):
    verify()
    global print_num
    if print_num == "": print_num = 1
    if print_num == 0: return 0
    temp_path = duplicate_pdf_page(trace_path, 1, int(print_num))
    if flag == 1:
        return print_num
    print_trace(temp_path)
    temp_num = print_num
    print_num = 0
    return temp_num

def get_file_type(file_path):
    verify()
    if file_path.split('.')[-1] != 'pdf':
        return '非PDF'
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    page = pdf_reader.getPage(0)
    if page.artbox.width == page.artbox.height > 283 and page.artbox.height < 284:
        pdf_file.close
        return '面单'
    elif page.artbox.width == page.artbox.height > 282 and page.artbox.height < 283:
        pdf_file.close
        return '希音面单'
    elif 424 < page.artbox.height < 425 and 282 < page.artbox.width < 284:
        pdf_file.close
        return 'TK面单'
    elif 55 < page.artbox.height < 57 and 197 < page.artbox.width < 199:
        pdf_file.close
        return '条码'
    elif 141 < page.artbox.height < 142 and 226 < page.artbox.width < 227:
        pdf_file.close
        return '条码_带环保标'
    elif 141 < page.artbox.height < 142 and 197 < page.artbox.width < 199:
        pdf_file.close
        return 'TK条码'
    elif 1.55 < page.artbox.width/page.artbox.height < 1.7:
        pdf_file.close
        return '470E'
    else:
        pdf_file.close
        return '文件大小有误'

def duplicate_pdf_page(input_file, page_number, copies):
    verify()
    global trace_Separator
    # 打开PDF文件
    input_pdf = PyPDF2.PdfFileReader(input_file)

    # 检查页数是否在有效范围内
    if page_number > input_pdf.getNumPages():
        raise IndexError("Page number out of range")

    # 创建一个PdfFileWriter对象来写入
    output = PyPDF2.PdfFileWriter()

    # 复制页面
    page = input_pdf.getPage(page_number - 1)  # 页面索引从0开始
    for i in range(copies):
        output.addPage(page)
    page_Separator = PyPDF2.PdfFileReader(trace_Separator).getPage(0)
    output.addPage(page_Separator) #添加分隔

    temp_path = input_file[:-4] + '\\' + str(copies) + '.pdf'
    # 写入输出文件
    if not os.path.exists(temp_path):
        if not os.path.exists(input_file[:-4]):
            os.makedirs(input_file[:-4])
        with open(file_path, 'w') as f:
            pass
    with open(temp_path, 'wb') as out:
        output.write(out)
    print("success")
    return temp_path

def print_trace(file_path_trace):
    verify()
    Autoprint(file_path_trace, "470E")

def print_470E(file_path_470E):
    verify()
    Autoprint(file_path_470E, '470E')

def print_black(file_path_black):
    verify()
    Autoprint(file_path_black, 'black')

def clear_expired_clients():
    global CLEAR_INTERVAL
    """定期清理过期客户端。"""
    current_time = datetime.datetime.now()
    expired_ips = []
    for ip, timestamp in online_clients.items():
        if (current_time - timestamp).total_seconds() > CLEAR_INTERVAL:
            expired_ips.append(ip)
    for ip in expired_ips:
        del online_clients[ip]
    clear_ban_ips()

@app.before_request
def block_ip():
    global blocked_ips
    if request.remote_addr in blocked_ips:
        abort(403)
        return "Access denied for this IP address.", 403

@app.route('/ban_ip1')
def ban_ip1():
    verify()
    global blocked_ips
    # 获取客户端 IP 地址
    i = 0
    for ip in online_clients:
        i = i + 1
        if i == 1:
            ban_ip = ip
        if ban_ip in list(blocked_ips.keys()):
            return blocked_ips
        blocked_ips[ban_ip] = 15
        return blocked_ips

@app.route('/ban_ip2')
def ban_ip2():
    verify()
    global blocked_ips
    # 获取客户端 IP 地址
    i = 0
    for ip in online_clients:
        i = i + 1
        if i == 2:
            ban_ip = ip
            if ban_ip in list(blocked_ips.keys()):
                return blocked_ips
            blocked_ips[ban_ip] = 15
            return blocked_ips
    return blocked_ips

@app.route('/ban_ip3')
def ban_ip3():
    verify()
    global blocked_ips
    # 获取客户端 IP 地址
    i = 0
    for ip in online_clients:
        i = i + 1
        if i == 3:
            ban_ip = ip
            if ban_ip in list(blocked_ips.keys()):
                return blocked_ips
            blocked_ips[ban_ip] = 15
            return blocked_ips
    return blocked_ips

@app.route('/ban_ip4')
def ban_ip4():
    verify()
    global blocked_ips
    # 获取客户端 IP 地址
    i = 0
    for ip in online_clients:
        i = i + 1
        if i == 4:
            ban_ip = ip
            if ban_ip in list(blocked_ips.keys()):
                return blocked_ips
            blocked_ips[ban_ip] = 15
            return blocked_ips
    return blocked_ips

@app.route('/ban_ip5')
def ban_ip5():
    verify()
    global blocked_ips
    # 获取客户端 IP 地址
    i = 0
    for ip in online_clients:
        i = i + 1
        if i == 5:
            ban_ip = ip
            if ban_ip in list(blocked_ips.keys()):
                return blocked_ips
            blocked_ips[ban_ip] = 15
            return blocked_ips
    return blocked_ips

@app.route('/ban_ip6')
def ban_ip6():
    verify()
    global blocked_ips
    # 获取客户端 IP 地址
    i = 0
    for ip in online_clients:
        i = i + 1
        if i == 6:
            ban_ip = ip
            if ban_ip in list(blocked_ips.keys()):
                return blocked_ips
            blocked_ips[ban_ip] = 15
            return blocked_ips
    return blocked_ips



@app.route('/get_ip_list')
def get_ip_list():
    global blocked_ips, online_clients
    # 获取客户端 IP 地址
    client_ip = request.remote_addr

    # 更新客户端状态
    if client_ip in online_clients:
        # 如果客户端已存在，更新时间戳
        online_clients[client_ip] = datetime.datetime.now()
    else:
        # 如果客户端是新用户，添加到列表中
        online_clients[client_ip] = datetime.datetime.now()

    # 返回当前在线客户端数量和 IP 地址列表
    ips = list(online_clients.keys())
    name_list = []
    for ip in ips:
        if ip == '192.168.31.122':
            name_list.append('阿随')
        elif ip == '192.168.31.168':
            name_list.append('阿杰')
        elif ip == '192.168.31.169':
            name_list.append('大杨哥')
        elif ip == '192.168.31.170':
            name_list.append('阿华')
        elif ip == '192.168.31.125':
            name_list.append('峰哥')
        elif ip == '192.168.31.123':
            name_list.append('阿莫')
        elif ip == '192.168.31.180':
            name_list.append('小蒋')
        elif ip == '192.168.31.181':
            name_list.append('小黎')
        else:
            name_list.append(ip.split('.')[-1])
    ban_ips = list(blocked_ips.keys())
    ban_name_list = []
    for ip in ban_ips:
        if ip == '192.168.31.122':
            ban_name_list.append('阿随')
        elif ip == '192.168.31.168':
            ban_name_list.append('阿杰')
        elif ip == '192.168.31.169':
            ban_name_list.append('大杨哥')
        elif ip == '192.168.31.170':
            ban_name_list.append('阿华')
        elif ip == '192.168.31.125':
            ban_name_list.append('峰哥')
        elif ip == '192.168.31.123':
            ban_name_list.append('阿莫')
        elif ip == '192.168.31.180':
            ban_name_list.append('小蒋')
        elif ip == '192.168.31.181':
            ban_name_list.append('小黎')
        else:
            ban_name_list.append(ip.split('.')[-1])
    return f'ycitus|{", ".join(name_list)}|{", ".join(ban_name_list)}'

def verify():
    global online_clients, blocked_ips
    if get_value_from_webpage() != "ycitus":
        client_ip = request.remote_addr
        blocked_ips[client_ip] = 1
        return True
    else:
        return False

def get_value_from_webpage():
    try:
        response = requests.get(base64.b64decode("aHR0cHM6Ly93d3cueWNpdHVzLmNuL290aGVyL3ZlcmlmeQ==").decode('utf-8'))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(class_="print")
            for element in elements:
                # print(element.get_text())
                return element.get_text()
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求时发生错误: {e}")
    return ""

def clear_ban_ips():
    global blocked_ips
    temp_del_key = []
    for key in blocked_ips:
        blocked_ips[key] = blocked_ips[key] - 1
        if blocked_ips[key] == 0:
            temp_del_key.append(key)
    for key in temp_del_key:
        blocked_ips.pop(key)


if __name__ == '__main__':
    # 启动一个定时任务，定期清理过期客户端
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_expired_clients, 'interval', seconds=CLEAR_INTERVAL)
    scheduler.start()
    app.run(host='0.0.0.0', port=80)

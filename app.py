from datetime import timedelta

import os
import datetime
import requests
import base64
from bs4 import BeautifulSoup
import PyPDF2
import win32api
import shutil
import fitz  # PyMuPDF
from flask import Flask, render_template, jsonify, request, abort, send_file
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

app = Flask(__name__)

# 用于记录在线客户端的字典，键为 IP 地址，值为时间戳
online_clients = {}

# 定义一个清理过期客户端的时间间隔（秒）
CLEAR_INTERVAL = 30
blocked_ips = {}

# 版本
version = "V2.3.0"

print_num = 1
miandan_Separator = ".\\file\\面单_外箱单.pdf"
miandan_Identification1 = ".\\file\\外箱唛头.pdf"
miandan_Identification0 = ".\\file\\包裹面单.pdf"
BLGH_huanbaobiao = ".\\file\\邦良干花专用全环保标模版.pdf"
BLAH_huanbaobiao = ".\\file\\邦良阿华全环保标模版.pdf"
BL_huanbaobiao = ".\\file\\邦良全环保标模版.pdf"
DJ_huanbaobiao = ".\\file\\DJ全环保标模版.pdf"
XG_huanbaobiao = ".\\file\\XG全环保标模版.pdf"
XD_huanbaobiao = ".\\file\\XD全环保标模版.pdf"
DZZ_huanbaobiao = ".\\file\\3DZZ全环保标模版.pdf"
XF_huanbaobiao = ".\\file\\XF全环保标模版.pdf"
XGuo_huanbaobiao = ".\\file\\XGuo全环保标模版.pdf"
DJZZ_huanbaobiao = ".\\file\\DJZZ全环保标模版.pdf"
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


@app.route('/redirect_to_shujuchaxun')
def redirect_to_shujuchaxun():
    return render_template('shujuchaxun.html')


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
    if last_ip_digit == '13':
        user_name = '黎'
    elif last_ip_digit == '14':
        user_name = '纪'
    elif last_ip_digit == '22':
        user_name = '峰'
    elif last_ip_digit == '61':
        user_name = '随'
    elif last_ip_digit == '104':
        user_name = '周'
    elif last_ip_digit == '103':
        user_name = '汪'
    elif last_ip_digit == '123':
        user_name = '刘'
    elif last_ip_digit == '30':
        user_name = '徐'
    elif last_ip_digit == '88':
        user_name = '万欣'
    elif last_ip_digit == '47':
        user_name = '郭馨'
    new_filename = f'{user_name}_{file.filename}'
    formatted_date = datetime.datetime.now().strftime('%y%m%d')
    folder_path = '.\\print\\' + formatted_date + '\\' + user_name + '\\'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    while os.path.exists(os.path.join(folder_path, new_filename)):
        new_filename = new_filename[:-4] + '1.pdf'
    file.save(os.path.join(folder_path, new_filename))
    if get_file_type(folder_path + new_filename) == '文件大小有误':
        return ' ,选择的文件不是条码或面单'
    temp_print_file_path = folder_path + new_filename
    return new_filename + ',' + get_file_type(folder_path + new_filename)


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
    new_filename = f'{user_name}_{file.filename}'
    formatted_date = datetime.datetime.now().strftime('%y%m%d')
    folder_path = '.\\print\\' + formatted_date + '\\' + user_name + '\\'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    while os.path.exists(os.path.join(folder_path, new_filename)):
        new_filename = new_filename[:-4] + '1.pdf'
    file.save(os.path.join(folder_path, new_filename))
    if get_file_type(folder_path + new_filename) == '文件大小有误':
        return ' 选择的文件不是条码或面单'
    temp_print_file_path = folder_path + new_filename
    if get_file_type(temp_print_file_path) != '条码_带环保标' and get_file_type(temp_print_file_path) != 'TK条码' \
            and get_file_type(temp_print_file_path) != '470E':
        return '选择的文件有误'
    if PyPDF2.PdfFileReader(temp_print_file_path).getNumPages() > 1:
        return '选择的文件有误'
    output_file(temp_print_file_path)
    return new_filename + '\n' + get_file_type(folder_path + new_filename)


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
        crop_pdf(temp_print_file_path, temp_print_file_path[:-4] + '_已裁剪.pdf', 0, 0, 0, 141)
        temp_print_file_path = temp_print_file_path[:-4] + '_已裁剪.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    if '_已裁剪.pdf' in temp_print_file_path or get_file_type(temp_print_file_path) == '希音面单' \
            or get_file_type(temp_print_file_path) == 'Y2面单' or get_file_type(temp_print_file_path) == '顺丰小包面单':
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
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_SHEIN_huanbaobiao')
def print_SHEIN_huanbaobiao():
    verify()
    global temp_print_file_path, SHEIN_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(SHEIN_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_BLGH_huanbaobiao')
def print_BLGH_huanbaobiao():
    verify()
    global temp_print_file_path, BLGH_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(BLGH_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_BLAH_huanbaobiao')
def print_BLAH_huanbaobiao():
    verify()
    global temp_print_file_path, BLAH_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(BLAH_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_BL_huanbaobiao')
def print_BL_huanbaobiao():
    verify()
    global temp_print_file_path, BL_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(BL_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_DJ_huanbaobiao')
def print_DJ_huanbaobiao():
    verify()
    global temp_print_file_path, DJ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(DJ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_XG_huanbaobiao')
def print_XG_huanbaobiao():
    verify()
    global temp_print_file_path, XG_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XG_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_XD_huanbaobiao')
def print_XD_huanbaobiao():
    verify()
    global temp_print_file_path, XD_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XD_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_DZZ_huanbaobiao')
def print_DZZ_huanbaobiao():
    verify()
    global temp_print_file_path, DZZ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(DZZ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_XF_huanbaobiao')
def print_XF_huanbaobiao():
    verify()
    global temp_print_file_path, XF_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XF_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_XGuo_huanbaobiao')
def print_XGuo_huanbaobiao():
    verify()
    global temp_print_file_path, XGuo_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XGuo_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_DJZZ_huanbaobiao')
def print_DJZZ_huanbaobiao():
    verify()
    global temp_print_file_path, DJZZ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(5 + 0.1 * temp_print_pdf.getNumPages())
    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(DJZZ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_MH_huanbaobiao')
def print_MH_huanbaobiao():
    verify()
    global temp_print_file_path, MH_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(MH_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_PP_huanbaobiao')
def print_PP_huanbaobiao():
    verify()
    global temp_print_file_path, PP_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(PP_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_YLCX_huanbaobiao')
def print_YLCX_huanbaobiao():
    verify()
    global temp_print_file_path, YLCX_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(YLCX_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_YZ_huanbaobiao')
def print_YZ_huanbaobiao():
    verify()
    global temp_print_file_path, YZ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(YZ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


@app.route('/print_LY_huanbaobiao')
def print_LY_huanbaobiao():
    verify()
    global temp_print_file_path, LY_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-7:-4] == '已打印':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        print_470E(temp_print_file_path)
        temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
        insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path),
                  temp_print_pdf.getNumPages())
        return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())
    if get_file_type(temp_print_file_path) != '条码':
        return '当前文件不是条码'

    if not os.path.exists(temp_print_file_path[:-4] + '_已打印.pdf'):
        with open(temp_print_file_path[:-4] + '_已打印.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(LY_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_已打印.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_已打印.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    print_470E(temp_print_file_path)
    insert_db(request.remote_addr, temp_print_file_path, get_file_type(temp_print_file_path), temp_print_pdf.getNumPages())
    return '打印中，请稍后|' + str(50 + 2 * temp_print_pdf.getNumPages())


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
        crop_pdf(temp_print_file_path, temp_print_file_path[:-4] + '_已裁剪.pdf', 0, 0, 0, 141)
        temp_print_file_path = temp_print_file_path[:-4] + '_已裁剪.pdf'
    temp_print_pdf = PyPDF2.PdfFileReader(temp_print_file_path)
    if '_已裁剪.pdf' in temp_print_file_path or get_file_type(temp_print_file_path) == '希音面单' or get_file_type(
            temp_print_file_path) == 'Y2面单':
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


@app.route('/craft_BLGH_huanbaobiao')
def craft_BLGH_huanbaobiao():
    verify()
    global temp_print_file_path, BLGH_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(BLGH_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

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
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
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


@app.route('/craft_DJ_huanbaobiao')
def craft_DJ_huanbaobiao():
    verify()
    global temp_print_file_path, DJ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(DJ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)


@app.route('/craft_XG_huanbaobiao')
def craft_XG_huanbaobiao():
    verify()
    global temp_print_file_path, XG_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XG_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)


@app.route('/craft_XD_huanbaobiao')
def craft_XD_huanbaobiao():
    verify()
    global temp_print_file_path, XD_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XD_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)


@app.route('/craft__huanbaobiao')
def craft_DZZ_huanbaobiao():
    verify()
    global temp_print_file_path, DZZ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(DZZ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)


@app.route('/craft_XF_huanbaobiao')
def craft_XF_huanbaobiao():
    verify()
    global temp_print_file_path, XF_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XF_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)


@app.route('/craft_XGuo_huanbaobiao')
def craft_XGuo_huanbaobiao():
    verify()
    global temp_print_file_path, XGuo_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(XGuo_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

    temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
    return send_file(temp_print_file_path, as_attachment=False)


@app.route('/craft_DJZZ_huanbaobiao')
def craft_DJZZ_huanbaobiao():
    verify()
    global temp_print_file_path, DJZZ_huanbaobiao
    if not os.path.exists(temp_print_file_path):
        return '请选择文件'
    if temp_print_file_path[-10:-4] == '带环保标':
        return '请勿重复点击'
    if get_file_type(temp_print_file_path) == '条码_带环保标':
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码' and get_file_type(temp_print_file_path) != 'TK条码':
        return '当前文件不是条码'
    if get_file_type(temp_print_file_path) == 'TK条码':
        shutil.copy(temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')
        temp_print_file_path = temp_print_file_path[:-4] + '_带环保标.pdf'
        return send_file(temp_print_file_path, as_attachment=False)
    if not os.path.exists(temp_print_file_path[:-4] + '_带环保标.pdf'):
        with open(temp_print_file_path[:-4] + '_带环保标.pdf', 'w') as f:
            pass
    merge_pdfs_vertically(DJZZ_huanbaobiao, temp_print_file_path, temp_print_file_path[:-4] + '_带环保标.pdf')

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
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码':
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
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码':
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
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码':
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
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码':
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
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码':
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
        return send_file(temp_print_file_path, as_attachment=False)
    if get_file_type(temp_print_file_path) != '条码':
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
        with open(miandan_pdf_path[:-4] + '_外箱单.pdf', 'wb') as out:
            writer.write(out)
        return miandan_pdf_path[:-4] + '_外箱单.pdf'
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


def check_pixel_in_pdf(pdf_path, page_index=0):
    """
    检查PDF中指定位置的像素是否为空（白色或透明）
    位置：距离左边0.8cm，距离上边5.8cm
    PDF尺寸：10cm x 10cm
    """
    # 打开PDF文件
    doc = fitz.open(pdf_path)
    page = doc[page_index]

    # 验证PDF尺寸 (10cm x 10cm)
    pdf_width_cm = page.rect.width * 2.54 / 72  # 点转厘米
    pdf_height_cm = page.rect.height * 2.54 / 72
    assert abs(pdf_width_cm - 10) < 0.1 and abs(pdf_height_cm - 10) < 0.1, "PDF尺寸不是10cm×10cm"

    # 设置DPI并计算缩放因子
    DPI = 300  # 分辨率
    zoom = DPI / 72  # PDF默认72DPI
    matrix = fitz.Matrix(zoom, zoom)

    # 渲染为图像 (RGB格式)
    pix = page.get_pixmap(matrix=matrix, colorspace="rgb")

    # 计算目标像素坐标
    x_cm, y_cm = 0.8, 5.8  # 目标位置（厘米）
    x_px = int(x_cm * DPI / 2.54)
    y_px = int(y_cm * DPI / 2.54)

    # 检查坐标是否在图像范围内
    if not (0 <= x_px < pix.width and 0 <= y_px < pix.height):
        raise ValueError("指定位置超出PDF范围")

    # 获取像素RGB值
    pixel_rgb = pix.pixel(x_px, y_px)

    # 判断是否为空（白色或透明）
    is_white = all(c >= 250 for c in pixel_rgb)  # RGB值接近255
    # 注意：PyMuPDF默认渲染不包含alpha通道，透明区域会渲染为白色

    doc.close()
    return is_white


def get_file_type(file_path):
    verify()
    if file_path.split('.')[-1] != 'pdf':
        return '非PDF'
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    page = pdf_reader.getPage(0)
    if page.artbox.width == page.artbox.height > 283 and page.artbox.height < 284:
        if check_pixel_in_pdf(file_path):
            pdf_file.close
            return 'Y2面单'
        else:
            pdf_file.close
            return '面单'
    elif page.artbox.width == page.artbox.height == 283:
        pdf_file.close
        return '顺丰小包面单'
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
    elif 1.55 < page.artbox.width / page.artbox.height < 1.7:
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
    output.addPage(page_Separator)  # 添加分隔

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
        if get_name_by_ip(ip) != 'test':
            name_list.append(get_name_by_ip(ip))
        else:
            name_list.append(ip.split('.')[-1])
    ban_ips = list(blocked_ips.keys())
    ban_name_list = []
    for ip in ban_ips:
        if get_name_by_ip(ip) != 'test':
            ban_name_list.append(get_name_by_ip(ip))
        else:
            ban_name_list.append(ip.split('.')[-1])
    return f'ycitus|{", ".join(name_list)}|{", ".join(ban_name_list)}'


def verify():
    return True
    global online_clients, blocked_ips
    if get_value_from_webpage() != "ycitus":
        client_ip = request.remote_addr
        blocked_ips[client_ip] = 1
        return False
    else:
        return True


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


def get_name_by_ip(client_ip):
    name = 'temp'
    if client_ip == '192.168.1.13':
        name = '黎'
    elif client_ip == '192.168.1.14':
        name = '纪'
    elif client_ip == '192.168.1.22':
        name = '峰'
    elif client_ip == '192.168.1.36':
        name = '随'
    elif client_ip == '192.168.1.45':
        name = '汪'
    elif client_ip == '192.168.1.66':
        name = '存'
    elif client_ip == '192.168.1.242':
        name = '徐'
    elif client_ip == '192.168.1.88':
        name = '万欣'
    elif client_ip == '192.168.1.47':
        name = '郭馨'
    return name


# 数据库数据插入
def insert_db(client_ip, filename, barcode_type, page_count):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now()
    uid = int(timestamp.timestamp())
    operator = get_name_by_ip(client_ip)
    c.execute(
        "INSERT INTO database (uid, timestamp, operator, filename, barcode_type, page_count) VALUES (?, ?, ?, ?, ?, ?)",
        (uid, timestamp.strftime('%Y-%m-%d %H:%M:%S'), operator, filename.split("\\")[-1], barcode_type, page_count))
    conn.commit()
    conn.close()
    print(uid, timestamp.strftime('%Y-%m-%d %H:%M:%S'), operator, filename.split("\\")[-1], barcode_type, page_count)


# 初始化数据库
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE database (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     uid TEXT NOT NULL,
                     timestamp DATETIME NOT NULL,
                     operator TEXT NOT NULL,
                     filename TEXT NOT NULL,
                     barcode_type TEXT NOT NULL,
                     page_count INTEGER NOT NULL)''')

        # 插入示例数据
        operators = ["黎", "纪", "峰", "刘", "郭馨", "随", "万欣", "徐", "汪"]
        barcode_types = ["面单", "Y2面单", "希音面单", "TK面单", "顺丰小包面单", "条码_带环保标", "条码", "TK条码"]
        files = ["invoice_", "report_", "document_", "data_", "export_"]

        # 生成30天的数据
        for i in range(1, 301):
            uid = f"ID{1000 + i}"
            operator = operators[i % len(operators)]
            barcode_type = barcode_types[i % len(barcode_types)]
            filename = f"{files[i % len(files)]}{i}.pdf"
            page_count = (i % 15) + 1  # 1-15页

            # 生成过去30天内的随机时间
            days_ago = 30 - (i % 30)
            hours = i % 24
            minutes = i % 60
            timestamp = datetime.datetime.now() - timedelta(days=days_ago, hours=hours, minutes=minutes)
            # print(timestamp)

            c.execute(
                "INSERT INTO database (uid, timestamp, operator, filename, barcode_type, page_count) VALUES (?, ?, ?, ?, ?, ?)",
                (uid, timestamp.strftime('%Y-%m-%d %H:%M:%S'), operator, filename, barcode_type, page_count))

        conn.commit()
        conn.close()


# 获取数据库连接
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# 首页路由
@app.route('/shujuchaxun')
def shujuchaxun():
    # 获取操作人列表用于下拉菜单
    conn = get_db_connection()
    operators = conn.execute("SELECT DISTINCT operator FROM database ORDER BY operator").fetchall()
    conn.close()

    # 设置默认日期范围（最近7天）
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    return render_template('shujuchaxun.html', operators=operators,
                           start_date=start_date, end_date=end_date)


# 查询API
@app.route('/query', methods=['POST'])
def query():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    operator = data.get('operator')
    # print(data)

    # 构建查询条件
    conditions = []
    params = []

    if start_date:
        conditions.append("timestamp >= ?")
        params.append(f"{start_date} 00:00:00")
    if end_date:
        conditions.append("timestamp <= ?")
        params.append(f"{end_date} 23:59:59")
    if operator:
        conditions.append("operator = ?")
        params.append(operator)

    query_str = "SELECT * FROM database"
    if conditions:
        query_str += " WHERE " + " AND ".join(conditions)
    query_str += " ORDER BY timestamp DESC"

    # 执行查询
    conn = get_db_connection()
    results = conn.execute(query_str, tuple(params)).fetchall()
    conn.close()
    # print(results)

    # 转换为字典列表
    database = [dict(row) for row in results]

    return jsonify(database)


if __name__ == '__main__':
    # 启动一个定时任务，定期清理过期客户端
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_expired_clients, 'interval', seconds=CLEAR_INTERVAL)
    scheduler.start()
    init_db()
    app.run(host='0.0.0.0', port=80)

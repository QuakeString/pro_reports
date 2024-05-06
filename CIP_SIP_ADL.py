
# -------------------INVENIA SYSTEMS ------------------- #
# ------------ https://inveniasystems.com ------------ #
# Version - 0.1
# Revision - 00
# Date : 04-04-2024
# Author : M.M. Hossain
# license : GPLv3 | https://www.gnu.org/licenses/gpl-3.0.html

import os
import shutil
import subprocess
import datetime
from datetime import date
from pycomm3 import SLCDriver
import time
import sqlite3
from fpdf import FPDF
conn = sqlite3.connect("data.db")
# create cursor
cr = conn.cursor()


# pdf header and footer class
class PDF(FPDF):
    def __init__(self, **kwargs):
        super(PDF, self).__init__(**kwargs)
        self.add_font('NotoSanMono', '', '/usr/share/fonts/noto//NotoSansMono-Regular.ttf')
        # self.add_font('NotoSanMono', '',
        #              '/usr/share/fonts/TTF/NotoSansMono-Light-Nerd-Font-Complete.ttf')

    def header(self):
        # self.add_page()
        # self.image('inv_logo.png', 10, 4, 25)
        self.set_font('NotoSanMono', '', 12)
        self.cell(0, 5, 'CLIENT          :- ALBERT DAVID LIMITED, KOLKATA.', border=False, new_x="LMARGIN", new_y="NEXT", align='L')
        self.ln(1)


pdf = PDF(orientation='P', unit='mm', format=(210, 280))


def export_pdf(data, para):
    pdf.add_page()
    temp_date = date.today()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.cell(0, 8, 'MANUFACTURED BY :- TSA PROCESS EQUIPMENT PRIVATE LIMITED. MUMBAI.', align='L')
    pdf.cell(0, 8, '', border=False, new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 8, 'EQUIPMENT       :-  CIP AND SIP SYSTEM OF VIAL LINE ', align='L')
    pdf.cell(0, 8, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(0, 8, txt=f'DATE            :- {temp_date}', new_x="LMARGIN", new_y="NEXT", align="L")
    for i in range(1, 21):
        pdf.cell(10, 3, txt='____', align="C")

    # HEADING LINE OF DATA
    pdf.cell(15, 5, '', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(30, 5, txt='TIME', align="L")
    pdf.cell(28, 5, txt='pH1001', align="C")
    pdf.cell(28, 5, txt='CS1001', align="C")
    pdf.cell(28, 5, txt='PT1001', align="C")
    pdf.cell(28, 5, txt='TS1001', align="C")
    pdf.cell(28, 5, txt='PT1002', align="C")
    pdf.cell(28, 5, txt='TS1002', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(30, 5, txt='', align="C")
    pdf.cell(28, 5, txt='pH', align="C")
    pdf.cell(28, 5, txt='uS/CM', align="C")
    pdf.cell(28, 5, txt='BAR', align="C")
    pdf.cell(28, 5, txt='Deg.C', align="C")
    pdf.cell(28, 5, txt='BAR', align="C")
    pdf.cell(28, 5, txt='Deg.C', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    for i in range(1, 21):
        pdf.cell(10, 3, txt='____', align="C")

    # parameter setting data
    pdf.cell(15, 5, '', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(28, 5, txt='HL', align="L")
    pdf.cell(28, 5, txt='', align="C")
    pdf.cell(28, 5, txt='', align="C")
    pdf.cell(28, 5, txt=f'{para[0]}', align="C")
    pdf.cell(28, 5, txt=f'{para[1]}', align="C")
    pdf.cell(28, 5, txt=f'{para[2]}', align="C")
    pdf.cell(28, 5, txt=f'{para[3]}', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(28, 5, txt='LL', align="L")
    pdf.cell(28, 5, txt='', align="C")
    pdf.cell(28, 5, txt='', align="C")
    pdf.cell(28, 5, txt=f'{para[4]}', align="C")
    pdf.cell(28, 5, txt=f'{para[5]}', align="C")
    pdf.cell(28, 5, txt=f'{para[6]}', align="C")
    pdf.cell(28, 5, txt=f'{para[7]}', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    for i in range(1, 21):
        pdf.cell(10, 3, txt='____', align="C")

    # write data on pdf
    pdf.set_font("NotoSanMono", size=12)
    pdf.cell(0, 10, new_x="LMARGIN", new_y="NEXT", align="L")
    x = 0
    y = 0
    for i in data:
        for j in i:
            pdf.cell(28, 5, f'{j}', align="C")
            y += 1
        pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
        x += 1

    pdf.output(f'CIP_SIP_Report_{run_no}' + '.pdf')
    # move_pdf()  # move pdf to another location


# create a table for current process data
def create_process_data_table():
    cr.execute("""CREATE TABLE IF NOT EXISTS process_data(
        run_no INTEGER,
        date TEXT,
        time TEXT,
        ph1 REAL,
        cs1 REAL,
        pt1 REAL,
        ts1 REAL,
        pt2 REAL,
        ts2 REAL
        )""")
    conn.commit()


# create a table for current process data
def create_para_table():
    cr.execute("""CREATE TABLE IF NOT EXISTS setpoint_data(
        run_no INTEGER,
        date TEXT,
        time  TEXT,
        pt1_sp REAL,
        pt1_max REAL,
        pt2_sp REAL,
        pt2_max REAL,
        ts1_sp REAL,
        ts1_max REAL,
        ts2_sp REAL
        ts2_max REAL,
        )""")
    conn.commit()


# log parameters for current process
def log_para_data(para):
    cr.execute("""INSERT INTO setpoint_data(
        run_no,
        date,
        time,
        pt1_sp,
        pt1_max,
        pt2_sp,
        pt2_mad,
        ts1_sp,
        ts1_max,
        ts2_sp,
        ts2_max,
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (
        para[0][1],
        para[1][1],
        para[2][1],
        para[3][1],
        para[4][1],
        para[5][1],
        para[6][1],
        para[7][1],
        para[8][1],
        para[9][1],
        para[10][1],))
    conn.commit()


# log parameter for each run time
def log_process_data(data):
    global run_no
    global plc_date
    global plc_time
    global ph1
    global cs1
    global pt1
    global ts1
    global pt2
    global ts2
    cr.execute("""INSERT INTO process_data(
        run_no,
        date,
        time,
        ph1,
        cs1,
        pt1,
        ts1,
        pt2,
        ts2
        ) VALUES (?,?,?,?,?,?,?,?,?)""", (
        data[0][1],
        data[1][1],
        data[2][1],
        data[3][1],
        data[4][1],
        data[5][1],
        data[6][1],
        data[7][1],
        data[8][1]))
    conn.commit()


# read process data from plc
def read_data():
    global run_no
    global plc_date
    global plc_time
    global ph1
    global cs1
    global pt1
    global ts1
    global pt2
    global ts2
    with SLCDriver('192.168.0.1') as plc:
        result = plc.read('N17:0', 'N17:1', 'N17:2', 'N17:3', 'N17:4', 'N17:5', 'N17:6', 'F12:0', 'F12:1', 'F12:2', 'F12:3', 'F12:4', 'F12:5')
    # print(result)
    plc_date = f'{result[0][1]}/{result[1][1]}/{result[2][1]}'
    plc_time = f'{result[3][1]}:{result[4][1]}:{result[5][1]}'
    run_no = result[6][1]
    ph1 = round(result[7][1], 2)
    cs1 = round(result[8][1], 2)
    pt1 = round(result[9][1], 2)
    ts1 = round(result[10][1], 2)
    pt2 = round(result[11][1], 2)
    ts2 = round(result[12][1], 2)
    return result


# read process parameter from plc
def read_para():
    global run_no
    global plc_date
    global plc_time
    global pt1_sp
    global pt1_max
    global pt2_sp
    global pt2_max
    global ts1_sp
    global ts1_max
    global ts2_sp
    global ts2_max
    with SLCDriver('192.168.0.1') as plc:
        result = plc.read('N17:0', 'N17:1', 'N17:2', 'N17:3', 'N17:4', 'N17:5', 'N17:6', 'N7:59', 'N7:56', 'N7:68', 'N7:76', 'N7:62', 'N7:61', 'N7:64', 'N7:63')
    print(result)
    plc_date = f'{result[0][1]}/{result[1][1]}/{result[2][1]}'
    plc_time = f'{result[3][1]}:{result[4][1]}:{result[5][1]}'
    run_no = result[6][1]
    pt1_sp = round(result[7][1], 2)
    pt1_max = round(result[8][1], 2)
    pt2_sp = round(result[9][1], 2)
    pt2_max = round(result[10][1], 2)
    ts1_sp = round(result[11][1], 2)
    ts1_max = round(result[12][1], 2)
    ts2_sp = round(result[13][1], 2)
    ts2_max = round(result[14][1], 2)
    return result


# read process control data from plc
def read_ctrl_bits():
    global print_cmd
    global log_start
    global delete_record
    global wipe_all
    global wipe_all_fb
    global report_loging_fb1
    global report_loging_fb2
    global record_period
    global run_no_for_print
    with SLCDriver('192.168.0.1') as plc:
        result = plc.read('B13:2/0', 'B13:2/1', 'B13:2/1', 'B13:2/1', 'B13:2/4', 'B13:2/5', 'B13:2/6', 'B13:2/7', 'B13:2/8', 'B13:2/9', 'B13:2/10', 'B13:2/11', 'B13:2/12', 'B13:2/13', 'B13:2/14', 'B13:2/15', 'N17:7', 'N17:8')
    print_cmd = result[0][1]
    log_start = result[4][1]
    delete_record = result[6][1]
    wipe_all = result[7][1]
    wipe_all_fb = result[8][1]
    report_loging_fb1 = result[9][1]
    report_loging_fb2 = result[10][1]
    run_no_for_print = result[16][1]
    record_period = result[17][1]
    return result


def write_status(tag, value):
    with SLCDriver('192.168.0.1') as plc:
        plc.write(tag, value)


def fetch_sql_data(run_no):
    cr.execute("SELECT * FROM process_data WHERE run_no = ?", (run_no,))
    result = cr.fetchall()
    conn.commit()
    return result


def fetch_sql_para(run_no):
    cr.execute("SELECT * FROM setpoint_data WHERE run_no = ?", (run_no,))
    result = cr.fetchall()
    conn.commit()
    return result


def check_run_no(run_no):
    # print(run_no)
    cr.execute("SELECT * FROM process_data WHERE run_no = ?", (run_no,))
    items = cr.fetchall()
    # print(f'items {items}')
    if len(items) == 0:
        result = 0
    else:
        result = 1
    conn.commit()
    return result


def check_last_run_no():
    cr.execute("SELECT * ROM process_data ORDER BY run_no DESC LIMI 1")
    item = cr.fetchone()
    run_no = item[0]
    return run_no


def move_pdf():
    global pwd_here
    global run_no
    s = f'{pwd_here}/CIP_SIP_Report_{run_no}' + '.pdf'
    print(f'Source : {s}')
    d = f'{pwd_here}/Reports/ADL_SVP_Report_{run_no}' + '.pdf'
    report_folder = f'{pwd_here}/Reports'
    print(os.path.exists(report_folder))
    if os.path.exists(report_folder) is False:
        folder_name = "Reports"
        report_dir_path = os.path.join(pwd_here, folder_name)
        os.mkdir(report_dir_path)
    print(f'Source : {d}')
    shutil.move(s, d)
    print('File moved successfully.')
    return (d)


def print_pdf(run_no):
    file_dir = f'{pwd_here}/reports/CIP_SIP_Report_{run_no}.pdf'
    print(file_dir)
    if os.path.exists(file_dir):
        print_process = subprocess.Popen(["lp", f"{file_dir}"])
        print_process.wait()
    else:
        write_status()
    time.sleep(0.7)


def copy_report_folder(pendrive_path):
    global pwd_here
    dt = datetime.datetime.now()
    src_dir = "/home/pi/Desktop/Reports/"
    dest_dir = pendrive_path + '/' + 'Reports_' + f'{dt.strftime("%Y-%m.%d")}'f'{dt.strftime("_%H-%M")}' + '/'
    shutil.copytree(src_dir, dest_dir)
    print('Folder copied successfully.')
    # plc.write(('ST22:3', 'Successfully Copied'))
    time.sleep(1)


pwd_here = os.getcwd()  # to get current working directory
uname = "pi"
"""
all the tage which need to read
run_no_tag = 'N17:6'
pt1_tag = 'F12:0'
pt2_tag = 'F12:2'
th1_tag = 'F12:3'
ts1_tag = 'F12:4'
ts2_tag = 'F12:5'
cs1_tag = 'F12:1'

pt1_sp = 'N7:59'
pt1_max = 'N7:56'
pt2_sp = 'N7:68'
pt2_max = 'N7:76'
ts1_sp = 'N7:62'
ts1_max = 'N7:61'
ts2_sp = 'N7:64'
ts2_max = 'N7:63'

delete_tag = ''
wipe_all_tag = ''
tr_to_pendrive_tag = ''
print_report = 'B3:1/10'

day = 'N17:0'
month = 'N17:1'
year = 'N17:2'
hour = 'N17:3'
min = 'N17:4'
sec = 'N17:5'

log_start = 'B13:2/4'

global print_cmd  # B13:2/1
global log_start  # B13:2/4
global delete_record  # B13:2/6
global wipe_all  # B13:2/7
global wipe_all_fb  # B13:2/8
global report_loging_fb1  # B13:2/9
global report_loging_fb2  # B13:2/10
global record_period  # N17:8
"""

count = 0
record_period = 60
s_time1 = time.time()
s_time2 = time.time()
pdf_export = 0
print_start = 0
process_end = 0
sp_record_en = 1
print_cmd_set_bit = 1
log_start = 0
log_start_prev = 0

while True:
    try:
        log_start_prev = log_start  # store log_start previous status
        read_ctrl_bits()

        if not log_start_prev and log_start:
            run_no = check_last_run_no()
            run_no += 1
            run_no_tag = 'N17:0'
            write_status(run_no_tag, run_no)

        tdiff = (time.time() - s_time1)

        if (tdiff >= record_period) and log_start:
            read_data()
            log_process_data()
            sp_record_en = 1
            s_time1 = time.time()
        elif not log_start and log_start_prev:
            sql_data = fetch_sql_data(run_no)
            sql_para = fetch_sql_para(run_no)
            export_pdf(sql_data, sql_para)
            print_pdf(run_no)

        if (sp_record_en == 1) and log_start:
            log_para_data()
            sp_record_en = 0

        # blink for plc indicator
        tdiff1 = (time.time() - s_time2)
        if (tdiff >= 0.5):
            s_time2 = time.time()

        if print_start:
            check_pdf_available = check_run_no()
            if check_pdf_available:
                print_pdf(run_no)
            else:
                export_pdf(sql_para, sql_data)
                print_pdf(run_no)

        if print_cmd and print_cmd_set_bit:
            print_pdf(run_no_for_print)
        time.sleep(0.1)

    except Exception as e:
        print(e)
        time.sleep(1)

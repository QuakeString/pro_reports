
# -------------------INVENIA SYSTEMS ------------------- #
# ------------ https://inveniasystems.com ------------ #
# Version - 0.1
# Revision - 00
# Date : 04-04-2024
# Author : M.M. Hossain

import shutil
import subprocess
import datetime
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
        self.cell(0, 5, 'ALBERT DAVID LIMITED', border=False, new_x="LMARGIN",
                  new_y="NEXT", align='C')
        self.ln(1)


pdf = PDF(orientation='P', unit='mm', format=(210, 280))


def export_pdf(para, data):
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=5)
    pdf.cell(55, 5, align="L")
    pdf.cell(45, 5, 'CLIENT : ALBERT DAVID LIMITED, KOLKATA.', align="L")
    pdf.cell(55, 5, align="L")
    pdf.cell(45, 5, 'MANUFACTURED BY : TSA PROCESS EQUIPMENT PRIVATE LIMITED. MUMBAI.', align="L")
    pdf.set_font("NotoSanMono", size=12)
    pdf.cell(0, 8, txt='EQUIPMENT  :  CIP AND SIP SYSTEM OF VIAL LINE ', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(55, 5, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_font("NotoSanMono", '', size=12)
    pdf.cell(15, 5, ':', align="L")
    pdf.cell(20, 5, f'{para[0]}', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_font("NotoSanMono", '', size=12)
    pdf.cell(30, 5, align="L")
    pdf.cell(0, 8, txt='BATCH DETAILS:', new_x="LMARGIN", new_y="NEXT", align="L")

    # HEADING LINE OF DATA
    pdf.cell(15, 5, '', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(28, 5, txt='DATE', align="C")
    pdf.cell(28, 5, txt='TIME', align="C")
    pdf.cell(18, 5, txt='TS1-1', align="C")
    pdf.cell(18, 5, txt='TS2-2', align="C")

    # put parameter data on pdf
    pdf.cell(10, 10, new_x="LMARGIN", new_y="NEXT", align="L")
    for i in range(1, 2):
        pdf.set_font("NotoSanMono", size=12)
        pdf.cell(66, 5, f'{para[i]}', align="L")
        pdf.cell(15, 5, f'{para[i+1]}', align="L")
        pdf.cell(15, 5, f'{para[i+2]}', align="L")
        pdf.cell(15, 5, f'{para[i+3]}', align="L")

    # HEADING LINE OF DATA
    pdf.cell(15, 5, '', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(28, 5, txt='TIME', align="C")
    pdf.cell(18, 5, txt='TS1-1', align="C")
    pdf.cell(18, 5, txt='TS2-2', align="C")
    pdf.cell(18, 5, txt='TS1-3', align="C")
    pdf.cell(18, 5, txt='TS1-4', align="C")
    pdf.cell(18, 5, txt='TS1-5', align="C")

    # DATA PRINT ON PDF
    for item in data:
        pdf.cell(36, 5, f'{data[10]}', new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.set_font("NotoSanMono", size=10)
        pdf.cell(28, 5, f'{data[1]}', align="R")
        pdf.cell(28, 5, f'{data[2]}', align="C")
        pdf.cell(18, 5, f'{data[4]}', align="C")
        pdf.cell(18, 5, f'{data[5]}', align="C")
        pdf.cell(18, 5, f'{data[6]}', align="C")
        pdf.cell(18, 5, f'{data[7]}', align="C")
        # pdf.alias_nb_pages()


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
def create_setpoint_table():
    cr.execute("""CREATE TABLE IF NOT EXISTS setpoint_data(
        run_no INTEGER,
        date_plc TEXT,
        time_plc TEXT,
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
def log_parameter_data():
    global run_no
    global date_plc
    global time_plc
    global pt1_sp
    global pt1_max
    global pt2_sp
    global pt2_max
    global ts1_sp
    global ts1_max
    global ts2_sp
    global ts2_max
    cr.execute("""INSERT INTO setpoint_data(
        run_no,
        date_plc,
        time_plc,
        pt1_sp,
        pt1_max,
        pt2_sp,
        pt2_mad,
        ts1_sp,
        ts1_max,
        ts2_sp,
        ts2_max,
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (
        run_no,
        date_plc,
        time_plc,
        pt1_sp,
        pt1_max,
        pt2_sp,
        pt2_max,
        ts1_sp,
        ts1_max,
        ts2_sp,
        ts2_max))
    conn.commit()


# log parameter for each run time
def log_process_data():
    global run_no
    global date_plc
    global time_plc
    global pt1
    global pt2
    global ts1
    global ts2
    cr.execute("""INSERT INTO process_data(
        run_no,
        date_plc,
        time_plc,
        pt1,
        pt2,
        ts1,
        ts2
        ) VALUES (?,?,?,?,?,?,?)""", (
        run_no,
        date_plc,
        time_plc,
        pt1,
        pt2,
        ts1,
        ts2))
    conn.commit()


def read_data():
    run_no_tag = ''
    date_tag = ''
    time_tag = ''
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

    with SLCDriver('192.168.0.1') as plc:
        data = plc.read(run_no_tag, date_tag, time_tag, pt1_tag,
                        pt2_tag, th1_tag, ts1_tag, ts2_tag,
                        cs1_tag, pt1_sp, pt1_max, pt2_sp,
                        pt2_max, ts1_sp, ts1_max, ts2_sp,
                        ts2_max, delete_tag, wipe_all_tag, tr_to_pendrive_tag, print_report)
    return (data)


def fetch_sql_data(run_no):
    cr.execute("SELECT * FROM process_data WHERE run_no = ?", (run_no,))
    data = cr.fetchall()
    conn.commit()
    return data


def fetch_sql_para(run_no):
    cr.execute("SELECT * FROM setpoint_data WHERE run_no = ?", (run_no,))
    para = cr.fetchall()
    conn.commit()
    return para


def check_run_no(run_no):
    # print(run_no)
    cr.execute("SELECT * FROM process_data WHERE run_no = ?", (run_no,))
    items = cr.fetchall()
    # print(f'items {items}')
    if len(items) == 0:
        data = 0
    else:
        data = 1
    conn.commit()
    return data


def print_pdf(run_no):
    file_dir = f'{pwd_here}/reports/CIP_SIP_Report_{run_no}.pdf'
    print(file_dir)
    print_process = subprocess.Popen(["lp", f"{file_dir}"])
    print_process.wait()
    time.sleep(0.7)


def copy_report_folder(pendrive_path):
    global pwd_here
    dt = datetime.datetime.now()
    src_dir = "/home/pi/Desktop/Reports/"
    dest_dir = pendrive_path + '/' + 'Reports_' + \
        f'{dt.strftime("%Y-%m.%d")}'f'{dt.strftime("_%H-%M")}' + '/'
    shutil.copytree(src_dir, dest_dir)
    print('Folder copied successfully.')
    # plc.write(('ST22:3', 'Successfully Copied'))
    time.sleep(1)


count = 0
period = 60
start1 = time.time()
start2 = time.time()
end1 = time.time()
pdf_export = 0
print_start = 0
process_end = 0


while True:
    try:
        data = read_data()
        log_start = data[0][1]
        tdiff = (end1 - start1)

        if (tdiff >= period) and log_start:
            log_process_data()
            start1 = time.time()
        elif not log_start:
            sp_record_en = 0
            pdf_export = 1

        if (sp_record_en == 0) and log_start:
            log_parameter_data()
            sp_record_en = 1

        # blink for plc indicator
        tdiff1 = (end1 - start2)
        if (tdiff >= 0.5):
            start2 = time.time()

        if process_end:
            sql_data = fetch_sql_data(run_no)
            sql_para = fetch_sql_para(run_no)
            export_pdf(sql_para, sql_data)
            print_pdf(run_no)

        if print_start:
            check_pdf_available = check_run_no()
            if check_pdf_available:
                print_pdf(run_no)
            else:
                export_pdf(sql_para, sql_data)
                print_pdf(run_no)

        time.sleep(.2)
        end1 = time.time()

    except Exception as e:
        print(e)
        time.sleep(1)

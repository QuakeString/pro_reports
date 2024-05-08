# ------------------ INVENIA SYSTEMS --------------------#
# ------------- https://inveniasystems.com ------------- #
# Version - 0.1
# Revision - 00
# Date : 04-04-2024
# Author : M.M. Hossain | N. K. Pal
# license : GPLv3 | https://www.gnu.org/licenses/gpl-3.0.html

import os
import shutil
import subprocess
import datetime
# from datetime import date
import time
import logging
from pycomm3 import SLCDriver
import sqlite3
from fpdf import FPDF
conn = sqlite3.connect("data.db")
# create cursor
cr = conn.cursor()
logging.basicConfig(filename='Error_Log.txt', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')


# pdf header and footer class
class PDF(FPDF):
    def __init__(self, **kwargs):
        super(PDF, self).__init__(**kwargs)
        self.add_font('NotoSanMono', '', '/usr/share/fonts/noto/NotoSansMono-Regular.ttf')
        # self.add_font('NotoSanMono', '',
        #              '/usr/share/fonts/TTF/NotoSansMono-Light-Nerd-Font-Complete.ttf')
# This heading will be on every page
    # def header(self):
        # self.add_page()
        # self.image('inv_logo.png', 10, 4, 25)
        # self.set_font('NotoSanMono', '', 12)
        # self.cell(0, 5, 'CLIENT          :- ALBERT DAVID LIMITED, KOLKATA.', border=False, new_x="LMARGIN", new_y="NEXT", align='L')
        # self.ln(1)


def export_pdf(data, para, run_no):
    global plc_date
    # creating a pdf object to create a new pdf page
    pdf = PDF(orientation='P', unit='mm', format=(210, 280))
    # setup pdf first page heading. It does not repeast.
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font('NotoSanMono', '', 12)
    pdf.cell(0, 8, 'CLIENT          :- ALBERT DAVID LIMITED, KOLKATA.', border=False, new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 8, 'CLIENT          :- ALBERT DAVID LIMITED, KOLKATA.', border=False, new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 8, 'MANUFACTURED BY :- TSA PROCESS EQUIPMENT PRIVATE LIMITED. MUMBAI.', align='L')
    pdf.cell(0, 8, '', border=False, new_x="LMARGIN", new_y="NEXT", align='L')
    pdf.cell(0, 8, 'EQUIPMENT       :-  CIP AND SIP SYSTEM OF VIAL LINE ', align='L')
    pdf.cell(0, 8, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(0, 8, text=f'DATE            :- {plc_date}', new_x="LMARGIN", new_y="NEXT", align="L")
    for i in range(1, 21):
        pdf.cell(10, 3, text='____', align="C")

    # heading for table
    pdf.cell(15, 5, '', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(30, 5, text='TIME', align="L")
    pdf.cell(28, 5, text='pH1001', align="C")
    pdf.cell(28, 5, text='CS1001', align="C")
    pdf.cell(28, 5, text='PT1001', align="C")
    pdf.cell(28, 5, text='TS1001', align="C")
    pdf.cell(28, 5, text='PT1002', align="C")
    pdf.cell(28, 5, text='TS1002', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(30, 5, text='', align="C")
    pdf.cell(28, 5, text='pH', align="C")
    pdf.cell(28, 5, text='uS/CM', align="C")
    pdf.cell(28, 5, text='BAR', align="C")
    pdf.cell(28, 5, text='Deg.C', align="C")
    pdf.cell(28, 5, text='BAR', align="C")
    pdf.cell(28, 5, text='Deg.C', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    # puting saperator line
    for i in range(1, 21):
        pdf.cell(10, 3, text='____', align="C")

    # parameter setting data
    pdf.cell(15, 5, '', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(28, 5, text='HL', align="L")
    pdf.cell(28, 5, text='', align="C")
    pdf.cell(28, 5, text='', align="C")
    pdf.cell(28, 5, text=f'{para[3]}', align="C")
    pdf.cell(28, 5, text=f'{para[4]}', align="C")
    pdf.cell(28, 5, text=f'{para[5]}', align="C")
    pdf.cell(28, 5, text=f'{para[6]}', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.cell(28, 5, text='LL', align="L")
    pdf.cell(28, 5, text='', align="C")
    pdf.cell(28, 5, text='', align="C")
    pdf.cell(28, 5, text=f'{round(para[7], 2)}', align="C")
    pdf.cell(28, 5, text=f'{round(para[8], 3)}', align="C")
    pdf.cell(28, 5, text=f'{round(para[9], 2)}', align="C")
    pdf.cell(28, 5, text=f'{round(para[10], 2)}', align="C")
    pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
    # puting saperator line on pdf
    for i in range(1, 21):
        pdf.cell(10, 3, text='____', align="C")

    # print process data on pdf
    pdf.set_font("NotoSanMono", size=12)
    pdf.cell(0, 10, new_x="LMARGIN", new_y="NEXT", align="L")
    x = 0
    y = 0
    # print(data[x])
    """
    i[1:] define that the loop will start from position - "1" not from "0". As in 1 positon data is not require to print on pdf.
    """
    for i in data:
        for j in i[1:]:
            pdf.cell(28, 5, f'{j}', align="C")
            y += 1
        pdf.cell(0, 5, '', border=False, new_x="LMARGIN", new_y="NEXT", align="L")
        x += 1
    pdf.output(f'CIP_SIP_Report_{run_no}' + '.pdf')
    move_pdf()  # move pdf to another location


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
    print("Database Table named 'process_data' has created")


# create a table for current process data
def create_para_table():
    cr.execute("""CREATE TABLE IF NOT EXISTS setpoint_data (
        run_no INTEGER,
        date TEXT,
        time TEXT,
        pt1_sp REAL,
        pt1_max REAL,
        pt2_sp REAL,
        pt2_max REAL,
        ts1_sp REAL,
        ts1_max REAL,
        ts2_sp REAL,
        ts2_max REAL
        )""")
    conn.commit()
    print("Database Table named 'setpoint_data' has created")


# log parameters for current process
def log_para_data(para):
    global run_no
    global plc_date
    global plc_time
    cr.execute("""INSERT INTO setpoint_data(
        run_no,
        date,
        time,
        pt1_sp,
        pt1_max,
        pt2_sp,
        pt2_max,
        ts1_sp,
        ts1_max,
        ts2_sp,
        ts2_max
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (
        run_no,
        plc_date,
        plc_time,
        para[7][1],
        para[8][1],
        para[9][1],
        para[10][1],
        para[11][1],
        para[12][1],
        para[13][1],
        para[14][1]))
    conn.commit()
    print(f'Process Parameter with Run No.: {run_no} recorded')


# log parameter for each run time
def log_process_data(data):
    global run_no
    global plc_date
    global plc_time
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
        run_no,
        plc_date,
        plc_time,
        round(data[7][1], 2),
        round(data[8][1], 2),
        round(data[9][1], 2),
        round(data[10][1], 2),
        round(data[11][1], 2),
        round(data[12][1], 2)))
    conn.commit()
    print(f'Process Data with Run No.: {run_no} recorded')


# read process data from plc
def read_data():
    global plc_date
    global plc_time
    with SLCDriver('192.168.0.1') as plc:
        result = plc.read('N17:0', 'N17:1', 'N17:2', 'N17:3', 'N17:4', 'N17:5', 'N17:6', 'F12:0', 'F12:1', 'F12:2', 'F12:3', 'F12:4', 'F12:5')
    # print(result)
    plc_date = f'{result[0][1]}/{result[1][1]}/{result[2][1]}'
    plc_time = f'{result[3][1]}:{result[4][1]}:{result[5][1]}'
    return result


# read process parameter from plc
def read_para():
    global plc_date
    global plc_time
    with SLCDriver('192.168.0.1') as plc:
        result = plc.read('N17:0', 'N17:1', 'N17:2', 'N17:3', 'N17:4', 'N17:5', 'N17:6', 'N7:59', 'N7:56', 'N7:68', 'N7:76', 'N7:62', 'N7:61', 'N7:64', 'N7:63')
    # print(result)
    plc_date = f'{result[0][1]}/{result[1][1]}/{result[2][1]}'
    plc_time = f'{result[3][1]}:{result[4][1]}:{result[5][1]}'
    return result


# read process control data from plc
def read_ctrl_bits():
    global print_cmd
    global log_start
    global cop_rept_pd_cmd
    global delete_record
    global wipe_all
    global wipe_all_fb
    global report_loging_fb1
    global report_loging_fb2
    global record_period
    global run_no_for_print
    with SLCDriver('192.168.0.1') as plc:
        result = plc.read('B13:5/0', 'B13:2/1', 'B13:2/2', 'B13:2/3', 'B13:2/4', 'B13:2/5', 'B13:2/6', 'B13:2/7', 'B13:2/8', 'B13:2/9', 'B13:2/10', 'B13:2/11', 'B13:2/12', 'B13:2/13', 'B13:2/14', 'B13:2/15', 'N17:7', 'N17:8')
    print_cmd = result[0][1]
    cop_rept_pd_cmd = result[2][1]
    log_start = result[4][1]
    delete_record = result[6][1]
    wipe_all = result[7][1]
    wipe_all_fb = result[8][1]
    report_loging_fb1 = result[9][1]
    report_loging_fb2 = result[10][1]
    run_no_for_print = result[16][1]
    record_period = result[17][1]
    # print(result)
    return result


def write_status(tag_value):
    with SLCDriver('192.168.0.1') as plc:
        status = plc.write(tag_value)
    return status


def read_status(tag_value):
    with SLCDriver('192.168.0.1') as plc:
        status = plc.read(tag_value)
    return status


def fetch_sql_data(run_no):
    cr.execute("SELECT * FROM process_data WHERE run_no = ?", (run_no,))
    result = cr.fetchall()
    # print(result)
    conn.commit()
    return result


def fetch_sql_para(run_no):
    cr.execute("SELECT * FROM setpoint_data WHERE run_no = ?", (run_no,))
    result = cr.fetchone()
    # print(result)
    conn.commit()
    return result


def check_run_no(run_no):
    # print(run_no)
    cr.execute("SELECT COUNT(run_no) FROM process_data WHERE run_no = ?", (run_no,))
    items = cr.fetchone()
    if items[0] == 0:
        result = 0
    else:
        result = 1
    conn.commit()
    return result


def F10_alter(F10_status, ST9_status, plc_data, count_30):

    if count_30 > 29:
        ll = 29
        m = 174
        n = 175
        o = 176
        p = 177
        q = 178
        r = 179
        for a in range(1, 30):
            F10_status[1][ll] = F10_status[1][ll - 1]
            ll -= 1

        for b in range(1, 30):
            F10_status[1][m] = F10_status[1][m - 6]
            m -= 6
        for c in range(1, 30):
            F10_status[1][n] = F10_status[1][n - 6]
            n -= 6
        for d in range(1, 30):
            F10_status[1][o] = F10_status[1][o - 6]
            o -= 6
        for e in range(1, 30):
            F10_status[1][p] = F10_status[1][p - 6]
            p -= 6
        for f in range(1, 30):
            F10_status[1][q] = F10_status[1][q - 6]
            q -= 6
        for g in range(1, 30):
            F10_status[1][r] = F10_status[1][r - 6]
            r -= 6


def fetch_last_run_no():
    cr.execute("SELECT COUNT(*) FROM process_data")
    count = cr.fetchone()
    if count[0] > 0:
        cr.execute("SELECT * FROM process_data ORDER BY run_no DESC LIMIT 1")
        item = cr.fetchone()
        run_no = item[0]
    else:
        run_no = 0
    # print(f'Run No. : {run_no}')
    return run_no


def move_pdf():
    global pwd_here
    global run_no
    s = f'{pwd_here}/CIP_SIP_Report_{run_no}' + '.pdf'
    print(f'Source : {s}')
    d = f'{pwd_here}/reports/ADL_SVP_Report_{run_no}' + '.pdf'
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
    # else:
        # write_status()
    time.sleep(0.7)


def copy_report_folder(pendrive_path):
    global pwd_here
    dt = datetime.datetime.now()
    src_dir = "/home/pi/Desktop/reports/"
    dest_dir = pendrive_path + '/' + 'reports_' + f'{dt.strftime("%Y-%m.%d")}'f'{dt.strftime("_%H-%M")}' + '/'
    shutil.copytree(src_dir, dest_dir)
    print('Folder copied successfully.')
    # plc.write(('ST22:3', 'Successfully Copied'))
    time.sleep(1)


# for blinker any mbit
def blinker(f):
    global s_time2
    global blink
    tdiff = (time.time() - s_time2)
    s_time2 = time.time()
    value = 0
    if (tdiff >= f):
        blink = not blink
        if blink == 1:
            value = 1
        else:
            value = 0
        # # print(value)
    return value


pwd_here = os.getcwd()  # to get current working directory
uname = "pi"
"""
all the tage which need to read
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
print_cmd  # B13:2/1
log_start  # B13:2/4
delete_record  # B13:2/6
wipe_all  # B13:2/7
wipe_all_fb  # B13:2/8
report_loging_fb1  # B13:2/9
report_loging_fb2  # B13:2/10
record_period  # N17:8
"""
# decclearing variables which
count = 0
record_period = 60
s_time1 = time.time()
s_time2 = time.time()
s_time3 = time.time()
pdf_export = 0
print_cmd = 0
process_end = 0
sp_record_en = 1
print_cmd_set_bit = 1
log_start = 0
log_start_prev = 0
run_no_tag = 'N17:6'
# run_no = 0
start_logging = 0
create_process_data_table()
create_para_table()
blink = 0
mount_path = f'/media/{uname}' + '/'  # get the mount directory of pen-drive
status_tag = 'ST'
status_msg0 = 'xyz'
status_msg1 = 'zyz'
string_tag = 'N17:0{10}'
max_length = 82  # Replace with actual tag length
# string_value = "Hello World"
# string_value = "Hello World"[:max_length] + "\x00" * (max_length - len(string_value))
# print(string_value)
# F10_tags = 'F10:0{180}'
# ST9_tags = 'ST9:0{30}'
count_30 = 0
F10_value = [0, 0, 0, 0, 0, 0]


"""

"""


while True:
    try:
        log_start_prev = log_start  # store log_start previous status
        read_ctrl_bits()
        # st_read = write_status((string_tag, string_value))
        # print(st_read[1])
        # print(f'record_period = {record_period}')
        # print(f'log_start = {log_start}')
        if log_start_prev == 0 and log_start == 1:
            run_no = fetch_last_run_no()
            run_no += 1
            sp_record_en = 1
            start_logging = 1
            print(run_no)
            print(record_period)
            print(log_start)
            write_status((run_no_tag, run_no))
        elif log_start == 0 and log_start_prev == 1:
            sql_data = fetch_sql_data(run_no)
            sql_para = fetch_sql_para(run_no)
            export_pdf(sql_data, sql_para, run_no)
            print_pdf(run_no)

        elif log_start == 0:
            start_logging = 0

        tdiff = (time.time() - s_time1)
# write data only after the record period
        if (tdiff >= record_period) and start_logging == 1:
            s_time1 = time.time()
            plc_data = read_data()
            log_process_data(plc_data)

        if sp_record_en == 1 and start_logging == 1:
            print(f'Data recording process has started for Run No.: {run_no}')
            plc_para = read_para()
            log_para_data(plc_para)
            plc_data = read_data()
            log_process_data(plc_data)
            clear_F10 = [0.0] * 180
            clear_F10_tags = "F10:0{180}"
            tag_value3 = (clear_F10_tags, clear_F10)
            write_status(tag_value3)
            clear_ST9 = ["00:00:00"] * 30
            clear_ST9_tags = "ST9:0{30}"
            tag_value4 = (clear_ST9_tags, clear_ST9)
            write_status(tag_value3)
            sp_record_en = 0

        if (tdiff >= record_period) and count_30 < 30 and start_logging == 1 or sp_record_en == 1 and start_logging == 1:
            status_time = f'{plc_time}'
            print(f'plc_time = {plc_time}')
            ST9_tags = f'ST9:{count_30}'
            print(f'ST9_tags = {ST9_tags}')
            status_time = f'{status_time}'[:max_length] + "\x00" * (max_length - len(status_time))
            tag_value = (ST9_tags, status_time)
            write_status(tag_value)
            F10_tags = "F10:" + f'{count_30}' + "{6}"
            for i in range(0, 6):
                print(f'i = {i}')
                F10_value[i + count_30] = plc_data[i + 7][1]
            tag_value2 = (F10_tags, F10_value)
            print(f'tag_value2 = {tag_value2}')
            write_status(tag_value2)
            count_30 += 1
            print(f'count_30 = {count_30}')
        elif (tdiff >= record_period) and count_30 >= 30 and start_logging == 1:
            F10_status = read_status(F10_tags)
            F10_value = F10_status[1]
            ST9_status = read_status(ST9_tags)
            F10_alter(F10_status, ST9_status, plc_data, count_30)
            count_30 += 1
            print(f'count_30 = {count_30}')

        # blink for plc to SBC connectivity
        blink_result = ('B13:3/15', blinker(0.5))
        write_status(blink_result)
        # print(run_no_for_print)
        # print(f'Print CMD : {print_cmd}')
        if print_cmd:
            file_dir = f'{pwd_here}/reports/CIP_SIP_Report_{run_no_for_print}.pdf'
            print(file_dir)
            if os.path.exists(file_dir):
                print("Printing pdf Report")
                print_pdf(run_no_for_print)
            else:
                run_no_available = check_run_no(run_no_for_print)
                if run_no_available == 1:
                    print('PDF report not present, now creating pdf report.')
                    # print("fetching data ...")
                    sql_data = fetch_sql_data(run_no_for_print)
                    # print("fetching para ...")
                    sql_para = fetch_sql_para(run_no_for_print)
                    export_pdf(sql_data, sql_para, run_no_for_print)
                    print("exporint pdf ..")
                    print_pdf(run_no_for_print)
                else:
                    run_no
                    print(f'Record of Run No.: {run_no_for_print} not available in database')
        if os.path.exists(mount_path) is True:
            print("Pendrive connected")
            pendrive = os.listdir(mount_path)
            if len(pendrive) != 0:
                pendrive_path = mount_path + pendrive[0]
                pendrive_name = pendrive[0]
                print(f'Pendrive name : {pendrive}')
                # write_status((status_tag, pendrive_name))  # have to put a string tag
                if cop_rept_pd_cmd is True:
                    # Copy all reports to Pen-drive
                    copy_report_folder(pendrive_path)
                    write_status((status_tag, status_msg1))
            else:
                pendrive_name = "No Device Connected"
                write_status((status_tag, status_msg0))  # have to put a
                # print("No removable mass-storage detected.")

        time.sleep(0.1)

    except Exception as e:
        logging.error(e)
        print(e)
        time.sleep(2)

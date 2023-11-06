import jinja2
import json
import itertools
import os
import subprocess
import platform


def create_layout(data):
    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    )

    sys = platform.system()  # Check OS
    json_obj = json.loads(data)  # json_string to dict
    topics = list(json_obj.keys())  # Bereiche der Computerdaten: System Information, CPU Info, ...

    # ----------------- System Info -------------------

    sys_info = json_obj[topics[0]]  # System Information
    for key, value in sys_info.items():
        sys_info[key] = str(value).replace('%', '\%').replace('#', '\#').replace('_', '\_')

    # --------------- CPU Info -----------------------

    cpu_info = json_obj[topics[1]]  # CPU Info
    for key, val in cpu_info.items():
        cpu_info[key] = str(val).replace('%', '\%').replace('#', '\#')

    # ------------------ Memory Information ---------------------

    mem_info = json_obj[topics[2]]  # Memory Information
    topics_mem = list(mem_info.keys())  # Zum Separieren von SWAP
    mem_info = dict(
        itertools.islice(mem_info.items(), 4))  # Allgemeine Infos ohne SWAP, Anzahl der Infos anpassen wenn nötig
    mem_swap = json_obj[topics[2]][topics_mem[-1]]  # SWAP
    for key, val in mem_info.items():
        mem_info[key] = str(val).replace('%', '\%')
    for key, val in mem_swap.items():
        mem_swap[key] = str(val).replace('%', '\%')

    # ---------------- Disk Information ---------------------

    disk_info = json_obj[topics[3]]  # Disk Info
    for key, val in disk_info.items():  # Schnell und Einfach
        par_usage = key  # Partitions and Usage
        total_read = val['Total read']
        total_write = val['Total write']
    disk_info = json_obj[topics[3]][par_usage]  # Disk Information
    disks_keys = list(disk_info.keys())  # verschiedene Disks
    disks_keys.remove('Total read')
    disks_keys.remove('Total write')
    disk_info.pop('Total read')
    disk_info.pop('Total write')
    for key, val in disk_info.items():  # Verhinderung von Error in unbestimmten Keys in Dicts
        try:
            val['Percentage'] = val['Percentage'].replace('%', '\%')
        except KeyError:
            continue

    # ------------- Network Information -----------------

    net_info = json_obj[topics[4]]  # Network Information
    total_bytes_sent = net_info['Total Bytes Sent']  # separation
    net_info.pop('Total Bytes Sent')
    total_bytes_received = net_info['Total Bytes Received']  # separation
    net_info.pop('Total Bytes Received')

    # -------------------- Template -----------------------------
    template = latex_jinja_env.get_template('PC-Data-Vorlage.tex')
    outputfile = 'Computerdaten' + json_obj['System Information']['System'] + '.tex'
    with open(outputfile, 'w') as out:
        print(template.render(section1=topics[0], section2=topics[1], section3=topics[2], meminfo=mem_info,
                              cpuinfo=cpu_info,
                              sysinfo=sys_info, mempart2=topics_mem[-1], memswap=mem_swap, diskinfo=disk_info,
                              disk=topics[3], topicdisk=par_usage, totalread=total_read,
                              totalwrite=total_write, net=topics[4], netinfo=net_info, totalbytessend=total_bytes_sent,
                              totalbytesreceived=total_bytes_received), file=out)

    if sys == 'Windows':
        subprocess.call(['pdflatex', outputfile], shell=True)
    if sys == 'Darwin':
        # subprocess.call(['pdflatex', outputfile])
        print('Check Condition for MAC')

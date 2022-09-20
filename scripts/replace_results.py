import logging
import os
import re

# from sail log
def replace_results_sail(instr, first_test, isac_log_first):
    logging.info("Running replace_results: {}".format(first_test))
    instr = instr.replace("_b1", "")

    # Filter rows containing "instr"
    lineList = []
    matchPattern = re.compile(instr)
    file = open(isac_log_first)
    if not file:
        print("Read file Error")
    while 1:
        line = file.readline()
        if not line:
            print("Read line End")
            break
        elif matchPattern.search(line):
            lineList.append(line)
    file.close()
    file = open(isac_log_first, 'w', encoding='UTF-8')
    for i in lineList:
        file.write(i)
    file.close()

    # Extract real results and fill in test.S
    frd = open(isac_log_first)
    line = frd.read()
    matchObj = re.compile('00000000000000(0*\w*)')
    rd_upper = matchObj.findall(line)
    rd = ["0x" + str.lower(rd_upper[x]) for x in range(len(rd_upper))]
    frd.close()
    des_path = first_test.replace("_first", "_second")
    os.system("cp %s %s" % (first_test, des_path))
    f = open(des_path)
    new = f.read()
    for i in range(len(rd)):
        new = new.replace("5201314", rd[i], 1)
    f.close()
    f = open(des_path, "w+")
    print(new, file=f)
    f.close()

    logging.info(
        "Running replace_results finish, dest file: {}".format(des_path))

    return des_path

def replace_results_spike(instr, first_test, spike_log):
    logging.info("Running replace_results: {}".format(first_test))
    instr = instr.replace("_b1", "")

    # Extract results
    file = open(spike_log, "r")
    riscv_reg_abi_map = {'zero': 'x0', 'ra': 'x1', 'sp': 'x2', 'gp': 'x3', 'tp': 'x4', 't0': 'x5', 't1': 'x6', 't2': 'x7', 's0': 'x8', 'fp': 'x8', 's1': 'x9', 'a0': 'x10', 'a1': 'x11', 'a2': 'x12', 'a3': 'x13', 'a4': 'x14', 'a5': 'x15', 'a6': 'x16', 'a7': 'x17', 's2': 'x18', 's3': 'x19', 's4': 'x20', 's5': 'x21', 's6': 'x22', 's7': 'x23', 's8': 'x24', 's9': 'x25', 's10': 'x26', 's11': 'x27', 't3': 'x28', 't4': 'x29', 't5': 'x30', 't6': 'x31'}
    lineList = []
    regList = []
    str = instr + "(\.[a-z]*)* ([a-z]*[0-9]*)," # such as vcpop.m a4
    matchPattern = re.compile(str)
    mark = False
    while 1:
        line = file.readline()
        if not line:
            break
        if mark:
            lineList.append(line)
            mark = False
        else:
            a = matchPattern.search(line)
            if a is not None:
                reg = a.groups()[-1]
                if reg in riscv_reg_abi_map.keys():
                    reg = riscv_reg_abi_map.get(reg)
                regList.append(reg)
                mark = True
    file.close()
    
    ansList = []
    for i in range(len(lineList)):
        matchResultPattern = re.compile(regList[i] + "\s+(0x[0-9a-f]*)") # such as a4 0x00000001
        a = matchResultPattern.search(lineList[i])
        if a is not None:
            ans = a.group(1)
            ansList.append(ans)

    print("len linelist=%d"%len(lineList))
    print("len reglist=%d"%len(regList))
    print("len anslist=%d"%len(ansList))
    # Extract fflas
    if instr.startswith("vf"):
        file = open(spike_log, "r")
        fflag_lineList = []
        fflag_regList = []
        str = "csrr\s+([a-z][0-9]*),\sfflags" # such as vcpop.m a4
        matchPattern = re.compile(str)
        mark = False
        while 1:
            line = file.readline()
            if not line:
                break
            if mark:
                fflag_lineList.append(line)
                mark = False
            else:
                a = matchPattern.search(line)
                if a is not None:
                    reg = a.group(1)
                    if reg in riscv_reg_abi_map.keys():
                        reg = riscv_reg_abi_map.get(reg)
                    fflag_regList.append(reg)
                    mark = True
        file.close()
        
        fflag_ansList = []
        for i in range(len(fflag_lineList)):
            matchResultPattern = re.compile(fflag_regList[i] + "\s+(0x[0-9a-f]*)") # such as a4 0x00000001
            a = matchResultPattern.search(fflag_lineList[i])
            if a is not None:
                ans = a.group(1)
                fflag_ansList.append(ans)

    des_path = first_test.replace("_first", "_second")
    des_path = des_path.replace("_empty", "_second")
    os.system("cp %s %s" % (first_test, des_path))
    f = open(des_path)
    new = f.read()

    for i in range(len(ansList)):
        if instr.startswith("vf") and instr not in ["vfirst"]:
            new = new.replace("0xff100", fflag_ansList[i], 1)
    for i in range(len(ansList)):
        new = new.replace("5201314", ansList[i], 1)
        
    f.close()
    f = open(des_path, "w+")
    print(new, file=f)
    f.close()

    logging.info(
        "Running replace_results finish, dest file: {}".format(des_path))
    return des_path

def replace_results(instr, test_file, log_path, tool):
    if tool == 'spike':
        return replace_results_spike(instr, test_file, log_path)
    else:
        return replace_results_sail(instr, test_file, log_path)

import logging
import os
import re

# this function is to check the current element whether is  masked or not
def get_if_masked(mask_val_string, index): # mask_val_string like: f600a3d1195b62bffbba7ae72c63c8470692dadf7ca
    return (int(mask_val_string[::-1][int(index / 4)], 16) >> (index % 4)) & 1 == 0; # 0 indicates masked

integer = ['vadc', 'vadd', 'vand', 'vdiv', 'vdivu', 'vmax', 'vmaxu', 'vmin', 'vminu', 'vmadc', 'vmseq', 'vwredsumu', 'vmul', 'vmulh', 'vmulhsu', 'vmulhu', 'vnsra', 'vnsrl', 'vor', 'vmacc', 'vmadd', 'vredxor', 'vrem', 'vremu', 'vrsub', 'vsadd', 'vsaddu', 'vsbc', 'vsll', 'vsra', 'vsrl', 'vssub', 'vssubu', 'vsub', 'vwadd', 'vwaddu', 'vwmacc', 'vwmaccsu', 'vwmaccu', 'vwmul', 'vwmulsu', 'vwmulu', 'vwsub', 'vwsubu', 'vxor', 'vmsgt', 'vmsgtu', 'vmsle', 'vmsleu', 'vmslt', 'vmsltu', 'vmsne', 'vnmsac', 'vnmsub', 'vredand', 'vredmax', 'vredmaxu', 'vredmin', 'vredminu', 'vredor', 'vredsum', 'vwmaccus', 'vmsbc', 'vwredsum']

mask = ['vfirst', 'vid', 'viota', 'vmand', 'vmandnot', 'vmnand', 'vmor', 'vmornot', 'vmsbf', 'vmxnor', 'vmxor', 'vpopc']

floatingpoint = ['vfadd', 'vfclass', 'vfdiv', 'vfmacc', 'vfmadd', 'vfmax', 'vfmerge', 'vfmin', 'vfmsac', 'vfmsub', 'vfmul', 'vfmv', 'vfnmacc', 'vfnmadd', 'vfnmsac', 'vfnmsub', 'vfrdiv', 'vfrec7', 'vfredmax', 'vfredmin', 'vfredosum', 'vfredusum', 'vfrsqrt7', 'vfrsub', 'vfsgnj', 'vfsgnjn', 'vfsgnjx', 'vfsqrt', 'vfsub', 'vfwadd', 'vfwmacc', 'vfwmsac', 'vfwmul', 'vfwnmacc', 'vfwnmsac', 'vfwredsum', 'vfwsub', 'vfncvt', 'vfwcvt', 'vfcvt']

permute = ['vmre', 'vslide1', 'vmv', 'vrgather', 'vrgatherei16', 'vfslide', 'vcompress', 'vslide']

fixpoint = ['vaadd', 'vaaddu', 'vasub', 'vasubu', 'vnclip', 'vnclipu', 'vsmul', 'vssra', 'vssrl']

loadstore = ['vle16', 'vle32', 'vle64', 'vle8', 'vluxei16', 'vluxei32', 'vluxei8', 'vluxsegei16', 'vluxsegei32', 'vluxsegei8', 'vlre16', 'vlre32', 'vlre8', 'vlse16', 'vlse32', 'vlse64', 'vlse8', 'vlssege32', 'vlssege8', 'vlsege16', 'vlsege32', 'vlsege8', 'vlssege16', 'vs1r', 'vs2r', 'vs4r', 'vs8r', 'vse16', 'vse32', 'vse8', 'vsse16', 'vsse32', 'vsse8', 'vssege16', 'vssege32', 'vssege8', 'vsssege16', 'vsssege32', 'vsssege8', 'vsuxei32', 'vsuxei8', 'vsuxsegei16', 'vsuxsegei32', 'vsuxsegei8',  'vsuxei16']


# from sail log
def replace_results_sail(instr, first_test, isac_log_first, origin_inst = ""):
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

def replace_results_spike(instr, first_test, spike_log, origin_inst = ""):
    logging.info("Running replace_results: {}".format(first_test))
    instr = instr.replace("_b1", "")

    # Extract results
    file = open(spike_log, "r")
    riscv_reg_abi_map = {'zero': 'x0', 'ra': 'x1', 'sp': 'x2', 'gp': 'x3', 'tp': 'x4', 't0': 'x5', 't1': 'x6', 't2': 'x7', 's0': 'x8', 'fp': 'x8', 's1': 'x9', 'a0': 'x10', 'a1': 'x11', 'a2': 'x12', 'a3': 'x13', 'a4': 'x14', 'a5': 'x15', 'a6': 'x16', 'a7': 'x17', 's2': 'x18', 's3': 'x19', 's4': 'x20', 's5': 'x21', 's6': 'x22', 's7': 'x23', 's8': 'x24', 's9': 'x25', 's10': 'x26', 's11': 'x27', 't3': 'x28', 't4': 'x29', 't5': 'x30', 't6': 'x31'}
    lineList = []
    regList = []
    str = instr + "(\.[a-z]*)*\s+([a-z]*[0-9]*)," # such as vcpop.m a4
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
    # if instr != 'vid':
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
    if (instr.startswith("vf") or ("vmf" in origin_inst)):
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
    des_path_temp = des_path + "_temp"
    os.system("cp %s %s" % (first_test, des_path))
    os.system("cp %s %s" % (first_test, des_path_temp))
    f = open(des_path_temp, "r")
    eachLine = f.readlines()
    ansListIndex = 0
    fflag_ansListIndex = 0
    for i in range(0, len(eachLine)):
        if "5201314" in eachLine[i]:
            if ansListIndex < len(ansList):
                eachLine[i] = eachLine[i].replace("5201314", ansList[ansListIndex], 1)
                ansListIndex = ansListIndex + 1
        if (instr.startswith("vf") or ("vmf" in origin_inst)) and "0xff100" in eachLine[i]:
            eachLine[i] = eachLine[i].replace("0xff100", fflag_ansList[fflag_ansListIndex], 1)
            fflag_ansListIndex = fflag_ansListIndex + 1
    f.close()
    with open(des_path, 'w') as f2:
        f2.writelines(eachLine)
    os.system("rm %s" % (des_path_temp))

    logging.info(
        "Running replace_results finish, dest file: {}".format(des_path))
    return des_path

def replace_results_spike_new(instr, first_test, spike_log, origin_inst = ""):
    logging.info("Running replace_results: {}".format(first_test))
    instr = instr.replace("_b1", "")

    vsew = int(os.environ['RVV_ATG_VSEW'])
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    masked = os.environ["RVV_ATG_MASKED"]
    vma = os.environ["RVV_ATG_VMA"]
    agnostic_type = int(os.environ['RVV_ATG_AGNOSTIC_TYPE'])
    lmul_double = lmul * 2
    lmul_double_1 = 1 if lmul_double < 1 else int(lmul_double)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_per_reg = int(vlen / vsew);
    # Extract results
    file = open(spike_log, "r")
    riscv_reg_abi_map = {'zero': 'x0', 'ra': 'x1', 'sp': 'x2', 'gp': 'x3', 'tp': 'x4', 't0': 'x5', 't1': 'x6', 't2': 'x7', 's0': 'x8', 'fp': 'x8', 's1': 'x9', 'a0': 'x10', 'a1': 'x11', 'a2': 'x12', 'a3': 'x13', 'a4': 'x14', 'a5': 'x15', 'a6': 'x16', 'a7': 'x17', 's2': 'x18', 's3': 'x19', 's4': 'x20', 's5': 'x21', 's6': 'x22', 's7': 'x23', 's8': 'x24', 's9': 'x25', 's10': 'x26', 's11': 'x27', 't3': 'x28', 't4': 'x29', 't5': 'x30', 't6': 'x31'}
    lineList = []
    regList = []
    maskValList = []
    instructionLineNumber = []
    matchMaskPattern = re.compile("vle\d+.v\s+v0")
    mark = False
    matchMaskValuePattern = re.compile("v0\s+(0x[0-9a-f]*)") # such as v0 0xfffffff7fffffffbfffffffdfffffffe
    lineNo = 0
    if masked == "True":
        # This loop extract all mask value
        while 1:
            line = file.readline()
            if not line:
                break
            if mark:
                a = matchMaskValuePattern.search(line)
                if a is not None:
                    ans = a.group(1)
                    ans = ans.replace('0x', '')
                    maskValList.append(ans)
                    mark = False
            else:
                # print('========================================={}=================='.format(line))
                a = matchMaskPattern.search(line)
                # print('========================================={}=================='.format(a))
                if a is not None:
                    mark = True
    str = instr + "(\.[a-z0-9]*)*\s+([a-z]*[0-9]*)," # such as vcpop.m a4; vadd.vv v14
    file.seek(0)
    matchPattern = re.compile(str)
    mark = False
    # This loop extract commit value log line of rd into lineList
    while 1:
        line = file.readline()
        if not line:
            break
        lineNo = lineNo + 1
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
                instructionLineNumber.append(lineNo)
                mark = True
    if instr == 'vadd':  # vadd will use VADD_NOUSE at last, this don't need analyse
        regList.pop()
        lineList.pop()
    print("len reglist=%d"%len(regList))
    print("len reglist=%d"%len(regList))
    print("len linelist=%d"%len(lineList))
    print("len maskValList=%d"%len(maskValList))
    file.seek(0)
    lineNo = 0
    # This loop extract rd origin value(before instruction) commit value line into rdLineList
    if len(regList) > 0:
        rdLineList = []
        index = 0
        matchVLEPattern = re.compile("vle\d+.v\s+%s"%regList[index])
        while 1:
            line = file.readline()
            if not line:
                break
            lineNo = lineNo + 1
            if mark:
                rdLineList.append(line)
                if (index >= len(regList)):
                    break
                mark = False
            else:
                a = matchVLEPattern.search(line)
                if a is not None and lineNo < instructionLineNumber[index] and (index < 1 or lineNo > instructionLineNumber[index - 1]):
                    index = index + 1
                    if (index < len(regList)):
                        matchVLEPattern = re.compile("vle\d+.v\s+%s"%regList[index])
                    # if (index < len(regList)):
                    mark = True
        print("len rdLinelist=%d"%len(rdLineList))
    file.close()
    ansList = []
    if 'pop' in instr:
        for i in range(len(lineList)):
            matchResultPattern = re.compile(regList[i] + "\s+(0x[0-9a-f]*)") # such as a4 0x00000001
            a = matchResultPattern.search(lineList[i])
            if a is not None:
                ans = a.group(1)
                ansList.append(ans)
    else:
        # This loop extract actual commit value from commit value line, including [rd, rd+lmul)
        for i in range(len(lineList)):
            reg = regList[i]
            reg_num = int(reg[1:])
            rd_vreg_nums = lmul_1
            if instr.startswith("vw") or instr.startswith("vfw"):
                rd_vreg_nums = lmul_double_1
            for j in range(rd_vreg_nums):
                matchResultPattern = re.compile("v%d"%(reg_num+j) + "\s+(0x[0-9a-f]*)") # such as v14 0xfffffff7fffffffbfffffffdfffffffe
                a = matchResultPattern.search(lineList[i])
                if a is not None:
                    ans = a.group(1)
                    ans = ans.replace('0x', '')
                    ans_element_bits = int(vsew/4)
                    valid_bits = int((vlen * min(lmul, 1) / 4))
                    num_elem_per_reg = int(vlen / vsew)
                    if instr.startswith("vw") or instr.startswith("vfw") :
                        ans_element_bits *= 2
                        valid_bits *= 2
                        num_elem_per_reg = int(num_elem_per_reg / 2)
                    # Only use lmul*vlen
                    ans = ans[-valid_bits:]  
                    ans_arr = [(ans[i:i+ans_element_bits]) for i in range(0, len(ans), ans_element_bits)] # when vsew=32, ans_arr = ['ffffffee', 'fffffff6', 'fffffffa', 'fffffffc']
                    ans_arr.reverse()
                    # print('------------------------------------------------------------')
                    # print("len ans_arr=%d"%len(ans_arr))
                    # print(list(set(maskValList)))
                    if masked == "True" and vma == "True" and agnostic_type == 1:
                        # masked element will written with 1s
                        for ele in range(num_elem_per_reg):
                        #     print(maskValList[i])
                        #     print('j={}'.format(j))
                        #     print('num_elem_per_reg={}'.format(num_elem_per_reg))
                        #     print('element={}'.format(ele))
                        #     print(get_if_masked(maskValList[i], j * num_elem_per_reg + ele))
                            if get_if_masked(maskValList[i], j * num_elem_per_reg + ele):
                                ans_arr[ele] = '0' * int((vsew / 4) - 1) + '1'
                    ansList = ansList + (ans_arr)
                else:
                    # reg j is not show in commit log, use origin rd value
                    b = matchResultPattern.search(rdLineList[i])
                    if b is not None:
                        ans = b.group(1)
                        ans = ans.replace('0x', '')
                        ans_element_bits = int(vsew/4)
                        valid_bits = int((vlen * min(lmul, 1) / 4))
                        num_elem_per_reg = int(vlen / vsew)
                        if instr.startswith("vw") or instr.startswith("vfw"):
                            ans_element_bits *= 2
                            valid_bits *= 2
                            num_elem_per_reg = int(num_elem_per_reg / 2)
                        # Only use lmul*vlen
                        ans = ans[-valid_bits:]
                        ans_arr = [(ans[i:i+ans_element_bits]) for i in range(0, len(ans), ans_element_bits)] # when vsew=32, ans_arr = ['ffffffee', 'fffffff6', 'fffffffa', 'fffffffc']
                        ans_arr.reverse()
                        if masked == "True" and vma == "True" and agnostic_type == 1:
                            # masked element will written with 1s
                            for ele in range(num_elem_per_reg):
                                if get_if_masked(maskValList[i], j * num_elem_per_reg + ele):
                                    ans_arr[ele] = '0' * int((vsew / 4) - 1) + '1'
                        ansList = ansList + (ans_arr)



    print("len anslist=%d"%len(ansList))
    # Extract fflas
    if (instr.startswith("vf") or ("vmf" in origin_inst)):
        file = open(spike_log, "r")
        fflag_lineList = []
        fflag_regList = []
        str = "csrr\s+([a-z][0-9]*),\sfflags" # such as csrr    a1, fflags
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
        print("len fflag_ansList=%d"%len(fflag_ansList))

    des_path = first_test.replace("_first", "_second")
    des_path = des_path.replace("_empty", "_second")
    des_path_temp = des_path + "_temp"
    os.system("cp %s %s" % (first_test, des_path))
    os.system("cp %s %s" % (first_test, des_path_temp))
    f = open(des_path_temp, "r")
    eachLine = f.readlines()
    ansListIndex = 0
    fflag_ansListIndex = 0
    for i in range(0, len(eachLine)):
        if "5201314" in eachLine[i]:
            if ansListIndex < len(ansList):
                eachLine[i] = eachLine[i].replace("5201314", ansList[ansListIndex], 1)
                ansListIndex = ansListIndex + 1
        if (instr.startswith("vf") or ("vmf" in origin_inst)) and "0xff100" in eachLine[i]:
            eachLine[i] = eachLine[i].replace("0xff100", fflag_ansList[fflag_ansListIndex], 1)
            fflag_ansListIndex = fflag_ansListIndex + 1
    f.close()
    with open(des_path, 'w') as f2:
        f2.writelines(eachLine)
    os.system("rm %s" % (des_path_temp))

    logging.info(
        "Running replace_results finish, dest file: {}".format(des_path))
    return des_path


def replace_results(instr, test_file, log_path, tool, origin_inst = ""):
    if tool == 'spike':
        if (instr in mask) or (instr in permute and "vrgather" not in instr) or (instr in loadstore) or ("red" in instr) or (instr.startswith("vfmv")):
            print('+++++++++++++++++++++++++++++++++++++++ without new +++++++++++++++++++++++++++++++++++++++++++')
            return replace_results_spike(instr, test_file, log_path, origin_inst)
        else:
            print('---------------------------------------- with new ---------------------------------------------')
            return replace_results_spike_new(instr, test_file, log_path, origin_inst)
    else:
        return replace_results_sail(instr, test_file, log_path, origin_inst)

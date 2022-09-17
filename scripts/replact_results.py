import logging
import os
import re


def replace_results(instr, first_test, isac_log_first):
    logging.info("Running replace_results: {}".format(first_test))

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

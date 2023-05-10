import sys
import datetime
import logging

# this function is to check the current element whether is  masked or not
def get_if_masked(mask_val_string, index): # mask_val_string like: f600a3d1195b62bffbba7ae72c63c8470692dadf7ca
    return (int(mask_val_string[::-1][int(index / 4)], 16) >> (index % 4)) & 1 == 0; # 0 indicates masked

# $1 is the instructuion name
# $2 is vsew
# $3 is vlen

# following variables can be easily understood by name
date = datetime.datetime.now().strftime('%m-%d')
ins_name = sys.argv[1]
vsew = int(sys.argv[2])
vlen = int(sys.argv[3])
txt_path = sys.argv[4]              # txt_path is the path stores mask data, spike results and modified results
elem_num = int(vlen / vsew)         # elem_num is the number of elements per registers
valid_byte = int(vlen / 4)          # valid_byte is the number of per registers bits in byte

# import mask data, spike results and modified results
f=open(txt_path)
lines = f.readlines()

# deal widen instructions
if ins_name.startswith("vw") or ins_name.startswith("vfw"):
    if len(lines) != 5:
        logging.error("ERROR! get results failed")
    else:
        mask_data        = lines[0]
        spike_result_1   = lines[1]
        spike_result_2   = lines[2]
        replace_result_1 = lines[3]
        replace_result_2 = lines[4]
        # widen instructions double the size of per element bits
        elem_in_byte = int(vsew / 2)
        mask_data=mask_data.replace("0x","")
        mask_data=mask_data.replace("\n","")
        spike_result_1     =   spike_result_1.replace("\n","")
        spike_result_2     =   spike_result_2.replace("\n","")
        spike_result_1     =   spike_result_1.replace("0x","")
        spike_result_2     =   spike_result_2.replace("0x","")
        replace_result_1   =   replace_result_1.replace("0x","")
        replace_result_2   =   replace_result_2.replace("0x","")
        replace_result_1   =   replace_result_1.replace("\n","")
        replace_result_2   =   replace_result_2.replace("\n","")
        #reverse the array to better process list
        for i in range(1,3):
            exec(f'replace_result_{i}   =   replace_result_{i}[-valid_byte:]')
            exec(f'spike_elem_{i} = [spike_result_{i}[j:j+elem_in_byte] for j in range(0,len(spike_result_{i}),elem_in_byte)]')
            exec(f'spike_elem_{i}.reverse()')
            exec(f'replace_elem_{i} = [replace_result_{i}[j:j+elem_in_byte] for j in range(0,len(replace_result_{i}),elem_in_byte)]')
            exec(f'replace_elem_{i}.reverse()')
            success_elem_num = 0
        # checking statementswiden instructions always has double results, so use two loops
        for ele in range(int(elem_num/2)):
            if get_if_masked(mask_data, ele) and replace_elem_1[ele] == "0" * (elem_in_byte - 1) + '1':
                success_elem_num += 1
                continue
            elif not(get_if_masked(mask_data, ele)) and replace_elem_1[ele] == spike_elem_1[ele] :
                success_elem_num += 1
                continue
            else:
                logging.error("FAILED!! Mismatch in %d element,please check it out"%ele)
                break
        for ele in range(int(elem_num/2)):
            if get_if_masked(mask_data, ele+int(elem_num/2)) and replace_elem_2[ele] == "0" * (elem_in_byte - 1) + '1':
                success_elem_num += 1
                continue
            elif not(get_if_masked(mask_data, ele+int(elem_num/2))) and replace_elem_2[ele] == spike_elem_2[ele] :
                success_elem_num += 1
                continue
            else:
                logging.error("FAILED!! Mismatch in %d element,please check it out"%ele)
                break
        if success_elem_num == elem_num:
            # print('elem_num:{}'.format(elem_num))
            print("SUCCESS!! The results has been successfully replaced")

# deal other instructions
else:    
    if len(lines) != 3:
        logging.error("ERROR! get results failed")
    else:
        # data process, transform into pure numbers
        mask_data      = lines[0]
        spike_result   = lines[1]
        replace_result = lines[2]
        elem_in_byte = int(vsew / 4)
        mask_data=mask_data.replace("0x","")
        mask_data=mask_data.replace("\n","")
        spike_result=spike_result.replace("\n","")
        spike_result=spike_result.replace("0x","")
        replace_result=replace_result.replace("0x","")
        replace_result=replace_result.replace("\n","")
        #reverse the array to better process list
        spike_result = spike_result[-valid_byte:]
        replace_result = replace_result[-valid_byte:]
        spike_elem = [spike_result[i :i+elem_in_byte] for i in range(0,len(spike_result),elem_in_byte)]
        spike_elem.reverse()
        replace_elem = [replace_result[i :i+elem_in_byte] for i in range(0,len(replace_result),elem_in_byte)]
        replace_elem.reverse()
        success_elem_num = 0
        # checking statements
        for ele in range(elem_num):
            if get_if_masked(mask_data, ele) and replace_elem[ele] == "0" * (elem_in_byte - 1) + '1':
                success_elem_num += 1
                continue
            elif not(get_if_masked(mask_data, ele)) and replace_elem[ele] == spike_elem[ele] :
                success_elem_num += 1
                continue
            else:
                logging.error("FAILED!! Mismatch in %d element,please check it out"%ele)
                break
        if success_elem_num == elem_num:
            print("SUCCESS!! The results has been successfully replaced")
            

    

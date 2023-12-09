import re
import random
import os
from scripts.test_common_info import print_data_width_prefix, print_mask_origin_data_ending, get_mask_bit

MEM = ['07', '3e', 'e3', '49', '09', '5c', '57', '96', '0d', '95', '47', '70', 'e7', 'fb', '2d', '31', '02', '49', 'bf', 'c9', '43', '03', 'fb', '1a', '82', '3a', '33', 'cf', 'e8', '7d', '28', '50', '9b', 'c4', '87', '84', 'f3', '80', 'c2', 'ec', '7f', '29', '4b', '19', '03', 'f5', 'a5', '1f', 'cb', '1b', '98', 'aa', 'a1', '3a', 'e6', '49', 'c8', '81', 'fb', '57', '6e', '9f', 'f4', 'd9', 'b4', '92', '2d', '80', '34', 'de', 'bc', 'f4', '10', 'b7', '0b', '55', '0c', '16', '3f', '6b', '35', 'ad', '27', '30', '9a', '8a', '42', '98', '86', '33', '6f', '3c', '8f', '21', 'e0', '6c', 'd3', 'a0', '54', '25', 'cc', 'af', '24', 'd5', '3b', '24', '54', 'd7', 'b0', 'a4', 'bb', '04', '95', 'f7', 'd2', 'da', '8f', '33', '92', 'f0', 'cd', 'c7', '2f', '74', '97', '2f', '52', '8f', '56', 'd0', 'dd', 'a2', '83', 'd4', '56', '6b', '51', 'bc', 'e0', '96', 'fc', '0c', '43', '2c', '16', 'f6', 'de', 'db', '1a', 'a0', '26', '5e', 'b4', '50', 'bc', '23', '4e', '81', '80', '1d', '1b', '6b', 'c7', '8b', '5a', '55', 'aa', '62', '56', '48', '2e', 'a6', 'ca', '8d', 'eb', 'ac', '1c', '26', '28', '74', '5c', 'b1', 'f3', '80', 'b9', '9a', '46', 'f1', '23', 'f8', '7f', 'df', '3a', '8d', '55', 'fb', '94', 'c1', 'fb', 'fa', '26', 'ac', 'b6', '27', '1c', 'fc', '40', '79', 'e7', '83', '6c', 'ef', 'd5', '55', '77', 'c3', '21', '8e', '10', '29', 'd2', '2d', '26', '4e', '7c', '59', '87', 'b8', 'f3', 'ef', '13', '18', 'b7', '96', '4b', '6e', '10', '5d', 'b8', '1e', 'd5', '07', '72', 'bb', 'f8', '65', '6d', '9b', '7b', 'b7', '8c', '31', 'fb', '09', 'a1', '1e', 'f6', 'd5', '48', '6b', '43', '2b', 'dc', '4c', '42', 'f1', '2f', '4b', 'a3', 'ac', 'ba', '98', 'b4', 'e3', '4b', 'b5', '51', 'db', '2c', 'a4', '11', 'ef', '06', '5a', '43', '7f', '3a', 'b4', '4b', '66', '42', '30', '68', '61', '10', 'd3', 'fd', '92', 'a8', '08', 'cf', 'ee', '8c', '0c', '64', '17', 'ab', '6c', 'ca', 'be', 'ff', '2f', 'f5', 'b1', '06', '0f', '0a', '67', '1c', '5b', 'a0', '93', 'e3', '7b', '87', '61', 'cf', '96', '28', '52', 'c2', '35', 'db', 'a0', 'ac', 'f8', '50', '2a', '36', '68', 'ca', '97', 'f5', 'aa', '69', '43', '37', '91', 'ed', 'a1', '62', '84', 'd1', '5a', '8e', '18', '07', '7d', 'a7', '35', '7f', '67', '1d', '56', '48', '0d', '7a', 'f5', '9e', '4f', '38', '4e', '6e', 'e3', '6b', '52', 'd1', 'ec', '7a', '8d', 'e1', 'f9', '72', '6e', '25', '3a', 'ac', '6f', '17', '3b', '21', '70', '7f', '58', 'f5', '4d', 'bb', '18', '18', '78', '5b', 'ec', '94', 'b8', 'b2', '50', 'c6', '1b', 'fc', 'd4', 'fc', 'fa', 'd7', 'e3', 'ac', 'cf', '2e', 'ab', '72', '2f', '63', '5f', '25', 'd7', '39', 'cc', 'ab', '56', 'ab', '3e', '79', '90', '01', '2d', 'b4', '0f', '31', '57', '1f', '03', '3f', '32', '9d', 'c9', 'a0', '85', '99', '61', 'e4', '55', 'eb', '42', 'ca', '68', 'ac', '8d', '7a', '17', 'eb', 'cb', '75', 'b3', 'e5', '21', '0f', '3b', '27', '34', 'd0', '59', 'ed', '4f', 'f4', 'e0', 'be', '7b', '85', '13', 'f3', '37', 'eb', '67', 'a8', 'ba', 'd2', '04', '14', '4b', 'ad', '6d', '70', '99', '0e', '3e', '82', '8d', '3f', 'ea', 'e8', '06', '4e', '0f', 'b6', '33', '1f', '7d', '0b', '46', '2f', '68', 'fa', 'b6', '07', '3e', 'e3', '49', '09', '5c', '57', '96', '0d', '95', '47', '70', 'e7', 'fb', '2d', '31', '02', '49', 'bf', 'c9', '43', '03', 'fb', '1a', '82', '3a', '33', 'cf', 'e8', '7d', '28', '50', '9b', 'c4', '87', '84', 'f3', '80', 'c2', 'ec', '7f', '29', '4b', '19', '03', 'f5', 'a5', '1f', 'cb', '1b', '98', 'aa', 'a1', '3a', 'e6', '49', 'c8', '81', 'fb', '57', '6e', '9f', 'f4', 'd9', 'b4', '92', '2d', '80', '34', 'de', 'bc', 'f4', '10', 'b7', '0b', '55', '0c', '16', '3f', '6b', '35', 'ad', '27', '30', '9a', '8a', '42', '98', '86', '33', '6f', '3c', '8f', '21', 'e0', '6c', 'd3', 'a0', '54', '25', 'cc', 'af', '24', 'd5', '3b', '24', '54', 'd7', 'b0', 'a4', 'bb', '04', '95', 'f7', 'd2', 'da', '8f', '33', '92', 'f0', 'cd', 'c7', '2f', '74', '97', '2f', '52', '8f', '56', 'd0', 'dd', 'a2', '83', 'd4', '56', '6b', '51', 'bc', 'e0', '96', 'fc', '0c', '43', '2c', '16', 'f6', 'de', 'db', '1a', 'a0', '26', '5e', 'b4', '50', 'bc', '23', '4e', '81', '80', '1d', '1b', '6b', 'c7', '8b', '5a', '55', 'aa', '62', '56', '48', '2e', 'a6', 'ca', '8d', 'eb', 'ac', '1c', '26', '28', '74', '5c', 'b1', 'f3', '80', 'b9', '9a', '46', 'f1', '23', 'f8', '7f', 'df', '3a', '8d', '55', 'fb', '94', 'c1', 'fb', 'fa', '26', 'ac', 'b6', '27', '1c', 'fc', '40', '79', 'e7', '83', '6c', 'ef', 'd5', '55', '77', 'c3', '21', '8e', '10', '29', 'd2', '2d', '26', '4e', '7c', '59', '87', 'b8', 'f3', 'ef', '13', '18', 'b7', '96', '4b', '6e', '10', '5d', 'b8', '1e', 'd5', '07', '72', 'bb', 'f8', '65', '6d', '9b', '7b', 'b7', '8c', '31', 'fb', '09', 'a1', '1e', 'f6', 'd5', '48', '6b', '43', '2b', 'dc', '4c', '42', 'f1', '2f', '4b', 'a3', 'ac', 'ba', '98', 'b4', 'e3', '4b', 'b5', '51', 'db', '2c', 'a4', '11', 'ef', '06', '5a', '43', '7f', '3a', 'b4', '4b', '66', '42', '30', '68', '61', '10', 'd3', 'fd', '92', 'a8', '08', 'cf', 'ee', '8c', '0c', '64', '17', 'ab', '6c', 'ca', 'be', 'ff', '2f', 'f5', 'b1', '06', '0f', '0a', '67', '1c', '5b', 'a0', '93', 'e3', '7b', '87', '61', 'cf', '96', '28', '52', 'c2', '35', 'db', 'a0', 'ac', 'f8', '50', '2a', '36', '68', 'ca', '97', 'f5', 'aa', '69', '43', '37', '91', 'ed', 'a1', '62', '84', 'd1', '5a', '8e', '18', '07', '7d', 'a7', '35', '7f', '67', '1d', '56', '48', '0d', '7a', 'f5', '9e', '4f', '38', '4e', '6e', 'e3', '6b', '52', 'd1', 'ec', '7a', '8d', 'e1', 'f9', '72', '6e', '25', '3a', 'ac', '6f', '17', '3b', '21', '70', '7f', '58', 'f5', '4d', 'bb', '18', '18', '78', '5b', 'ec', '94', 'b8', 'b2', '50', 'c6', '1b', 'fc', 'd4', 'fc', 'fa', 'd7', 'e3', 'ac', 'cf', '2e', 'ab', '72', '2f', '63', '5f', '25', 'd7', '39', 'cc', 'ab', '56', 'ab', '3e', '79', '90', '01', '2d', 'b4', '0f', '31', '57', '1f', '03', '3f', '32', '9d', 'c9', 'a0', '85', '99', '61', 'e4', '55', 'eb', '42', 'ca', '68', 'ac', '8d', '7a', '17', 'eb', 'cb', '75', 'b3', 'e5', '21', '0f', '3b', '27', '34', 'd0', '59', 'ed', '4f', 'f4', 'e0', 'be', '7b', '85', '13', 'f3', '37', 'eb', '67', 'a8', 'ba', 'd2', '04', '14', '4b', 'ad', '6d', '70', '99', '0e', '3e', '82', '8d', '3f', 'ea', 'e8', '06', '4e', '0f', 'b6', '33', '1f', '7d', '0b', '46', '2f', '68', 'fa', 'b6''07', '3e', 'e3', '49', '09', '5c', '57', '96', '0d', '95', '47', '70', 'e7', 'fb', '2d', '31', '02', '49', 'bf', 'c9', '43', '03', 'fb', '1a', '82', '3a', '33', 'cf', 'e8', '7d', '28', '50', '9b', 'c4', '87', '84', 'f3', '80', 'c2', 'ec', '7f', '29', '4b', '19', '03', 'f5', 'a5', '1f', 'cb', '1b', '98', 'aa', 'a1', '3a', 'e6', '49', 'c8', '81', 'fb', '57', '6e', '9f', 'f4', 'd9', 'b4', '92', '2d', '80', '34', 'de', 'bc', 'f4', '10', 'b7', '0b', '55', '0c', '16', '3f', '6b', '35', 'ad', '27', '30', '9a', '8a', '42', '98', '86', '33', '6f', '3c', '8f', '21', 'e0', '6c', 'd3', 'a0', '54', '25', 'cc', 'af', '24', 'd5', '3b', '24', '54', 'd7', 'b0', 'a4', 'bb', '04', '95', 'f7', 'd2', 'da', '8f', '33', '92', 'f0', 'cd', 'c7', '2f', '74', '97', '2f', '52', '8f', '56', 'd0', 'dd', 'a2', '83', 'd4', '56', '6b', '51', 'bc', 'e0', '96', 'fc', '0c', '43', '2c', '16', 'f6', 'de', 'db', '1a', 'a0', '26', '5e', 'b4', '50', 'bc', '23', '4e', '81', '80', '1d', '1b', '6b', 'c7', '8b', '5a', '55', 'aa', '62', '56', '48', '2e', 'a6', 'ca', '8d', 'eb', 'ac', '1c', '26', '28', '74', '5c', 'b1', 'f3', '80', 'b9', '9a', '46', 'f1', '23', 'f8', '7f', 'df', '3a', '8d', '55', 'fb', '94', 'c1', 'fb', 'fa', '26', 'ac', 'b6', '27', '1c', 'fc', '40', '79', 'e7', '83', '6c', 'ef', 'd5', '55', '77', 'c3', '21', '8e', '10', '29', 'd2', '2d', '26', '4e', '7c', '59', '87', 'b8', 'f3', 'ef', '13', '18', 'b7', '96', '4b', '6e', '10', '5d', 'b8', '1e', 'd5', '07', '72', 'bb', 'f8', '65', '6d', '9b', '7b', 'b7', '8c', '31', 'fb', '09', 'a1', '1e', 'f6', 'd5', '48', '6b', '43', '2b', 'dc', '4c', '42', 'f1', '2f', '4b', 'a3', 'ac', 'ba', '98', 'b4', 'e3', '4b', 'b5', '51', 'db', '2c', 'a4', '11', 'ef', '06', '5a', '43', '7f', '3a', 'b4', '4b', '66', '42', '30', '68', '61', '10', 'd3', 'fd', '92', 'a8', '08', 'cf', 'ee', '8c', '0c', '64', '17', 'ab', '6c', 'ca', 'be', 'ff', '2f', 'f5', 'b1', '06', '0f', '0a', '67', '1c', '5b', 'a0', '93', 'e3', '7b', '87', '61', 'cf', '96', '28', '52', 'c2', '35', 'db', 'a0', 'ac', 'f8', '50', '2a', '36', '68', 'ca', '97', 'f5', 'aa', '69', '43', '37', '91', 'ed', 'a1', '62', '84', 'd1', '5a', '8e', '18', '07', '7d', 'a7', '35', '7f', '67', '1d', '56', '48', '0d', '7a', 'f5', '9e', '4f', '38', '4e', '6e', 'e3', '6b', '52', 'd1', 'ec', '7a', '8d', 'e1', 'f9', '72', '6e', '25', '3a', 'ac', '6f', '17', '3b', '21', '70', '7f', '58', 'f5', '4d', 'bb', '18', '18', '78', '5b', 'ec', '94', 'b8', 'b2', '50', 'c6', '1b', 'fc', 'd4', 'fc', 'fa', 'd7', 'e3', 'ac', 'cf', '2e', 'ab', '72', '2f', '63', '5f', '25', 'd7', '39', 'cc', 'ab', '56', 'ab', '3e', '79', '90', '01', '2d', 'b4', '0f', '31', '57', '1f', '03', '3f', '32', '9d', 'c9', 'a0', '85', '99', '61', 'e4', '55', 'eb', '42', 'ca', '68', 'ac', '8d', '7a', '17', 'eb', 'cb', '75', 'b3', 'e5', '21', '0f', '3b', '27', '34', 'd0', '59', 'ed', '4f', 'f4', 'e0', 'be', '7b', '85', '13', 'f3', '37', 'eb', '67', 'a8', 'ba', 'd2', '04', '14', '4b', 'ad', '6d', '70', '99', '0e', '3e', '82', '8d', '3f', 'ea', 'e8', '06', '4e', '0f', 'b6', '33', '1f', '7d', '0b', '46', '2f', '68', 'fa', 'b6']*3 # 1024*3 elements * 1Byte

INDEX = [24, 64, 24, 80, 64, 24, 32, 48, 16, 24, 72, 0, 40, 64, 80, 48, 24, 72, 24, 64, 64, 40, 64, 72, 40, 16, 24, 32, 16, 0, 32, 64, 64, 16, 0, 16, 0, 48, 80, 16, 8, 16, 16, 64, 0, 16, 24, 40, 80, 0, 0, 48, 32, 32, 72, 40, 80, 0, 48, 24, 56, 72, 72, 56, 8, 64, 64, 8, 72, 64, 56, 80, 56, 64, 48, 72, 72, 80, 32, 8, 16, 56, 48, 80, 16, 40, 40, 72, 72, 72, 32, 56, 40, 16, 24, 64, 40, 56, 64, 56, 32, 48, 56, 80, 16, 8, 32, 56, 48, 0, 72, 24, 72, 56, 80, 64, 32, 64, 80, 56, 40, 56, 80, 64, 0, 56, 48, 24, 32, 72, 72, 48, 0, 48, 72, 48, 8, 40, 72, 72, 16, 24, 48, 32, 0, 48, 8, 72, 64, 0, 56, 56, 24, 72, 0, 24, 16, 8, 56, 40, 80, 56, 56, 0, 32, 16, 8, 32, 56, 0, 32, 80, 48, 72, 56, 32, 72, 40, 56, 32, 80, 0, 56, 56, 32, 8, 0, 0, 56, 0, 72, 32, 80, 80, 16, 48, 16, 0, 56, 16, 64, 80, 64, 64, 40, 40, 24, 64, 24, 24, 8, 32, 64, 8, 72, 8, 80, 16, 32, 72, 8, 8, 16, 56, 64, 56, 32, 16, 32, 32, 40, 24, 8, 8, 16, 8, 16, 24, 8, 0, 80, 80, 64, 16, 32, 64, 56, 72, 48, 0, 64, 64, 24, 64, 0, 40, 48, 48, 0, 8, 64, 0, 8, 48, 8, 32, 56, 40, 80, 8, 64, 0, 32, 24, 32, 24, 72, 56, 72, 16, 72, 16, 48, 64, 0, 72, 80, 24, 8, 56, 16, 40, 72, 16, 56, 32, 0, 8, 64, 64, 48, 64, 40, 0, 72, 0, 64, 0, 8, 24, 56, 40, 24, 24, 8, 48, 0, 80, 32, 32, 40, 24, 40, 40, 72, 48, 16, 56, 80, 56, 0, 48, 48, 8, 64, 0, 64, 64, 32, 8, 64, 0, 0, 64, 0, 48, 24, 8, 80, 56, 8, 72, 16, 48, 24, 40, 32, 80, 64, 56, 16, 0, 72, 8, 80, 8, 16, 40, 8, 48, 40, 24, 64, 40, 48, 40, 56, 64, 72, 32, 48, 72, 48, 72, 72, 40, 40, 48, 64, 16, 32, 0, 8, 40, 40, 72, 72, 56, 72, 16, 24, 24, 80, 64, 16, 24, 72, 64, 80, 72, 56, 0, 56, 72, 80, 0, 0, 24, 24, 32, 64, 48, 64, 16, 72, 8, 32, 16, 40, 8, 8, 80, 48, 40, 0, 24, 80, 16, 56, 80, 56, 8, 48, 56, 40, 8, 16, 40, 80, 32, 32, 48, 40, 80, 72, 8, 8, 32, 32, 0, 80, 64, 24, 24, 24, 56, 72, 56, 16, 24, 24, 80, 80, 32, 56, 16, 72, 32, 32, 32, 64, 32, 48, 8, 56, 0, 48, 8, 64, 72, 8, 0, 16, 48, 24, 80, 72, 56, 64, 16, 80, 8, 40, 8, 56, 72, 72, 80, 64, 32, 80, 8]

def extract_operands(f, rpt_path):
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    matchObj = re.compile('rs1_val ?== ?(-?\d+)')
    rs1_val_10 = matchObj.findall(line)
    rs1_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs1_val_10]
    matchObj = re.compile('rs2_val ?== ?(-?\d+)')
    rs2_val_10 = matchObj.findall(line)
    rs2_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs2_val_10]
    f.close()
    return rs1_val, rs2_val

def generate_macros_load_vx_Nregs(f, eew, rs2):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    emul = int(eew / vsew * lmul) #16 / vsew * lmul
    emul_1 = 1 if emul < 1 else int(emul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    seq = 1
    for field in range(1, 9):
        if 24+field*emul > 32:
            continue
        result_identifier = field
        print("\n#define TEST_LOAD_VX_%dregs( testnum, inst ) \\"%(field), file=f)
        print(" vsetvli x31, x0, e%d, m8, tu, mu; \\\n "%vsew + " \
                la x7, mem + 40; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, mem; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                li x8, %d; \\\n\
                inst v24, (x7), x8%s;\\"%(rs2, ", v0.t" if masked else ""), file=f)
        if emul >= 2:
            print(" vsetvli x31, x0, e%d, m%d, tu, mu; \\ "%(vsew,emul), file=f)
        for i in range(field):
            print("    vsetvli x31, x0, e%d, m%d, tu, mu; "%(vsew,emul_1), file=f, end = "\\\n")
            print("    TEST_CASE_LOOP( %d, v%d, result_%d)"%(seq, 24+i*emul_1, result_identifier*10+i), file=f, end = "\\\n")
            seq = seq + 1
        print("VSET_VSEW \n", file=f)

global seq 
seq = 1
def generate_macros_load_vx_offset(f, eew, offset, vd, rs):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    emul = int(eew / vsew * lmul) #16 / vsew * lmul
    emul_1 = 1 if emul < 1 else int(emul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    for field in range(1, 2):
        if 24+field*emul > 32:
            continue
        # result_identifier = field
        print("\n#define TEST_LOAD_V%dX%d_offset( testnum, inst ) \\"%(vd,rs), file=f)
        print(" vsetvli x31, x0, e%d, m%d, tu, mu; \\\n "%(eew,emul_1) + " \
                la x7, mem + 40; \\\n\
                vle%d.v v%d, (x7);"%(eew,vd) + " \\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_data; \\\n  vsetvli x31, x0, e8, m1, tu, mu; \\\n  vle%d.v v0, (x7); \\\n  "%(vsew) if masked else "")+" \
                la x%d, mem; \\\n\
                "%(rs) + " VSET_VSEW_4AVL \\\n " + "\\\n\
                inst v%d, %d(x%d)%s;\\"%(vd ,offset,rs ,", v0.t" if masked else ""), file=f)
        if emul >= 2:
            print(" vsetvli x31, x0, e%d, m%d, tu, mu; \\ "%(vsew,emul), file=f)
        for i in range(field):
            print("    vsetvli x31, x0, e%d, m%d, tu, mu; "%(vsew,emul_1), file=f, end = "\\\n")     
            global seq       
            print("    TEST_CASE_LOOP( %d, v%d, result_%d)"%(seq, vd+i*emul_1, 1*10+i), file=f, end = "\\\n")

            seq = seq + 1
        print("VSET_VSEW \n", file=f)
        if(rs==7):   
            # print("\n#ifndef TEST_LOAD_V%dXFF_offset( testnum, inst ) "%(vd), file=f) 
            print("\n#define TEST_LOAD_V%dXFF_offset( testnum, inst ) \\"%(vd), file=f)
            print(" vsetvli x31, x0, e%d, m%d, tu, mu; \\\n "%(eew,emul_1) + " \
                    la x7, mem + 40; \\\n\
                    vle%d.v v%d, (x7);"%(eew,vd) + " \\\n\
                    VSET_VSEW_4AVL \\\n\
                    %s "%("la x7, mask_data; \\\n  vsetvli x31, x0, e8, m1, tu, mu; \\\n  vle%d.v v0, (x7); \\\n  "%(vsew) if masked else "")+" \
                    la x7, mem; \\\n\
                    " + " VSET_VSEW_4AVL \\\n " + "\\\n\
                    li x8, %d; \\\n\
                    inst v%d, %d(x7)%s;\\"%(offset, vd ,offset ,", v0.t" if masked else ""), file=f)
            if emul >= 2:
                print(" vsetvli x31, x0, e%d, m%d, tu, mu; \\ "%(vsew,emul), file=f)
            for i in range(field):
                print("    vsetvli x31, x0, e%d, m%d, tu, mu; "%(vsew,emul_1), file=f, end = "\\\n")
                print("    TEST_CASE_LOOP( %d, v%d, result_%d)"%(seq, vd+i*emul_1, 1*10+i), file=f, end = "\\\n")
                seq = seq + 1
            print("VSET_VSEW \\\n ", file=f)

def generate_macros_load_vv_Nregs(f, eew):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    emul = int(eew / vsew)
    emul_1 = 1 if emul < 1 else int(emul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    seq = 1
    for field in range(1, 9):
        if 24+field*emul > 32:
            continue
        result_identifier = field
        print("\n#define TEST_LOAD_VV_%dregs( testnum, inst ) \\"%(field), file=f)
        print(" vsetvli x31, x0, e%d, m8, tu, mu; \\\n "%vsew + " \
                la x7, mem + 40; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, index; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, mem; \\\n\
                inst v24, (x7), v8%s;\\"%(", v0.t" if masked else ""), file=f)
        if emul >= 2:
            print(" vsetvli x31, x0, e%d, m%d, tu, mu; \\ "%(vsew,emul), file=f)
        for i in range(field):
            print("    TEST_CASE_LOOP( %d, v%d, result_%d)"%(seq, 24+i*emul_1, result_identifier*10+i), file=f, end = "\\\n")
            seq = seq + 1
        print("VSET_VSEW \n", file=f)

def generate_results_load_vlsseg_Nregs(f, rs2, eew, rd_base, is_vx = False, is_vv = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    lmul_1 = 1 if lmul < 1 else int(lmul)
    emul = int(eew / vsew* lmul)
    emul_1 = 1 if emul < 1 else int(emul)
    element_num_ans_per_reggroup = int(vlen * emul_1 / 8);
    vl = int(vlen * lmul / vsew)
    mem_mul = int(eew / 8)
    for field in range(1, 9):
        print("-----field: ", field)
        result_identifier = field
        # Build N-dimension array, Byte addressable always
        ans = [["" for _1 in range(element_num_ans_per_reggroup)] for _2 in range(field)]
        # Assign ans as RD origin value
        for i in range(field):
            for j in range(element_num_ans_per_reggroup):
                if((rd_base + (i * element_num_ans_per_reggroup + j)>1024)):    #will overflow otherwise
                    continue
                ans[i][j] = MEM[rd_base + (i * element_num_ans_per_reggroup + j)]
        # Simulate vlsseg, first column then row
        for j in range(0, int(vl * (eew / 8)), mem_mul):
            big_element_index = int(j / mem_mul)
            for i in range(field):
                for index_inside in range(mem_mul):
                    if(not masked or (masked and get_mask_bit(big_element_index) == 1)): # Unmasked
                        stride = 0
                        if is_vx:
                            stride = (rs2 * big_element_index)
                        elif is_vv:
                            stride = INDEX[big_element_index]
                        ans[i][j+index_inside] = MEM[int(stride + (i * mem_mul + index_inside))]
        # print
        for i in range(field):
            print("\n.align 4", file=f)
            print("result_%d:"%(int(result_identifier*10)+i), file=f)
            for j in range(element_num_ans_per_reggroup):
                print_data_width_prefix(f, 8)
                print("0x"+ans[i][j], file=f)



def print_load_ending_new(f, eew, rs2, is_vx = False, is_vv = False):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    print("  vsetvli x31,x0,e8,m1;\n\
    #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
mem:", file=f)
    for i in MEM:
        print(".byte 0x%s"%i, file=f)
    print("\n.align 4\nindex:", file=f)
    for i in INDEX:
        print_data_width_prefix(f, vsew)
        print("%d"%i, file=f)
    # generate_results_load_vlsseg_Nregs(f, 16, eew, 40, is_vx = is_vx, is_vv = is_vv);#for vlsseg
    generate_results_load_vlsseg_Nregs(f, rs2, eew, 40, is_vx = is_vx, is_vv = is_vv);#for vle8
    print_mask_origin_data_ending(f)
    print("\n\
    RVTEST_DATA_END\n", file=f)
    print_rvmodel_data(f)
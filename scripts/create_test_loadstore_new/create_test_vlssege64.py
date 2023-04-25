import logging
import os
from scripts.create_test_loadstore_new.create_test_common import generate_macros_load_vx_Nregs, print_load_ending_new, generate_results_load_vlsseg_Nregs
from scripts.test_common_info import *
import re

name = 'vlssege64'

def generate_tests(f, vsew, lmul):
    emul = 64 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(1):
        if 2 * emul <= 8 and 24 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 2
            print("  TEST_LOAD_VX_2regs( "+str(n)+",  vlsseg2e64.v );", file=f)
        if 3 * emul <= 8 and 24 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_LOAD_VX_3regs( "+str(n)+",  vlsseg3e64.v );", file=f)
        if 4 * emul <= 8 and 24 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_LOAD_VX_4regs( "+str(n)+",  vlsseg4e64.v );", file=f)
        if 5 * emul <= 8 and 24 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_LOAD_VX_5regs( "+str(n)+",  vlsseg5e64.v );", file=f)
        if 6 * emul <= 8 and 24 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_LOAD_VX_6regs( "+str(n)+",  vlsseg6e64.v );", file=f)
        if 7 * emul <= 8 and 24 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_LOAD_VX_7regs( "+str(n)+",  vlsseg7e64.v );", file=f)
        if 8 * emul <= 8 and 24 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_LOAD_VX_8regs( "+str(n)+",  vlsseg8e64.v );", file=f)
        

    # if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
    #     for i in range(100):     
    #         k = i%30+1
    #         if k != 8 and k != 16 and k % emul == 0 and k + 2 * emul <= 32:
    #             n+=1
    #             print("  TEST_VLSSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0xff"+", "+"1"+", "+"0 + tdat"+" );",file=f)
            
    #         k = i%30+2
    #         if(k == 31):
    #             continue;
    #         n +=1
    #         print("  TEST_VLSSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0x00"+", "+"1"+", "+"4 + tdat"+" );",file=f)
    
def create_empty_test_vlssege64(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Generate macros to test diffrent register
    generate_macros_load_vx_Nregs(f, 64, 16); # for vlsseg2e8

    # Generate tests
    generate_tests(f, vsew, lmul)

    print_load_ending_new(f, 64, is_vx = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path

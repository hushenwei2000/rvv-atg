import logging
import os

from scripts.constants import *

def run_riscof_coverage(instr, rvv_atg_root, cgf_path, output_dir, test_path, suffix, xlen, flen, vlen, elen, vsew, lmul, use_fail_macro, tool):
    gcc = GCC_CONST
    objdump = OBJDUMP_CONST
    logging.info("Running riscof coverage: {}.{}".format(instr, suffix))
    test_path = os.path.basename(test_path)
    # cgf_path = os.path.basename(cgf_path)
    isac_log_name = 'isac_log_' + suffix
    os.chdir(output_dir)
    lmul_num = lmul
    if lmul < 1:
        lmul = str(lmul).replace(".", "")
    else:
        lmul = str(int(lmul))
        lmul_num = int(lmul_num)
    logging.info("Running riscof coverage: {}.{}, stage: Compiling...".format(instr, suffix))

    gcc_string = "%s -march=rv64gv    -w     -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles         -T /work/stu/swhu/projects/riscof-sample/spike/env/link.ld         -I %s/env/macros/vsew%d_lmul%s%s         -I %s/env/p         -I %s/env         -I %s/env/sail_cSim -mabi=lp64 -I /work/stu/swhu/projects/riscof-sample/spike/env %s -o ref_%s.elf -DTEST_CASE_1=True -DXLEN=%d -DFLEN=%d;" %(gcc, rvv_atg_root, vsew, lmul, ("" if use_fail_macro else "_nofail"), rvv_atg_root, rvv_atg_root, rvv_atg_root, test_path, suffix, xlen, flen)
    
    print(gcc_string)
    os.system(gcc_string)


    logging.info("Running riscof coverage: {}.{}, stage: ObjDumping...".format(instr, suffix))

    os.system("%s -D ref_%s.elf > ref_%s.disass;" %
              (objdump, suffix, suffix))

    # EITHER Use sail log to run isac
    if tool == 'sail':
        logging.info("Running riscof coverage: {}.{}, stage: Sail Running...".format(instr, suffix))
        os.system("riscv_sim_RV64 --test-signature=%s/Reference-sail_c_simulator.signature ref_%s.elf > %s_%s.log 2>&1;" % (output_dir, suffix, instr, suffix))
        isac_string = "riscv_isac --verbose info coverage -d                         -t %s_%s.log --parser-name c_sail -o coverage_%s.rpt                         --sig-label begin_signature  end_signature                         --test-label rvtest_code_begin cleanup_epilogs                         -e ref_%s.elf -c %s/cgfs/dataset.yaml -c %s -x%d -v%d --vsew %d --lmul %s --flen %d -l %s > %s 2>&1;" %(instr, suffix, suffix, suffix, rvv_atg_root, cgf_path, xlen, vlen, vsew, str(lmul_num), flen, instr, isac_log_name)
    else:
        # OR Use spike log to run isac
        logging.info("Running riscof coverage: {}.{}, stage: Spike Running...".format(instr, suffix))
        os.system("spike --isa rv64gcv_zfh -l --log-commits --varch=vlen:%d,elen:%d ref_%s.elf > spike_%s_%s.log 2>&1;" % (vlen, elen, suffix, instr, suffix))
        isac_string = "riscv_isac --verbose info coverage -d                         -t spike_%s_%s.log --parser-name spike -o coverage_%s.rpt                         --sig-label begin_signature  end_signature                         --test-label rvtest_code_begin cleanup_epilogs                         -e ref_%s.elf -c %s/cgfs/dataset.yaml -c %s -x%d -v%d --vsew %d --lmul %s --flen %d -l %s > %s 2>&1;" %(instr, suffix, suffix, suffix, rvv_atg_root, cgf_path, xlen, vlen, vsew, str(lmul_num), flen, instr, isac_log_name)

    print(isac_string)
    logging.info("Running riscof coverage: {}.{}, stage: RISCV-ISAC Running...".format(instr, suffix))

    os.system(isac_string)

    os.chdir(rvv_atg_root)

    logging.info("Running riscof coverage {} finish!".format(instr))
    return (rvv_atg_root + '/' + output_dir + '/coverage_%s.rpt' % suffix, rvv_atg_root + '/' + output_dir + '/' + isac_log_name)
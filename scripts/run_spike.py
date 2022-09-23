import logging
import os


def run_spike(instr, rvv_atg_root, cgf_path, output_dir, test_path, suffix, xlen, flen, vlen, vsew, use_fail_macro):
    logging.info("Running spike: {}.{}".format(instr, suffix))
    test_path = os.path.basename(test_path)
    cgf_path = os.path.basename(cgf_path)
    spike_log_name = "spike_%s_%s.log"%(instr, suffix)
    os.chdir(output_dir)

    logging.info("Running spike: {}.{}, stage: Compiling...".format(instr, suffix))

    gcc_string = "riscv64-rivai-elf-gcc -march=rv64gv    -w     -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles         -T %s/env/p/link.ld         -I %s/env/macros/vsew%d%s         -I %s/env/p         -I %s/env         -I %s/env/sail_cSim -mabi=lp64  %s -o ref_%s.elf -DTEST_CASE_1=True -DXLEN=%d -DFLEN=%d;" %(rvv_atg_root, rvv_atg_root, vsew, ("" if use_fail_macro else "_nofail"), rvv_atg_root, rvv_atg_root, rvv_atg_root, test_path, suffix, xlen, flen)
    
    print(gcc_string)
    os.system(gcc_string)


    logging.info("Running spike: {}.{}, stage: ObjDumping...".format(instr, suffix))

    os.system("riscv64-rivai-elf-objdump -D ref_%s.elf > ref_%s.disass;" %
              (suffix, suffix))

    logging.info("Running spike: {}.{}, stage: Spike Running...".format(instr, suffix))

    os.system("spike --isa rv64gcv_zfh -l --log-commits --varch=vlen:%d,elen:%d ref_%s.elf > %s 2>&1;" %
              (vlen, vlen, suffix, spike_log_name))

    os.chdir(rvv_atg_root)

    logging.info("Running spike {} finish!".format(instr))
    return rvv_atg_root + '/' + output_dir + '/' + spike_log_name

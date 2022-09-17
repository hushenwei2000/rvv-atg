import logging
import os


def run_riscof_coverage(instr, rvv_atg_root, cgf_path, output_dir, riscof_dir, test_path, suffix, xlen, flen, vlen, use_fail_macro):
    logging.info("Running riscof coverage: {}.{}".format(instr, suffix))
    test_path = os.path.basename(test_path)
    cgf_path = os.path.basename(cgf_path)
    isac_log_name = 'isac_log_' + suffix
    os.chdir(output_dir)

    os.system("riscv64-rivai-elf-gcc -march=rv64gv         -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles         -T %s/riscv-tests-vector/env/p/link.ld         -I %s/riscv-tests-vector/env/../isa/macros/%s         -I %s/riscv-tests-vector/env/p         -I %s/riscv-tests-vector/env         -I %s/sail_cSim/env -mabi=lp64  %s -o ref_%s.elf -DTEST_CASE_1=True -DXLEN=%d -DFLEN=%d;" %
              (riscof_dir, riscof_dir, ("fail" if use_fail_macro else "scalar"), riscof_dir, riscof_dir, riscof_dir, test_path, suffix, xlen, flen))

    os.system("riscv64-rivai-elf-objdump -D ref_%s.elf > ref_%s.disass;" %
              (suffix, suffix))

    os.system("riscv_sim_RV64 --test-signature=%s/Reference-sail_c_simulator.signature ref_%s.elf > %s_%s.log 2>&1;" %
              (output_dir, suffix, instr, suffix))

    os.system("riscv_isac --verbose info coverage -d                         -t %s_%s.log --parser-name c_sail -o coverage_%s.rpt                         --sig-label begin_signature  end_signature                         --test-label _start _end                         -e ref_%s.elf -c %s/dataset.yaml -c %s -x%d -v%d -l %s > %s 2>&1;" %
              (instr, suffix, suffix, suffix, riscof_dir, cgf_path, xlen, vlen, instr, isac_log_name))

    os.chdir(rvv_atg_root)

    logging.info("Running riscof coverage {} finish!".format(instr))
    return (rvv_atg_root + '/' + output_dir + '/coverage_%s.rpt' % suffix, rvv_atg_root + '/' + output_dir + '/' + isac_log_name)

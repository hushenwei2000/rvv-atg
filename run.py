
import argparse
from ast import arg
import os

from scripts.lib import *
from scripts.replace_results import replace_results
from scripts.run_riscof_coverage import run_riscof_coverage
from scripts.run_spike import run_spike


def parse_args(cwd):
    """Create a command line parser.
    Returns: The created parser.
    """
    # Parse input arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--xlen", type=int, default="64",
                        help="XLEN Value for the ISA: \
                            32, 64(default)")
    parser.add_argument("--flen", type=int, default="-1",
                        help="FLEN Value for the ISA: \
                            32(default), 64")
    parser.add_argument("--vlen", type=int, default="128",
                        help="Vector Register Length: \
                        32, 64, 128(default), 256, 512, 1024")
    parser.add_argument("--elen", type=int, default="-1",
                        help="The maximum size of a vector element that any operation can produce or consume in bits: \
                        default = vlen")
    parser.add_argument("--vsew", type=int, default="32",
                        help="Selected Element Width: \
                        8, 16, 32(default), 64")
    parser.add_argument("--lmul", type=float, default="1",
                        help="Vector Register Grouping Multiplier: \
                        0.125, 0.25, 0.5, 1(default), 2, 4, 8")
    parser.add_argument("--vta", type=int, default="1",
                        help="Vector Tail Agnostic Mode: \
                        0(undisturbed, default), 1(agnostic)")
    parser.add_argument("--vma", type=float, default="1",
                        help="Vector Mask Agnostic Mode: \
                        0(undisturbed, default), 1(agnostic)")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        default=False,
                        help="Verbose Logging")
    parser.add_argument("-o", "--output", type=str,
                        help="Output Directory Name", dest="o")
    parser.add_argument("-i", "--instr", type=str,
                        help="One Instruction Needing to Generate Tests", dest="i")
    parser.add_argument("-t", "--type", type=str,
                        help="Type of Instruction: i, f, m", dest="t")
    args = parser.parse_args()
    if args.elen == -1:
        args.elen = args.vlen
    if args.flen == -1:
        if args.vsew == 32 or args.vsew == 64:
            args.flen = args.vsew
        else:
            args.flen = 32
    return args


def run_vf(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4-1. Run sail and riscof coverage and extract true result from isac_log
    # (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                    #   output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 4-2. Or run spike to generate commit info log
    spike_first_log = run_spike(args.i, cwd, cgf,
              output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 5-1. Replace old result with true results using sail and isac log
    # des_path = replace_results(args.i, first_test, isac_log_first, 'sail')

    # 5-2. Or use spike log
    des_path = replace_results(args.i, first_test, spike_first_log, 'spike')

    # 6. Run spike test generated ref_final.elf
    # run_spike(args.i, cwd, cgf,
    #           output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)


    # 6. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    check_spikelog(output_dir, args.i)

def run_integer(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4-1. Run sail and riscof coverage and extract true result from isac_log
    # (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
    #                                                   output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 4-2. Or run spike to generate commit info log
    spike_first_log = run_spike(args.i, cwd, cgf,
              output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    search_ins = args.i
    if args.i in ["vmadc", "vmsbc", "vmseq", "vmsgt", "vmsgtu", "vmsle", "vmsleu", "vmslt", "vmsltu", "vmsne"]:
        search_ins = "vcpop"
    # 5-1. Replace old result with true results using sail and isac log
    # des_path = replace_results(search_ins, first_test, isac_log_first, 'sail')

    # 5-2. Or use spike log
    des_path = replace_results(search_ins, first_test, spike_first_log, 'spike')

    # 6. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    # 7. Run spike test generated ref_final.elf
    # run_spike(args.i, cwd, cgf,
    #       output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    check_spikelog(output_dir, args.i)

def run_mask(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    riscof_dir = '/work/stu/swhu/projects/riscof-sample'

    # 2-1. Run sail and riscof coverage and extract true result from isac_log
    # (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
    #                                                   output_dir, empty_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 2-2. Or run spike to generate commit info log
    spike_first_log = run_spike(args.i, cwd, cgf,
              output_dir, empty_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 3-1. Replace old result with true results using sail and isac_log_first
    # des_path = replace_results("vcpop", empty_test, isac_log_first, 'sail')

    # 3-2. Or use spike log
    search_ins = "vcpop"
    if args.i in ["vfirst", "vrgather", "vrgatherei16"]:
        search_ins = args.i
    des_path = replace_results(search_ins, empty_test, spike_first_log, 'spike')

    # 5. Run spike test generated ref_final.elf
    # run_spike(args.i, cwd, cgf,
    #           output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)
    
    # 4. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    check_spikelog(output_dir, args.i)

def run_loadstore(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4-1. Run sail and riscof coverage and extract true result from isac_log
    # (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                    #   output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    # 4-2. Or run spike to generate commit info log
    # spike_first_log = run_spike(args.i, cwd, cgf,
    #           output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, use_fail_macro=False)

    # 5-1. Replace old result with true results using sail and isac log
    # des_path = replace_results(args.i, first_test, isac_log_first, 'sail')

    # 5-2. Or use spike log
    # des_path = replace_results(args.i, first_test, spike_first_log, 'spike')

    # 6. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, first_test, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    # 7. Run spike test generated ref_final.elf
    # run_spike(args.i, cwd, cgf,
    #       output_dir, first_test, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    check_spikelog(output_dir, args.i)

def main():
    # Full path of current dir
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.environ["RVV_ATG_ROOT"] = cwd
    args = parse_args(cwd)
    setup_logging(args.verbose)
    output_dir = create_output(args)
    cgf = create_cgf_path(args.i, args.t, args.lmul, cwd, output_dir)
    logging.info("RVV-ATG: instr: %s, vlen: %d, vsew: %d, lmul: %d"%(args.i, args.vlen, args.vsew, args.lmul))
    if not check_type(args.i, args.t):
        logging.error("Type is not match Instruction!")
        return
    if args.t == "f":
        run_vf(cwd, args, cgf, output_dir)
    elif args.t == "i" or args.t == "x":
        run_integer(cwd, args, cgf,  output_dir)
    elif args.t == "m" or args.t == "p":
        run_mask(cwd, args, cgf, output_dir)
    elif args.t == "l":
        run_loadstore(cwd, args, cgf, output_dir)


if __name__ == "__main__":
    main()

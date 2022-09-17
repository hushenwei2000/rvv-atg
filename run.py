
import argparse
from ast import arg
import os

from scripts.lib import *
from scripts.replact_results import replace_results
from scripts.run_riscof_coverage import run_riscof_coverage


def parse_args(cwd):
    """Create a command line parser.
    Returns: The created parser.
    """
    # Parse input arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--xlen", type=int, default="64",
                        help="XLEN Value for the ISA: \
                            32, 64(default)")
    parser.add_argument("--flen", type=int, default="32",
                        help="FLEN Value for the ISA: \
                            32(default), 64")
    parser.add_argument("--vlen", type=int, default="128",
                        help="Vector Register Length: \
                        32, 64, 128(default), 256, 512, 1024")
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
    return args


def run_vf(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    riscof_dir = '/work/stu/swhu/projects/riscof-sample'
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, use_fail_macro=False)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4. Run riscof coverage and extract true result from isac_log
    (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, first_test, 'first', args.xlen, args.flen, args.vlen, use_fail_macro=False)

    # 5. Replace old result with true results
    replace_results(args.i, first_test, isac_log_first)

    # 6. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, first_test, 'final', args.xlen, args.flen, args.vlen, use_fail_macro=True)


def run_integer(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    riscof_dir = '/work/stu/swhu/projects/riscof-sample'
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, use_fail_macro=False)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4. Run riscof coverage and extract true result from isac_log
    (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, first_test, 'first', args.xlen, args.flen, args.vlen, use_fail_macro=False)

    # 5. Replace old result with true results
    des_path = replace_results(args.i, first_test, isac_log_first)

    # 6. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, des_path, 'final', args.xlen, args.flen, args.vlen, use_fail_macro=True)


def run_mask(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    riscof_dir = '/work/stu/swhu/projects/riscof-sample'

    # 4. Run riscof coverage and extract true result from isac_log
    (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, empty_test, 'first', args.xlen, args.flen, args.vlen, use_fail_macro=False)

    # 5. Replace old result with true results
    des_path = replace_results("vpopc", empty_test, isac_log_first)

    # 6. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, riscof_dir, des_path, 'final', args.xlen, args.flen, args.vlen, use_fail_macro=True)


def main():
    # Full path of current dir
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.environ["RVV_ATG_ROOT"] = cwd
    args = parse_args(cwd)
    setup_logging(args.verbose)
    output_dir = create_output(args.i, args.o)
    cgf = create_cgf_path(args.i, args.t, cwd, output_dir)

    if args.t == "f":
        run_vf(cwd, args, cgf, output_dir)
    elif args.t == "i":
        run_integer(cwd, args, cgf,  output_dir)
    elif args.t == "m":
        run_mask(cwd, args, cgf, output_dir)


if __name__ == "__main__":
    main()

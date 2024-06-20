
import argparse
from ast import arg
import os

from scripts.lib import *
from scripts.replace_results import replace_results
from scripts.run_riscof_coverage import run_riscof_coverage
from scripts.run_spike import run_spike
from scripts.constants import *
from scripts.create_test_combination.testgen import *


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
    parser.add_argument("--elen", type=int, default="-1",
                        help="The maximum size of a vector element that any operation can produce or consume in bits: \
                        default = 64")
    parser.add_argument("--vsew", type=int, default="32",
                        help="Selected Element Width: \
                        8, 16, 32(default), 64")
    parser.add_argument("--lmul", type=float, default="1",
                        help="Vector Register Grouping Multiplier: \
                        0.125, 0.25, 0.5, 1(default), 2, 4, 8")
    parser.add_argument("--vta", type=int, default="0",
                        help="Vector Tail Agnostic Mode: \
                        0(undisturbed, default), 1(agnostic)")
    parser.add_argument("--vma", type=int, default="0",
                        help="Vector Mask Agnostic Mode: \
                        0(undisturbed, default), 1(agnostic)")
    parser.add_argument("--agnostic_type", type=int, default="0",
                        help="If vta or vma is 1(agnostic),  \
                        0(retain the value they previously held, default), or 1(written with 1s)")
    parser.add_argument("--masked", type=str, default="True",
                        help="If enable masked")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        default=False,
                        help="Verbose Logging")
    parser.add_argument("-o", "--output", type=str,
                        help="Output Directory Name", dest="o")
    parser.add_argument("-i", "--instr", type=str,
                        help="One Instruction Needing to Generate Tests", dest="i")
    parser.add_argument("-t", "--type", type=str,
                        help="Type of Instruction: i, f, m", dest="t")
    parser.add_argument("--tool", type=str,
                        help="Tool to rgenerate log: spike(default), sail", default="spike")
    parser.add_argument("--etype", type=str,
                        help="Type of exception to test",default="illegal_instruction")
    parser.add_argument("--etest", type=str,
                        help="which exception to test",default="vs")
    parser.add_argument("-b","--batch", type=int, default="1",
                        help="Batch mode")
    args = parser.parse_args()
    if args.elen == -1:
        args.elen = 64
    if args.vma == 0:
        args.vma = False
    else:
        args.vma = True
    if args.vta == 0:
        args.vta = False
    else:
        args.vta = True
    return args


def run_vf(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False, tool=args.tool)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    if args.tool == 'sail':
        # 4-1. Run sail and riscof coverage and extract true result from isac_log
        (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                        output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False, tool=args.tool)
    else:
        # 4-2. Or run spike to generate commit info log
        spike_first_log = run_spike(args.i, cwd, 
                  output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    search_ins = args.i
    original_ins = args.i
    if args.i.startswith("vmf"):
        search_ins = "vcpop"


    if args.tool == 'sail':
        # 5-1. Replace old result with true results using sail and isac log
        des_path = replace_results(search_ins, first_test, isac_log_first, 'sail', original_ins)
    else:
        # 5-2. Or use spike log
        des_path = replace_results(search_ins, first_test, spike_first_log, 'spike', original_ins)

    # 6. Run final riscof coverage
    # (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
    #                                                   output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True, tool='spike')

    spike_final_log = run_spike(args.i, cwd, 
            output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    if os.environ["RVV_ATG_AGNOSTIC_TYPE"] != "1":
        check_spikelog(output_dir, args.i)

def run_integer(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False, tool=args.tool)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    if args.tool == 'sail':
        # 4-1. Run sail and riscof coverage and extract true result from isac_log
        (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                          output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False, tool=args.tool)
    else:
        # 4-2. Or run spike to generate commit info log
        spike_first_log = run_spike(args.i, cwd,
                output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    search_ins = args.i
    if args.i in ["vmadc", "vmsbc", "vmseq", "vmsgt", "vmsgtu", "vmsle", "vmsleu", "vmslt", "vmsltu", "vmsne"]:
        search_ins = "vcpop"
    
    if args.tool == 'sail':
        # 5-1. Replace old result with true results using sail and isac log
        des_path = replace_results(search_ins, first_test, isac_log_first, 'sail')
    else:
        # 5-2. Or use spike log
        des_path = replace_results(search_ins, first_test, spike_first_log, 'spike')

    # 6. Run final riscof coverage
    # (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
    #                                                   output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True, tool='spike')

    spike_final_log = run_spike(args.i, cwd, 
            output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    if os.environ["RVV_ATG_AGNOSTIC_TYPE"] != "1":
        check_spikelog(output_dir, args.i)

def run_mask(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    riscof_dir = RISCOF_CONST

    if args.tool == 'sail':
        # 2-1. Run sail and riscof coverage and extract true result from isac_log
        (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                          output_dir, empty_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False, tool=args.tool)
    else:
        # 2-2. Or run spike to generate commit info log
        spike_first_log = run_spike(args.i, cwd, 
                output_dir, empty_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False)

    if args.tool == 'sail':
        # 3-1. Replace old result with true results using sail and isac_log_first
        des_path = replace_results("vcpop", empty_test, isac_log_first, 'sail')
    else:
        # 3-2. Or use spike log
        search_ins = "vcpop"
        if args.i in ["vfirst", "vrgather", "vrgatherei16"]:
            search_ins = args.i
        des_path = replace_results(search_ins, empty_test, spike_first_log, 'spike')
 
    # 4. Run final riscof coverage
    # (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
    #                                                   output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True, tool='spike')

    spike_final_log = run_spike(args.i, cwd, 
            output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)
    
    if os.environ["RVV_ATG_AGNOSTIC_TYPE"] != "1":
        check_spikelog(output_dir, args.i)

def run_loadstore(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False, tool=args.tool)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    if args.tool == 'sail':
        # 4-1. Run sail and riscof coverage and extract true result from isac_log
        (rpt_first, isac_log_first) = run_riscof_coverage(args.i, cwd, cgf,
                                                          output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=False, tool=args.tool)
    else:
        # 4-2. Or run spike to generate commit info log
        spike_first_log = run_spike(args.i, cwd, 
                  output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    if args.tool == 'sail':
        # 5-1. Replace old result with true results using sail and isac log
        des_path = replace_results(args.i, first_test, isac_log_first, 'sail')
    else:
        # 5-2. Or use spike log
        des_path = replace_results(args.i, first_test, spike_first_log, 'spike')

    # 6. Run final riscof coverage
    # (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
    #                                                   output_dir, first_test, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True, tool='spike')

    spike_final_log = run_spike(args.i, cwd, 
            output_dir, des_path, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    if os.environ["RVV_ATG_AGNOSTIC_TYPE"] != "1":
        check_spikelog(output_dir, args.i)

def run_loadstore_new(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Or run spike to generate commit info log
    spike_first_log = run_spike(args.i, cwd, 
                output_dir, empty_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True)

    # 3. Run final riscof coverage
    (rpt_final, isac_log_final) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'final', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, use_fail_macro=True, tool='spike')

    if os.environ["RVV_ATG_AGNOSTIC_TYPE"] != "1":
        check_spikelog(output_dir, args.i)


def run_exception(cwd,args):
    gcc = GCC_CONST
    objdump = OBJDUMP_CONST
    # 1. create output directory
    etype = args.etype
    etest = args.etest
    output = args.o
    if output is None:
        output = str(date.today())[5:] + "-" + str(etype)+ "-" + str(etest)
    os.system("rm -rf {}".format(output))

    logging.info("Creating output directory: {}".format(output))
    subprocess.run(["mkdir", "-p", output])
    #2. run make
    os.chdir('./scripts/create_test_exception')
    os.system("rm -rf ./build")
    os.system("make GCC=%s OBJ=%s TYPE=%s TEST=%s DEBUG=%s" %(gcc, objdump, args.etype, args.etest, args.batch))
    #3. move output to output directory
    os.system("mv ./build %s/%s" %(cwd,output))

def run_combination(cwd, args):
    output_dir = args.o
    if output_dir is None:
        output_dir = str(date.today())[5:] + "-vlen" + str(args.vlen) + "-vsew" + str(args.vsew) + "-lmul" + str(args.lmul)
    os.system("rm -rf {}".format(output_dir))
    logging.info("Creating output directory: {}".format(output_dir))
    subprocess.run(["mkdir", "-p", output_dir])
    test_generator(cwd, args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul, output_dir)

def run_combination_all(cwd, args):
    output_dir = args.o
    if output_dir is None:
        output_dir = str(date.today())[5:] + "-ctest_vlen" + str(args.vlen)
    os.system("rm -rf {}".format(output_dir))
    logging.info("Creating output directory: {}".format(output_dir))
    subprocess.run(["mkdir", "-p", output_dir])
    ctest_all(cwd, args.xlen, args.flen, args.vlen, args.elen, output_dir)

def main():
    # Full path of current dir
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.environ["RVV_ATG_ROOT"] = cwd
    args = parse_args(cwd)
    setup_logging(args.verbose)
    # run exception test
    if args.t == "e":
        # print("get e!")
        run_exception(cwd, args)
        return
    # combination test, ignore instr in this case
    elif args.t == "c":
        run_combination(cwd, args)
        return
    elif args.t == "ca":
        run_combination_all(cwd, args)
        return
    
    output_dir = create_output(args)
    cgf = create_cgf_path(args.i, args.t, args.lmul, cwd, output_dir)
    rewrite_macro_vtavma(args.vsew, args.lmul, args.vta, args.vma)
    logging.info("RVV-ATG: instr: %s, vlen: %d, vsew: %d, lmul: %f"%(args.i, args.vlen, args.vsew, args.lmul))
    os.environ["RVV_ATG_VLEN"] = str(args.vlen)
    os.environ["RVV_ATG_VSEW"] = str(args.vsew)
    os.environ["RVV_ATG_LMUL"] = str(args.lmul)
    os.environ["RVV_ATG_MASKED"] = str(args.masked)
    os.environ["RVV_ATG_VMA"] = str(args.vma)
    os.environ["RVV_ATG_VTA"] = str(args.vta)
    os.environ["RVV_ATG_AGNOSTIC_TYPE"] = str(args.agnostic_type)
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
        # TODO: new load store
        # if args.i in ["vlssege8", "vlssege16", "vlssege32", "vlssege64"]:
        #     run_loadstore_new(cwd, args, cgf, output_dir)
        # else:
        #     run_loadstore(cwd, args, cgf, output_dir)
        run_loadstore(cwd, args, cgf, output_dir)


if __name__ == "__main__":
    main()
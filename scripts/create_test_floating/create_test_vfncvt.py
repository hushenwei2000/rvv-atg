import logging
import os
from scripts.test_common_info import *
import re

instr = 'vfncvt'
rs1_val = ["0x00000000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000",
           "0x00800000", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", ]
rs2_val = ["0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000",
           "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", ]


def generate_fdat_seg(f):
    print("fdat_rs1:", file=f)
    for i in range(len(rs1_val)):
        print("fdat_rs1_" + str(i) + ":  .word " + rs1_val[i], file=f)
    print("", file=f)
    print("fdat_rs2:", file=f)
    for i in range(len(rs2_val)):
        print("fdat_rs2_" + str(i) + ":  .word " + rs2_val[i], file=f)


def generate_macros(f):
    for n in range(1,32):
        if n == 14:
            continue
        print("#define TEST_N_FP_INT_OP_rs1_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE_N_FP_INT( testnum, v14, flags, __riscv_vsew, result, val, \\\n\
                fld f0, 0(a0); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vfmv.s.f v%d, f0; "%n + "\\\n\
                VSET_VSEW \\\n\
                inst v14, v%d; "%n + "\\\n\
            )", file = f)

    for n in range(1,32):
        if n == 2:
            continue
        print("#define TEST_N_FP_INT_OP_rd_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE_N_FP_INT( testnum, v%d, flags, __riscv_vsew, result, val,"%n + "   \\\n\
                fld f0, 0(a0); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vfmv.s.f v2, f0; \\\n\
                VSET_VSEW \\\n\
                inst v%d, v2; "%n + "\\\n\
            )", file = f)

    for n in range(1,32):
        if n == 14:
            continue
        print("#define TEST_N_INT_FP_OP_rs1_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE_INT_FP( testnum, v14, flags, result, val, \\\n\
                li x7, MASK_DOUBLE_VSEW(val); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v%d, x7;   "%n + "\\\n\
                VSET_VSEW \\\n\
                flw f2, 0(a0); \\\n\
                inst v14, v%d; "%n + "\\\n\
            )", file = f)

    for n in range(1,32):
        if n == 2:
            continue
        print("#define TEST_N_INT_FP_OP_rd_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE_INT_FP( testnum, v%d, flags, result, val, "%n + " \\\n\
                li x7, MASK_DOUBLE_VSEW(val); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v2, x7;  \\\n\
                VSET_VSEW \\\n\
                flw f2, 0(a0); \\\n\
                inst v%d, v2; "%n + "\\\n\
            )", file = f)

    for n in range(1,32):
        if n == 14:
            continue
        print("#define TEST_N_FP_1OPERAND_OP_rs1_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE_N_FP( testnum, v14, flags, result, val, 0, \\\n\
                fld f0, 0(a0); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vfmv.s.f v%d, f0; "%n + "\\\n\
                VSET_VSEW \\\n\
                flw f2, 8(a0); \\\n\
                inst v14, v%d; "%n + "\\\n\
            )", file = f)

    for n in range(1,32):
        if n == 2:
            continue
        print("#define TEST_N_FP_1OPERAND_OP_rd_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE_N_FP( testnum, v%d, flags, result, val, 0, "%n + "\\\n\
                fld f0, 0(a0); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vfmv.s.f v2, f0; \\\n\
                VSET_VSEW \\\n\
                flw f2, 8(a0); \\\n\
                inst v%d, v2; "%n + "\\\n\
            )", file = f)


def extract_operands(f, rpt_path):
    # Floating pooints tests don't need to extract operands, rs1 and rs2 are fixed
    return 0


def generate_tests(f, rs1_val, rs2_val):    
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.xu.f.w (double-width float to unsigned integer) tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):        
        print("TEST_N_FP_INT_OP( %d,  %s.xu.f.w, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.x.f.w (double-width float to signed integer) tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):
        print("TEST_N_FP_INT_OP( %d,  %s.x.f.w, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.rtz.xu.f.w (double-width float to signed integer truncating) tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):
        print("TEST_N_FP_INT_OP( %d,  %s.rtz.xu.f.w, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.rtz.x.f.w (double-width float to signed integer truncating) tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):
        print("TEST_N_FP_INT_OP( %d,  %s.rtz.x.f.w, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.f.xu.w (double-width unsigned integer to float) tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):
        print("TEST_N_INT_FP_OP( %d,  %s.f.xu.w, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.f.x.w (double-width signed integer to float) tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):        
        print("TEST_N_INT_FP_OP( %d,  %s.f.x.w, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.f.f.w (single-width float to double-width float) tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):        
        print("TEST_N_FP_1OPERAND_OP( %d,  %s.f.f.w, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n +=1


    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.xu.f.w (double-width float to unsigned integer) tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):
        k = i%31+1
        if k == 2:
            continue        
        print("  TEST_N_FP_INT_OP_rd_%d( "%k+str(n)+",  %s.xu.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n+=1
        
        k = i%31+1
        if k == 14:
            continue        
        print("  TEST_N_FP_INT_OP_rs1_%d( "%k+str(n)+",  %s.xu.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n +=1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.x.f.w (double-width float to signed integer) tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):     
        k = i%31+1
        if k == 2:
            continue        
        print("  TEST_N_FP_INT_OP_rd_%d( "%k+str(n)+",  %s.x.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n+=1
        
        k = i%31+1
        if k == 14:
            continue        
        print("  TEST_N_FP_INT_OP_rs1_%d( "%k+str(n)+",  %s.x.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.rtz.xu.f.w (double-width float to unsigned integer truncating) tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):     
        k = i%31+1
        if k == 2:
            continue        
        print("  TEST_N_FP_INT_OP_rd_%d( "%k+str(n)+",  %s.rtz.xu.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n+=1
        
        k = i%31+1
        if k == 14:
            continue        
        print("  TEST_N_FP_INT_OP_rs1_%d( "%k+str(n)+",  %s.rtz.xu.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.rtz.x.f.w (double-width float to signed integer truncating) tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):     
        k = i%31+1
        if k == 2:
            continue        
        print("  TEST_N_FP_INT_OP_rd_%d( "%k+str(n)+",  %s.rtz.x.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n+=1
        
        k = i%31+1
        if k == 14:
            continue        
        print("  TEST_N_FP_INT_OP_rs1_%d( "%k+str(n)+",  %s.rtz.x.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.f.xu.w (double-width unsigned integer to float) tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)   
    for i in range(len(rs1_val)):     
        k = i%31+1
        if k == 2:
            continue       
        print("  TEST_N_INT_FP_OP_rd_%d( "%k+str(n)+",  %s.f.xu.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n+=1
        
        k = i%31+1
        if k == 14:
            continue        
        print("  TEST_N_INT_FP_OP_rs1_%d( "%k+str(n)+",  %s.f.xu.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.f.x.w (double-width signed integer to float) tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)   
    for i in range(len(rs1_val)):     
        k = i%31+1
        if k == 2:
            continue        
        print("  TEST_N_INT_FP_OP_rd_%d( "%k+str(n)+",  %s.f.x.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n+=1

        k = i%31+1
        if k == 14:
            continue        
        print("  TEST_N_INT_FP_OP_rs1_%d( "%k+str(n)+",  %s.f.x.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfncvt.f.f.w (single-width float to double-width float) tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):     
        k = i%31+1
        if k == 2:
            continue        
        print("  TEST_N_FP_1OPERAND_OP_rd_%d( "%k+str(n)+",  %s.f.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n+=1

        k = i%31+1
        if k == 14:
            continue        
        print("  TEST_N_FP_1OPERAND_OP_rs1_%d( "%k+str(n)+",  %s.f.f.w, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n +=1

def print_ending(f):
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
    \n\
    TEST_VV_OP(9999, vadd.vv, 2, 1, 1)\n\
    TEST_PASSFAIL\n\
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
    ", file=f)

    generate_fdat_seg(f)

    print("signature_x12_0:\n\
        .fill 0,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x12_1:\n\
        .fill 32,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_0:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_1:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_2:\n\
        .fill 376,4,0xdeadbeef\n\
    \n\
    #ifdef rvtest_mtrap_routine\n\
    \n\
    mtrap_sigptr:\n\
        .fill 128,4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    #ifdef rvtest_gpr_save\n\
    \n\
    gpr_save:\n\
        .fill 32*(XLEN/32),4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    RVTEST_DATA_END\n\
    ", file=f)


def create_empty_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VFMVF_OP( 1,  fdat_rs1_0 );", file=f)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path

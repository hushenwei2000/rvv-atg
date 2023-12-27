#----------------------------------------------------------------------------- 
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # can not test
    #-----------------------------------------------------------------------------
    #
    # test offset with eew which not support
    #

    #include "model_test.h"
    #include "arch_test.h"
    #include "riscv_test.h"
    #include "test_macros_vector.h"

RVTEST_ISA("RV64RV64IMAFDCVZicsr")
    
    .section .text.init
    .globl rvtest_entry_point
    rvtest_entry_point:
    
    
    RVTEST_CASE(0,"//check ISA:=regex(.*64.*);check ISA:=regex(.*V.*);def TEST_CASE_1=True;",vadd)
    
    RVTEST_RV64UV
    RVMODEL_BOOT
    RVTEST_CODE_BEGIN
    RVTEST_VSET
# begin test here-----------------------------------------------------------------------------------
    li a0,59285;
    vsetivli x31, 1, e64, m1;
    li  t0,0x80005000;
    li  t2,0x0123456789abcdef;
    sd  t2,(t0);
    li  t2,0xdeadbeefdeadbeef;
    sd  t2,8(t0);    

    li  t1,0x001000000c080400;
    vmv.v.x	v16,t1;
    vsetivli x31, 4, e32, m1;
    vluxei8.v v5,(t0),v16;

    vsetivli x31, 1, e64, m1;
    li  t1,0x000c000800040000;
    vmv.v.x	v16,t1;
    vsetivli x31, 4, e32, m1;
    vluxei16.v v5,(t0),v16;

    vsetivli x31, 1, e64, m1;
    li  t1,0x000000800000000;
    vmv.v.x	v16,t1;
    vsetivli x31, 2, e64, m1;
    vluxei32.v v5,(t0),v16;

    vsetivli x31, 1, e64, m1;
    li  t1,0x00000000000000;
    li  t2,0x80006000;
    sd  t1,(t2);
    li  t1,0x00000000000008;
    sd  t1,8(t2);
    vsetivli x31, 2, e64, m1;
    vle64.v v16,(t2);
    vsetivli x31, 2, e64, m1;
    vluxei64.v v6,(t0),v16;

    call pass;

# end test here-------------------------------------------------------------------------------------
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)
    TEST_PASSFAIL

handle_illegal_instruction:                                             
    li t0,59285;                                                 
    beq a0,t0,pass;   
    call other_exception;  

handle_misaligned_load_store:
    call other_exception;

handle_misaligned_fetch:
    call other_exception;
    
handle_page_fault:
    call other_exception;

handle_access:
    call other_exception;

    RVTEST_CODE_END

    RVMODEL_HALT
    
    .data
    RVTEST_DATA_BEGIN
    
    TEST_DATA
 

    signature_x12_0:
        .fill 0,4,0xdeadbeef
    
    
    signature_x12_1:
        .fill 32,4,0xdeadbeef
    
    
    signature_x20_0:
        .fill 512,4,0xdeadbeef
    
    
    signature_x20_1:
        .fill 512,4,0xdeadbeef
    
    
    signature_x20_2:
        .fill 376,4,0xdeadbeef
    
    #ifdef rvtest_mtrap_routine
    
    mtrap_sigptr:
        .fill 128,4,0xdeadbeef
    
    #endif
    
    #ifdef rvtest_gpr_save
    
    gpr_save:
        .fill 32*(XLEN/32),4,0xdeadbeef
    
    #endif
    
    RVTEST_DATA_END
    


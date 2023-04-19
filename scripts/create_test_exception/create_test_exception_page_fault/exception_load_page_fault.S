#----------------------------------------------------------------------------- 
    #-----------------------------------------------------------------------------
    #
    # test load page fault    
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
    li a0, 59285;
    la  t1,test_32766

    # auipc a2, 0;
    # addi a2,a2,16;
    # csrw mepc,a2;
    # mret;
    # nop;

# set satp, 
    li a2,0x8000000000080005;
    csrw satp,a2;


    la a2,page_test;

# set level0,1 pte
    li a3,0x80005000;
    srli a3,a3,2    ;
    li a4,0x3FFFFFFFFFFC00;
    and a3, a3,a4;
    li a4,1;
    or a3,a3,a4;
    li a5,0x80005000;
    sd a3,(a5);
# set level2 pte
    la a3,page_test;
    srli a3,a3,2    ;
    li a4,0x3FFFFFFFFFFC00;
    and a3, a3,a4;
# set lower bits of pte
    li a4,127;
    or a3,a3,a4;
    sd a3,8(a5);
# set va:|0|0|1|offset
    li a4,0xfff;
    and a2,a2,a4;
    li a4,0x1000;
    or a2,a2,a4;
    csrw mepc,a2;
# return to user mode
    mret;

page_test:
    li a3,0x0000000000000000 
    ld a3,(a3)
    # sfence.vma


# end test here-------------------------------------------------------------------------------------
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)
    TEST_PASSFAIL

handle_illegal_instruction:                                                 
    call other_exception; 

handle_misaligned_load_store:
    call other_exception;

handle_misaligned_fetch:
    call other_exception;

handle_page_fault:
    li t0,59285;                                                    
    beq a0,t0,pass;

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
    


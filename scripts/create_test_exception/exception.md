# Usage

```
python3 run.py  -t e --etype <exception type> --etest <exception test>
```

exception type and exception test are shown below:

if want to test exception_csr.S:

```
python3 run.py  -t e --etype illegal_instruction --etest csr
```

if want to debug with spike, you can change the parameter `DEBUG` value in `rvv-atg/scripts/create_test_exception/Makefile`

# illegal instruction

| Tests                               | **Status** | **Note**                                                                                                                                                                                              | **ISA**          |
| ----------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **exception_csr.S**           | **P**      | **Try to access mstatus in user mode**                                                                                                                                                                | **unprivileged** |
| **exception_eew_offset.S**    | **P**      | **Indexed vector load with not supported <br />offset EEW**                                                                                                                                          | **vector**       |
| **exception_frm.S**           | **P**      | **Dynamic rounding mode is used when the<br /> rounding mode of fcsr is set to an invalid value**                                                                                                     | **unprivileged** |
| **exception_fs.S**            | **P**      | **Try to perform vector floating-point operations after turning off the FS bit of mstatus or vsstatus**                                                                                               | **vector**       |
| **exception_lmul_mismatch.S** | **P**      | **The vector instruction uses a source vector operand that <br />does not match the LMUL setting (for example, LMUL is set to 2, <br />but the source operand uses v3 and is not a multiple of 2)** | **vector**       |
| **exception_shift.S**         | **F**      | **this won't happen in 64 bit implementation**                                                                                                                                                        | **unprivileged** |
| **exception_vill.S**          | **P**      | **When vill is set, try to execute other vector instructions that depend on this vtype register; for example：sew=1xx or lmul=100**                                                                       | **vector**       |
| **exception_vs.S**            | **P**      | **Try to perform vector operations after turning off the VS bit of mstatus or vsstatus**                                                                                                              | **vector**       |
| **exception_vstart.S**        | **P**      | **Try to excute following instructions when vstart is not zero：reduction operations、<br />vcpop、vfirst、vmsbf、vmsif、vmsof、viota、vcompress**                                                    | **vector**       |

# misaligned_address

| **Tests**                       | Status      | **Note**                                             | **ISA**          |
| ------------------------------------- | ----------- | ---------------------------------------------------------- | ---------------------- |
| **exception_base_misalign.S**   | **P** | **base address misaligned when indexed vector load** | **vector**       |
| **exception_offset_misalign.S** | **P** | **offset misaligned when indexed vector load**       | **vector**       |
| **exception_ld_st.S**           | **P** | **address misaligned when scalar load or store**     | **unprivileged** |

# misaligned_fetch

| **Tests**            | **Status** | **Note**                                                                                 | **ISA**          |
| -------------------------- | ---------------- | ---------------------------------------------------------------------------------------------- | ---------------------- |
| **exception_jump.S** | **P**      | **Jumping to an unaligned address, will not be triggered if C extension is implemented** | **unprivileged** |

# ECALL

| **Tests**                  | ****Status**** | Note                                 | **ISA**       |
| -------------------------------- | -------------------------- | ------------------------------------ | ------------------- |
| **exception_machine.S**    | **P**                | **ecall from Machine mode**    | **privilege** |
| **exception_user.S**       | **P**                | **ecall from user mode**       | **privilege** |
| **exception_supervisor.S** | **P**                | **ecall from supervisor mode** | **privilege** |
| **exception_hypervisor.S** | **P**                | **ecall from hypervisor mode** | **privilege** |

# Page Fault

| **Tests**                        | **Status** | Note                            | **ISA**       |
| -------------------------------------- | ---------------- | ------------------------------- | ------------------- |
| **exception_fetch_page_fault.S** | **P**      | **page fault when fetch** | **privilege** |
| **exception_load_page_fault.S**  | **P**      | **page fault when load**  | **privilege** |
| **exception_store_page_fault.S** | **P**      | **page fault when store** | **privilege** |

# access fault

| **Tests**                    | Status      | Note                             | **ISA**         |
| ---------------------------------- | ----------- | -------------------------------- | --------------------- |
| **exception_fetch_access.S** | **P** | **Fetch access exception** | **unprivilege** |
| **exception_load_access.S**  | **P** | **Load access exception**  | **unprivilege** |
| **exception_store_access.S** | **P** | **Store access exception** | **unprivilege** |

# EXAMPLE

    the tests begin from line 22 to 46, and it's running on machine mode by default. If want add other exception test, please add exception handler like line 50~75, and add entrance in`rvv-atg/scripts/create_test_exception/p/riscv_test.h` at line 245

```ams
//rvv-atg/scripts/create_test_exception/create_test_exception_illegal_instruction/exception_vs.S

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
    csrr a2,misa;
    andi a2,a2,128;
    beq x0,a2,no_hyper;
    li a3,0xab
    # close FS in vsstatus
    li t5,1536
    csrrc a7, vsstatus,t5
    li a1,0x8000000800;
    csrrs a1,mstatus,a1;
    auipc a2, 0;
    addi a2,a2,16;
    csrw mepc,a2;
    mret;
    nop;
    vadd.vv v24, v8, v1
    li t5,1536
    csrrs x0, vsstatus,t5
no_hyper:
    li a0,59285
    # close FS in mstatus
    li t0,24576
    csrrc x0, mstatus,t0
    vfadd.vf v24, v8, f1
# end test here-------------------------------------------------------------------------------------
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)
    TEST_PASSFAIL

handle_illegal_instruction: 
    li t0,0xab;
    bne t0,a3,handle_no_hyper;  
    li a3,0
    csrr t2,mepc;
    addi t2,t2,4;
    csrw mepc,t2;
    li a1,0x000001800;
    csrrs a1,mstatus,a1;
    mret
handle_no_hyper:                                      
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
  


```

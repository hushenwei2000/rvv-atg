#----------------------------------------------------------------------------- 
    # vaadd.S
    #-----------------------------------------------------------------------------
    #
    # Test vaadd instructions.
    #

    #include "model_test.h"
    #include "arch_test.h"
    #include "test_macros_vector.h"

RVTEST_ISA("RV64RV64IMAFDCVZicsr")
    
    .section .text.init
    .globl rvtest_entry_point
    rvtest_entry_point:
    
    #ifdef TEST_CASE_1
    
    RVTEST_CASE(0,"//check ISA:=regex(.*64.*);check ISA:=regex(.*V.*);def TEST_CASE_1=True;",vaadd)
    
    RVMODEL_BOOT
    RVTEST_CODE_BEGIN
    RVTEST_VSET
    
    RVTEST_SIGBASE( x12,signature_x12_0)
    RVTEST_SIGBASE( x20,signature_x20_0)
    RVTEST_SIGBASE( x24,signature_x24_0)
    
    
#undef TEST_AVG_VV_OP 
#define TEST_AVG_VV_OP( testnum, inst, vxrm_val, result, val2, val1 ) \
        TEST_CASE_LOOP( testnum, v24, result, \
            VSET_VSEW_4AVL \
            la x7, rd_origin_data; \
            vle32.v v24, (x7); \
            la x7, mask_data; \
    vle32.v v0, (x7); \
                csrwi vxrm, vxrm_val; \
            la x7, val2; \
            vle32.v v16, (x7); \
            la x7, val1; \
            vle32.v v8, (x7); \
            inst v24, v16, v8, v0.t; \
        )
#undef TEST_AVG_VX_OP 
#define TEST_AVG_VX_OP( testnum, inst, vxrm_val, result, val2, val1 ) \
        TEST_CASE_LOOP( testnum, v24, result, \
            VSET_VSEW_4AVL \
            la x7, rd_origin_data; \
            vle32.v v24, (x7); \
            la x7, mask_data; \
    vle32.v v0, (x7); \
                csrwi vxrm, vxrm_val; \
            la x7, val2; \
            vle32.v v16, (x7); \
            li x1, MASK_XLEN(val1); \
            inst v24, v16, x1, v0.t; \
        )
#undef TEST_AVG_VI_OP 
#define TEST_AVG_VI_OP( testnum, inst, vxrm_val, result, val2, val1 ) \
        TEST_CASE_LOOP( testnum, v24, result, \
            VSET_VSEW_4AVL \
            la x7, rd_origin_data; \
            vle32.v v24, (x7); \
            la x7, mask_data; \
    vle32.v v0, (x7); \
                csrwi vxrm, vxrm_val; \
            la x7, val2; \
            vle32.v v16, (x7); \
            inst v24, v16, SEXT_IMM(val1), v0.t; \
        )
#define TEST_AVG_VV_OP_1_1( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v1, (x7); \
                inst v24, v16, v1, v0.t; \
            )
#define TEST_AVG_VV_OP_1_2( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v2, (x7); \
                inst v24, v16, v2, v0.t; \
            )
#define TEST_AVG_VV_OP_1_3( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v3, (x7); \
                inst v24, v16, v3, v0.t; \
            )
#define TEST_AVG_VV_OP_1_4( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v4, (x7); \
                inst v24, v16, v4, v0.t; \
            )
#define TEST_AVG_VV_OP_1_5( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v5, (x7); \
                inst v24, v16, v5, v0.t; \
            )
#define TEST_AVG_VV_OP_1_6( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v6, (x7); \
                inst v24, v16, v6, v0.t; \
            )
#define TEST_AVG_VV_OP_1_7( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v7, (x7); \
                inst v24, v16, v7, v0.t; \
            )
#define TEST_AVG_VV_OP_1_9( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v9, (x7); \
                inst v24, v16, v9, v0.t; \
            )
#define TEST_AVG_VV_OP_1_10( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v10, (x7); \
                inst v24, v16, v10, v0.t; \
            )
#define TEST_AVG_VV_OP_1_11( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v11, (x7); \
                inst v24, v16, v11, v0.t; \
            )
#define TEST_AVG_VV_OP_1_12( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v12, (x7); \
                inst v24, v16, v12, v0.t; \
            )
#define TEST_AVG_VV_OP_1_13( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v13, (x7); \
                inst v24, v16, v13, v0.t; \
            )
#define TEST_AVG_VV_OP_1_14( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v14, (x7); \
                inst v24, v16, v14, v0.t; \
            )
#define TEST_AVG_VV_OP_1_15( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v15, (x7); \
                inst v24, v16, v15, v0.t; \
            )
#define TEST_AVG_VV_OP_1_17( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v17, (x7); \
                inst v24, v16, v17, v0.t; \
            )
#define TEST_AVG_VV_OP_1_18( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v18, (x7); \
                inst v24, v16, v18, v0.t; \
            )
#define TEST_AVG_VV_OP_1_19( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v19, (x7); \
                inst v24, v16, v19, v0.t; \
            )
#define TEST_AVG_VV_OP_1_20( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v20, (x7); \
                inst v24, v16, v20, v0.t; \
            )
#define TEST_AVG_VV_OP_1_21( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v21, (x7); \
                inst v24, v16, v21, v0.t; \
            )
#define TEST_AVG_VV_OP_1_22( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v22, (x7); \
                inst v24, v16, v22, v0.t; \
            )
#define TEST_AVG_VV_OP_1_23( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v23, (x7); \
                inst v24, v16, v23, v0.t; \
            )
#define TEST_AVG_VV_OP_1_25( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v25, (x7); \
                inst v24, v16, v25, v0.t; \
            )
#define TEST_AVG_VV_OP_1_26( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v26, (x7); \
                inst v24, v16, v26, v0.t; \
            )
#define TEST_AVG_VV_OP_1_27( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v27, (x7); \
                inst v24, v16, v27, v0.t; \
            )
#define TEST_AVG_VV_OP_1_28( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v28, (x7); \
                inst v24, v16, v28, v0.t; \
            )
#define TEST_AVG_VV_OP_1_29( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v29, (x7); \
                inst v24, v16, v29, v0.t; \
            )
#define TEST_AVG_VV_OP_1_30( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v30, (x7); \
                inst v24, v16, v30, v0.t; \
            )
#define TEST_AVG_VV_OP_1_31( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v24, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v24, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v31, (x7); \
                inst v24, v16, v31, v0.t; \
            )
#define TEST_AVG_VV_OP_rd1( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v1, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v1, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v1, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd2( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v2, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v2, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v2, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd3( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v3, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v3, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v3, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd4( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v4, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v4, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v4, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd5( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v5, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v5, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v5, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd6( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v6, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v6, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v6, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd7( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v7, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v7, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v7, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd9( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v9, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v9, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v9, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd10( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v10, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v10, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v10, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd11( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v11, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v11, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v11, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd12( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v12, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v12, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v12, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd13( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v13, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v13, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v13, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd14( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v14, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v14, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v14, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd15( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v15, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v15, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v15, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd17( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v17, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v17, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v17, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd18( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v18, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v18, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v18, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd19( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v19, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v19, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v19, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd20( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v20, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v20, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v20, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd21( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v21, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v21, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v21, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd22( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v22, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v22, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v22, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd23( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v23, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v23, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v23, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd25( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v25, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v25, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v25, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd26( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v26, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v26, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v26, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd27( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v27, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v27, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v27, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd28( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v28, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v28, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v28, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd29( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v29, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v29, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v29, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd30( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v30, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v30, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v30, v16, v8, v0.t; \
            )
#define TEST_AVG_VV_OP_rd31( testnum, inst, vxrm_val, result, val2, val1 ) \
            TEST_CASE_LOOP( testnum, v31, result, \
                VSET_VSEW_4AVL \
                la x7, rd_origin_data; \
                vle32.v v31, (x7); \
                la x7, mask_data; \
    vle32.v v0, (x7); \
                    csrwi vxrm, vxrm_val; \
                la x7, val2; \
                vle32.v v16, (x7); \
                la x7, val1; \
                vle32.v v8, (x7); \
                inst v31, v16, v8, v0.t; \
            )
  #-------------------------------------------------------------
  # VV Tests
  #-------------------------------------------------------------
  TEST_AVG_VV_OP( 1,  vaadd.vv, 0, rd_data_vv+0, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP( 2,  vaadd.vv, 1, rd_data_vv+16, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP( 3,  vaadd.vv, 2, rd_data_vv+32, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP( 4,  vaadd.vv, 3, rd_data_vv+48, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP( 5,  vaadd.vv, 0, rd_data_vv+64, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP( 6,  vaadd.vv, 1, rd_data_vv+80, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP( 7,  vaadd.vv, 2, rd_data_vv+96, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP( 8,  vaadd.vv, 3, rd_data_vv+112, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP( 9,  vaadd.vv, 0, rd_data_vv+128, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP( 10,  vaadd.vv, 1, rd_data_vv+144, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP( 11,  vaadd.vv, 2, rd_data_vv+160, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP( 12,  vaadd.vv, 3, rd_data_vv+176, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP( 13,  vaadd.vv, 0, rd_data_vv+192, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP( 14,  vaadd.vv, 1, rd_data_vv+208, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP( 15,  vaadd.vv, 2, rd_data_vv+224, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP( 16,  vaadd.vv, 3, rd_data_vv+240, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP( 17,  vaadd.vv, 0, rd_data_vv+256, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP( 18,  vaadd.vv, 1, rd_data_vv+272, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP( 19,  vaadd.vv, 2, rd_data_vv+288, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP( 20,  vaadd.vv, 3, rd_data_vv+304, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP( 21,  vaadd.vv, 0, rd_data_vv+320, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP( 22,  vaadd.vv, 1, rd_data_vv+336, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP( 23,  vaadd.vv, 2, rd_data_vv+352, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP( 24,  vaadd.vv, 3, rd_data_vv+368, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP( 25,  vaadd.vv, 0, rd_data_vv+384, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP( 26,  vaadd.vv, 1, rd_data_vv+400, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP( 27,  vaadd.vv, 2, rd_data_vv+416, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP( 28,  vaadd.vv, 3, rd_data_vv+432, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP( 29,  vaadd.vv, 0, rd_data_vv+448, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP( 30,  vaadd.vv, 1, rd_data_vv+464, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP( 31,  vaadd.vv, 2, rd_data_vv+480, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP( 32,  vaadd.vv, 3, rd_data_vv+496, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP( 33,  vaadd.vv, 0, rd_data_vv+512, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP( 34,  vaadd.vv, 1, rd_data_vv+528, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP( 35,  vaadd.vv, 2, rd_data_vv+544, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP( 36,  vaadd.vv, 3, rd_data_vv+560, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP( 37,  vaadd.vv, 0, rd_data_vv+576, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP( 38,  vaadd.vv, 1, rd_data_vv+592, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP( 39,  vaadd.vv, 2, rd_data_vv+608, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP( 40,  vaadd.vv, 3, rd_data_vv+624, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP( 41,  vaadd.vv, 0, rd_data_vv+640, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP( 42,  vaadd.vv, 1, rd_data_vv+656, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP( 43,  vaadd.vv, 2, rd_data_vv+672, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP( 44,  vaadd.vv, 3, rd_data_vv+688, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP( 45,  vaadd.vv, 0, rd_data_vv+704, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP( 46,  vaadd.vv, 1, rd_data_vv+720, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP( 47,  vaadd.vv, 2, rd_data_vv+736, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP( 48,  vaadd.vv, 3, rd_data_vv+752, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP( 49,  vaadd.vv, 0, rd_data_vv+768, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP( 50,  vaadd.vv, 1, rd_data_vv+784, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP( 51,  vaadd.vv, 2, rd_data_vv+800, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP( 52,  vaadd.vv, 3, rd_data_vv+816, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP( 53,  vaadd.vv, 0, rd_data_vv+832, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP( 54,  vaadd.vv, 1, rd_data_vv+848, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP( 55,  vaadd.vv, 2, rd_data_vv+864, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP( 56,  vaadd.vv, 3, rd_data_vv+880, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP( 57,  vaadd.vv, 0, rd_data_vv+896, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP( 58,  vaadd.vv, 1, rd_data_vv+912, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP( 59,  vaadd.vv, 2, rd_data_vv+928, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP( 60,  vaadd.vv, 3, rd_data_vv+944, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP( 61,  vaadd.vv, 0, rd_data_vv+960, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP( 62,  vaadd.vv, 1, rd_data_vv+976, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP( 63,  vaadd.vv, 2, rd_data_vv+992, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP( 64,  vaadd.vv, 3, rd_data_vv+1008, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP( 65,  vaadd.vv, 0, rd_data_vv+1024, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP( 66,  vaadd.vv, 1, rd_data_vv+1040, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP( 67,  vaadd.vv, 2, rd_data_vv+1056, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP( 68,  vaadd.vv, 3, rd_data_vv+1072, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP( 69,  vaadd.vv, 0, rd_data_vv+1088, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP( 70,  vaadd.vv, 1, rd_data_vv+1104, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP( 71,  vaadd.vv, 2, rd_data_vv+1120, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP( 72,  vaadd.vv, 3, rd_data_vv+1136, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP( 73,  vaadd.vv, 0, rd_data_vv+1152, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP( 74,  vaadd.vv, 1, rd_data_vv+1168, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP( 75,  vaadd.vv, 2, rd_data_vv+1184, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP( 76,  vaadd.vv, 3, rd_data_vv+1200, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP( 77,  vaadd.vv, 0, rd_data_vv+1216, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP( 78,  vaadd.vv, 1, rd_data_vv+1232, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP( 79,  vaadd.vv, 2, rd_data_vv+1248, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP( 80,  vaadd.vv, 3, rd_data_vv+1264, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP( 81,  vaadd.vv, 0, rd_data_vv+1280, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP( 82,  vaadd.vv, 1, rd_data_vv+1296, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP( 83,  vaadd.vv, 2, rd_data_vv+1312, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP( 84,  vaadd.vv, 3, rd_data_vv+1328, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP( 85,  vaadd.vv, 0, rd_data_vv+1344, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP( 86,  vaadd.vv, 1, rd_data_vv+1360, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP( 87,  vaadd.vv, 2, rd_data_vv+1376, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP( 88,  vaadd.vv, 3, rd_data_vv+1392, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP( 89,  vaadd.vv, 0, rd_data_vv+1408, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP( 90,  vaadd.vv, 1, rd_data_vv+1424, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP( 91,  vaadd.vv, 2, rd_data_vv+1440, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP( 92,  vaadd.vv, 3, rd_data_vv+1456, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP( 93,  vaadd.vv, 0, rd_data_vv+1472, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP( 94,  vaadd.vv, 1, rd_data_vv+1488, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP( 95,  vaadd.vv, 2, rd_data_vv+1504, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP( 96,  vaadd.vv, 3, rd_data_vv+1520, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP( 97,  vaadd.vv, 0, rd_data_vv+1536, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP( 98,  vaadd.vv, 1, rd_data_vv+1552, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP( 99,  vaadd.vv, 2, rd_data_vv+1568, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP( 100,  vaadd.vv, 3, rd_data_vv+1584, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP( 101,  vaadd.vv, 0, rd_data_vv+1600, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP( 102,  vaadd.vv, 1, rd_data_vv+1616, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP( 103,  vaadd.vv, 2, rd_data_vv+1632, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP( 104,  vaadd.vv, 3, rd_data_vv+1648, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP( 105,  vaadd.vv, 0, rd_data_vv+1664, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP( 106,  vaadd.vv, 1, rd_data_vv+1680, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP( 107,  vaadd.vv, 2, rd_data_vv+1696, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP( 108,  vaadd.vv, 3, rd_data_vv+1712, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP( 109,  vaadd.vv, 0, rd_data_vv+1728, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP( 110,  vaadd.vv, 1, rd_data_vv+1744, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP( 111,  vaadd.vv, 2, rd_data_vv+1760, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP( 112,  vaadd.vv, 3, rd_data_vv+1776, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP( 113,  vaadd.vv, 0, rd_data_vv+1792, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP( 114,  vaadd.vv, 1, rd_data_vv+1808, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP( 115,  vaadd.vv, 2, rd_data_vv+1824, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP( 116,  vaadd.vv, 3, rd_data_vv+1840, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP( 117,  vaadd.vv, 0, rd_data_vv+1856, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP( 118,  vaadd.vv, 1, rd_data_vv+1872, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP( 119,  vaadd.vv, 2, rd_data_vv+1888, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP( 120,  vaadd.vv, 3, rd_data_vv+1904, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP( 121,  vaadd.vv, 0, rd_data_vv+1920, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP( 122,  vaadd.vv, 1, rd_data_vv+1936, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP( 123,  vaadd.vv, 2, rd_data_vv+1952, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP( 124,  vaadd.vv, 3, rd_data_vv+1968, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP( 125,  vaadd.vv, 0, rd_data_vv+1984, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP( 126,  vaadd.vv, 1, rd_data_vv+2000, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP( 127,  vaadd.vv, 2, rd_data_vv+2016, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP( 128,  vaadd.vv, 3, rd_data_vv+2032, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP( 129,  vaadd.vv, 0, rd_data_vv+2048, rs2_data+512, rs1_data+512)
  TEST_AVG_VV_OP( 130,  vaadd.vv, 1, rd_data_vv+2064, rs2_data+512, rs1_data+512)
  TEST_AVG_VV_OP( 131,  vaadd.vv, 2, rd_data_vv+2080, rs2_data+512, rs1_data+512)
  TEST_AVG_VV_OP( 132,  vaadd.vv, 3, rd_data_vv+2096, rs2_data+512, rs1_data+512)
  TEST_AVG_VV_OP( 133,  vaadd.vv, 0, rd_data_vv+2112, rs2_data+528, rs1_data+528)
  TEST_AVG_VV_OP( 134,  vaadd.vv, 1, rd_data_vv+2128, rs2_data+528, rs1_data+528)
  TEST_AVG_VV_OP( 135,  vaadd.vv, 2, rd_data_vv+2144, rs2_data+528, rs1_data+528)
  TEST_AVG_VV_OP( 136,  vaadd.vv, 3, rd_data_vv+2160, rs2_data+528, rs1_data+528)
  TEST_AVG_VV_OP( 137,  vaadd.vv, 0, rd_data_vv+2176, rs2_data+544, rs1_data+544)
  TEST_AVG_VV_OP( 138,  vaadd.vv, 1, rd_data_vv+2192, rs2_data+544, rs1_data+544)
  TEST_AVG_VV_OP( 139,  vaadd.vv, 2, rd_data_vv+2208, rs2_data+544, rs1_data+544)
  TEST_AVG_VV_OP( 140,  vaadd.vv, 3, rd_data_vv+2224, rs2_data+544, rs1_data+544)
  TEST_AVG_VV_OP( 141,  vaadd.vv, 0, rd_data_vv+2240, rs2_data+560, rs1_data+560)
  TEST_AVG_VV_OP( 142,  vaadd.vv, 1, rd_data_vv+2256, rs2_data+560, rs1_data+560)
  TEST_AVG_VV_OP( 143,  vaadd.vv, 2, rd_data_vv+2272, rs2_data+560, rs1_data+560)
  TEST_AVG_VV_OP( 144,  vaadd.vv, 3, rd_data_vv+2288, rs2_data+560, rs1_data+560)
  TEST_AVG_VV_OP( 145,  vaadd.vv, 0, rd_data_vv+2304, rs2_data+576, rs1_data+576)
  TEST_AVG_VV_OP( 146,  vaadd.vv, 1, rd_data_vv+2320, rs2_data+576, rs1_data+576)
  TEST_AVG_VV_OP( 147,  vaadd.vv, 2, rd_data_vv+2336, rs2_data+576, rs1_data+576)
  TEST_AVG_VV_OP( 148,  vaadd.vv, 3, rd_data_vv+2352, rs2_data+576, rs1_data+576)
  TEST_AVG_VV_OP( 149,  vaadd.vv, 0, rd_data_vv+2368, rs2_data+592, rs1_data+592)
  TEST_AVG_VV_OP( 150,  vaadd.vv, 1, rd_data_vv+2384, rs2_data+592, rs1_data+592)
  TEST_AVG_VV_OP( 151,  vaadd.vv, 2, rd_data_vv+2400, rs2_data+592, rs1_data+592)
  TEST_AVG_VV_OP( 152,  vaadd.vv, 3, rd_data_vv+2416, rs2_data+592, rs1_data+592)
  TEST_AVG_VV_OP( 153,  vaadd.vv, 0, rd_data_vv+2432, rs2_data+608, rs1_data+608)
  TEST_AVG_VV_OP( 154,  vaadd.vv, 1, rd_data_vv+2448, rs2_data+608, rs1_data+608)
  TEST_AVG_VV_OP( 155,  vaadd.vv, 2, rd_data_vv+2464, rs2_data+608, rs1_data+608)
  TEST_AVG_VV_OP( 156,  vaadd.vv, 3, rd_data_vv+2480, rs2_data+608, rs1_data+608)
  TEST_AVG_VV_OP( 157,  vaadd.vv, 0, rd_data_vv+2496, rs2_data+624, rs1_data+624)
  TEST_AVG_VV_OP( 158,  vaadd.vv, 1, rd_data_vv+2512, rs2_data+624, rs1_data+624)
  TEST_AVG_VV_OP( 159,  vaadd.vv, 2, rd_data_vv+2528, rs2_data+624, rs1_data+624)
  TEST_AVG_VV_OP( 160,  vaadd.vv, 3, rd_data_vv+2544, rs2_data+624, rs1_data+624)
  TEST_AVG_VV_OP( 161,  vaadd.vv, 0, rd_data_vv+2560, rs2_data+640, rs1_data+640)
  TEST_AVG_VV_OP( 162,  vaadd.vv, 1, rd_data_vv+2576, rs2_data+640, rs1_data+640)
  TEST_AVG_VV_OP( 163,  vaadd.vv, 2, rd_data_vv+2592, rs2_data+640, rs1_data+640)
  TEST_AVG_VV_OP( 164,  vaadd.vv, 3, rd_data_vv+2608, rs2_data+640, rs1_data+640)
  TEST_AVG_VV_OP( 165,  vaadd.vv, 0, rd_data_vv+2624, rs2_data+656, rs1_data+656)
  TEST_AVG_VV_OP( 166,  vaadd.vv, 1, rd_data_vv+2640, rs2_data+656, rs1_data+656)
  TEST_AVG_VV_OP( 167,  vaadd.vv, 2, rd_data_vv+2656, rs2_data+656, rs1_data+656)
  TEST_AVG_VV_OP( 168,  vaadd.vv, 3, rd_data_vv+2672, rs2_data+656, rs1_data+656)
  TEST_AVG_VV_OP( 169,  vaadd.vv, 0, rd_data_vv+2688, rs2_data+672, rs1_data+672)
  TEST_AVG_VV_OP( 170,  vaadd.vv, 1, rd_data_vv+2704, rs2_data+672, rs1_data+672)
  TEST_AVG_VV_OP( 171,  vaadd.vv, 2, rd_data_vv+2720, rs2_data+672, rs1_data+672)
  TEST_AVG_VV_OP( 172,  vaadd.vv, 3, rd_data_vv+2736, rs2_data+672, rs1_data+672)
  TEST_AVG_VV_OP( 173,  vaadd.vv, 0, rd_data_vv+2752, rs2_data+688, rs1_data+688)
  TEST_AVG_VV_OP( 174,  vaadd.vv, 1, rd_data_vv+2768, rs2_data+688, rs1_data+688)
  TEST_AVG_VV_OP( 175,  vaadd.vv, 2, rd_data_vv+2784, rs2_data+688, rs1_data+688)
  TEST_AVG_VV_OP( 176,  vaadd.vv, 3, rd_data_vv+2800, rs2_data+688, rs1_data+688)
  TEST_AVG_VV_OP( 177,  vaadd.vv, 0, rd_data_vv+2816, rs2_data+704, rs1_data+704)
  TEST_AVG_VV_OP( 178,  vaadd.vv, 1, rd_data_vv+2832, rs2_data+704, rs1_data+704)
  TEST_AVG_VV_OP( 179,  vaadd.vv, 2, rd_data_vv+2848, rs2_data+704, rs1_data+704)
  TEST_AVG_VV_OP( 180,  vaadd.vv, 3, rd_data_vv+2864, rs2_data+704, rs1_data+704)
  TEST_AVG_VV_OP( 181,  vaadd.vv, 0, rd_data_vv+2880, rs2_data+720, rs1_data+720)
  TEST_AVG_VV_OP( 182,  vaadd.vv, 1, rd_data_vv+2896, rs2_data+720, rs1_data+720)
  TEST_AVG_VV_OP( 183,  vaadd.vv, 2, rd_data_vv+2912, rs2_data+720, rs1_data+720)
  TEST_AVG_VV_OP( 184,  vaadd.vv, 3, rd_data_vv+2928, rs2_data+720, rs1_data+720)
  TEST_AVG_VV_OP( 185,  vaadd.vv, 0, rd_data_vv+2944, rs2_data+736, rs1_data+736)
  TEST_AVG_VV_OP( 186,  vaadd.vv, 1, rd_data_vv+2960, rs2_data+736, rs1_data+736)
  TEST_AVG_VV_OP( 187,  vaadd.vv, 2, rd_data_vv+2976, rs2_data+736, rs1_data+736)
  TEST_AVG_VV_OP( 188,  vaadd.vv, 3, rd_data_vv+2992, rs2_data+736, rs1_data+736)
  TEST_AVG_VV_OP( 189,  vaadd.vv, 0, rd_data_vv+3008, rs2_data+752, rs1_data+752)
  TEST_AVG_VV_OP( 190,  vaadd.vv, 1, rd_data_vv+3024, rs2_data+752, rs1_data+752)
  TEST_AVG_VV_OP( 191,  vaadd.vv, 2, rd_data_vv+3040, rs2_data+752, rs1_data+752)
  TEST_AVG_VV_OP( 192,  vaadd.vv, 3, rd_data_vv+3056, rs2_data+752, rs1_data+752)
  TEST_AVG_VV_OP( 193,  vaadd.vv, 0, rd_data_vv+3072, rs2_data+768, rs1_data+768)
  TEST_AVG_VV_OP( 194,  vaadd.vv, 1, rd_data_vv+3088, rs2_data+768, rs1_data+768)
  TEST_AVG_VV_OP( 195,  vaadd.vv, 2, rd_data_vv+3104, rs2_data+768, rs1_data+768)
  TEST_AVG_VV_OP( 196,  vaadd.vv, 3, rd_data_vv+3120, rs2_data+768, rs1_data+768)
  TEST_AVG_VV_OP( 197,  vaadd.vv, 0, rd_data_vv+3136, rs2_data+784, rs1_data+784)
  TEST_AVG_VV_OP( 198,  vaadd.vv, 1, rd_data_vv+3152, rs2_data+784, rs1_data+784)
  TEST_AVG_VV_OP( 199,  vaadd.vv, 2, rd_data_vv+3168, rs2_data+784, rs1_data+784)
  TEST_AVG_VV_OP( 200,  vaadd.vv, 3, rd_data_vv+3184, rs2_data+784, rs1_data+784)
  TEST_AVG_VV_OP( 201,  vaadd.vv, 0, rd_data_vv+3200, rs2_data+800, rs1_data+800)
  TEST_AVG_VV_OP( 202,  vaadd.vv, 1, rd_data_vv+3216, rs2_data+800, rs1_data+800)
  TEST_AVG_VV_OP( 203,  vaadd.vv, 2, rd_data_vv+3232, rs2_data+800, rs1_data+800)
  TEST_AVG_VV_OP( 204,  vaadd.vv, 3, rd_data_vv+3248, rs2_data+800, rs1_data+800)
  TEST_AVG_VV_OP( 205,  vaadd.vv, 0, rd_data_vv+3264, rs2_data+816, rs1_data+816)
  TEST_AVG_VV_OP( 206,  vaadd.vv, 1, rd_data_vv+3280, rs2_data+816, rs1_data+816)
  TEST_AVG_VV_OP( 207,  vaadd.vv, 2, rd_data_vv+3296, rs2_data+816, rs1_data+816)
  TEST_AVG_VV_OP( 208,  vaadd.vv, 3, rd_data_vv+3312, rs2_data+816, rs1_data+816)
  TEST_AVG_VV_OP( 209,  vaadd.vv, 0, rd_data_vv+3328, rs2_data+832, rs1_data+832)
  TEST_AVG_VV_OP( 210,  vaadd.vv, 1, rd_data_vv+3344, rs2_data+832, rs1_data+832)
  TEST_AVG_VV_OP( 211,  vaadd.vv, 2, rd_data_vv+3360, rs2_data+832, rs1_data+832)
  TEST_AVG_VV_OP( 212,  vaadd.vv, 3, rd_data_vv+3376, rs2_data+832, rs1_data+832)
  TEST_AVG_VV_OP( 213,  vaadd.vv, 0, rd_data_vv+3392, rs2_data+848, rs1_data+848)
  TEST_AVG_VV_OP( 214,  vaadd.vv, 1, rd_data_vv+3408, rs2_data+848, rs1_data+848)
  TEST_AVG_VV_OP( 215,  vaadd.vv, 2, rd_data_vv+3424, rs2_data+848, rs1_data+848)
  TEST_AVG_VV_OP( 216,  vaadd.vv, 3, rd_data_vv+3440, rs2_data+848, rs1_data+848)
  TEST_AVG_VV_OP( 217,  vaadd.vv, 0, rd_data_vv+3456, rs2_data+864, rs1_data+864)
  TEST_AVG_VV_OP( 218,  vaadd.vv, 1, rd_data_vv+3472, rs2_data+864, rs1_data+864)
  TEST_AVG_VV_OP( 219,  vaadd.vv, 2, rd_data_vv+3488, rs2_data+864, rs1_data+864)
  TEST_AVG_VV_OP( 220,  vaadd.vv, 3, rd_data_vv+3504, rs2_data+864, rs1_data+864)
  TEST_AVG_VV_OP( 221,  vaadd.vv, 0, rd_data_vv+3520, rs2_data+880, rs1_data+880)
  TEST_AVG_VV_OP( 222,  vaadd.vv, 1, rd_data_vv+3536, rs2_data+880, rs1_data+880)
  TEST_AVG_VV_OP( 223,  vaadd.vv, 2, rd_data_vv+3552, rs2_data+880, rs1_data+880)
  TEST_AVG_VV_OP( 224,  vaadd.vv, 3, rd_data_vv+3568, rs2_data+880, rs1_data+880)
  TEST_AVG_VV_OP( 225,  vaadd.vv, 0, rd_data_vv+3584, rs2_data+896, rs1_data+896)
  TEST_AVG_VV_OP( 226,  vaadd.vv, 1, rd_data_vv+3600, rs2_data+896, rs1_data+896)
  TEST_AVG_VV_OP( 227,  vaadd.vv, 2, rd_data_vv+3616, rs2_data+896, rs1_data+896)
  TEST_AVG_VV_OP( 228,  vaadd.vv, 3, rd_data_vv+3632, rs2_data+896, rs1_data+896)
  TEST_AVG_VV_OP( 229,  vaadd.vv, 0, rd_data_vv+3648, rs2_data+912, rs1_data+912)
  TEST_AVG_VV_OP( 230,  vaadd.vv, 1, rd_data_vv+3664, rs2_data+912, rs1_data+912)
  TEST_AVG_VV_OP( 231,  vaadd.vv, 2, rd_data_vv+3680, rs2_data+912, rs1_data+912)
  TEST_AVG_VV_OP( 232,  vaadd.vv, 3, rd_data_vv+3696, rs2_data+912, rs1_data+912)
  TEST_AVG_VV_OP( 233,  vaadd.vv, 0, rd_data_vv+3712, rs2_data+928, rs1_data+928)
  TEST_AVG_VV_OP( 234,  vaadd.vv, 1, rd_data_vv+3728, rs2_data+928, rs1_data+928)
  TEST_AVG_VV_OP( 235,  vaadd.vv, 2, rd_data_vv+3744, rs2_data+928, rs1_data+928)
  TEST_AVG_VV_OP( 236,  vaadd.vv, 3, rd_data_vv+3760, rs2_data+928, rs1_data+928)
  TEST_AVG_VV_OP( 237,  vaadd.vv, 0, rd_data_vv+3776, rs2_data+944, rs1_data+944)
  TEST_AVG_VV_OP( 238,  vaadd.vv, 1, rd_data_vv+3792, rs2_data+944, rs1_data+944)
  TEST_AVG_VV_OP( 239,  vaadd.vv, 2, rd_data_vv+3808, rs2_data+944, rs1_data+944)
  TEST_AVG_VV_OP( 240,  vaadd.vv, 3, rd_data_vv+3824, rs2_data+944, rs1_data+944)
  TEST_AVG_VV_OP( 241,  vaadd.vv, 0, rd_data_vv+3840, rs2_data+960, rs1_data+960)
  TEST_AVG_VV_OP( 242,  vaadd.vv, 1, rd_data_vv+3856, rs2_data+960, rs1_data+960)
  TEST_AVG_VV_OP( 243,  vaadd.vv, 2, rd_data_vv+3872, rs2_data+960, rs1_data+960)
  TEST_AVG_VV_OP( 244,  vaadd.vv, 3, rd_data_vv+3888, rs2_data+960, rs1_data+960)
  TEST_AVG_VV_OP( 245,  vaadd.vv, 0, rd_data_vv+3904, rs2_data+976, rs1_data+976)
  TEST_AVG_VV_OP( 246,  vaadd.vv, 1, rd_data_vv+3920, rs2_data+976, rs1_data+976)
  TEST_AVG_VV_OP( 247,  vaadd.vv, 2, rd_data_vv+3936, rs2_data+976, rs1_data+976)
  TEST_AVG_VV_OP( 248,  vaadd.vv, 3, rd_data_vv+3952, rs2_data+976, rs1_data+976)
  TEST_AVG_VV_OP( 249,  vaadd.vv, 0, rd_data_vv+3968, rs2_data+992, rs1_data+992)
  TEST_AVG_VV_OP( 250,  vaadd.vv, 1, rd_data_vv+3984, rs2_data+992, rs1_data+992)
  TEST_AVG_VV_OP( 251,  vaadd.vv, 2, rd_data_vv+4000, rs2_data+992, rs1_data+992)
  TEST_AVG_VV_OP( 252,  vaadd.vv, 3, rd_data_vv+4016, rs2_data+992, rs1_data+992)
  TEST_AVG_VV_OP( 253,  vaadd.vv, 0, rd_data_vv+4032, rs2_data+1008, rs1_data+1008)
  TEST_AVG_VV_OP( 254,  vaadd.vv, 1, rd_data_vv+4048, rs2_data+1008, rs1_data+1008)
  TEST_AVG_VV_OP( 255,  vaadd.vv, 2, rd_data_vv+4064, rs2_data+1008, rs1_data+1008)
  TEST_AVG_VV_OP( 256,  vaadd.vv, 3, rd_data_vv+4080, rs2_data+1008, rs1_data+1008)
  TEST_AVG_VV_OP( 257,  vaadd.vv, 0, rd_data_vv+4096, rs2_data+1024, rs1_data+1024)
  TEST_AVG_VV_OP( 258,  vaadd.vv, 1, rd_data_vv+4112, rs2_data+1024, rs1_data+1024)
  TEST_AVG_VV_OP( 259,  vaadd.vv, 2, rd_data_vv+4128, rs2_data+1024, rs1_data+1024)
  TEST_AVG_VV_OP( 260,  vaadd.vv, 3, rd_data_vv+4144, rs2_data+1024, rs1_data+1024)
  TEST_AVG_VV_OP( 261,  vaadd.vv, 0, rd_data_vv+4160, rs2_data+1040, rs1_data+1040)
  TEST_AVG_VV_OP( 262,  vaadd.vv, 1, rd_data_vv+4176, rs2_data+1040, rs1_data+1040)
  TEST_AVG_VV_OP( 263,  vaadd.vv, 2, rd_data_vv+4192, rs2_data+1040, rs1_data+1040)
  TEST_AVG_VV_OP( 264,  vaadd.vv, 3, rd_data_vv+4208, rs2_data+1040, rs1_data+1040)
  TEST_AVG_VV_OP( 265,  vaadd.vv, 0, rd_data_vv+4224, rs2_data+1056, rs1_data+1056)
  TEST_AVG_VV_OP( 266,  vaadd.vv, 1, rd_data_vv+4240, rs2_data+1056, rs1_data+1056)
  TEST_AVG_VV_OP( 267,  vaadd.vv, 2, rd_data_vv+4256, rs2_data+1056, rs1_data+1056)
  TEST_AVG_VV_OP( 268,  vaadd.vv, 3, rd_data_vv+4272, rs2_data+1056, rs1_data+1056)
  TEST_AVG_VV_OP( 269,  vaadd.vv, 0, rd_data_vv+4288, rs2_data+1072, rs1_data+1072)
  TEST_AVG_VV_OP( 270,  vaadd.vv, 1, rd_data_vv+4304, rs2_data+1072, rs1_data+1072)
  TEST_AVG_VV_OP( 271,  vaadd.vv, 2, rd_data_vv+4320, rs2_data+1072, rs1_data+1072)
  TEST_AVG_VV_OP( 272,  vaadd.vv, 3, rd_data_vv+4336, rs2_data+1072, rs1_data+1072)
  TEST_AVG_VV_OP( 273,  vaadd.vv, 0, rd_data_vv+4352, rs2_data+1088, rs1_data+1088)
  TEST_AVG_VV_OP( 274,  vaadd.vv, 1, rd_data_vv+4368, rs2_data+1088, rs1_data+1088)
  TEST_AVG_VV_OP( 275,  vaadd.vv, 2, rd_data_vv+4384, rs2_data+1088, rs1_data+1088)
  TEST_AVG_VV_OP( 276,  vaadd.vv, 3, rd_data_vv+4400, rs2_data+1088, rs1_data+1088)
  TEST_AVG_VV_OP( 277,  vaadd.vv, 0, rd_data_vv+4416, rs2_data+1104, rs1_data+1104)
  TEST_AVG_VV_OP( 278,  vaadd.vv, 1, rd_data_vv+4432, rs2_data+1104, rs1_data+1104)
  TEST_AVG_VV_OP( 279,  vaadd.vv, 2, rd_data_vv+4448, rs2_data+1104, rs1_data+1104)
  TEST_AVG_VV_OP( 280,  vaadd.vv, 3, rd_data_vv+4464, rs2_data+1104, rs1_data+1104)
  TEST_AVG_VV_OP( 281,  vaadd.vv, 0, rd_data_vv+4480, rs2_data+1120, rs1_data+1120)
  TEST_AVG_VV_OP( 282,  vaadd.vv, 1, rd_data_vv+4496, rs2_data+1120, rs1_data+1120)
  TEST_AVG_VV_OP( 283,  vaadd.vv, 2, rd_data_vv+4512, rs2_data+1120, rs1_data+1120)
  TEST_AVG_VV_OP( 284,  vaadd.vv, 3, rd_data_vv+4528, rs2_data+1120, rs1_data+1120)
  TEST_AVG_VV_OP( 285,  vaadd.vv, 0, rd_data_vv+4544, rs2_data+1136, rs1_data+1136)
  TEST_AVG_VV_OP( 286,  vaadd.vv, 1, rd_data_vv+4560, rs2_data+1136, rs1_data+1136)
  TEST_AVG_VV_OP( 287,  vaadd.vv, 2, rd_data_vv+4576, rs2_data+1136, rs1_data+1136)
  TEST_AVG_VV_OP( 288,  vaadd.vv, 3, rd_data_vv+4592, rs2_data+1136, rs1_data+1136)
  TEST_AVG_VV_OP( 289,  vaadd.vv, 0, rd_data_vv+4608, rs2_data+1152, rs1_data+1152)
  TEST_AVG_VV_OP( 290,  vaadd.vv, 1, rd_data_vv+4624, rs2_data+1152, rs1_data+1152)
  TEST_AVG_VV_OP( 291,  vaadd.vv, 2, rd_data_vv+4640, rs2_data+1152, rs1_data+1152)
  TEST_AVG_VV_OP( 292,  vaadd.vv, 3, rd_data_vv+4656, rs2_data+1152, rs1_data+1152)
  TEST_AVG_VV_OP( 293,  vaadd.vv, 0, rd_data_vv+4672, rs2_data+1168, rs1_data+1168)
  TEST_AVG_VV_OP( 294,  vaadd.vv, 1, rd_data_vv+4688, rs2_data+1168, rs1_data+1168)
  TEST_AVG_VV_OP( 295,  vaadd.vv, 2, rd_data_vv+4704, rs2_data+1168, rs1_data+1168)
  TEST_AVG_VV_OP( 296,  vaadd.vv, 3, rd_data_vv+4720, rs2_data+1168, rs1_data+1168)
  TEST_AVG_VV_OP( 297,  vaadd.vv, 0, rd_data_vv+4736, rs2_data+1184, rs1_data+1184)
  TEST_AVG_VV_OP( 298,  vaadd.vv, 1, rd_data_vv+4752, rs2_data+1184, rs1_data+1184)
  TEST_AVG_VV_OP( 299,  vaadd.vv, 2, rd_data_vv+4768, rs2_data+1184, rs1_data+1184)
  TEST_AVG_VV_OP( 300,  vaadd.vv, 3, rd_data_vv+4784, rs2_data+1184, rs1_data+1184)
  TEST_AVG_VV_OP( 301,  vaadd.vv, 0, rd_data_vv+4800, rs2_data+1200, rs1_data+1200)
  TEST_AVG_VV_OP( 302,  vaadd.vv, 1, rd_data_vv+4816, rs2_data+1200, rs1_data+1200)
  TEST_AVG_VV_OP( 303,  vaadd.vv, 2, rd_data_vv+4832, rs2_data+1200, rs1_data+1200)
  TEST_AVG_VV_OP( 304,  vaadd.vv, 3, rd_data_vv+4848, rs2_data+1200, rs1_data+1200)
  TEST_AVG_VV_OP( 305,  vaadd.vv, 0, rd_data_vv+4864, rs2_data+1216, rs1_data+1216)
  TEST_AVG_VV_OP( 306,  vaadd.vv, 1, rd_data_vv+4880, rs2_data+1216, rs1_data+1216)
  TEST_AVG_VV_OP( 307,  vaadd.vv, 2, rd_data_vv+4896, rs2_data+1216, rs1_data+1216)
  TEST_AVG_VV_OP( 308,  vaadd.vv, 3, rd_data_vv+4912, rs2_data+1216, rs1_data+1216)
  TEST_AVG_VV_OP( 309,  vaadd.vv, 0, rd_data_vv+4928, rs2_data+1232, rs1_data+1232)
  TEST_AVG_VV_OP( 310,  vaadd.vv, 1, rd_data_vv+4944, rs2_data+1232, rs1_data+1232)
  TEST_AVG_VV_OP( 311,  vaadd.vv, 2, rd_data_vv+4960, rs2_data+1232, rs1_data+1232)
  TEST_AVG_VV_OP( 312,  vaadd.vv, 3, rd_data_vv+4976, rs2_data+1232, rs1_data+1232)
  TEST_AVG_VV_OP( 313,  vaadd.vv, 0, rd_data_vv+4992, rs2_data+1248, rs1_data+1248)
  TEST_AVG_VV_OP( 314,  vaadd.vv, 1, rd_data_vv+5008, rs2_data+1248, rs1_data+1248)
  TEST_AVG_VV_OP( 315,  vaadd.vv, 2, rd_data_vv+5024, rs2_data+1248, rs1_data+1248)
  TEST_AVG_VV_OP( 316,  vaadd.vv, 3, rd_data_vv+5040, rs2_data+1248, rs1_data+1248)
  TEST_AVG_VV_OP( 317,  vaadd.vv, 0, rd_data_vv+5056, rs2_data+1264, rs1_data+1264)
  TEST_AVG_VV_OP( 318,  vaadd.vv, 1, rd_data_vv+5072, rs2_data+1264, rs1_data+1264)
  TEST_AVG_VV_OP( 319,  vaadd.vv, 2, rd_data_vv+5088, rs2_data+1264, rs1_data+1264)
  TEST_AVG_VV_OP( 320,  vaadd.vv, 3, rd_data_vv+5104, rs2_data+1264, rs1_data+1264)
  TEST_AVG_VV_OP( 321,  vaadd.vv, 0, rd_data_vv+5120, rs2_data+1280, rs1_data+1280)
  TEST_AVG_VV_OP( 322,  vaadd.vv, 1, rd_data_vv+5136, rs2_data+1280, rs1_data+1280)
  TEST_AVG_VV_OP( 323,  vaadd.vv, 2, rd_data_vv+5152, rs2_data+1280, rs1_data+1280)
  TEST_AVG_VV_OP( 324,  vaadd.vv, 3, rd_data_vv+5168, rs2_data+1280, rs1_data+1280)
  TEST_AVG_VV_OP( 325,  vaadd.vv, 0, rd_data_vv+5184, rs2_data+1296, rs1_data+1296)
  TEST_AVG_VV_OP( 326,  vaadd.vv, 1, rd_data_vv+5200, rs2_data+1296, rs1_data+1296)
  TEST_AVG_VV_OP( 327,  vaadd.vv, 2, rd_data_vv+5216, rs2_data+1296, rs1_data+1296)
  TEST_AVG_VV_OP( 328,  vaadd.vv, 3, rd_data_vv+5232, rs2_data+1296, rs1_data+1296)
  TEST_AVG_VV_OP( 329,  vaadd.vv, 0, rd_data_vv+5248, rs2_data+1312, rs1_data+1312)
  TEST_AVG_VV_OP( 330,  vaadd.vv, 1, rd_data_vv+5264, rs2_data+1312, rs1_data+1312)
  TEST_AVG_VV_OP( 331,  vaadd.vv, 2, rd_data_vv+5280, rs2_data+1312, rs1_data+1312)
  TEST_AVG_VV_OP( 332,  vaadd.vv, 3, rd_data_vv+5296, rs2_data+1312, rs1_data+1312)
  TEST_AVG_VV_OP( 333,  vaadd.vv, 0, rd_data_vv+5312, rs2_data+1328, rs1_data+1328)
  TEST_AVG_VV_OP( 334,  vaadd.vv, 1, rd_data_vv+5328, rs2_data+1328, rs1_data+1328)
  TEST_AVG_VV_OP( 335,  vaadd.vv, 2, rd_data_vv+5344, rs2_data+1328, rs1_data+1328)
  TEST_AVG_VV_OP( 336,  vaadd.vv, 3, rd_data_vv+5360, rs2_data+1328, rs1_data+1328)
  TEST_AVG_VV_OP( 337,  vaadd.vv, 0, rd_data_vv+5376, rs2_data+1344, rs1_data+1344)
  TEST_AVG_VV_OP( 338,  vaadd.vv, 1, rd_data_vv+5392, rs2_data+1344, rs1_data+1344)
  TEST_AVG_VV_OP( 339,  vaadd.vv, 2, rd_data_vv+5408, rs2_data+1344, rs1_data+1344)
  TEST_AVG_VV_OP( 340,  vaadd.vv, 3, rd_data_vv+5424, rs2_data+1344, rs1_data+1344)
  TEST_AVG_VV_OP( 341,  vaadd.vv, 0, rd_data_vv+5440, rs2_data+1360, rs1_data+1360)
  TEST_AVG_VV_OP( 342,  vaadd.vv, 1, rd_data_vv+5456, rs2_data+1360, rs1_data+1360)
  TEST_AVG_VV_OP( 343,  vaadd.vv, 2, rd_data_vv+5472, rs2_data+1360, rs1_data+1360)
  TEST_AVG_VV_OP( 344,  vaadd.vv, 3, rd_data_vv+5488, rs2_data+1360, rs1_data+1360)
  TEST_AVG_VV_OP( 345,  vaadd.vv, 0, rd_data_vv+5504, rs2_data+1376, rs1_data+1376)
  TEST_AVG_VV_OP( 346,  vaadd.vv, 1, rd_data_vv+5520, rs2_data+1376, rs1_data+1376)
  TEST_AVG_VV_OP( 347,  vaadd.vv, 2, rd_data_vv+5536, rs2_data+1376, rs1_data+1376)
  TEST_AVG_VV_OP( 348,  vaadd.vv, 3, rd_data_vv+5552, rs2_data+1376, rs1_data+1376)
  TEST_AVG_VV_OP( 349,  vaadd.vv, 0, rd_data_vv+5568, rs2_data+1392, rs1_data+1392)
  TEST_AVG_VV_OP( 350,  vaadd.vv, 1, rd_data_vv+5584, rs2_data+1392, rs1_data+1392)
  TEST_AVG_VV_OP( 351,  vaadd.vv, 2, rd_data_vv+5600, rs2_data+1392, rs1_data+1392)
  TEST_AVG_VV_OP( 352,  vaadd.vv, 3, rd_data_vv+5616, rs2_data+1392, rs1_data+1392)
  TEST_AVG_VV_OP( 353,  vaadd.vv, 0, rd_data_vv+5632, rs2_data+1408, rs1_data+1408)
  TEST_AVG_VV_OP( 354,  vaadd.vv, 1, rd_data_vv+5648, rs2_data+1408, rs1_data+1408)
  TEST_AVG_VV_OP( 355,  vaadd.vv, 2, rd_data_vv+5664, rs2_data+1408, rs1_data+1408)
  TEST_AVG_VV_OP( 356,  vaadd.vv, 3, rd_data_vv+5680, rs2_data+1408, rs1_data+1408)
  TEST_AVG_VV_OP( 357,  vaadd.vv, 0, rd_data_vv+5696, rs2_data+1424, rs1_data+1424)
  TEST_AVG_VV_OP( 358,  vaadd.vv, 1, rd_data_vv+5712, rs2_data+1424, rs1_data+1424)
  TEST_AVG_VV_OP( 359,  vaadd.vv, 2, rd_data_vv+5728, rs2_data+1424, rs1_data+1424)
  TEST_AVG_VV_OP( 360,  vaadd.vv, 3, rd_data_vv+5744, rs2_data+1424, rs1_data+1424)
  TEST_AVG_VV_OP( 361,  vaadd.vv, 0, rd_data_vv+5760, rs2_data+1440, rs1_data+1440)
  TEST_AVG_VV_OP( 362,  vaadd.vv, 1, rd_data_vv+5776, rs2_data+1440, rs1_data+1440)
  TEST_AVG_VV_OP( 363,  vaadd.vv, 2, rd_data_vv+5792, rs2_data+1440, rs1_data+1440)
  TEST_AVG_VV_OP( 364,  vaadd.vv, 3, rd_data_vv+5808, rs2_data+1440, rs1_data+1440)
  TEST_AVG_VV_OP( 365,  vaadd.vv, 0, rd_data_vv+5824, rs2_data+1456, rs1_data+1456)
  TEST_AVG_VV_OP( 366,  vaadd.vv, 1, rd_data_vv+5840, rs2_data+1456, rs1_data+1456)
  TEST_AVG_VV_OP( 367,  vaadd.vv, 2, rd_data_vv+5856, rs2_data+1456, rs1_data+1456)
  TEST_AVG_VV_OP( 368,  vaadd.vv, 3, rd_data_vv+5872, rs2_data+1456, rs1_data+1456)
  TEST_AVG_VV_OP( 369,  vaadd.vv, 0, rd_data_vv+5888, rs2_data+1472, rs1_data+1472)
  TEST_AVG_VV_OP( 370,  vaadd.vv, 1, rd_data_vv+5904, rs2_data+1472, rs1_data+1472)
  TEST_AVG_VV_OP( 371,  vaadd.vv, 2, rd_data_vv+5920, rs2_data+1472, rs1_data+1472)
  TEST_AVG_VV_OP( 372,  vaadd.vv, 3, rd_data_vv+5936, rs2_data+1472, rs1_data+1472)
  TEST_AVG_VV_OP( 373,  vaadd.vv, 0, rd_data_vv+5952, rs2_data+1488, rs1_data+1488)
  TEST_AVG_VV_OP( 374,  vaadd.vv, 1, rd_data_vv+5968, rs2_data+1488, rs1_data+1488)
  TEST_AVG_VV_OP( 375,  vaadd.vv, 2, rd_data_vv+5984, rs2_data+1488, rs1_data+1488)
  TEST_AVG_VV_OP( 376,  vaadd.vv, 3, rd_data_vv+6000, rs2_data+1488, rs1_data+1488)
  TEST_AVG_VV_OP( 377,  vaadd.vv, 0, rd_data_vv+6016, rs2_data+1504, rs1_data+1504)
  TEST_AVG_VV_OP( 378,  vaadd.vv, 1, rd_data_vv+6032, rs2_data+1504, rs1_data+1504)
  TEST_AVG_VV_OP( 379,  vaadd.vv, 2, rd_data_vv+6048, rs2_data+1504, rs1_data+1504)
  TEST_AVG_VV_OP( 380,  vaadd.vv, 3, rd_data_vv+6064, rs2_data+1504, rs1_data+1504)
  TEST_AVG_VV_OP( 381,  vaadd.vv, 0, rd_data_vv+6080, rs2_data+1520, rs1_data+1520)
  TEST_AVG_VV_OP( 382,  vaadd.vv, 1, rd_data_vv+6096, rs2_data+1520, rs1_data+1520)
  TEST_AVG_VV_OP( 383,  vaadd.vv, 2, rd_data_vv+6112, rs2_data+1520, rs1_data+1520)
  TEST_AVG_VV_OP( 384,  vaadd.vv, 3, rd_data_vv+6128, rs2_data+1520, rs1_data+1520)
  TEST_AVG_VV_OP( 385,  vaadd.vv, 0, rd_data_vv+6144, rs2_data+1536, rs1_data+1536)
  TEST_AVG_VV_OP( 386,  vaadd.vv, 1, rd_data_vv+6160, rs2_data+1536, rs1_data+1536)
  TEST_AVG_VV_OP( 387,  vaadd.vv, 2, rd_data_vv+6176, rs2_data+1536, rs1_data+1536)
  TEST_AVG_VV_OP( 388,  vaadd.vv, 3, rd_data_vv+6192, rs2_data+1536, rs1_data+1536)
  TEST_AVG_VV_OP( 389,  vaadd.vv, 0, rd_data_vv+6208, rs2_data+1552, rs1_data+1552)
  TEST_AVG_VV_OP( 390,  vaadd.vv, 1, rd_data_vv+6224, rs2_data+1552, rs1_data+1552)
  TEST_AVG_VV_OP( 391,  vaadd.vv, 2, rd_data_vv+6240, rs2_data+1552, rs1_data+1552)
  TEST_AVG_VV_OP( 392,  vaadd.vv, 3, rd_data_vv+6256, rs2_data+1552, rs1_data+1552)
  TEST_AVG_VV_OP( 393,  vaadd.vv, 0, rd_data_vv+6272, rs2_data+1568, rs1_data+1568)
  TEST_AVG_VV_OP( 394,  vaadd.vv, 1, rd_data_vv+6288, rs2_data+1568, rs1_data+1568)
  TEST_AVG_VV_OP( 395,  vaadd.vv, 2, rd_data_vv+6304, rs2_data+1568, rs1_data+1568)
  TEST_AVG_VV_OP( 396,  vaadd.vv, 3, rd_data_vv+6320, rs2_data+1568, rs1_data+1568)
  TEST_AVG_VV_OP( 397,  vaadd.vv, 0, rd_data_vv+6336, rs2_data+1584, rs1_data+1584)
  TEST_AVG_VV_OP( 398,  vaadd.vv, 1, rd_data_vv+6352, rs2_data+1584, rs1_data+1584)
  TEST_AVG_VV_OP( 399,  vaadd.vv, 2, rd_data_vv+6368, rs2_data+1584, rs1_data+1584)
  TEST_AVG_VV_OP( 400,  vaadd.vv, 3, rd_data_vv+6384, rs2_data+1584, rs1_data+1584)
  TEST_AVG_VV_OP( 401,  vaadd.vv, 0, rd_data_vv+6400, rs2_data+1600, rs1_data+1600)
  TEST_AVG_VV_OP( 402,  vaadd.vv, 1, rd_data_vv+6416, rs2_data+1600, rs1_data+1600)
  TEST_AVG_VV_OP( 403,  vaadd.vv, 2, rd_data_vv+6432, rs2_data+1600, rs1_data+1600)
  TEST_AVG_VV_OP( 404,  vaadd.vv, 3, rd_data_vv+6448, rs2_data+1600, rs1_data+1600)
  TEST_AVG_VV_OP( 405,  vaadd.vv, 0, rd_data_vv+6464, rs2_data+1616, rs1_data+1616)
  TEST_AVG_VV_OP( 406,  vaadd.vv, 1, rd_data_vv+6480, rs2_data+1616, rs1_data+1616)
  TEST_AVG_VV_OP( 407,  vaadd.vv, 2, rd_data_vv+6496, rs2_data+1616, rs1_data+1616)
  TEST_AVG_VV_OP( 408,  vaadd.vv, 3, rd_data_vv+6512, rs2_data+1616, rs1_data+1616)
  TEST_AVG_VV_OP( 409,  vaadd.vv, 0, rd_data_vv+6528, rs2_data+1632, rs1_data+1632)
  TEST_AVG_VV_OP( 410,  vaadd.vv, 1, rd_data_vv+6544, rs2_data+1632, rs1_data+1632)
  TEST_AVG_VV_OP( 411,  vaadd.vv, 2, rd_data_vv+6560, rs2_data+1632, rs1_data+1632)
  TEST_AVG_VV_OP( 412,  vaadd.vv, 3, rd_data_vv+6576, rs2_data+1632, rs1_data+1632)
  TEST_AVG_VV_OP( 413,  vaadd.vv, 0, rd_data_vv+6592, rs2_data+1648, rs1_data+1648)
  TEST_AVG_VV_OP( 414,  vaadd.vv, 1, rd_data_vv+6608, rs2_data+1648, rs1_data+1648)
  TEST_AVG_VV_OP( 415,  vaadd.vv, 2, rd_data_vv+6624, rs2_data+1648, rs1_data+1648)
  TEST_AVG_VV_OP( 416,  vaadd.vv, 3, rd_data_vv+6640, rs2_data+1648, rs1_data+1648)
  TEST_AVG_VV_OP( 417,  vaadd.vv, 0, rd_data_vv+6656, rs2_data+1664, rs1_data+1664)
  TEST_AVG_VV_OP( 418,  vaadd.vv, 1, rd_data_vv+6672, rs2_data+1664, rs1_data+1664)
  TEST_AVG_VV_OP( 419,  vaadd.vv, 2, rd_data_vv+6688, rs2_data+1664, rs1_data+1664)
  TEST_AVG_VV_OP( 420,  vaadd.vv, 3, rd_data_vv+6704, rs2_data+1664, rs1_data+1664)
  TEST_AVG_VV_OP( 421,  vaadd.vv, 0, rd_data_vv+6720, rs2_data+1680, rs1_data+1680)
  TEST_AVG_VV_OP( 422,  vaadd.vv, 1, rd_data_vv+6736, rs2_data+1680, rs1_data+1680)
  TEST_AVG_VV_OP( 423,  vaadd.vv, 2, rd_data_vv+6752, rs2_data+1680, rs1_data+1680)
  TEST_AVG_VV_OP( 424,  vaadd.vv, 3, rd_data_vv+6768, rs2_data+1680, rs1_data+1680)
  TEST_AVG_VV_OP( 425,  vaadd.vv, 0, rd_data_vv+6784, rs2_data+1696, rs1_data+1696)
  TEST_AVG_VV_OP( 426,  vaadd.vv, 1, rd_data_vv+6800, rs2_data+1696, rs1_data+1696)
  TEST_AVG_VV_OP( 427,  vaadd.vv, 2, rd_data_vv+6816, rs2_data+1696, rs1_data+1696)
  TEST_AVG_VV_OP( 428,  vaadd.vv, 3, rd_data_vv+6832, rs2_data+1696, rs1_data+1696)
  TEST_AVG_VV_OP( 429,  vaadd.vv, 0, rd_data_vv+6848, rs2_data+1712, rs1_data+1712)
  TEST_AVG_VV_OP( 430,  vaadd.vv, 1, rd_data_vv+6864, rs2_data+1712, rs1_data+1712)
  TEST_AVG_VV_OP( 431,  vaadd.vv, 2, rd_data_vv+6880, rs2_data+1712, rs1_data+1712)
  TEST_AVG_VV_OP( 432,  vaadd.vv, 3, rd_data_vv+6896, rs2_data+1712, rs1_data+1712)
  TEST_AVG_VV_OP( 433,  vaadd.vv, 0, rd_data_vv+6912, rs2_data+1728, rs1_data+1728)
  TEST_AVG_VV_OP( 434,  vaadd.vv, 1, rd_data_vv+6928, rs2_data+1728, rs1_data+1728)
  TEST_AVG_VV_OP( 435,  vaadd.vv, 2, rd_data_vv+6944, rs2_data+1728, rs1_data+1728)
  TEST_AVG_VV_OP( 436,  vaadd.vv, 3, rd_data_vv+6960, rs2_data+1728, rs1_data+1728)
  TEST_AVG_VV_OP( 437,  vaadd.vv, 0, rd_data_vv+6976, rs2_data+1744, rs1_data+1744)
  TEST_AVG_VV_OP( 438,  vaadd.vv, 1, rd_data_vv+6992, rs2_data+1744, rs1_data+1744)
  TEST_AVG_VV_OP( 439,  vaadd.vv, 2, rd_data_vv+7008, rs2_data+1744, rs1_data+1744)
  TEST_AVG_VV_OP( 440,  vaadd.vv, 3, rd_data_vv+7024, rs2_data+1744, rs1_data+1744)
  TEST_AVG_VV_OP( 441,  vaadd.vv, 0, rd_data_vv+7040, rs2_data+1760, rs1_data+1760)
  TEST_AVG_VV_OP( 442,  vaadd.vv, 1, rd_data_vv+7056, rs2_data+1760, rs1_data+1760)
  TEST_AVG_VV_OP( 443,  vaadd.vv, 2, rd_data_vv+7072, rs2_data+1760, rs1_data+1760)
  TEST_AVG_VV_OP( 444,  vaadd.vv, 3, rd_data_vv+7088, rs2_data+1760, rs1_data+1760)
  TEST_AVG_VV_OP( 445,  vaadd.vv, 0, rd_data_vv+7104, rs2_data+1776, rs1_data+1776)
  TEST_AVG_VV_OP( 446,  vaadd.vv, 1, rd_data_vv+7120, rs2_data+1776, rs1_data+1776)
  TEST_AVG_VV_OP( 447,  vaadd.vv, 2, rd_data_vv+7136, rs2_data+1776, rs1_data+1776)
  TEST_AVG_VV_OP( 448,  vaadd.vv, 3, rd_data_vv+7152, rs2_data+1776, rs1_data+1776)
  TEST_AVG_VV_OP( 449,  vaadd.vv, 0, rd_data_vv+7168, rs2_data+1792, rs1_data+1792)
  TEST_AVG_VV_OP( 450,  vaadd.vv, 1, rd_data_vv+7184, rs2_data+1792, rs1_data+1792)
  TEST_AVG_VV_OP( 451,  vaadd.vv, 2, rd_data_vv+7200, rs2_data+1792, rs1_data+1792)
  TEST_AVG_VV_OP( 452,  vaadd.vv, 3, rd_data_vv+7216, rs2_data+1792, rs1_data+1792)
  TEST_AVG_VV_OP( 453,  vaadd.vv, 0, rd_data_vv+7232, rs2_data+1808, rs1_data+1808)
  TEST_AVG_VV_OP( 454,  vaadd.vv, 1, rd_data_vv+7248, rs2_data+1808, rs1_data+1808)
  TEST_AVG_VV_OP( 455,  vaadd.vv, 2, rd_data_vv+7264, rs2_data+1808, rs1_data+1808)
  TEST_AVG_VV_OP( 456,  vaadd.vv, 3, rd_data_vv+7280, rs2_data+1808, rs1_data+1808)
  TEST_AVG_VV_OP( 457,  vaadd.vv, 0, rd_data_vv+7296, rs2_data+1824, rs1_data+1824)
  TEST_AVG_VV_OP( 458,  vaadd.vv, 1, rd_data_vv+7312, rs2_data+1824, rs1_data+1824)
  TEST_AVG_VV_OP( 459,  vaadd.vv, 2, rd_data_vv+7328, rs2_data+1824, rs1_data+1824)
  TEST_AVG_VV_OP( 460,  vaadd.vv, 3, rd_data_vv+7344, rs2_data+1824, rs1_data+1824)
  TEST_AVG_VV_OP( 461,  vaadd.vv, 0, rd_data_vv+7360, rs2_data+1840, rs1_data+1840)
  TEST_AVG_VV_OP( 462,  vaadd.vv, 1, rd_data_vv+7376, rs2_data+1840, rs1_data+1840)
  TEST_AVG_VV_OP( 463,  vaadd.vv, 2, rd_data_vv+7392, rs2_data+1840, rs1_data+1840)
  TEST_AVG_VV_OP( 464,  vaadd.vv, 3, rd_data_vv+7408, rs2_data+1840, rs1_data+1840)
  TEST_AVG_VV_OP( 465,  vaadd.vv, 0, rd_data_vv+7424, rs2_data+1856, rs1_data+1856)
  TEST_AVG_VV_OP( 466,  vaadd.vv, 1, rd_data_vv+7440, rs2_data+1856, rs1_data+1856)
  TEST_AVG_VV_OP( 467,  vaadd.vv, 2, rd_data_vv+7456, rs2_data+1856, rs1_data+1856)
  TEST_AVG_VV_OP( 468,  vaadd.vv, 3, rd_data_vv+7472, rs2_data+1856, rs1_data+1856)
  TEST_AVG_VV_OP( 469,  vaadd.vv, 0, rd_data_vv+7488, rs2_data+1872, rs1_data+1872)
  TEST_AVG_VV_OP( 470,  vaadd.vv, 1, rd_data_vv+7504, rs2_data+1872, rs1_data+1872)
  TEST_AVG_VV_OP( 471,  vaadd.vv, 2, rd_data_vv+7520, rs2_data+1872, rs1_data+1872)
  TEST_AVG_VV_OP( 472,  vaadd.vv, 3, rd_data_vv+7536, rs2_data+1872, rs1_data+1872)
  TEST_AVG_VV_OP( 473,  vaadd.vv, 0, rd_data_vv+7552, rs2_data+1888, rs1_data+1888)
  TEST_AVG_VV_OP( 474,  vaadd.vv, 1, rd_data_vv+7568, rs2_data+1888, rs1_data+1888)
  TEST_AVG_VV_OP( 475,  vaadd.vv, 2, rd_data_vv+7584, rs2_data+1888, rs1_data+1888)
  TEST_AVG_VV_OP( 476,  vaadd.vv, 3, rd_data_vv+7600, rs2_data+1888, rs1_data+1888)
  TEST_AVG_VV_OP( 477,  vaadd.vv, 0, rd_data_vv+7616, rs2_data+1904, rs1_data+1904)
  TEST_AVG_VV_OP( 478,  vaadd.vv, 1, rd_data_vv+7632, rs2_data+1904, rs1_data+1904)
  TEST_AVG_VV_OP( 479,  vaadd.vv, 2, rd_data_vv+7648, rs2_data+1904, rs1_data+1904)
  TEST_AVG_VV_OP( 480,  vaadd.vv, 3, rd_data_vv+7664, rs2_data+1904, rs1_data+1904)
  TEST_AVG_VV_OP( 481,  vaadd.vv, 0, rd_data_vv+7680, rs2_data+1920, rs1_data+1920)
  TEST_AVG_VV_OP( 482,  vaadd.vv, 1, rd_data_vv+7696, rs2_data+1920, rs1_data+1920)
  TEST_AVG_VV_OP( 483,  vaadd.vv, 2, rd_data_vv+7712, rs2_data+1920, rs1_data+1920)
  TEST_AVG_VV_OP( 484,  vaadd.vv, 3, rd_data_vv+7728, rs2_data+1920, rs1_data+1920)
  TEST_AVG_VV_OP( 485,  vaadd.vv, 0, rd_data_vv+7744, rs2_data+1936, rs1_data+1936)
  TEST_AVG_VV_OP( 486,  vaadd.vv, 1, rd_data_vv+7760, rs2_data+1936, rs1_data+1936)
  TEST_AVG_VV_OP( 487,  vaadd.vv, 2, rd_data_vv+7776, rs2_data+1936, rs1_data+1936)
  TEST_AVG_VV_OP( 488,  vaadd.vv, 3, rd_data_vv+7792, rs2_data+1936, rs1_data+1936)
  TEST_AVG_VV_OP( 489,  vaadd.vv, 0, rd_data_vv+7808, rs2_data+1952, rs1_data+1952)
  TEST_AVG_VV_OP( 490,  vaadd.vv, 1, rd_data_vv+7824, rs2_data+1952, rs1_data+1952)
  TEST_AVG_VV_OP( 491,  vaadd.vv, 2, rd_data_vv+7840, rs2_data+1952, rs1_data+1952)
  TEST_AVG_VV_OP( 492,  vaadd.vv, 3, rd_data_vv+7856, rs2_data+1952, rs1_data+1952)
  TEST_AVG_VV_OP( 493,  vaadd.vv, 0, rd_data_vv+7872, rs2_data+1968, rs1_data+1968)
  TEST_AVG_VV_OP( 494,  vaadd.vv, 1, rd_data_vv+7888, rs2_data+1968, rs1_data+1968)
  TEST_AVG_VV_OP( 495,  vaadd.vv, 2, rd_data_vv+7904, rs2_data+1968, rs1_data+1968)
  TEST_AVG_VV_OP( 496,  vaadd.vv, 3, rd_data_vv+7920, rs2_data+1968, rs1_data+1968)
  TEST_AVG_VV_OP( 497,  vaadd.vv, 0, rd_data_vv+7936, rs2_data+1984, rs1_data+1984)
  TEST_AVG_VV_OP( 498,  vaadd.vv, 1, rd_data_vv+7952, rs2_data+1984, rs1_data+1984)
  TEST_AVG_VV_OP( 499,  vaadd.vv, 2, rd_data_vv+7968, rs2_data+1984, rs1_data+1984)
  TEST_AVG_VV_OP( 500,  vaadd.vv, 3, rd_data_vv+7984, rs2_data+1984, rs1_data+1984)
  TEST_AVG_VV_OP( 501,  vaadd.vv, 0, rd_data_vv+8000, rs2_data+2000, rs1_data+2000)
  TEST_AVG_VV_OP( 502,  vaadd.vv, 1, rd_data_vv+8016, rs2_data+2000, rs1_data+2000)
  TEST_AVG_VV_OP( 503,  vaadd.vv, 2, rd_data_vv+8032, rs2_data+2000, rs1_data+2000)
  TEST_AVG_VV_OP( 504,  vaadd.vv, 3, rd_data_vv+8048, rs2_data+2000, rs1_data+2000)
  TEST_AVG_VV_OP( 505,  vaadd.vv, 0, rd_data_vv+8064, rs2_data+2016, rs1_data+2016)
  TEST_AVG_VV_OP( 506,  vaadd.vv, 1, rd_data_vv+8080, rs2_data+2016, rs1_data+2016)
  TEST_AVG_VV_OP( 507,  vaadd.vv, 2, rd_data_vv+8096, rs2_data+2016, rs1_data+2016)
  TEST_AVG_VV_OP( 508,  vaadd.vv, 3, rd_data_vv+8112, rs2_data+2016, rs1_data+2016)
  TEST_AVG_VV_OP( 509,  vaadd.vv, 0, rd_data_vv+8128, rs2_data+2032, rs1_data+2032)
  TEST_AVG_VV_OP( 510,  vaadd.vv, 1, rd_data_vv+8144, rs2_data+2032, rs1_data+2032)
  TEST_AVG_VV_OP( 511,  vaadd.vv, 2, rd_data_vv+8160, rs2_data+2032, rs1_data+2032)
  TEST_AVG_VV_OP( 512,  vaadd.vv, 3, rd_data_vv+8176, rs2_data+2032, rs1_data+2032)
  TEST_AVG_VV_OP( 513,  vaadd.vv, 0, rd_data_vv+8192, rs2_data+2048, rs1_data+2048)
  TEST_AVG_VV_OP( 514,  vaadd.vv, 1, rd_data_vv+8208, rs2_data+2048, rs1_data+2048)
  TEST_AVG_VV_OP( 515,  vaadd.vv, 2, rd_data_vv+8224, rs2_data+2048, rs1_data+2048)
  TEST_AVG_VV_OP( 516,  vaadd.vv, 3, rd_data_vv+8240, rs2_data+2048, rs1_data+2048)
  TEST_AVG_VV_OP( 517,  vaadd.vv, 0, rd_data_vv+8256, rs2_data+2064, rs1_data+2064)
  TEST_AVG_VV_OP( 518,  vaadd.vv, 1, rd_data_vv+8272, rs2_data+2064, rs1_data+2064)
  TEST_AVG_VV_OP( 519,  vaadd.vv, 2, rd_data_vv+8288, rs2_data+2064, rs1_data+2064)
  TEST_AVG_VV_OP( 520,  vaadd.vv, 3, rd_data_vv+8304, rs2_data+2064, rs1_data+2064)
  TEST_AVG_VV_OP( 521,  vaadd.vv, 0, rd_data_vv+8320, rs2_data+2080, rs1_data+2080)
  TEST_AVG_VV_OP( 522,  vaadd.vv, 1, rd_data_vv+8336, rs2_data+2080, rs1_data+2080)
  TEST_AVG_VV_OP( 523,  vaadd.vv, 2, rd_data_vv+8352, rs2_data+2080, rs1_data+2080)
  TEST_AVG_VV_OP( 524,  vaadd.vv, 3, rd_data_vv+8368, rs2_data+2080, rs1_data+2080)
  TEST_AVG_VV_OP( 525,  vaadd.vv, 0, rd_data_vv+8384, rs2_data+2096, rs1_data+2096)
  TEST_AVG_VV_OP( 526,  vaadd.vv, 1, rd_data_vv+8400, rs2_data+2096, rs1_data+2096)
  TEST_AVG_VV_OP( 527,  vaadd.vv, 2, rd_data_vv+8416, rs2_data+2096, rs1_data+2096)
  TEST_AVG_VV_OP( 528,  vaadd.vv, 3, rd_data_vv+8432, rs2_data+2096, rs1_data+2096)
  TEST_AVG_VV_OP( 529,  vaadd.vv, 0, rd_data_vv+8448, rs2_data+2112, rs1_data+2112)
  TEST_AVG_VV_OP( 530,  vaadd.vv, 1, rd_data_vv+8464, rs2_data+2112, rs1_data+2112)
  TEST_AVG_VV_OP( 531,  vaadd.vv, 2, rd_data_vv+8480, rs2_data+2112, rs1_data+2112)
  TEST_AVG_VV_OP( 532,  vaadd.vv, 3, rd_data_vv+8496, rs2_data+2112, rs1_data+2112)
  TEST_AVG_VV_OP( 533,  vaadd.vv, 0, rd_data_vv+8512, rs2_data+2128, rs1_data+2128)
  TEST_AVG_VV_OP( 534,  vaadd.vv, 1, rd_data_vv+8528, rs2_data+2128, rs1_data+2128)
  TEST_AVG_VV_OP( 535,  vaadd.vv, 2, rd_data_vv+8544, rs2_data+2128, rs1_data+2128)
  TEST_AVG_VV_OP( 536,  vaadd.vv, 3, rd_data_vv+8560, rs2_data+2128, rs1_data+2128)
  TEST_AVG_VV_OP( 537,  vaadd.vv, 0, rd_data_vv+8576, rs2_data+2144, rs1_data+2144)
  TEST_AVG_VV_OP( 538,  vaadd.vv, 1, rd_data_vv+8592, rs2_data+2144, rs1_data+2144)
  TEST_AVG_VV_OP( 539,  vaadd.vv, 2, rd_data_vv+8608, rs2_data+2144, rs1_data+2144)
  TEST_AVG_VV_OP( 540,  vaadd.vv, 3, rd_data_vv+8624, rs2_data+2144, rs1_data+2144)
  TEST_AVG_VV_OP( 541,  vaadd.vv, 0, rd_data_vv+8640, rs2_data+2160, rs1_data+2160)
  TEST_AVG_VV_OP( 542,  vaadd.vv, 1, rd_data_vv+8656, rs2_data+2160, rs1_data+2160)
  TEST_AVG_VV_OP( 543,  vaadd.vv, 2, rd_data_vv+8672, rs2_data+2160, rs1_data+2160)
  TEST_AVG_VV_OP( 544,  vaadd.vv, 3, rd_data_vv+8688, rs2_data+2160, rs1_data+2160)
  TEST_AVG_VV_OP( 545,  vaadd.vv, 0, rd_data_vv+8704, rs2_data+2176, rs1_data+2176)
  TEST_AVG_VV_OP( 546,  vaadd.vv, 1, rd_data_vv+8720, rs2_data+2176, rs1_data+2176)
  TEST_AVG_VV_OP( 547,  vaadd.vv, 2, rd_data_vv+8736, rs2_data+2176, rs1_data+2176)
  TEST_AVG_VV_OP( 548,  vaadd.vv, 3, rd_data_vv+8752, rs2_data+2176, rs1_data+2176)
  TEST_AVG_VV_OP_rd1( 549,  vaadd.vv, 0, rd_data_vv+0, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_1_2( 550,  vaadd.vv, 0, rd_data_vv+0, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_rd1( 551,  vaadd.vv, 1, rd_data_vv+16, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_1_2( 552,  vaadd.vv, 1, rd_data_vv+16, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_rd1( 553,  vaadd.vv, 2, rd_data_vv+32, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_1_2( 554,  vaadd.vv, 2, rd_data_vv+32, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_rd1( 555,  vaadd.vv, 3, rd_data_vv+48, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_1_2( 556,  vaadd.vv, 3, rd_data_vv+48, rs2_data+0, rs1_data+0)
  TEST_AVG_VV_OP_rd2( 557,  vaadd.vv, 0, rd_data_vv+64, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_1_3( 558,  vaadd.vv, 0, rd_data_vv+64, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_rd2( 559,  vaadd.vv, 1, rd_data_vv+80, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_1_3( 560,  vaadd.vv, 1, rd_data_vv+80, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_rd2( 561,  vaadd.vv, 2, rd_data_vv+96, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_1_3( 562,  vaadd.vv, 2, rd_data_vv+96, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_rd2( 563,  vaadd.vv, 3, rd_data_vv+112, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_1_3( 564,  vaadd.vv, 3, rd_data_vv+112, rs2_data+16, rs1_data+16)
  TEST_AVG_VV_OP_rd3( 565,  vaadd.vv, 0, rd_data_vv+128, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_1_4( 566,  vaadd.vv, 0, rd_data_vv+128, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_rd3( 567,  vaadd.vv, 1, rd_data_vv+144, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_1_4( 568,  vaadd.vv, 1, rd_data_vv+144, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_rd3( 569,  vaadd.vv, 2, rd_data_vv+160, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_1_4( 570,  vaadd.vv, 2, rd_data_vv+160, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_rd3( 571,  vaadd.vv, 3, rd_data_vv+176, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_1_4( 572,  vaadd.vv, 3, rd_data_vv+176, rs2_data+32, rs1_data+32)
  TEST_AVG_VV_OP_rd4( 573,  vaadd.vv, 0, rd_data_vv+192, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_1_5( 574,  vaadd.vv, 0, rd_data_vv+192, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_rd4( 575,  vaadd.vv, 1, rd_data_vv+208, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_1_5( 576,  vaadd.vv, 1, rd_data_vv+208, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_rd4( 577,  vaadd.vv, 2, rd_data_vv+224, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_1_5( 578,  vaadd.vv, 2, rd_data_vv+224, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_rd4( 579,  vaadd.vv, 3, rd_data_vv+240, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_1_5( 580,  vaadd.vv, 3, rd_data_vv+240, rs2_data+48, rs1_data+48)
  TEST_AVG_VV_OP_rd5( 581,  vaadd.vv, 0, rd_data_vv+256, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_1_6( 582,  vaadd.vv, 0, rd_data_vv+256, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_rd5( 583,  vaadd.vv, 1, rd_data_vv+272, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_1_6( 584,  vaadd.vv, 1, rd_data_vv+272, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_rd5( 585,  vaadd.vv, 2, rd_data_vv+288, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_1_6( 586,  vaadd.vv, 2, rd_data_vv+288, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_rd5( 587,  vaadd.vv, 3, rd_data_vv+304, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_1_6( 588,  vaadd.vv, 3, rd_data_vv+304, rs2_data+64, rs1_data+64)
  TEST_AVG_VV_OP_rd6( 589,  vaadd.vv, 0, rd_data_vv+320, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_1_7( 590,  vaadd.vv, 0, rd_data_vv+320, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_rd6( 591,  vaadd.vv, 1, rd_data_vv+336, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_1_7( 592,  vaadd.vv, 1, rd_data_vv+336, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_rd6( 593,  vaadd.vv, 2, rd_data_vv+352, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_1_7( 594,  vaadd.vv, 2, rd_data_vv+352, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_rd6( 595,  vaadd.vv, 3, rd_data_vv+368, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_1_7( 596,  vaadd.vv, 3, rd_data_vv+368, rs2_data+80, rs1_data+80)
  TEST_AVG_VV_OP_rd7( 597,  vaadd.vv, 0, rd_data_vv+384, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP_rd7( 598,  vaadd.vv, 1, rd_data_vv+400, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP_rd7( 599,  vaadd.vv, 2, rd_data_vv+416, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP_rd7( 600,  vaadd.vv, 3, rd_data_vv+432, rs2_data+96, rs1_data+96)
  TEST_AVG_VV_OP_1_9( 601,  vaadd.vv, 0, rd_data_vv+448, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP_1_9( 602,  vaadd.vv, 1, rd_data_vv+464, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP_1_9( 603,  vaadd.vv, 2, rd_data_vv+480, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP_1_9( 604,  vaadd.vv, 3, rd_data_vv+496, rs2_data+112, rs1_data+112)
  TEST_AVG_VV_OP_rd9( 605,  vaadd.vv, 0, rd_data_vv+512, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_1_10( 606,  vaadd.vv, 0, rd_data_vv+512, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_rd9( 607,  vaadd.vv, 1, rd_data_vv+528, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_1_10( 608,  vaadd.vv, 1, rd_data_vv+528, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_rd9( 609,  vaadd.vv, 2, rd_data_vv+544, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_1_10( 610,  vaadd.vv, 2, rd_data_vv+544, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_rd9( 611,  vaadd.vv, 3, rd_data_vv+560, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_1_10( 612,  vaadd.vv, 3, rd_data_vv+560, rs2_data+128, rs1_data+128)
  TEST_AVG_VV_OP_rd10( 613,  vaadd.vv, 0, rd_data_vv+576, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_1_11( 614,  vaadd.vv, 0, rd_data_vv+576, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_rd10( 615,  vaadd.vv, 1, rd_data_vv+592, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_1_11( 616,  vaadd.vv, 1, rd_data_vv+592, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_rd10( 617,  vaadd.vv, 2, rd_data_vv+608, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_1_11( 618,  vaadd.vv, 2, rd_data_vv+608, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_rd10( 619,  vaadd.vv, 3, rd_data_vv+624, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_1_11( 620,  vaadd.vv, 3, rd_data_vv+624, rs2_data+144, rs1_data+144)
  TEST_AVG_VV_OP_rd11( 621,  vaadd.vv, 0, rd_data_vv+640, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP_rd11( 622,  vaadd.vv, 1, rd_data_vv+656, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP_rd11( 623,  vaadd.vv, 2, rd_data_vv+672, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP_rd11( 624,  vaadd.vv, 3, rd_data_vv+688, rs2_data+160, rs1_data+160)
  TEST_AVG_VV_OP_1_13( 625,  vaadd.vv, 0, rd_data_vv+704, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP_1_13( 626,  vaadd.vv, 1, rd_data_vv+720, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP_1_13( 627,  vaadd.vv, 2, rd_data_vv+736, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP_1_13( 628,  vaadd.vv, 3, rd_data_vv+752, rs2_data+176, rs1_data+176)
  TEST_AVG_VV_OP_rd13( 629,  vaadd.vv, 0, rd_data_vv+768, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_1_14( 630,  vaadd.vv, 0, rd_data_vv+768, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_rd13( 631,  vaadd.vv, 1, rd_data_vv+784, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_1_14( 632,  vaadd.vv, 1, rd_data_vv+784, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_rd13( 633,  vaadd.vv, 2, rd_data_vv+800, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_1_14( 634,  vaadd.vv, 2, rd_data_vv+800, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_rd13( 635,  vaadd.vv, 3, rd_data_vv+816, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_1_14( 636,  vaadd.vv, 3, rd_data_vv+816, rs2_data+192, rs1_data+192)
  TEST_AVG_VV_OP_rd14( 637,  vaadd.vv, 0, rd_data_vv+832, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_1_15( 638,  vaadd.vv, 0, rd_data_vv+832, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_rd14( 639,  vaadd.vv, 1, rd_data_vv+848, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_1_15( 640,  vaadd.vv, 1, rd_data_vv+848, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_rd14( 641,  vaadd.vv, 2, rd_data_vv+864, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_1_15( 642,  vaadd.vv, 2, rd_data_vv+864, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_rd14( 643,  vaadd.vv, 3, rd_data_vv+880, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_1_15( 644,  vaadd.vv, 3, rd_data_vv+880, rs2_data+208, rs1_data+208)
  TEST_AVG_VV_OP_rd15( 645,  vaadd.vv, 0, rd_data_vv+896, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP_rd15( 646,  vaadd.vv, 1, rd_data_vv+912, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP_rd15( 647,  vaadd.vv, 2, rd_data_vv+928, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP_rd15( 648,  vaadd.vv, 3, rd_data_vv+944, rs2_data+224, rs1_data+224)
  TEST_AVG_VV_OP_1_17( 649,  vaadd.vv, 0, rd_data_vv+960, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP_1_17( 650,  vaadd.vv, 1, rd_data_vv+976, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP_1_17( 651,  vaadd.vv, 2, rd_data_vv+992, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP_1_17( 652,  vaadd.vv, 3, rd_data_vv+1008, rs2_data+240, rs1_data+240)
  TEST_AVG_VV_OP_rd17( 653,  vaadd.vv, 0, rd_data_vv+1024, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_1_18( 654,  vaadd.vv, 0, rd_data_vv+1024, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_rd17( 655,  vaadd.vv, 1, rd_data_vv+1040, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_1_18( 656,  vaadd.vv, 1, rd_data_vv+1040, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_rd17( 657,  vaadd.vv, 2, rd_data_vv+1056, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_1_18( 658,  vaadd.vv, 2, rd_data_vv+1056, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_rd17( 659,  vaadd.vv, 3, rd_data_vv+1072, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_1_18( 660,  vaadd.vv, 3, rd_data_vv+1072, rs2_data+256, rs1_data+256)
  TEST_AVG_VV_OP_rd18( 661,  vaadd.vv, 0, rd_data_vv+1088, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_1_19( 662,  vaadd.vv, 0, rd_data_vv+1088, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_rd18( 663,  vaadd.vv, 1, rd_data_vv+1104, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_1_19( 664,  vaadd.vv, 1, rd_data_vv+1104, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_rd18( 665,  vaadd.vv, 2, rd_data_vv+1120, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_1_19( 666,  vaadd.vv, 2, rd_data_vv+1120, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_rd18( 667,  vaadd.vv, 3, rd_data_vv+1136, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_1_19( 668,  vaadd.vv, 3, rd_data_vv+1136, rs2_data+272, rs1_data+272)
  TEST_AVG_VV_OP_rd19( 669,  vaadd.vv, 0, rd_data_vv+1152, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP_rd19( 670,  vaadd.vv, 1, rd_data_vv+1168, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP_rd19( 671,  vaadd.vv, 2, rd_data_vv+1184, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP_rd19( 672,  vaadd.vv, 3, rd_data_vv+1200, rs2_data+288, rs1_data+288)
  TEST_AVG_VV_OP_1_21( 673,  vaadd.vv, 0, rd_data_vv+1216, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP_1_21( 674,  vaadd.vv, 1, rd_data_vv+1232, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP_1_21( 675,  vaadd.vv, 2, rd_data_vv+1248, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP_1_21( 676,  vaadd.vv, 3, rd_data_vv+1264, rs2_data+304, rs1_data+304)
  TEST_AVG_VV_OP_rd21( 677,  vaadd.vv, 0, rd_data_vv+1280, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_1_22( 678,  vaadd.vv, 0, rd_data_vv+1280, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_rd21( 679,  vaadd.vv, 1, rd_data_vv+1296, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_1_22( 680,  vaadd.vv, 1, rd_data_vv+1296, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_rd21( 681,  vaadd.vv, 2, rd_data_vv+1312, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_1_22( 682,  vaadd.vv, 2, rd_data_vv+1312, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_rd21( 683,  vaadd.vv, 3, rd_data_vv+1328, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_1_22( 684,  vaadd.vv, 3, rd_data_vv+1328, rs2_data+320, rs1_data+320)
  TEST_AVG_VV_OP_rd22( 685,  vaadd.vv, 0, rd_data_vv+1344, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_1_23( 686,  vaadd.vv, 0, rd_data_vv+1344, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_rd22( 687,  vaadd.vv, 1, rd_data_vv+1360, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_1_23( 688,  vaadd.vv, 1, rd_data_vv+1360, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_rd22( 689,  vaadd.vv, 2, rd_data_vv+1376, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_1_23( 690,  vaadd.vv, 2, rd_data_vv+1376, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_rd22( 691,  vaadd.vv, 3, rd_data_vv+1392, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_1_23( 692,  vaadd.vv, 3, rd_data_vv+1392, rs2_data+336, rs1_data+336)
  TEST_AVG_VV_OP_rd23( 693,  vaadd.vv, 0, rd_data_vv+1408, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP_rd23( 694,  vaadd.vv, 1, rd_data_vv+1424, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP_rd23( 695,  vaadd.vv, 2, rd_data_vv+1440, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP_rd23( 696,  vaadd.vv, 3, rd_data_vv+1456, rs2_data+352, rs1_data+352)
  TEST_AVG_VV_OP_1_25( 697,  vaadd.vv, 0, rd_data_vv+1472, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP_1_25( 698,  vaadd.vv, 1, rd_data_vv+1488, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP_1_25( 699,  vaadd.vv, 2, rd_data_vv+1504, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP_1_25( 700,  vaadd.vv, 3, rd_data_vv+1520, rs2_data+368, rs1_data+368)
  TEST_AVG_VV_OP_rd25( 701,  vaadd.vv, 0, rd_data_vv+1536, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_1_26( 702,  vaadd.vv, 0, rd_data_vv+1536, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_rd25( 703,  vaadd.vv, 1, rd_data_vv+1552, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_1_26( 704,  vaadd.vv, 1, rd_data_vv+1552, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_rd25( 705,  vaadd.vv, 2, rd_data_vv+1568, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_1_26( 706,  vaadd.vv, 2, rd_data_vv+1568, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_rd25( 707,  vaadd.vv, 3, rd_data_vv+1584, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_1_26( 708,  vaadd.vv, 3, rd_data_vv+1584, rs2_data+384, rs1_data+384)
  TEST_AVG_VV_OP_rd26( 709,  vaadd.vv, 0, rd_data_vv+1600, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_1_27( 710,  vaadd.vv, 0, rd_data_vv+1600, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_rd26( 711,  vaadd.vv, 1, rd_data_vv+1616, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_1_27( 712,  vaadd.vv, 1, rd_data_vv+1616, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_rd26( 713,  vaadd.vv, 2, rd_data_vv+1632, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_1_27( 714,  vaadd.vv, 2, rd_data_vv+1632, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_rd26( 715,  vaadd.vv, 3, rd_data_vv+1648, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_1_27( 716,  vaadd.vv, 3, rd_data_vv+1648, rs2_data+400, rs1_data+400)
  TEST_AVG_VV_OP_rd27( 717,  vaadd.vv, 0, rd_data_vv+1664, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_1_28( 718,  vaadd.vv, 0, rd_data_vv+1664, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_rd27( 719,  vaadd.vv, 1, rd_data_vv+1680, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_1_28( 720,  vaadd.vv, 1, rd_data_vv+1680, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_rd27( 721,  vaadd.vv, 2, rd_data_vv+1696, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_1_28( 722,  vaadd.vv, 2, rd_data_vv+1696, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_rd27( 723,  vaadd.vv, 3, rd_data_vv+1712, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_1_28( 724,  vaadd.vv, 3, rd_data_vv+1712, rs2_data+416, rs1_data+416)
  TEST_AVG_VV_OP_rd28( 725,  vaadd.vv, 0, rd_data_vv+1728, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_1_29( 726,  vaadd.vv, 0, rd_data_vv+1728, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_rd28( 727,  vaadd.vv, 1, rd_data_vv+1744, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_1_29( 728,  vaadd.vv, 1, rd_data_vv+1744, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_rd28( 729,  vaadd.vv, 2, rd_data_vv+1760, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_1_29( 730,  vaadd.vv, 2, rd_data_vv+1760, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_rd28( 731,  vaadd.vv, 3, rd_data_vv+1776, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_1_29( 732,  vaadd.vv, 3, rd_data_vv+1776, rs2_data+432, rs1_data+432)
  TEST_AVG_VV_OP_rd29( 733,  vaadd.vv, 0, rd_data_vv+1792, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_1_30( 734,  vaadd.vv, 0, rd_data_vv+1792, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_rd29( 735,  vaadd.vv, 1, rd_data_vv+1808, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_1_30( 736,  vaadd.vv, 1, rd_data_vv+1808, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_rd29( 737,  vaadd.vv, 2, rd_data_vv+1824, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_1_30( 738,  vaadd.vv, 2, rd_data_vv+1824, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_rd29( 739,  vaadd.vv, 3, rd_data_vv+1840, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_1_30( 740,  vaadd.vv, 3, rd_data_vv+1840, rs2_data+448, rs1_data+448)
  TEST_AVG_VV_OP_rd30( 741,  vaadd.vv, 0, rd_data_vv+1856, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_1_31( 742,  vaadd.vv, 0, rd_data_vv+1856, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_rd30( 743,  vaadd.vv, 1, rd_data_vv+1872, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_1_31( 744,  vaadd.vv, 1, rd_data_vv+1872, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_rd30( 745,  vaadd.vv, 2, rd_data_vv+1888, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_1_31( 746,  vaadd.vv, 2, rd_data_vv+1888, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_rd30( 747,  vaadd.vv, 3, rd_data_vv+1904, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_1_31( 748,  vaadd.vv, 3, rd_data_vv+1904, rs2_data+464, rs1_data+464)
  TEST_AVG_VV_OP_rd31( 749,  vaadd.vv, 0, rd_data_vv+1920, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_1_2( 750,  vaadd.vv, 0, rd_data_vv+1920, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_rd31( 751,  vaadd.vv, 1, rd_data_vv+1936, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_1_2( 752,  vaadd.vv, 1, rd_data_vv+1936, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_rd31( 753,  vaadd.vv, 2, rd_data_vv+1952, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_1_2( 754,  vaadd.vv, 2, rd_data_vv+1952, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_rd31( 755,  vaadd.vv, 3, rd_data_vv+1968, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_1_2( 756,  vaadd.vv, 3, rd_data_vv+1968, rs2_data+480, rs1_data+480)
  TEST_AVG_VV_OP_rd1( 757,  vaadd.vv, 0, rd_data_vv+1984, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP_1_3( 758,  vaadd.vv, 0, rd_data_vv+1984, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP_rd1( 759,  vaadd.vv, 1, rd_data_vv+2000, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP_1_3( 760,  vaadd.vv, 1, rd_data_vv+2000, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP_rd1( 761,  vaadd.vv, 2, rd_data_vv+2016, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP_1_3( 762,  vaadd.vv, 2, rd_data_vv+2016, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP_rd1( 763,  vaadd.vv, 3, rd_data_vv+2032, rs2_data+496, rs1_data+496)
  TEST_AVG_VV_OP_1_3( 764,  vaadd.vv, 3, rd_data_vv+2032, rs2_data+496, rs1_data+496)
  #-------------------------------------------------------------
  # VX Tests
  #-------------------------------------------------------------
  TEST_AVG_VX_OP( 765,  vaadd.vx, 0,rd_data_vx+0, rs2_data+0, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 766,  vaadd.vx, 1,rd_data_vx+16, rs2_data+0, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 767,  vaadd.vx, 2,rd_data_vx+32, rs2_data+0, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 768,  vaadd.vx, 3,rd_data_vx+48, rs2_data+0, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 769,  vaadd.vx, 0,rd_data_vx+64, rs2_data+16, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 770,  vaadd.vx, 1,rd_data_vx+80, rs2_data+16, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 771,  vaadd.vx, 2,rd_data_vx+96, rs2_data+16, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 772,  vaadd.vx, 3,rd_data_vx+112, rs2_data+16, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 773,  vaadd.vx, 0,rd_data_vx+128, rs2_data+32, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 774,  vaadd.vx, 1,rd_data_vx+144, rs2_data+32, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 775,  vaadd.vx, 2,rd_data_vx+160, rs2_data+32, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 776,  vaadd.vx, 3,rd_data_vx+176, rs2_data+32, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 777,  vaadd.vx, 0,rd_data_vx+192, rs2_data+48, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 778,  vaadd.vx, 1,rd_data_vx+208, rs2_data+48, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 779,  vaadd.vx, 2,rd_data_vx+224, rs2_data+48, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 780,  vaadd.vx, 3,rd_data_vx+240, rs2_data+48, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 781,  vaadd.vx, 0,rd_data_vx+256, rs2_data+64, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 782,  vaadd.vx, 1,rd_data_vx+272, rs2_data+64, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 783,  vaadd.vx, 2,rd_data_vx+288, rs2_data+64, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 784,  vaadd.vx, 3,rd_data_vx+304, rs2_data+64, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 785,  vaadd.vx, 0,rd_data_vx+320, rs2_data+80, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 786,  vaadd.vx, 1,rd_data_vx+336, rs2_data+80, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 787,  vaadd.vx, 2,rd_data_vx+352, rs2_data+80, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 788,  vaadd.vx, 3,rd_data_vx+368, rs2_data+80, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 789,  vaadd.vx, 0,rd_data_vx+384, rs2_data+96, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 790,  vaadd.vx, 1,rd_data_vx+400, rs2_data+96, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 791,  vaadd.vx, 2,rd_data_vx+416, rs2_data+96, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 792,  vaadd.vx, 3,rd_data_vx+432, rs2_data+96, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 793,  vaadd.vx, 0,rd_data_vx+448, rs2_data+112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 794,  vaadd.vx, 1,rd_data_vx+464, rs2_data+112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 795,  vaadd.vx, 2,rd_data_vx+480, rs2_data+112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 796,  vaadd.vx, 3,rd_data_vx+496, rs2_data+112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 797,  vaadd.vx, 0,rd_data_vx+512, rs2_data+128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 798,  vaadd.vx, 1,rd_data_vx+528, rs2_data+128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 799,  vaadd.vx, 2,rd_data_vx+544, rs2_data+128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 800,  vaadd.vx, 3,rd_data_vx+560, rs2_data+128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 801,  vaadd.vx, 0,rd_data_vx+576, rs2_data+144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 802,  vaadd.vx, 1,rd_data_vx+592, rs2_data+144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 803,  vaadd.vx, 2,rd_data_vx+608, rs2_data+144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 804,  vaadd.vx, 3,rd_data_vx+624, rs2_data+144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 805,  vaadd.vx, 0,rd_data_vx+640, rs2_data+160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 806,  vaadd.vx, 1,rd_data_vx+656, rs2_data+160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 807,  vaadd.vx, 2,rd_data_vx+672, rs2_data+160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 808,  vaadd.vx, 3,rd_data_vx+688, rs2_data+160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 809,  vaadd.vx, 0,rd_data_vx+704, rs2_data+176, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 810,  vaadd.vx, 1,rd_data_vx+720, rs2_data+176, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 811,  vaadd.vx, 2,rd_data_vx+736, rs2_data+176, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 812,  vaadd.vx, 3,rd_data_vx+752, rs2_data+176, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 813,  vaadd.vx, 0,rd_data_vx+768, rs2_data+192, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 814,  vaadd.vx, 1,rd_data_vx+784, rs2_data+192, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 815,  vaadd.vx, 2,rd_data_vx+800, rs2_data+192, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 816,  vaadd.vx, 3,rd_data_vx+816, rs2_data+192, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 817,  vaadd.vx, 0,rd_data_vx+832, rs2_data+208, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 818,  vaadd.vx, 1,rd_data_vx+848, rs2_data+208, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 819,  vaadd.vx, 2,rd_data_vx+864, rs2_data+208, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 820,  vaadd.vx, 3,rd_data_vx+880, rs2_data+208, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 821,  vaadd.vx, 0,rd_data_vx+896, rs2_data+224, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 822,  vaadd.vx, 1,rd_data_vx+912, rs2_data+224, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 823,  vaadd.vx, 2,rd_data_vx+928, rs2_data+224, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 824,  vaadd.vx, 3,rd_data_vx+944, rs2_data+224, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 825,  vaadd.vx, 0,rd_data_vx+960, rs2_data+240, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 826,  vaadd.vx, 1,rd_data_vx+976, rs2_data+240, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 827,  vaadd.vx, 2,rd_data_vx+992, rs2_data+240, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 828,  vaadd.vx, 3,rd_data_vx+1008, rs2_data+240, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 829,  vaadd.vx, 0,rd_data_vx+1024, rs2_data+256, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 830,  vaadd.vx, 1,rd_data_vx+1040, rs2_data+256, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 831,  vaadd.vx, 2,rd_data_vx+1056, rs2_data+256, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 832,  vaadd.vx, 3,rd_data_vx+1072, rs2_data+256, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 833,  vaadd.vx, 0,rd_data_vx+1088, rs2_data+272, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 834,  vaadd.vx, 1,rd_data_vx+1104, rs2_data+272, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 835,  vaadd.vx, 2,rd_data_vx+1120, rs2_data+272, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 836,  vaadd.vx, 3,rd_data_vx+1136, rs2_data+272, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 837,  vaadd.vx, 0,rd_data_vx+1152, rs2_data+288, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 838,  vaadd.vx, 1,rd_data_vx+1168, rs2_data+288, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 839,  vaadd.vx, 2,rd_data_vx+1184, rs2_data+288, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 840,  vaadd.vx, 3,rd_data_vx+1200, rs2_data+288, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 841,  vaadd.vx, 0,rd_data_vx+1216, rs2_data+304, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 842,  vaadd.vx, 1,rd_data_vx+1232, rs2_data+304, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 843,  vaadd.vx, 2,rd_data_vx+1248, rs2_data+304, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 844,  vaadd.vx, 3,rd_data_vx+1264, rs2_data+304, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 845,  vaadd.vx, 0,rd_data_vx+1280, rs2_data+320, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 846,  vaadd.vx, 1,rd_data_vx+1296, rs2_data+320, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 847,  vaadd.vx, 2,rd_data_vx+1312, rs2_data+320, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 848,  vaadd.vx, 3,rd_data_vx+1328, rs2_data+320, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 849,  vaadd.vx, 0,rd_data_vx+1344, rs2_data+336, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 850,  vaadd.vx, 1,rd_data_vx+1360, rs2_data+336, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 851,  vaadd.vx, 2,rd_data_vx+1376, rs2_data+336, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 852,  vaadd.vx, 3,rd_data_vx+1392, rs2_data+336, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 853,  vaadd.vx, 0,rd_data_vx+1408, rs2_data+352, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 854,  vaadd.vx, 1,rd_data_vx+1424, rs2_data+352, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 855,  vaadd.vx, 2,rd_data_vx+1440, rs2_data+352, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 856,  vaadd.vx, 3,rd_data_vx+1456, rs2_data+352, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 857,  vaadd.vx, 0,rd_data_vx+1472, rs2_data+368, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 858,  vaadd.vx, 1,rd_data_vx+1488, rs2_data+368, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 859,  vaadd.vx, 2,rd_data_vx+1504, rs2_data+368, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 860,  vaadd.vx, 3,rd_data_vx+1520, rs2_data+368, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 861,  vaadd.vx, 0,rd_data_vx+1536, rs2_data+384, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 862,  vaadd.vx, 1,rd_data_vx+1552, rs2_data+384, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 863,  vaadd.vx, 2,rd_data_vx+1568, rs2_data+384, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 864,  vaadd.vx, 3,rd_data_vx+1584, rs2_data+384, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 865,  vaadd.vx, 0,rd_data_vx+1600, rs2_data+400, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 866,  vaadd.vx, 1,rd_data_vx+1616, rs2_data+400, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 867,  vaadd.vx, 2,rd_data_vx+1632, rs2_data+400, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 868,  vaadd.vx, 3,rd_data_vx+1648, rs2_data+400, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 869,  vaadd.vx, 0,rd_data_vx+1664, rs2_data+416, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 870,  vaadd.vx, 1,rd_data_vx+1680, rs2_data+416, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 871,  vaadd.vx, 2,rd_data_vx+1696, rs2_data+416, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 872,  vaadd.vx, 3,rd_data_vx+1712, rs2_data+416, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 873,  vaadd.vx, 0,rd_data_vx+1728, rs2_data+432, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 874,  vaadd.vx, 1,rd_data_vx+1744, rs2_data+432, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 875,  vaadd.vx, 2,rd_data_vx+1760, rs2_data+432, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 876,  vaadd.vx, 3,rd_data_vx+1776, rs2_data+432, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 877,  vaadd.vx, 0,rd_data_vx+1792, rs2_data+448, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 878,  vaadd.vx, 1,rd_data_vx+1808, rs2_data+448, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 879,  vaadd.vx, 2,rd_data_vx+1824, rs2_data+448, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 880,  vaadd.vx, 3,rd_data_vx+1840, rs2_data+448, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 881,  vaadd.vx, 0,rd_data_vx+1856, rs2_data+464, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 882,  vaadd.vx, 1,rd_data_vx+1872, rs2_data+464, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 883,  vaadd.vx, 2,rd_data_vx+1888, rs2_data+464, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 884,  vaadd.vx, 3,rd_data_vx+1904, rs2_data+464, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 885,  vaadd.vx, 0,rd_data_vx+1920, rs2_data+480, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 886,  vaadd.vx, 1,rd_data_vx+1936, rs2_data+480, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 887,  vaadd.vx, 2,rd_data_vx+1952, rs2_data+480, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 888,  vaadd.vx, 3,rd_data_vx+1968, rs2_data+480, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 889,  vaadd.vx, 0,rd_data_vx+1984, rs2_data+496, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 890,  vaadd.vx, 1,rd_data_vx+2000, rs2_data+496, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 891,  vaadd.vx, 2,rd_data_vx+2016, rs2_data+496, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 892,  vaadd.vx, 3,rd_data_vx+2032, rs2_data+496, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 893,  vaadd.vx, 0,rd_data_vx+2048, rs2_data+512, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 894,  vaadd.vx, 1,rd_data_vx+2064, rs2_data+512, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 895,  vaadd.vx, 2,rd_data_vx+2080, rs2_data+512, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 896,  vaadd.vx, 3,rd_data_vx+2096, rs2_data+512, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 897,  vaadd.vx, 0,rd_data_vx+2112, rs2_data+528, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 898,  vaadd.vx, 1,rd_data_vx+2128, rs2_data+528, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 899,  vaadd.vx, 2,rd_data_vx+2144, rs2_data+528, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 900,  vaadd.vx, 3,rd_data_vx+2160, rs2_data+528, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 901,  vaadd.vx, 0,rd_data_vx+2176, rs2_data+544, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 902,  vaadd.vx, 1,rd_data_vx+2192, rs2_data+544, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 903,  vaadd.vx, 2,rd_data_vx+2208, rs2_data+544, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 904,  vaadd.vx, 3,rd_data_vx+2224, rs2_data+544, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 905,  vaadd.vx, 0,rd_data_vx+2240, rs2_data+560, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 906,  vaadd.vx, 1,rd_data_vx+2256, rs2_data+560, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 907,  vaadd.vx, 2,rd_data_vx+2272, rs2_data+560, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 908,  vaadd.vx, 3,rd_data_vx+2288, rs2_data+560, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 909,  vaadd.vx, 0,rd_data_vx+2304, rs2_data+576, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 910,  vaadd.vx, 1,rd_data_vx+2320, rs2_data+576, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 911,  vaadd.vx, 2,rd_data_vx+2336, rs2_data+576, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 912,  vaadd.vx, 3,rd_data_vx+2352, rs2_data+576, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 913,  vaadd.vx, 0,rd_data_vx+2368, rs2_data+592, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 914,  vaadd.vx, 1,rd_data_vx+2384, rs2_data+592, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 915,  vaadd.vx, 2,rd_data_vx+2400, rs2_data+592, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 916,  vaadd.vx, 3,rd_data_vx+2416, rs2_data+592, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 917,  vaadd.vx, 0,rd_data_vx+2432, rs2_data+608, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 918,  vaadd.vx, 1,rd_data_vx+2448, rs2_data+608, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 919,  vaadd.vx, 2,rd_data_vx+2464, rs2_data+608, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 920,  vaadd.vx, 3,rd_data_vx+2480, rs2_data+608, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 921,  vaadd.vx, 0,rd_data_vx+2496, rs2_data+624, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 922,  vaadd.vx, 1,rd_data_vx+2512, rs2_data+624, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 923,  vaadd.vx, 2,rd_data_vx+2528, rs2_data+624, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 924,  vaadd.vx, 3,rd_data_vx+2544, rs2_data+624, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 925,  vaadd.vx, 0,rd_data_vx+2560, rs2_data+640, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 926,  vaadd.vx, 1,rd_data_vx+2576, rs2_data+640, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 927,  vaadd.vx, 2,rd_data_vx+2592, rs2_data+640, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 928,  vaadd.vx, 3,rd_data_vx+2608, rs2_data+640, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 929,  vaadd.vx, 0,rd_data_vx+2624, rs2_data+656, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 930,  vaadd.vx, 1,rd_data_vx+2640, rs2_data+656, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 931,  vaadd.vx, 2,rd_data_vx+2656, rs2_data+656, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 932,  vaadd.vx, 3,rd_data_vx+2672, rs2_data+656, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 933,  vaadd.vx, 0,rd_data_vx+2688, rs2_data+672, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 934,  vaadd.vx, 1,rd_data_vx+2704, rs2_data+672, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 935,  vaadd.vx, 2,rd_data_vx+2720, rs2_data+672, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 936,  vaadd.vx, 3,rd_data_vx+2736, rs2_data+672, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 937,  vaadd.vx, 0,rd_data_vx+2752, rs2_data+688, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 938,  vaadd.vx, 1,rd_data_vx+2768, rs2_data+688, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 939,  vaadd.vx, 2,rd_data_vx+2784, rs2_data+688, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 940,  vaadd.vx, 3,rd_data_vx+2800, rs2_data+688, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 941,  vaadd.vx, 0,rd_data_vx+2816, rs2_data+704, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 942,  vaadd.vx, 1,rd_data_vx+2832, rs2_data+704, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 943,  vaadd.vx, 2,rd_data_vx+2848, rs2_data+704, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 944,  vaadd.vx, 3,rd_data_vx+2864, rs2_data+704, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 945,  vaadd.vx, 0,rd_data_vx+2880, rs2_data+720, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 946,  vaadd.vx, 1,rd_data_vx+2896, rs2_data+720, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 947,  vaadd.vx, 2,rd_data_vx+2912, rs2_data+720, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 948,  vaadd.vx, 3,rd_data_vx+2928, rs2_data+720, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 949,  vaadd.vx, 0,rd_data_vx+2944, rs2_data+736, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 950,  vaadd.vx, 1,rd_data_vx+2960, rs2_data+736, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 951,  vaadd.vx, 2,rd_data_vx+2976, rs2_data+736, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 952,  vaadd.vx, 3,rd_data_vx+2992, rs2_data+736, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 953,  vaadd.vx, 0,rd_data_vx+3008, rs2_data+752, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 954,  vaadd.vx, 1,rd_data_vx+3024, rs2_data+752, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 955,  vaadd.vx, 2,rd_data_vx+3040, rs2_data+752, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 956,  vaadd.vx, 3,rd_data_vx+3056, rs2_data+752, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 957,  vaadd.vx, 0,rd_data_vx+3072, rs2_data+768, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 958,  vaadd.vx, 1,rd_data_vx+3088, rs2_data+768, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 959,  vaadd.vx, 2,rd_data_vx+3104, rs2_data+768, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 960,  vaadd.vx, 3,rd_data_vx+3120, rs2_data+768, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 961,  vaadd.vx, 0,rd_data_vx+3136, rs2_data+784, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 962,  vaadd.vx, 1,rd_data_vx+3152, rs2_data+784, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 963,  vaadd.vx, 2,rd_data_vx+3168, rs2_data+784, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 964,  vaadd.vx, 3,rd_data_vx+3184, rs2_data+784, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 965,  vaadd.vx, 0,rd_data_vx+3200, rs2_data+800, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 966,  vaadd.vx, 1,rd_data_vx+3216, rs2_data+800, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 967,  vaadd.vx, 2,rd_data_vx+3232, rs2_data+800, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 968,  vaadd.vx, 3,rd_data_vx+3248, rs2_data+800, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 969,  vaadd.vx, 0,rd_data_vx+3264, rs2_data+816, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 970,  vaadd.vx, 1,rd_data_vx+3280, rs2_data+816, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 971,  vaadd.vx, 2,rd_data_vx+3296, rs2_data+816, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 972,  vaadd.vx, 3,rd_data_vx+3312, rs2_data+816, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 973,  vaadd.vx, 0,rd_data_vx+3328, rs2_data+832, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 974,  vaadd.vx, 1,rd_data_vx+3344, rs2_data+832, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 975,  vaadd.vx, 2,rd_data_vx+3360, rs2_data+832, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 976,  vaadd.vx, 3,rd_data_vx+3376, rs2_data+832, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 977,  vaadd.vx, 0,rd_data_vx+3392, rs2_data+848, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 978,  vaadd.vx, 1,rd_data_vx+3408, rs2_data+848, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 979,  vaadd.vx, 2,rd_data_vx+3424, rs2_data+848, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 980,  vaadd.vx, 3,rd_data_vx+3440, rs2_data+848, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 981,  vaadd.vx, 0,rd_data_vx+3456, rs2_data+864, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 982,  vaadd.vx, 1,rd_data_vx+3472, rs2_data+864, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 983,  vaadd.vx, 2,rd_data_vx+3488, rs2_data+864, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 984,  vaadd.vx, 3,rd_data_vx+3504, rs2_data+864, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 985,  vaadd.vx, 0,rd_data_vx+3520, rs2_data+880, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 986,  vaadd.vx, 1,rd_data_vx+3536, rs2_data+880, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 987,  vaadd.vx, 2,rd_data_vx+3552, rs2_data+880, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 988,  vaadd.vx, 3,rd_data_vx+3568, rs2_data+880, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 989,  vaadd.vx, 0,rd_data_vx+3584, rs2_data+896, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 990,  vaadd.vx, 1,rd_data_vx+3600, rs2_data+896, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 991,  vaadd.vx, 2,rd_data_vx+3616, rs2_data+896, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 992,  vaadd.vx, 3,rd_data_vx+3632, rs2_data+896, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 993,  vaadd.vx, 0,rd_data_vx+3648, rs2_data+912, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 994,  vaadd.vx, 1,rd_data_vx+3664, rs2_data+912, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 995,  vaadd.vx, 2,rd_data_vx+3680, rs2_data+912, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 996,  vaadd.vx, 3,rd_data_vx+3696, rs2_data+912, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 997,  vaadd.vx, 0,rd_data_vx+3712, rs2_data+928, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 998,  vaadd.vx, 1,rd_data_vx+3728, rs2_data+928, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 999,  vaadd.vx, 2,rd_data_vx+3744, rs2_data+928, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1000,  vaadd.vx, 3,rd_data_vx+3760, rs2_data+928, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1001,  vaadd.vx, 0,rd_data_vx+3776, rs2_data+944, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1002,  vaadd.vx, 1,rd_data_vx+3792, rs2_data+944, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1003,  vaadd.vx, 2,rd_data_vx+3808, rs2_data+944, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1004,  vaadd.vx, 3,rd_data_vx+3824, rs2_data+944, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1005,  vaadd.vx, 0,rd_data_vx+3840, rs2_data+960, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1006,  vaadd.vx, 1,rd_data_vx+3856, rs2_data+960, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1007,  vaadd.vx, 2,rd_data_vx+3872, rs2_data+960, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1008,  vaadd.vx, 3,rd_data_vx+3888, rs2_data+960, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1009,  vaadd.vx, 0,rd_data_vx+3904, rs2_data+976, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1010,  vaadd.vx, 1,rd_data_vx+3920, rs2_data+976, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1011,  vaadd.vx, 2,rd_data_vx+3936, rs2_data+976, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1012,  vaadd.vx, 3,rd_data_vx+3952, rs2_data+976, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1013,  vaadd.vx, 0,rd_data_vx+3968, rs2_data+992, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1014,  vaadd.vx, 1,rd_data_vx+3984, rs2_data+992, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1015,  vaadd.vx, 2,rd_data_vx+4000, rs2_data+992, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1016,  vaadd.vx, 3,rd_data_vx+4016, rs2_data+992, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1017,  vaadd.vx, 0,rd_data_vx+4032, rs2_data+1008, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1018,  vaadd.vx, 1,rd_data_vx+4048, rs2_data+1008, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1019,  vaadd.vx, 2,rd_data_vx+4064, rs2_data+1008, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1020,  vaadd.vx, 3,rd_data_vx+4080, rs2_data+1008, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1021,  vaadd.vx, 0,rd_data_vx+4096, rs2_data+1024, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1022,  vaadd.vx, 1,rd_data_vx+4112, rs2_data+1024, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1023,  vaadd.vx, 2,rd_data_vx+4128, rs2_data+1024, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1024,  vaadd.vx, 3,rd_data_vx+4144, rs2_data+1024, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1025,  vaadd.vx, 0,rd_data_vx+4160, rs2_data+1040, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1026,  vaadd.vx, 1,rd_data_vx+4176, rs2_data+1040, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1027,  vaadd.vx, 2,rd_data_vx+4192, rs2_data+1040, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1028,  vaadd.vx, 3,rd_data_vx+4208, rs2_data+1040, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1029,  vaadd.vx, 0,rd_data_vx+4224, rs2_data+1056, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1030,  vaadd.vx, 1,rd_data_vx+4240, rs2_data+1056, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1031,  vaadd.vx, 2,rd_data_vx+4256, rs2_data+1056, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1032,  vaadd.vx, 3,rd_data_vx+4272, rs2_data+1056, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1033,  vaadd.vx, 0,rd_data_vx+4288, rs2_data+1072, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1034,  vaadd.vx, 1,rd_data_vx+4304, rs2_data+1072, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1035,  vaadd.vx, 2,rd_data_vx+4320, rs2_data+1072, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1036,  vaadd.vx, 3,rd_data_vx+4336, rs2_data+1072, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1037,  vaadd.vx, 0,rd_data_vx+4352, rs2_data+1088, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1038,  vaadd.vx, 1,rd_data_vx+4368, rs2_data+1088, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1039,  vaadd.vx, 2,rd_data_vx+4384, rs2_data+1088, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1040,  vaadd.vx, 3,rd_data_vx+4400, rs2_data+1088, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1041,  vaadd.vx, 0,rd_data_vx+4416, rs2_data+1104, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1042,  vaadd.vx, 1,rd_data_vx+4432, rs2_data+1104, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1043,  vaadd.vx, 2,rd_data_vx+4448, rs2_data+1104, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1044,  vaadd.vx, 3,rd_data_vx+4464, rs2_data+1104, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1045,  vaadd.vx, 0,rd_data_vx+4480, rs2_data+1120, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1046,  vaadd.vx, 1,rd_data_vx+4496, rs2_data+1120, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1047,  vaadd.vx, 2,rd_data_vx+4512, rs2_data+1120, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1048,  vaadd.vx, 3,rd_data_vx+4528, rs2_data+1120, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1049,  vaadd.vx, 0,rd_data_vx+4544, rs2_data+1136, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1050,  vaadd.vx, 1,rd_data_vx+4560, rs2_data+1136, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1051,  vaadd.vx, 2,rd_data_vx+4576, rs2_data+1136, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1052,  vaadd.vx, 3,rd_data_vx+4592, rs2_data+1136, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1053,  vaadd.vx, 0,rd_data_vx+4608, rs2_data+1152, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1054,  vaadd.vx, 1,rd_data_vx+4624, rs2_data+1152, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1055,  vaadd.vx, 2,rd_data_vx+4640, rs2_data+1152, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1056,  vaadd.vx, 3,rd_data_vx+4656, rs2_data+1152, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1057,  vaadd.vx, 0,rd_data_vx+4672, rs2_data+1168, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1058,  vaadd.vx, 1,rd_data_vx+4688, rs2_data+1168, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1059,  vaadd.vx, 2,rd_data_vx+4704, rs2_data+1168, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1060,  vaadd.vx, 3,rd_data_vx+4720, rs2_data+1168, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1061,  vaadd.vx, 0,rd_data_vx+4736, rs2_data+1184, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1062,  vaadd.vx, 1,rd_data_vx+4752, rs2_data+1184, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1063,  vaadd.vx, 2,rd_data_vx+4768, rs2_data+1184, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1064,  vaadd.vx, 3,rd_data_vx+4784, rs2_data+1184, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1065,  vaadd.vx, 0,rd_data_vx+4800, rs2_data+1200, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1066,  vaadd.vx, 1,rd_data_vx+4816, rs2_data+1200, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1067,  vaadd.vx, 2,rd_data_vx+4832, rs2_data+1200, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1068,  vaadd.vx, 3,rd_data_vx+4848, rs2_data+1200, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1069,  vaadd.vx, 0,rd_data_vx+4864, rs2_data+1216, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1070,  vaadd.vx, 1,rd_data_vx+4880, rs2_data+1216, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1071,  vaadd.vx, 2,rd_data_vx+4896, rs2_data+1216, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1072,  vaadd.vx, 3,rd_data_vx+4912, rs2_data+1216, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1073,  vaadd.vx, 0,rd_data_vx+4928, rs2_data+1232, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1074,  vaadd.vx, 1,rd_data_vx+4944, rs2_data+1232, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1075,  vaadd.vx, 2,rd_data_vx+4960, rs2_data+1232, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1076,  vaadd.vx, 3,rd_data_vx+4976, rs2_data+1232, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1077,  vaadd.vx, 0,rd_data_vx+4992, rs2_data+1248, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1078,  vaadd.vx, 1,rd_data_vx+5008, rs2_data+1248, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1079,  vaadd.vx, 2,rd_data_vx+5024, rs2_data+1248, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1080,  vaadd.vx, 3,rd_data_vx+5040, rs2_data+1248, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1081,  vaadd.vx, 0,rd_data_vx+5056, rs2_data+1264, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1082,  vaadd.vx, 1,rd_data_vx+5072, rs2_data+1264, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1083,  vaadd.vx, 2,rd_data_vx+5088, rs2_data+1264, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1084,  vaadd.vx, 3,rd_data_vx+5104, rs2_data+1264, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1085,  vaadd.vx, 0,rd_data_vx+5120, rs2_data+1280, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1086,  vaadd.vx, 1,rd_data_vx+5136, rs2_data+1280, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1087,  vaadd.vx, 2,rd_data_vx+5152, rs2_data+1280, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1088,  vaadd.vx, 3,rd_data_vx+5168, rs2_data+1280, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1089,  vaadd.vx, 0,rd_data_vx+5184, rs2_data+1296, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1090,  vaadd.vx, 1,rd_data_vx+5200, rs2_data+1296, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1091,  vaadd.vx, 2,rd_data_vx+5216, rs2_data+1296, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1092,  vaadd.vx, 3,rd_data_vx+5232, rs2_data+1296, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1093,  vaadd.vx, 0,rd_data_vx+5248, rs2_data+1312, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1094,  vaadd.vx, 1,rd_data_vx+5264, rs2_data+1312, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1095,  vaadd.vx, 2,rd_data_vx+5280, rs2_data+1312, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1096,  vaadd.vx, 3,rd_data_vx+5296, rs2_data+1312, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1097,  vaadd.vx, 0,rd_data_vx+5312, rs2_data+1328, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1098,  vaadd.vx, 1,rd_data_vx+5328, rs2_data+1328, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1099,  vaadd.vx, 2,rd_data_vx+5344, rs2_data+1328, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1100,  vaadd.vx, 3,rd_data_vx+5360, rs2_data+1328, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1101,  vaadd.vx, 0,rd_data_vx+5376, rs2_data+1344, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1102,  vaadd.vx, 1,rd_data_vx+5392, rs2_data+1344, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1103,  vaadd.vx, 2,rd_data_vx+5408, rs2_data+1344, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1104,  vaadd.vx, 3,rd_data_vx+5424, rs2_data+1344, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1105,  vaadd.vx, 0,rd_data_vx+5440, rs2_data+1360, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1106,  vaadd.vx, 1,rd_data_vx+5456, rs2_data+1360, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1107,  vaadd.vx, 2,rd_data_vx+5472, rs2_data+1360, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1108,  vaadd.vx, 3,rd_data_vx+5488, rs2_data+1360, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1109,  vaadd.vx, 0,rd_data_vx+5504, rs2_data+1376, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1110,  vaadd.vx, 1,rd_data_vx+5520, rs2_data+1376, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1111,  vaadd.vx, 2,rd_data_vx+5536, rs2_data+1376, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1112,  vaadd.vx, 3,rd_data_vx+5552, rs2_data+1376, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1113,  vaadd.vx, 0,rd_data_vx+5568, rs2_data+1392, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1114,  vaadd.vx, 1,rd_data_vx+5584, rs2_data+1392, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1115,  vaadd.vx, 2,rd_data_vx+5600, rs2_data+1392, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1116,  vaadd.vx, 3,rd_data_vx+5616, rs2_data+1392, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1117,  vaadd.vx, 0,rd_data_vx+5632, rs2_data+1408, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1118,  vaadd.vx, 1,rd_data_vx+5648, rs2_data+1408, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1119,  vaadd.vx, 2,rd_data_vx+5664, rs2_data+1408, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1120,  vaadd.vx, 3,rd_data_vx+5680, rs2_data+1408, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1121,  vaadd.vx, 0,rd_data_vx+5696, rs2_data+1424, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1122,  vaadd.vx, 1,rd_data_vx+5712, rs2_data+1424, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1123,  vaadd.vx, 2,rd_data_vx+5728, rs2_data+1424, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1124,  vaadd.vx, 3,rd_data_vx+5744, rs2_data+1424, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1125,  vaadd.vx, 0,rd_data_vx+5760, rs2_data+1440, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1126,  vaadd.vx, 1,rd_data_vx+5776, rs2_data+1440, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1127,  vaadd.vx, 2,rd_data_vx+5792, rs2_data+1440, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1128,  vaadd.vx, 3,rd_data_vx+5808, rs2_data+1440, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1129,  vaadd.vx, 0,rd_data_vx+5824, rs2_data+1456, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1130,  vaadd.vx, 1,rd_data_vx+5840, rs2_data+1456, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1131,  vaadd.vx, 2,rd_data_vx+5856, rs2_data+1456, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1132,  vaadd.vx, 3,rd_data_vx+5872, rs2_data+1456, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1133,  vaadd.vx, 0,rd_data_vx+5888, rs2_data+1472, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1134,  vaadd.vx, 1,rd_data_vx+5904, rs2_data+1472, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1135,  vaadd.vx, 2,rd_data_vx+5920, rs2_data+1472, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1136,  vaadd.vx, 3,rd_data_vx+5936, rs2_data+1472, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1137,  vaadd.vx, 0,rd_data_vx+5952, rs2_data+1488, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1138,  vaadd.vx, 1,rd_data_vx+5968, rs2_data+1488, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1139,  vaadd.vx, 2,rd_data_vx+5984, rs2_data+1488, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1140,  vaadd.vx, 3,rd_data_vx+6000, rs2_data+1488, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1141,  vaadd.vx, 0,rd_data_vx+6016, rs2_data+1504, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1142,  vaadd.vx, 1,rd_data_vx+6032, rs2_data+1504, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1143,  vaadd.vx, 2,rd_data_vx+6048, rs2_data+1504, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1144,  vaadd.vx, 3,rd_data_vx+6064, rs2_data+1504, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1145,  vaadd.vx, 0,rd_data_vx+6080, rs2_data+1520, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1146,  vaadd.vx, 1,rd_data_vx+6096, rs2_data+1520, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1147,  vaadd.vx, 2,rd_data_vx+6112, rs2_data+1520, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1148,  vaadd.vx, 3,rd_data_vx+6128, rs2_data+1520, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1149,  vaadd.vx, 0,rd_data_vx+6144, rs2_data+1536, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1150,  vaadd.vx, 1,rd_data_vx+6160, rs2_data+1536, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1151,  vaadd.vx, 2,rd_data_vx+6176, rs2_data+1536, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1152,  vaadd.vx, 3,rd_data_vx+6192, rs2_data+1536, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1153,  vaadd.vx, 0,rd_data_vx+6208, rs2_data+1552, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1154,  vaadd.vx, 1,rd_data_vx+6224, rs2_data+1552, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1155,  vaadd.vx, 2,rd_data_vx+6240, rs2_data+1552, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1156,  vaadd.vx, 3,rd_data_vx+6256, rs2_data+1552, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1157,  vaadd.vx, 0,rd_data_vx+6272, rs2_data+1568, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1158,  vaadd.vx, 1,rd_data_vx+6288, rs2_data+1568, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1159,  vaadd.vx, 2,rd_data_vx+6304, rs2_data+1568, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1160,  vaadd.vx, 3,rd_data_vx+6320, rs2_data+1568, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1161,  vaadd.vx, 0,rd_data_vx+6336, rs2_data+1584, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1162,  vaadd.vx, 1,rd_data_vx+6352, rs2_data+1584, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1163,  vaadd.vx, 2,rd_data_vx+6368, rs2_data+1584, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1164,  vaadd.vx, 3,rd_data_vx+6384, rs2_data+1584, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1165,  vaadd.vx, 0,rd_data_vx+6400, rs2_data+1600, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1166,  vaadd.vx, 1,rd_data_vx+6416, rs2_data+1600, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1167,  vaadd.vx, 2,rd_data_vx+6432, rs2_data+1600, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1168,  vaadd.vx, 3,rd_data_vx+6448, rs2_data+1600, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1169,  vaadd.vx, 0,rd_data_vx+6464, rs2_data+1616, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1170,  vaadd.vx, 1,rd_data_vx+6480, rs2_data+1616, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1171,  vaadd.vx, 2,rd_data_vx+6496, rs2_data+1616, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1172,  vaadd.vx, 3,rd_data_vx+6512, rs2_data+1616, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1173,  vaadd.vx, 0,rd_data_vx+6528, rs2_data+1632, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1174,  vaadd.vx, 1,rd_data_vx+6544, rs2_data+1632, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1175,  vaadd.vx, 2,rd_data_vx+6560, rs2_data+1632, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1176,  vaadd.vx, 3,rd_data_vx+6576, rs2_data+1632, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1177,  vaadd.vx, 0,rd_data_vx+6592, rs2_data+1648, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1178,  vaadd.vx, 1,rd_data_vx+6608, rs2_data+1648, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1179,  vaadd.vx, 2,rd_data_vx+6624, rs2_data+1648, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1180,  vaadd.vx, 3,rd_data_vx+6640, rs2_data+1648, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1181,  vaadd.vx, 0,rd_data_vx+6656, rs2_data+1664, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1182,  vaadd.vx, 1,rd_data_vx+6672, rs2_data+1664, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1183,  vaadd.vx, 2,rd_data_vx+6688, rs2_data+1664, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1184,  vaadd.vx, 3,rd_data_vx+6704, rs2_data+1664, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1185,  vaadd.vx, 0,rd_data_vx+6720, rs2_data+1680, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1186,  vaadd.vx, 1,rd_data_vx+6736, rs2_data+1680, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1187,  vaadd.vx, 2,rd_data_vx+6752, rs2_data+1680, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1188,  vaadd.vx, 3,rd_data_vx+6768, rs2_data+1680, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1189,  vaadd.vx, 0,rd_data_vx+6784, rs2_data+1696, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1190,  vaadd.vx, 1,rd_data_vx+6800, rs2_data+1696, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1191,  vaadd.vx, 2,rd_data_vx+6816, rs2_data+1696, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1192,  vaadd.vx, 3,rd_data_vx+6832, rs2_data+1696, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1193,  vaadd.vx, 0,rd_data_vx+6848, rs2_data+1712, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1194,  vaadd.vx, 1,rd_data_vx+6864, rs2_data+1712, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1195,  vaadd.vx, 2,rd_data_vx+6880, rs2_data+1712, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1196,  vaadd.vx, 3,rd_data_vx+6896, rs2_data+1712, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1197,  vaadd.vx, 0,rd_data_vx+6912, rs2_data+1728, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1198,  vaadd.vx, 1,rd_data_vx+6928, rs2_data+1728, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1199,  vaadd.vx, 2,rd_data_vx+6944, rs2_data+1728, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1200,  vaadd.vx, 3,rd_data_vx+6960, rs2_data+1728, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1201,  vaadd.vx, 0,rd_data_vx+6976, rs2_data+1744, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1202,  vaadd.vx, 1,rd_data_vx+6992, rs2_data+1744, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1203,  vaadd.vx, 2,rd_data_vx+7008, rs2_data+1744, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1204,  vaadd.vx, 3,rd_data_vx+7024, rs2_data+1744, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1205,  vaadd.vx, 0,rd_data_vx+7040, rs2_data+1760, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1206,  vaadd.vx, 1,rd_data_vx+7056, rs2_data+1760, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1207,  vaadd.vx, 2,rd_data_vx+7072, rs2_data+1760, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1208,  vaadd.vx, 3,rd_data_vx+7088, rs2_data+1760, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1209,  vaadd.vx, 0,rd_data_vx+7104, rs2_data+1776, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1210,  vaadd.vx, 1,rd_data_vx+7120, rs2_data+1776, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1211,  vaadd.vx, 2,rd_data_vx+7136, rs2_data+1776, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1212,  vaadd.vx, 3,rd_data_vx+7152, rs2_data+1776, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1213,  vaadd.vx, 0,rd_data_vx+7168, rs2_data+1792, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1214,  vaadd.vx, 1,rd_data_vx+7184, rs2_data+1792, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1215,  vaadd.vx, 2,rd_data_vx+7200, rs2_data+1792, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1216,  vaadd.vx, 3,rd_data_vx+7216, rs2_data+1792, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1217,  vaadd.vx, 0,rd_data_vx+7232, rs2_data+1808, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1218,  vaadd.vx, 1,rd_data_vx+7248, rs2_data+1808, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1219,  vaadd.vx, 2,rd_data_vx+7264, rs2_data+1808, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1220,  vaadd.vx, 3,rd_data_vx+7280, rs2_data+1808, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1221,  vaadd.vx, 0,rd_data_vx+7296, rs2_data+1824, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1222,  vaadd.vx, 1,rd_data_vx+7312, rs2_data+1824, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1223,  vaadd.vx, 2,rd_data_vx+7328, rs2_data+1824, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1224,  vaadd.vx, 3,rd_data_vx+7344, rs2_data+1824, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1225,  vaadd.vx, 0,rd_data_vx+7360, rs2_data+1840, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1226,  vaadd.vx, 1,rd_data_vx+7376, rs2_data+1840, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1227,  vaadd.vx, 2,rd_data_vx+7392, rs2_data+1840, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1228,  vaadd.vx, 3,rd_data_vx+7408, rs2_data+1840, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1229,  vaadd.vx, 0,rd_data_vx+7424, rs2_data+1856, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1230,  vaadd.vx, 1,rd_data_vx+7440, rs2_data+1856, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1231,  vaadd.vx, 2,rd_data_vx+7456, rs2_data+1856, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1232,  vaadd.vx, 3,rd_data_vx+7472, rs2_data+1856, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1233,  vaadd.vx, 0,rd_data_vx+7488, rs2_data+1872, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1234,  vaadd.vx, 1,rd_data_vx+7504, rs2_data+1872, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1235,  vaadd.vx, 2,rd_data_vx+7520, rs2_data+1872, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1236,  vaadd.vx, 3,rd_data_vx+7536, rs2_data+1872, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1237,  vaadd.vx, 0,rd_data_vx+7552, rs2_data+1888, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1238,  vaadd.vx, 1,rd_data_vx+7568, rs2_data+1888, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1239,  vaadd.vx, 2,rd_data_vx+7584, rs2_data+1888, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1240,  vaadd.vx, 3,rd_data_vx+7600, rs2_data+1888, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1241,  vaadd.vx, 0,rd_data_vx+7616, rs2_data+1904, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1242,  vaadd.vx, 1,rd_data_vx+7632, rs2_data+1904, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1243,  vaadd.vx, 2,rd_data_vx+7648, rs2_data+1904, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1244,  vaadd.vx, 3,rd_data_vx+7664, rs2_data+1904, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1245,  vaadd.vx, 0,rd_data_vx+7680, rs2_data+1920, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1246,  vaadd.vx, 1,rd_data_vx+7696, rs2_data+1920, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1247,  vaadd.vx, 2,rd_data_vx+7712, rs2_data+1920, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1248,  vaadd.vx, 3,rd_data_vx+7728, rs2_data+1920, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1249,  vaadd.vx, 0,rd_data_vx+7744, rs2_data+1936, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1250,  vaadd.vx, 1,rd_data_vx+7760, rs2_data+1936, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1251,  vaadd.vx, 2,rd_data_vx+7776, rs2_data+1936, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1252,  vaadd.vx, 3,rd_data_vx+7792, rs2_data+1936, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1253,  vaadd.vx, 0,rd_data_vx+7808, rs2_data+1952, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1254,  vaadd.vx, 1,rd_data_vx+7824, rs2_data+1952, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1255,  vaadd.vx, 2,rd_data_vx+7840, rs2_data+1952, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1256,  vaadd.vx, 3,rd_data_vx+7856, rs2_data+1952, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1257,  vaadd.vx, 0,rd_data_vx+7872, rs2_data+1968, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1258,  vaadd.vx, 1,rd_data_vx+7888, rs2_data+1968, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1259,  vaadd.vx, 2,rd_data_vx+7904, rs2_data+1968, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1260,  vaadd.vx, 3,rd_data_vx+7920, rs2_data+1968, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1261,  vaadd.vx, 0,rd_data_vx+7936, rs2_data+1984, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1262,  vaadd.vx, 1,rd_data_vx+7952, rs2_data+1984, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1263,  vaadd.vx, 2,rd_data_vx+7968, rs2_data+1984, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1264,  vaadd.vx, 3,rd_data_vx+7984, rs2_data+1984, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1265,  vaadd.vx, 0,rd_data_vx+8000, rs2_data+2000, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1266,  vaadd.vx, 1,rd_data_vx+8016, rs2_data+2000, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1267,  vaadd.vx, 2,rd_data_vx+8032, rs2_data+2000, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1268,  vaadd.vx, 3,rd_data_vx+8048, rs2_data+2000, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1269,  vaadd.vx, 0,rd_data_vx+8064, rs2_data+2016, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1270,  vaadd.vx, 1,rd_data_vx+8080, rs2_data+2016, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1271,  vaadd.vx, 2,rd_data_vx+8096, rs2_data+2016, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1272,  vaadd.vx, 3,rd_data_vx+8112, rs2_data+2016, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1273,  vaadd.vx, 0,rd_data_vx+8128, rs2_data+2032, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1274,  vaadd.vx, 1,rd_data_vx+8144, rs2_data+2032, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1275,  vaadd.vx, 2,rd_data_vx+8160, rs2_data+2032, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1276,  vaadd.vx, 3,rd_data_vx+8176, rs2_data+2032, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1277,  vaadd.vx, 0,rd_data_vx+8192, rs2_data+2048, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1278,  vaadd.vx, 1,rd_data_vx+8208, rs2_data+2048, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1279,  vaadd.vx, 2,rd_data_vx+8224, rs2_data+2048, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1280,  vaadd.vx, 3,rd_data_vx+8240, rs2_data+2048, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1281,  vaadd.vx, 0,rd_data_vx+8256, rs2_data+2064, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1282,  vaadd.vx, 1,rd_data_vx+8272, rs2_data+2064, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1283,  vaadd.vx, 2,rd_data_vx+8288, rs2_data+2064, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1284,  vaadd.vx, 3,rd_data_vx+8304, rs2_data+2064, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1285,  vaadd.vx, 0,rd_data_vx+8320, rs2_data+2080, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1286,  vaadd.vx, 1,rd_data_vx+8336, rs2_data+2080, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1287,  vaadd.vx, 2,rd_data_vx+8352, rs2_data+2080, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1288,  vaadd.vx, 3,rd_data_vx+8368, rs2_data+2080, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1289,  vaadd.vx, 0,rd_data_vx+8384, rs2_data+2096, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1290,  vaadd.vx, 1,rd_data_vx+8400, rs2_data+2096, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1291,  vaadd.vx, 2,rd_data_vx+8416, rs2_data+2096, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1292,  vaadd.vx, 3,rd_data_vx+8432, rs2_data+2096, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1293,  vaadd.vx, 0,rd_data_vx+8448, rs2_data+2112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1294,  vaadd.vx, 1,rd_data_vx+8464, rs2_data+2112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1295,  vaadd.vx, 2,rd_data_vx+8480, rs2_data+2112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1296,  vaadd.vx, 3,rd_data_vx+8496, rs2_data+2112, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1297,  vaadd.vx, 0,rd_data_vx+8512, rs2_data+2128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1298,  vaadd.vx, 1,rd_data_vx+8528, rs2_data+2128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1299,  vaadd.vx, 2,rd_data_vx+8544, rs2_data+2128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1300,  vaadd.vx, 3,rd_data_vx+8560, rs2_data+2128, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1301,  vaadd.vx, 0,rd_data_vx+8576, rs2_data+2144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1302,  vaadd.vx, 1,rd_data_vx+8592, rs2_data+2144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1303,  vaadd.vx, 2,rd_data_vx+8608, rs2_data+2144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1304,  vaadd.vx, 3,rd_data_vx+8624, rs2_data+2144, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1305,  vaadd.vx, 0,rd_data_vx+8640, rs2_data+2160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1306,  vaadd.vx, 1,rd_data_vx+8656, rs2_data+2160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1307,  vaadd.vx, 2,rd_data_vx+8672, rs2_data+2160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1308,  vaadd.vx, 3,rd_data_vx+8688, rs2_data+2160, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1309,  vaadd.vx, 0,rd_data_vx+8704, rs2_data+2176, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1310,  vaadd.vx, 1,rd_data_vx+8720, rs2_data+2176, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1311,  vaadd.vx, 2,rd_data_vx+8736, rs2_data+2176, 0xfffffffffffffffe)
  TEST_AVG_VX_OP( 1312,  vaadd.vx, 3,rd_data_vx+8752, rs2_data+2176, 0xfffffffffffffffe)
#endif
    
    RVTEST_CODE_END
    RVMODEL_HALT
    
    .data
    RVTEST_DATA_BEGIN
    
    TEST_DATA
    
    
.align 4
rs1_data:
.word	0xfffffffffffffffe
.word	0xfffffffffffffffd
.word	0xfffffffffffffffb
.word	0xfffffffffffffff7
.word	0xffffffffffffffef
.word	0xffffffffffffffdf
.word	0xffffffffffffffbf
.word	0xffffffffffffff7f
.word	0xfffffffffffffeff
.word	0xfffffffffffffdff
.word	0xfffffffffffffbff
.word	0xfffffffffffff7ff
.word	0xffffffffffffefff
.word	0xffffffffffffdfff
.word	0xffffffffffffbfff
.word	0xffffffffffff7fff
.word	0xfffffffffffeffff
.word	0xfffffffffffdffff
.word	0xfffffffffffbffff
.word	0xfffffffffff7ffff
.word	0xffffffffffefffff
.word	0xffffffffffdfffff
.word	0xffffffffffbfffff
.word	0xffffffffff7fffff
.word	0xfffffffffeffffff
.word	0xfffffffffdffffff
.word	0xfffffffffbffffff
.word	0xfffffffff7ffffff
.word	0xffffffffefffffff
.word	0xffffffffdfffffff
.word	0xffffffffbfffffff
.word	0x0000007fffffff
.word	0x00000000000001
.word	0x00000000000002
.word	0x00000000000004
.word	0x00000000000008
.word	0x00000000000010
.word	0x00000000000020
.word	0x00000000000040
.word	0x00000000000080
.word	0x00000000000100
.word	0x00000000000200
.word	0x00000000000400
.word	0x00000000000800
.word	0x00000000001000
.word	0x00000000002000
.word	0x00000000004000
.word	0x00000000008000
.word	0x00000000010000
.word	0x00000000020000
.word	0x00000000040000
.word	0x00000000080000
.word	0x00000000100000
.word	0x00000000200000
.word	0x00000000400000
.word	0x00000000800000
.word	0x00000001000000
.word	0x00000002000000
.word	0x00000004000000
.word	0x00000008000000
.word	0x00000010000000
.word	0x00000020000000
.word	0x00000040000000
.word	0xffffffff80000000
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000055555555
.word	0x00000000000003
.word	0xffffffffaaaaaaaa
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000003
.word	0x00000000000000
.word	0x00000000000003
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000033333333
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000033333332
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x00000066666665
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x0000000000b503
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000033333334
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505
.word	0x0000000000b505

.align 4
rs2_data:
.word	0xfffffffffffffffe
.word	0xfffffffffffffffd
.word	0xfffffffffffffffb
.word	0xfffffffffffffff7
.word	0xffffffffffffffef
.word	0xffffffffffffffdf
.word	0xffffffffffffffbf
.word	0xffffffffffffff7f
.word	0xfffffffffffffeff
.word	0xfffffffffffffdff
.word	0xfffffffffffffbff
.word	0xfffffffffffff7ff
.word	0xffffffffffffefff
.word	0xffffffffffffdfff
.word	0xffffffffffffbfff
.word	0xffffffffffff7fff
.word	0xfffffffffffeffff
.word	0xfffffffffffdffff
.word	0xfffffffffffbffff
.word	0xfffffffffff7ffff
.word	0xffffffffffefffff
.word	0xffffffffffdfffff
.word	0xffffffffffbfffff
.word	0xffffffffff7fffff
.word	0xfffffffffeffffff
.word	0xfffffffffdffffff
.word	0xfffffffffbffffff
.word	0xfffffffff7ffffff
.word	0xffffffffefffffff
.word	0xffffffffdfffffff
.word	0xffffffffbfffffff
.word	0x0000007fffffff
.word	0x00000000000001
.word	0x00000000000002
.word	0x00000000000004
.word	0x00000000000008
.word	0x00000000000010
.word	0x00000000000020
.word	0x00000000000040
.word	0x00000000000080
.word	0x00000000000100
.word	0x00000000000200
.word	0x00000000000400
.word	0x00000000000800
.word	0x00000000001000
.word	0x00000000002000
.word	0x00000000004000
.word	0x00000000008000
.word	0x00000000010000
.word	0x00000000020000
.word	0x00000000040000
.word	0x00000000080000
.word	0x00000000100000
.word	0x00000000200000
.word	0x00000000400000
.word	0x00000000800000
.word	0x00000001000000
.word	0x00000002000000
.word	0x00000004000000
.word	0x00000008000000
.word	0x00000010000000
.word	0x00000020000000
.word	0x00000040000000
.word	0xffffffff80000000
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x00000055555555
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0xffffffffaaaaaaaa
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x00000000000000
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505
.word	0x00000000000003
.word	0x00000055555555
.word	0xffffffffaaaaaaaa
.word	0x00000000000005
.word	0x00000033333333
.word	0x00000066666666
.word	0xffffffffffff4afc
.word	0x0000000000b504
.word	0x00000000000002
.word	0x00000055555554
.word	0x00000000000000
.word	0x00000000000004
.word	0x00000033333332
.word	0x00000066666665
.word	0x0000000000b503
.word	0x00000055555556
.word	0xffffffffaaaaaaab
.word	0x00000000000006
.word	0x00000033333334
.word	0x00000066666667
.word	0xffffffffffff4afd
.word	0x0000000000b505

.align 4
rd_data_vv:
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314

rd_data_vx:
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314
.word	0x5201314

rd_data_vi:

.align 4
mask_data:
	.word 0x11111111
	.word 0x86569d27
	.word 0x429ede3d
	.word 0x20219a51
	.word 0x91a8d5fd
	.word 0xbd8f6c65
	.word 0x466250f
	.word 0xe31ffa64
	.word 0xc737ad3a
	.word 0xe54c8c1e
	.word 0x7ca660db
	.word 0x692dadf
	.word 0x2c63c847
	.word 0xfbba7ae7
	.word 0x195b62bf
	.word 0xf600a3d1
	.word 0x34b80fd4
	.word 0x3aef5ff4
	.word 0x34267ad9
	.word 0x681454c0
	.word 0x67dd3492
	.word 0xb02d663e
	.word 0xb2d3f1c5
	.word 0x824d39ae
 

.align 4
rd_origin_data:
    .word 0x66da64aa
	.word 0xf682191a
	.word 0xfd2ce83f
	.word 0x67f9ab29
	.word 0x112e3ffd
	.word 0xc4d9b1e2
	.word 0x9ed4e137
	.word 0xb49ae54e
	.word 0xd075dd45
	.word 0x74daa72e
	.word 0x48324db4
	.word 0x167d97b5
	.word 0x8b536536
	.word 0xe85755eb
	.word 0x1cd86c0a
	.word 0x4c811ecf
	.word 0x8085dbf1
	.word 0x547cdce3
	.word 0x65d27882
	.word 0xb72d2ec4
	.word 0x954ee841
	.word 0xb36fd636
	.word 0xbc4988da
	.word 0xaea05c04
	.word 0xce7483a6
	.word 0xea0309d7
	.word 0x62498466
	.word 0x1cd29ac4
	.word 0x97f38b62
	.word 0x690bcf85
	.word 0x97f38b62
	.word 0x9bd83b8b
    

    RVTEST_DATA_END
    

 RVMODEL_DATA_BEGIN
    signature_x12_0:
        .fill 0,4,0xdeadbeef
    
    
    signature_x20_0:
        .fill 83968,4,0xdeadbeef
    
    
    signature_x24_0:
        .fill 0,4,0xdeadbeef
    
    
    #ifdef rvtest_mtrap_routine
    
    mtrap_sigptr:
        .fill 128,4,0xdeadbeef
    
    #endif
    
    #ifdef rvtest_gpr_save
    
    gpr_save:
        .fill 32*(XLEN/32),4,0xdeadbeef
    
    #endif
    
    RVMODEL_DATA_END
    

illegal instruction

| **测试**                      | **是否测试** | **描述**                                                                                                               | **ISA**          |
| ----------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **exception_csr.S**           | **P**        | **越权访问CSR**                                                                                                        | **unprivileged** |
| **exception_eew_offset.S**    | **P**        | **使用不受支持的EEW，如index的向量load使用了不支持的偏移宽度，但是由于spike支持所有sew设置，故不会触发exception**      | **vector**       |
| **exception_frm.S**           | **P**        | **当fcsr的舍入模式设置为无效值时，使用动态舍入模式**                                                                   | **unprivileged** |
| **exception_fs.S**            | **P**        | **关闭mstatus或vsstatus的FS位后尝试执行向量浮点操作**                                                                  | **vector**       |
| **exception_lmul_mismatch.S** | **P**        | **向量指令使用的源向量操作数与LMUL的设置不匹配（如LMUL设置为2，但源操作数使用了v3，不为2的倍数）**                     | **vector**       |
| **exception_shift.S**         | **F**        | **32位ISA尝试移动超过31位，无法测试，编译器报错**                                                                      | **unprivileged** |
| **exception_vill.S**          | **P**        | **当vill置位时，尝试执行其他依赖此vtype寄存器的向量指令；测试的非法配置如下：sew=1xx，lmul=100，均为目前标记为保留的值**    | **vector**       |
| **exception_vs.S**            | **P**        | **关闭mstatus或的VS位后尝试执行向量操作**                                                                              | **vector**       |
| **exception_vstart.S**        | **P**        | **当vstart不为零时执行一系列向量操作包括：reduction operations、vcpop、vfirst、vmsbf、vmsif、vmsof、viota、vcompress** | **vector**       |

# misaligned_address

| **测试**                        | **是否测试** | **描述**                                  | **ISA**          |
| ------------------------------------- | ------------------ | ----------------------------------------------- | ---------------------- |
| **exception_base_misalign.S**   | **P**        | **向量Index在load时，使用的基地址未对齐** | **vector**       |
| **exception_offset_misalign.S** | **P**        | **向量Index在load时，使用的偏移未对齐**   | **vector**       |
| **exception_ld_st.S**           | **P**        | **在load或store时，使用的地址未对齐**     | **unprivileged** |
|                                       |                    |                                                 |                        |
|                                       |                    |                                                 |                        |

# misaligned_fetch

| **测试**             | **是否测试** | **描述**                                         | **ISA**          |
| -------------------------- | ------------------ | ------------------------------------------------------ | ---------------------- |
| **exception_jump.S** | **P**        | **跳转到非对齐的地址，带压缩指令集系统不会触发** | **unprivileged** |
|                            |                    |                                                        |                        |
|                            |                    |                                                        |                        |
|                            |                    |                                                        |                        |
|                            |                    |                                                        |                        |

# ECALL

| **测试**                   | **是否测试** | **描述**        | **ISA**       |
| -------------------------------- | ------------------ | --------------------- | ------------------- |
| **exception_machine.S**    | **P**        | **机器态ecall** | **privilege** |
| **exception_user.S**       | **P**        | **用户态ecall** | **privilege** |
| **exception_supervisor.S** | **P**        | **监管态ecall** | **privilege** |
| **exception_hypervisor.S** | **P**        | **虚拟态ecall** | **privilege** |
|                                  |                    |                       |                     |

# Page Fault

| **测试**                         | **是否测试** | **描述**     | **ISA**       |
| -------------------------------------- | ------------------ | ------------------ | ------------------- |
| **exception_fetch_page_fault.S** | **P**        | **取指缺页** | **privilege** |
| **exception_load_page_fault.S**  | **P**        | **加载缺页** | **privilege** |
| **exception_store_page_fault.S** | **P**        | **存储缺页** | **privilege** |
|                                        |                    |                    |                     |
|                                        |                    |                    |                     |

# access fault

| **测试**                     | **是否测试** | **描述**         | **ISA**         |
| ---------------------------------- | ------------------ | ---------------------- | --------------------- |
| **exception_fetch_access.S** | **P**        | **取指访问异常** | **unprivilege** |
| **exception_load_access.S**  | **P**        | **加载访问异常** | **unprivilege** |
| **exception_store_access.S** | **P**        | **存储访问异常** | **unprivilege** |
|                                    |                    |                        |                       |
|                                    |                    |                        |                       |

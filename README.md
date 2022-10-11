# RISC-V Vector Autometic Tests Generator

## Prerequisite
1. RVV Compiler
   1. Set `gcc` and `objdump` variables in two files: `scripts/run_riscof_coverage.py` and `scripts/run_spike.py`
2. RISCV-ISAC RVV Support
   1. Install `https://github.com/hushenwei2000/riscv-isac-rvv` **branch `vector`**
3. RISCOF
   1. Just install official RISCOF
## Usage

```
python run.py -i <instruction> -t <type> [--vlen VLEN] [--vsew VSEW]
```

- The type shall be consistent with the instruction: i (integer), f (floating point), m (mask), p (permute), x (fix point), l (load store)
- Supported instruction and type can be seen in `cgfs/<type>/<instruction>.yaml`
- vlen VLEN       Vector Register Length: 32, 64, 128(default), 256, 512, 1024
- vsew VSEW       Selected Element Width: 8, 16, 32(default), 64

## Support Configuration

| Parameter | Numbers                 | Current Support|   Note                           |
| ---       | ---                     | ---            |   ----                           |
| vlen      |  128 ~ 2^16             |  128 ~ 1024    | Spike now support largest 4096   |
| vsew      |  8, 16, 32, 64          |  8, 16, 32, 64 |                                  |
| lmul      |1/8, 1/4, 1/2, 1, 2, 4, 8| 1, 4           |  lmul=4 except load/store        |
| vta       |  0, 1                   |  0             |                                  |
| vma       |  0, 1                   |  0             |                                  |

Notes:
- elen = vlen
## Develop

### Add a instruction

1. Give a `instr` such as `vadd`, this will include `vadd.vv/x/i` tests. If it is difficult to gather them, it can also be separated.
2. Put a yaml formatted CGF to `cgfs/<type>/` directory. The name should be `<instr>.yaml` .
3. Add a file to `scripts/create_test_<type>/<instr>.yaml` (can copy `vadd` first).You should mainly modify `generate_macros` and `generate_tests`.There are two functions:
4. Add a file to `scripts/create_test_<type>/<instr>.yaml` (can copy `vadd` first).You should mainly modify `generate_macros` and `generate_tests`.There are two functions:

   1. `create_empty_test_vadd`: create test which only contains one test, this file is used to generate coverage report.
   2. `create_first_test_vadd`: create test which has all operands from coverage report, but the expected answers are wrong. Used to run sail model to generate true results.
5. Add `import` info in `scripts/lib.py`.

## CheckList

- "-"   : Not test/support yet
- "P"   : Test file is correct(pass Spike), but not fully cover val_comb
- "P P" : Test file is correct and fully cover val_comb (rd, rs may not fully cover)
  - *Now cover over 95% coverage points is regarded as pass, remaining need some fine tune
- "/"   : Configuration not support for this instruction(no need to test)
- Not listed instruction are not tested yet

### Mask

#### vmand, vmandnot, vmnand, vmor, vmornot, vmxnor, vmxor; vmsbf; vpopc, vfirst; vid, viota

| Config                        | Status | Config                        | Status |
| ----------------------------- | ------ | ----------------------------- | ------ |
| vlen128 vsew8 lmul1           | P      | vlen128 vsew8 lmul4           |        |
| vlen128 vsew16 lmul1          | P      | vlen128 vsew16 lmul4          |        |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32 lmul4          | P      |
| vlen128 vsew64 lmul1          | P      | vlen128 vsew64 lmul4          |        |
| vlen256 vsew8 lmul1           | P      | vlen256 vsew8 lmul4           |        |
| vlen256 vsew16 lmul1          | P      | vlen256 vsew16 lmul4          |        |
| vlen256 vsew32 lmul1          | P P    | vlen256 vsew32 lmul4          |        |
| vlen256 vsew64 lmul1          | P      | vlen256 vsew64 lmul4          |        |
| vlen512 vsew8 lmul1           | P      | vlen512 vsew8 lmul4           |        |
| vlen512 vsew16 lmul1          | P      | vlen512 vsew16 lmul4          |        |
| vlen512 vsew32 lmul1          | P      | vlen512 vsew32 lmul4          |        |
| vlen512 vsew64 lmul1          | P      | vlen512 vsew64 lmul4          |        |
| vlen1024 vsew8 lmul1          | P      | vlen1024 vsew8 lmul4          |        |
| vlen1024 vsew16 lmul1         | P      | vlen1024 vsew16 lmul4         |        |
| vlen1024 vsew32 lmul1         | P      | vlen1024 vsew32 lmul4         |        |
| vlen1024 vsew64 lmul1         | P      | vlen1024 vsew64 lmul4         |        |

### Permute

#### vcompress, vmre, vmv, vfmv, vrgather, vrgatherei16, vslide, vslide1, vfslide

| Config                        | vcompress | vmre | vmv | vfmv | vrgather | vrgatherei16 | vslide | vslide1 | vfslide |
| ----------------------------- | --------- | ---- | --- | ---- | -------- | ------------ | ------ | ------- | ------- |
| vlen128 vsew8 lmul1           | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen128 vsew16 lmul1          | P         | P    | P   | /    | P        | P P          | P      | P       | /       |
| vlen128 vsew32 lmul1(default) | P P       | P    | P P | P P  | P P      | P P          | P P    | P       | P       |
| vlen128 vsew64 lmul1          | P P       | P    | P P | P P  | P P      | P P          | P P    | P P     | P       |
| vlen256 vsew8 lmul1           | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen256 vsew16 lmul1          | P         | P    | P   | /    | P        | P P          | P      | P       | /       |
| vlen256 vsew32 lmul1          | P P       | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen256 vsew64 lmul1          | P P       | P    | P P | P P  | P P      | P P          | P P    | P       | P       |
| vlen512 vsew8 lmul1           | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen512 vsew16 lmul1          | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen512 vsew32 lmul1          | P P       | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen512 vsew64 lmul1          | P P       | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen1024 vsew8 lmul1          | P         | P    | P P | /    | P        | P            | P      | P       | /       |
| vlen1024 vsew16 lmul1         | P         | P    | P   | /    | P        | P P          | P P    | P       | /       |
| vlen1024 vsew32 lmul1         | P         | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen1024 vsew64 lmul1         | P  P      | P    | P P | P P  | P P      | P P          | P P    | P       | P       |
| ----------------------------- | --------- | ---- | --- | ---- | -------- | ------------ | ------ | ------- | ------- |
| vlen128 vsew32 lmul4          | P P       | X    | P P | P P  | P P      | P            | P      | P       | P       |

note:

1. vmv

- vsew32 requires rs1val_walking_vector_unsgn
- vsew64 requires rs1val_walking_vector

1. mre NOT support lmul4 because vl set to VLMAX but vmre only move 1/2/4/8 registers

### Integer

#### Simple Arithmetic: vadc, vsbc; vadd, vand, vdiv, vdivu,  vmul, vmulh, vmulhsu, vmulhu, vsll, vsra, vsrl, vsub, vxor, vrem, vremu, vrsub, vsadd, vsaddu, vssub, vssubu, vmax, vmaxu, vmin, vminu, 

| Config                        | Status | Config                        | Status |
| ----------------------------- | ------ | ----------------------------- | ------ |
| vlen128 vsew8 lmul1           | P P    | vlen128 vsew8 lmul4           |        |
| vlen128 vsew16 lmul1          | P P    | vlen128 vsew16 lmul4          |        |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32 lmul4(default) |  P P   |
| vlen128 vsew64 lmul1          | P P    | vlen128 vsew64 lmul4          |        |
| vlen256 vsew8 lmul1           | P P    | vlen256 vsew8 lmul4           |        |
| vlen256 vsew16 lmul1          | P P    | vlen256 vsew16 lmul4          |        |
| vlen256 vsew32 lmul1          | P P    | vlen256 vsew32 lmul4          |        |
| vlen256 vsew64 lmul1          | P P    | vlen256 vsew64 lmul4          |        |
| vlen512 vsew8 lmul1           | P P    | vlen512 vsew8 lmul4           |        |
| vlen512 vsew16 lmul1          | P P    | vlen512 vsew16 lmul4          |        |
| vlen512 vsew32 lmul1          | P P    | vlen512 vsew32 lmul4          |        |
| vlen512 vsew64 lmul1          | P P    | vlen512 vsew64 lmul4          |        |
| vlen1024 vsew8 lmul1          | P P    | vlen1024 vsew8 lmul4          |        |
| vlen1024 vsew16 lmul1         | P P    | vlen1024 vsew16 lmul4         |        |
| vlen1024 vsew32 lmul1         | P P    | vlen1024 vsew32 lmul4         |        |
| vlen1024 vsew64 lmul1         | P P    | vlen1024 vsew64 lmul4         |        |


#### Multiply-Add & Add-with-Carry Subtract-with-Borrow & Comparison: vmacc, vmadd, vnmsac, vnmsub & vmadc, vmsbc & vmseq, vmsgt, vmsgtu, vmsle, vmsleu, vmslt, vmsltu, vmsne
| Config                        | Status | Config                        | Status |
| ----------------------------- | ------ | ----------------------------- | ------ |
| vlen128 vsew8 lmul1           | P P    |
| vlen128 vsew16 lmul1          | P P    |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32 lmul4          | P P    |
| vlen128 vsew64 lmul1          | P P    |
| vlen256 vsew8 lmul1           | P P    |
| vlen256 vsew16 lmul1          | P P    |
| vlen256 vsew32 lmul1          | P P    |
| vlen256 vsew64 lmul1          | P P    |
| vlen512 vsew8 lmul1           | P P    |
| vlen512 vsew16 lmul1          | P P    |
| vlen512 vsew32 lmul1          | P P    |
| vlen512 vsew64 lmul1          | P P    |
| vlen1024 vsew8 lmul1          | P P    |
| vlen1024 vsew16 lmul1         | P P    |
| vlen1024 vsew32 lmul1         | P P    |
| vlen1024 vsew64 lmul1         | P P    |

#### Reduction Arithmetic:  vor; vredand, vredmax, vredmaxu, vredmin, vredminu, vredor, vredsum, vredxor; 

| Config                        | Status |Config                        | Status |
| ----------------------------- | ------ |----------------------------- | ------ |
| vlen128 vsew8 lmul1           | P P    |
| vlen128 vsew16 lmul1          | P P    |
| vlen128 vsew32 lmul1(default) | P P    |vlen128 vsew32 lmul4          | P P    |
| vlen128 vsew64 lmul1          | P P    |
| vlen256 vsew8 lmul1           | P P    |
| vlen256 vsew16 lmul1          | P P    |
| vlen256 vsew32 lmul1          | P P    |
| vlen256 vsew64 lmul1          | P P    |
| vlen512 vsew8 lmul1           | P P    |
| vlen512 vsew16 lmul1          | P P    |
| vlen512 vsew32 lmul1          | P P    |
| vlen512 vsew64 lmul1          | P P    |
| vlen1024 vsew8 lmul1          | P P    |
| vlen1024 vsew16 lmul1         | P P    |
| vlen1024 vsew32 lmul1         | P P    |
| vlen1024 vsew64 lmul1         | P P    |


#### Widen Arithmetic: vwadd, vwaddu, vwmacc, vwmaccsu, vwmaccu, vwmaccus; vwmul, vwmulsu, vwmulu, vwredsum, vwredsumu, vwsub, vwsubu; vnsra, vnsrl;

* widen and narrow instruction not support VSEW=64 (vsew should be <= 64)

| Config                        | Status | Config                       | Status |
| ----------------------------- | ------ |----------------------------- | ------ |
| vlen128 vsew8 lmul1           | P P    |
| vlen128 vsew16 lmul1          | P P    |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32 lmul4         |  P P   |
| vlen256 vsew8 lmul1           | P P    |
| vlen256 vsew16 lmul1          | P P    |
| vlen256 vsew32 lmul1          | P P    |
| vlen512 vsew8 lmul1           | P P    |
| vlen512 vsew16 lmul1          | P P    |
| vlen512 vsew32 lmul1          | P P    |
| vlen1024 vsew8 lmul1          | P P    |
| vlen1024 vsew16 lmul1         | P P    |
| vlen1024 vsew32 lmul1         | P P    |
### Floating Points

#### vfadd, vfclas, *vfcvt*, vfdiv, vfmacc, vfmax, vfmin, vfmsac, vfmsub, vfmul, `vfncvt`, vfnmacc, vfnmadd, vfnmsac, vfnmsub, vfrdiv, vfrec7, vfredmax, vfredmin

| Config                        | vfadd | vfclas | *vfcvt* | vfdiv | vfmacc | vfmadd | vfmax | vfmin | vfmsac | vfmsub | vfmul | `vfncvt` | vfnmacc | vfnmadd | vfnmsac | vfnmsub | vfrdiv | vfrec7 | vfredmax | vfredmin |
| ----------------------------- | ----- | ------ | ------- | ----- | ------ | ------ | ----- | ----- | ------ | ------ | ----- | -------- | ------- | ------- | ------- | ------- | ------ | ------ | -------- | -------- |
| vlen128 vsew32 lmul1(default) | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen128 vsew64 lmul1          | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen256 vsew32 lmul1          | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen256 vsew64 lmul1          | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen512 vsew32 lmul1          | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen512 vsew64 lmul1          | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen1024 vsew32 lmul1         | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen1024 vsew64 lmul1         | P P   | P P    | -       | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -        | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |

>  vfcvt.x.f.v, vfcvt.rtz.xu.f.v, etc. not support

#### vfredosum, vfredusum, vfrsqrt7, vfrsub, vfsgnj, vfsgnjn, vfsgnjx, vfsqrt, vfsub

| Config                        | vfredosum | vfredusum | vfrsqrt7 | vfrsub | vfsgnj | vfsgnjn | vfsgnjx | vfsqrt | vfsub |
| ----------------------------- | --------- | --------- | -------- | ------ | ------ | ------- | ------- | ------ | ----- |
| vlen128 vsew32 lmul1(default) | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen128 vsew64 lmul1          | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen256 vsew32 lmul1          | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen256 vsew64 lmul1          | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen512 vsew32 lmul1          | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen512 vsew64 lmul1          | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen1024 vsew32 lmul1         | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen1024 vsew64 lmul1         | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen128 vsew32 lmul4          | P P          | P P          | P P         | P P       | P P       | P P        | P P        | P P       | P P      |
| vlen128 vsew64 lmul4          |           |           |          |        |        |         |         |        |       |
| vlen256 vsew32 lmul4          |           |           |          |        |        |         |         |        |       |
| vlen256 vsew64 lmul4          |           |           |          |        |        |         |         |        |       |
| vlen512 vsew32 lmul4          |           |           |          |        |        |         |         |        |       |
| vlen512 vsew64 lmul4          |           |           |          |        |        |         |         |        |       |
| vlen1024 vsew32 lmul4         |           |           |          |        |        |         |         |        |       |
| vlen1024 vsew64 lmul4         |           |           |          |        |        |         |         |        |       |

#### vfwadd, vfwcvt, vfwmacc, vfwmsac, vfwmul, vfwnmacc, vfwnmsac, vfwredsum, vfwsub

| Config                        | vfwadd | vfwcvt | vfwmacc | vfwmsac | vfwmul | vfwnmacc | vfwnmsac | vfwredsum | vfwsub |
| ----------------------------- | ------ | ------ | ------- | ------- | ------ | -------- | -------- | --------- | ------ |
| vlen128 vsew16 lmul1          | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen128 vsew32 lmul1(default) | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen256 vsew16 lmul1          | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen256 vsew32 lmul1          | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen512 vsew16 lmul1          | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen512 vsew32 lmul1          | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen1024 vsew16 lmul1         | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen1024 vsew32 lmul1         | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen128 vsew16 lmul4          | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen128 vsew32 lmul4          | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen256 vsew16 lmul4          | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen256 vsew32 lmul4          |     |     |      |      |     |       |       |        |     |
| vlen512 vsew16 lmul4          | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen512 vsew32 lmul4          |     |     |      |      |     |       |       |        |     |
| vlen1024 vsew16 lmul4         | /       | /       | /        | /        | /       | /         | /         | /          | /       |
| vlen1024 vsew32 lmul4         |     |     |      |      |     |       |       |        |     |

note:
- we do not have 16-bit floating point dataset

### Fix Points

|                                                                  | vaadd | vaaddu | vasub | vasubu | vnclip | vnclipu | vsmul | vssra | vssrl |
| ---------------------------------------------------------------- | ----- | ------ | ----- | ------ | ------ | ------- | ----- | ----- | ----- |
| vlen128 vsew8 lmul1                                              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128 vsew16 lmul1                                             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128 vsew32 lmul1(default)                                    | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128 vsew64 lmul1                                             | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| vlen256 vsew8 lmul1                                              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen256 vsew16 lmul1                                             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen256 vsew32 lmul1                                             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen256 vsew64 lmul1                                             | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| vlen512 vsew8 lmul1                                              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen512 vsew16 lmul1                                             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen512 vsew32 lmul1                                             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen512 vsew64 lmul1                                             | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| vlen1024 vsew8 lmul1                                             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen1024 vsew16 lmul1                                            | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen1024 vsew32 lmul1                                            | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen1024 vsew64 lmul1                                            | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| vlen128 vsew32 lmul4                                             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |

*vnclip and vnclipu not support vsew=64 because vsew will be 128 


### LOAD


|                               | vle8/16/32/64 |  vlre8/16/32  | vlse8/16/32 |vls(s)ege8 |vls(s)ege16|vls(s)ege32|vluxei8/16/32|vluxeiseg8/16/32|
| ------------------------------| ----          |  -----        | -----       |  -------  | --------  | --------  | -------     |  ------------  |
| vlen128 vsew8 lmul1           | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen128 vsew16 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen128 vsew32 lmul1(default) | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen128 vsew64 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen256 vsew8 lmul1           | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen256 vsew16 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen256 vsew32 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen256 vsew64 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen512 vsew8 lmul1           | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen512 vsew16 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen512 vsew32 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen512 vsew64 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen1024 vsew8 lmul1          | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen1024 vsew16 lmul1         | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen1024 vsew32 lmul1         | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |
| vlen1024 vsew64 lmul1         | P P           |  P P          | P P         |  P P      | P P       | P P       |   P P       |      P P       |

### Store

|                               | vs(s)(seg)e8/16/32/64 |
| ------------------------------| ------------          |
| vlen128 vsew8 lmul1           |     P P               |
| vlen128 vsew16 lmul1          |     P P               |
| vlen128 vsew32 lmul1(default) |     P P               |
| vlen128 vsew64 lmul1          |     P P               |
| vlen256 vsew8 lmul1           |     P P               |
| vlen256 vsew16 lmul1          |     P P               |
| vlen256 vsew32 lmul1          |     P P               |
| vlen256 vsew64 lmul1          |     P P               |
| vlen512 vsew8 lmul1           |     P P               |
| vlen512 vsew16 lmul1          |     P P               |
| vlen512 vsew32 lmul1          |     P P               |
| vlen512 vsew64 lmul1          |     P P               |
| vlen1024 vsew8 lmul1          |     P P               |
| vlen1024 vsew16 lmul1         |     P P               |
| vlen1024 vsew32 lmul1         |     P P               |
| vlen1024 vsew64 lmul1         |     P P               |


## Code Explain
### Register Alignment
- For example,  `require_noover(insn.rd(), rd_lmul, insn.rs1(), rs1_lmul)` require rs1 and rd will not overwrite each other
  - no overlap condition is **either** rightest rs1 is smaller than rd **or** rightest rd is smaller than rs1
  - `((rs1 + rs1_lmul - 1 < rd) or (rd + rd_lmul - 1 < rs1))`
  - There are many conditions like this in generating macros for different registers.
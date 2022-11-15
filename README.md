# RISC-V Vector Automatic Tests Generator

## Prerequisite

1. RVV Compiler
   1. Set `gcc`,`objdump`, and `riscof` directory's path variables in file: `scripts/constants.py`
2. RISCV-ISAC RVV Support
   1. `git clone https://github.com/hushenwei2000/riscv-isac-rvv`
   2. `cd riscv-isac-rvv`
   3. `git checkout vetcor`
   4. `pip install . --prefix=~/.local`  # Anywhere you want  
   5. Add `~/.local` to your PATH   
   
   If the terminal can find `riscv_isac` command then it's successful
3. Spike
   1. Install Latest [https://github.com/riscv-software-src/riscv-isa-sim](https://github.com/riscv-software-src/riscv-isa-sim).
   > $ apt-get install device-tree-compiler  
   > $ mkdir build  
   > $ cd build  
   > $ ../configure --prefix=$RISCV  --enable-commitlog   
   > $ make  
   > $ [sudo] make install   
   
   ⚠️ Need to add `--enable-commitlog`   
   2. Add `<spike_path>/build` to your PATH
   
   If the terminal can find `spike` command then it's successful

## Usage

### Generate One Instruction

```
python run.py -i <instruction> -t <type> [--vlen VLEN] [--vsew VSEW]
```
****
- The type shall be consistent with the instruction: i (integer), f (floating point), m (mask), p (permute), x (fix point), l (load store)
- Supported instruction and type can be seen in `cgfs/<type>/<instruction>.yaml`
- vlen VLEN       Vector Register Length: 32, 64, 128(default), 256, 512, 1024
- vsew VSEW       Selected Element Width: 8, 16, 32(default), 64
- Other options seen in `python run.py -h`
### Generate All Tests

```
python generate_all.py
```

- This will use default parameter configuration to generate all integer instructions tests.
- **Modify `runcommand_<type>` function to run different parameter.**
- **Modyfy `main` function to run different type of instructions.**
- Test file will generate in `generate_all` folder.
- ⚠️ Because we still have bugs, those tests are not correct (i.e. **CAN'T** be used as test file) will generate `spike.log` in `generate_all` folder. You can see FAIL in the ending of these logs.

### Check All Generated Tests

```
python check_all.py
```

- Check all generated folders. Find out if test file FAIL and the statistics of COVERAGE.
- Output will in 'check_all.out'.

## Support Configuration

| Parameter | Numbers                   | Current Support | Note                           |
| --------- | ------------------------- | --------------- | ------------------------------ |
| vlen      | 128 ~ 2^16                | 128 ~ 1024      | Spike now support largest 4096 |
| vsew      | 8, 16, 32, 64             | All             |                                |
| lmul      | 1/8, 1/4, 1/2, 1, 2, 4, 8 | All             | lmul=8 except load/store， 1/8 except eew>=32 loadstore       |
| vta       | 0, 1                      | 0               |                                |
| vma       | 0, 1                      | 0               |                                |

### Notice of Failure Tests

- elen = 64 for default
  - vsew should <= elen * lmul
  - So, when lmul = 0.125, load/store eew=32+ cannot test. 

- If there are failure tests, **most probably** is because that configuration can not be tested on that instruction. For example test widen instruction when vsew=64, or test floating point when vsew=8/16, or the elen related restriction above.
  - At present, users need to determine which configurations can be produced to avoid such failure. <kbd>FutureSupport</kbd>

## Develop

### Add a instruction

1. Give a `instr` such as `vadd`, this will include `vadd.vv/x/i` tests. If it is difficult to gather them, it can also be separated.
2. Put a yaml formatted CGF to `cgfs/<type>/` directory. The name should be `<instr>.yaml` .
3. Add a file to `scripts/create_test_<type>/<instr>.yaml` (can copy `vadd` first).You should mainly modify `generate_macros` and `generate_tests`.There are two functions:
4. Add a file to `scripts/create_test_<type>/<instr>.yaml` (can copy `vadd` first).You should mainly modify `generate_macros` and `generate_tests`.There are two functions:

   1. `create_empty_test_vadd`: create test which only contains one test, this file is used to generate coverage report.
   2. `create_first_test_vadd`: create test which has all operands from coverage report, but the expected answers are wrong. Used to run sail model to generate true results.
5. Add `import` info in `scripts/lib.py`.

### Add configuration

1. Add `vsew<vsew>_lmul<lmul>` and `vsew<vsew>_lmul<lmul>_nofail` folders in `env/macros` just like the current directory. You can copy .h from any other configuration folder.
2. If you modify `vsew`:
   1. Replace old vsew to new vsew globally. For example, search and replace `16` to `32` globally.
   2. Replace floating load instruction globally. For example vsew=64, search and replace 1) `flw` to `fld`, 2) `.word` to `.dword`, 3) `feq.s` to `feq.d` 4) offset of fld like `fld f2, 8(a0);` to `fld f2, 16(a0);` globally.
   3. Modify first part(below) carefully.
```
// VSEW temporarily hard-coded to 16 bits
#define RVTEST_VSET vsetivli x31, 1, e16, tu, mu;
#define __riscv_vsew 16
......
#define VSET_DOUBLE_VSEW vsetivli x31, 1, e32, tu, mu;
#define VSET_CONST_VSEW(eew_num) vsetivli x31, ##eew_num, m4, tu, mu;
```

3. If you modify `lmul`:
   1. Replace old `m<lmul>` to new `m<lmul>`. For example, search and replace `m1` to `m8` globally.

## CheckList

- "-"   : Not test/support yet
- "P"   : Test file is correct(pass Spike), but not fully cover val_comb
- "P P" : Test file is correct and fully cover val_comb (rd, rs may not fully cover)
  - *Now cover over 95% coverage points is regarded as pass, remaining need some fine tune
- "/"   : Configuration not support for this instruction(no need to test)
- Not listed instruction are not tested yet

### Mask

#### vmand, vmandnot, vmnand, vmor, vmornot, vmxnor, vmxor; vmsbf; vpopc, vfirst; vid, viota

| Config                        | Status | Config                  | Status | Config                        | Status |
| ----------------------------- | ------ | ---------------------   | ------ | ---------------------         | ------ |
| vlen128 vsew8 lmul1           | P      | vlen128 vsew8   lmul2-8 | P      | vlen128 vsew8   lmul0.125-0.5 | P      |
| vlen128 vsew16 lmul1          | P      | vlen128 vsew16  lmul2-8 | P      | vlen128 vsew16  lmul0.125-0.5 | P      |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32  lmul2-8 | P      | vlen128 vsew32  lmul0.125-0.5 | P      |
| vlen128 vsew64 lmul1          | P      | vlen128 vsew64  lmul2-8 | P      | vlen128 vsew64  lmul0.125-0.5 | P      |
| vlen256 vsew8 lmul1           | P      | vlen256 vsew8   lmul2-8 | P      | vlen256 vsew8   lmul0.125-0.5 | P      |
| vlen256 vsew16 lmul1          | P      | vlen256 vsew16  lmul2-8 | P      | vlen256 vsew16  lmul0.125-0.5 | P      |
| vlen256 vsew32 lmul1          | P P    | vlen256 vsew32  lmul2-8 | P      | vlen256 vsew32  lmul0.125-0.5 | P      |
| vlen256 vsew64 lmul1          | P      | vlen256 vsew64  lmul2-8 | P      | vlen256 vsew64  lmul0.125-0.5 | P      |
| vlen512 vsew8 lmul1           | P      | vlen512 vsew8   lmul2-8 | P      | vlen512 vsew8   lmul0.125-0.5 | P      |
| vlen512 vsew16 lmul1          | P      | vlen512 vsew16  lmul2-8 | P      | vlen512 vsew16  lmul0.125-0.5 | P      |
| vlen512 vsew32 lmul1          | P      | vlen512 vsew32  lmul2-8 | P      | vlen512 vsew32  lmul0.125-0.5 | P      |
| vlen512 vsew64 lmul1          | P      | vlen512 vsew64  lmul2-8 | P      | vlen512 vsew64  lmul0.125-0.5 | P      |
| vlen1024 vsew8 lmul1          | P      | vlen1024 vsew8  lmul2-8 | P      | vlen1024 vsew8  lmul0.125-0.5 | P      |
| vlen1024 vsew16 lmul1         | P      | vlen1024 vsew16 lmul2-8 | P      | vlen1024 vsew16 lmul0.125-0.5 | P      |
| vlen1024 vsew32 lmul1         | P      | vlen1024 vsew32 lmul2-8 | P      | vlen1024 vsew32 lmul0.125-0.5 | P      |
| vlen1024 vsew64 lmul1         | P      | vlen1024 vsew64 lmul2-8 | P      | vlen1024 vsew64 lmul0.125-0.5 | P      |

### Permute
⚠️ vslide, vcompress will generate too many tests if num_elems (vlen*lmul/vsew) is too big. Test them will take a long time (longer than 20min)
#### vcompress, vmre, vmv, vfmv, vrgather, vrgatherei16, vslide, vslide1, vfslide

| Config                            | vcompress | vmre | vmv | vfmv | vrgather | vrgatherei16 | vslide | vslide1 | vfslide |
| -----------------------------     | --------- | ---- | --- | ---- | -------- | ------------ | ------ | ------- | ------- |
| vlen128 vsew8 lmul1               | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen128 vsew16 lmul1              | P         | P    | P   | /    | P        | P P          | P      | P       | /       |
| vlen128 vsew32 lmul1(default)     | P P       | P    | P P | P P  | P P      | P P          | P P    | P       | P       |
| vlen128 vsew64 lmul1              | P P       | P    | P P | P P  | P P      | P P          | P P    | P P     | P       |
| vlen256 vsew8 lmul1               | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen256 vsew16 lmul1              | P         | P    | P   | /    | P        | P P          | P      | P       | /       |
| vlen256 vsew32 lmul1              | P P       | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen256 vsew64 lmul1              | P P       | P    | P P | P P  | P P      | P P          | P P    | P       | P       |
| vlen512 vsew8 lmul1               | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen512 vsew16 lmul1              | P         | P    | P   | /    | P        | P            | P      | P       | /       |
| vlen512 vsew32 lmul1              | P P       | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen512 vsew64 lmul1              | P P       | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen1024 vsew8 lmul1              | P         | P    | P P | /    | P        | P            | P      | P       | /       |
| vlen1024 vsew16 lmul1             | P         | P    | P   | /    | P        | P P          | P P    | P       | /       |
| vlen1024 vsew32 lmul1             | P         | P    | P P | P P  | P P      | P P          | P      | P       | P       |
| vlen1024 vsew64 lmul1             | P  P      | P    | P P | P P  | P P      | P P          | P P    | P       | P       |
| -----------------------------     | --------- | ---- | --- | ---- | -------- | ------------ | ------ | ------- | ------- |
| vlen128-1024 vsew8  lmul2-8       | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
| vlen128-1024 vsew16 lmul2-8       | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
| vlen128-1024 vsew32 lmul2-8       | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
| vlen128-1024 vsew64 lmul2-8       | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
| -----------------------------     | --------- | ---- | --- | ---- | -------- | ------------ | ------ | ------- | ------- |
| vlen128-1024 vsew8  lmul0.125-0.5 | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
| vlen128-1024 vsew16 lmul0.125-0.5 | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
| vlen128-1024 vsew32 lmul0.125-0.5 | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
| vlen128-1024 vsew64 lmul0.125-0.5 | P P       | P    | P P | P P  | P P      | P            | P      | P       | P       |
note:

1. vmv

- vsew32 requires rs1val_walking_vector_unsgn
- vsew64 requires rs1val_walking_vector

### Integer

#### Simple Arithmetic: vadc, vsbc; vadd, vand, vdiv, vdivu,  vmul, vmulh, vmulhsu, vmulhu, vsll, vsra, vsrl, vsub, vxor, vrem, vremu, vrsub, vsadd, vsaddu, vssub, vssubu, vmax, vmaxu, vmin, vminu,

| Config                        | Status | Config                  | Status | Config                        | Status |
| ----------------------------- | ------ | ----------------------  | ------ | ---------------------         | ------ |
| vlen128 vsew8 lmul1           | P P    | vlen128 vsew8   lmul2-8 | P P    | vlen128 vsew8   lmul0.125-0.5 | P      |
| vlen128 vsew16 lmul1          | P P    | vlen128 vsew16  lmul2-8 | P P    | vlen128 vsew16  lmul0.125-0.5 | P      |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32  lmul2-8 | P P    | vlen128 vsew32  lmul0.125-0.5 | P      |
| vlen128 vsew64 lmul1          | P P    | vlen128 vsew64  lmul2-8 | P P    | vlen128 vsew64  lmul0.125-0.5 | P      |
| vlen256 vsew8 lmul1           | P P    | vlen256 vsew8   lmul2-8 | P P    | vlen256 vsew8   lmul0.125-0.5 | P      |
| vlen256 vsew16 lmul1          | P P    | vlen256 vsew16  lmul2-8 | P P    | vlen256 vsew16  lmul0.125-0.5 | P      |
| vlen256 vsew32 lmul1          | P P    | vlen256 vsew32  lmul2-8 | P P    | vlen256 vsew32  lmul0.125-0.5 | P      |
| vlen256 vsew64 lmul1          | P P    | vlen256 vsew64  lmul2-8 | P P    | vlen256 vsew64  lmul0.125-0.5 | P      |
| vlen512 vsew8 lmul1           | P P    | vlen512 vsew8   lmul2-8 | P P    | vlen512 vsew8   lmul0.125-0.5 | P      |
| vlen512 vsew16 lmul1          | P P    | vlen512 vsew16  lmul2-8 | P P    | vlen512 vsew16  lmul0.125-0.5 | P      |
| vlen512 vsew32 lmul1          | P P    | vlen512 vsew32  lmul2-8 | P P    | vlen512 vsew32  lmul0.125-0.5 | P      |
| vlen512 vsew64 lmul1          | P P    | vlen512 vsew64  lmul2-8 | P P    | vlen512 vsew64  lmul0.125-0.5 | P      |
| vlen1024 vsew8 lmul1          | P P    | vlen1024 vsew8  lmul2-8 | P P    | vlen1024 vsew8  lmul0.125-0.5 | P      |
| vlen1024 vsew16 lmul1         | P P    | vlen1024 vsew16 lmul2-8 | P P    | vlen1024 vsew16 lmul0.125-0.5 | P      |
| vlen1024 vsew32 lmul1         | P P    | vlen1024 vsew32 lmuL2-8 | P P    | vlen1024 vsew32 lmul0.125-0.5 | P      |
| vlen1024 vsew64 lmul1         | P P    | vlen1024 vsew64 lmul2-8 | P P    | vlen1024 vsew64 lmul0.125-0.5 | P      |

#### Multiply-Add & Add-with-Carry Subtract-with-Borrow & Comparison: vmacc, vmadd, vnmsac, vnmsub & vmadc, vmsbc & vmseq, vmsgt, vmsgtu, vmsle, vmsleu, vmslt, vmsltu, vmsne

| Config                        | Status | Config                 | Status | Config                        | Status |
| ----------------------------- | ------ | --------------------   | ------ | ---------------------         | ------ |
| vlen128 vsew8 lmul1           | P P    | vlen128 vsew8   lmul2-8| P P    | vlen128 vsew8   lmul0.125-0.5 | P      |
| vlen128 vsew16 lmul1          | P P    | vlen128 vsew16  lmul2-8| P P    | vlen128 vsew16  lmul0.125-0.5 | P      |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32  lmul2-8| P P    | vlen128 vsew32  lmul0.125-0.5 | P      |
| vlen128 vsew64 lmul1          | P P    | vlen128 vsew64  lmul2-8| P P    | vlen128 vsew64  lmul0.125-0.5 | P      |
| vlen256 vsew8 lmul1           | P P    | vlen256 vsew8   lmul2-8| P P    | vlen256 vsew8   lmul0.125-0.5 | P      |
| vlen256 vsew16 lmul1          | P P    | vlen256 vsew16  lmul2-8| P P    | vlen256 vsew16  lmul0.125-0.5 | P      |
| vlen256 vsew32 lmul1          | P P    | vlen256 vsew32  lmul2-8| P P    | vlen256 vsew32  lmul0.125-0.5 | P      |
| vlen256 vsew64 lmul1          | P P    | vlen256 vsew64  lmul2-8| P P    | vlen256 vsew64  lmul0.125-0.5 | P      |
| vlen512 vsew8 lmul1           | P P    | vlen512 vsew8   lmul2-8| P P    | vlen512 vsew8   lmul0.125-0.5 | P      |
| vlen512 vsew16 lmul1          | P P    | vlen512 vsew16  lmul2-8| P P    | vlen512 vsew16  lmul0.125-0.5 | P      |
| vlen512 vsew32 lmul1          | P P    | vlen512 vsew32  lmul2-8| P P    | vlen512 vsew32  lmul0.125-0.5 | P      |
| vlen512 vsew64 lmul1          | P P    | vlen512 vsew64  lmul2-8| P P    | vlen512 vsew64  lmul0.125-0.5 | P      |
| vlen1024 vsew8 lmul1          | P P    | vlen1024 vsew8  lmul2-8| P P    | vlen1024 vsew8  lmul0.125-0.5 | P      |
| vlen1024 vsew16 lmul1         | P P    | vlen1024 vsew16 lmul2-8| P P    | vlen1024 vsew16 lmul0.125-0.5 | P      |
| vlen1024 vsew32 lmul1         | P P    | vlen1024 vsew32 lmul2-8| P P    | vlen1024 vsew32 lmul0.125-0.5 | P      |
| vlen1024 vsew64 lmul1         | P P    | vlen1024 vsew64 lmul2-8| P P    | vlen1024 vsew64 lmul0.125-0.5 | P      |

#### Reduction Arithmetic:  vor; vredand, vredmax, vredmaxu, vredmin, vredminu, vredor, vredsum, vredxor;

| Config                        | Status | Config                 | Status | Config                        | Status |
| ----------------------------- | ------ | --------------------   | ------ | ---------------------         | ------ |
| vlen128 vsew8 lmul1           | P P    | vlen128 vsew8   lmul2-8| P P    | vlen128 vsew8   lmul0.125-0.5 | P      |
| vlen128 vsew16 lmul1          | P P    | vlen128 vsew16  lmul2-8| P P    | vlen128 vsew16  lmul0.125-0.5 | P      |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32  lmul2-8| P P    | vlen128 vsew32  lmul0.125-0.5 | P      |
| vlen128 vsew64 lmul1          | P P    | vlen128 vsew64  lmul2-8| P P    | vlen128 vsew64  lmul0.125-0.5 | P      |
| vlen256 vsew8 lmul1           | P P    | vlen256 vsew8   lmul2-8| P P    | vlen256 vsew8   lmul0.125-0.5 | P      |
| vlen256 vsew16 lmul1          | P P    | vlen256 vsew16  lmul2-8| P P    | vlen256 vsew16  lmul0.125-0.5 | P      |
| vlen256 vsew32 lmul1          | P P    | vlen256 vsew32  lmul2-8| P P    | vlen256 vsew32  lmul0.125-0.5 | P      |
| vlen256 vsew64 lmul1          | P P    | vlen256 vsew64  lmul2-8| P P    | vlen256 vsew64  lmul0.125-0.5 | P      |
| vlen512 vsew8 lmul1           | P P    | vlen512 vsew8   lmul2-8| P P    | vlen512 vsew8   lmul0.125-0.5 | P      |
| vlen512 vsew16 lmul1          | P P    | vlen512 vsew16  lmul2-8| P P    | vlen512 vsew16  lmul0.125-0.5 | P      |
| vlen512 vsew32 lmul1          | P P    | vlen512 vsew32  lmul2-8| P P    | vlen512 vsew32  lmul0.125-0.5 | P      |
| vlen512 vsew64 lmul1          | P P    | vlen512 vsew64  lmul2-8| P P    | vlen512 vsew64  lmul0.125-0.5 | P      |
| vlen1024 vsew8 lmul1          | P P    | vlen1024 vsew8  lmul2-8| P P    | vlen1024 vsew8  lmul0.125-0.5 | P      |
| vlen1024 vsew16 lmul1         | P P    | vlen1024 vsew16 lmul2-8| P P    | vlen1024 vsew16 lmul0.125-0.5 | P      |
| vlen1024 vsew32 lmul1         | P P    | vlen1024 vsew32 lmul2-8| P P    | vlen1024 vsew32 lmul0.125-0.5 | P      |
| vlen1024 vsew64 lmul1         | P P    | vlen1024 vsew64 lmul2-8| P P    | vlen1024 vsew64 lmul0.125-0.5 | P      |

#### Widen Arithmetic: vwadd, vwaddu, vwmacc, vwmaccsu, vwmaccu, vwmaccus; vwmul, vwmulsu, vwmulu, vwredsum, vwredsumu, vwsub, vwsubu; vnsra, vnsrl;

* widen and narrow instruction not support VSEW=64 (vsew should be <= 64)
* widen instruction(except VWRED*) not support LMUL=8 (lmul should be <= 4), lmul8 in table only means VWRED* pass

| Config                        | Status | Config                 | Status | Config                        | Status |
| ----------------------------- | ------ | --------------------   | ------ | --------------------          | ------ |
| vlen128 vsew8 lmul1           | P P    | vlen128 vsew8   lmul2-8| P P    | vlen128 vsew8   lmul0.125-0.5 | P P    |
| vlen128 vsew16 lmul1          | P P    | vlen128 vsew16  lmul2-8| P P    | vlen128 vsew16  lmul0.125-0.5 | P P    |
| vlen128 vsew32 lmul1(default) | P P    | vlen128 vsew32  lmul2-8| P P    | vlen128 vsew32  lmul0.125-0.5 | P P    |
| vlen256 vsew8 lmul1           | P P    | vlen256 vsew8   lmul2-8| P P    | vlen256 vsew8   lmul0.125-0.5 | P P    |
| vlen256 vsew16 lmul1          | P P    | vlen256 vsew16  lmul2-8| P P    | vlen256 vsew16  lmul0.125-0.5 | P P    |
| vlen256 vsew32 lmul1          | P P    | vlen256 vsew32  lmul2-8| P P    | vlen256 vsew32  lmul0.125-0.5 | P P    |
| vlen512 vsew8 lmul1           | P P    | vlen512 vsew8   lmul2-8| P P    | vlen512 vsew8   lmul0.125-0.5 | P P    |
| vlen512 vsew16 lmul1          | P P    | vlen512 vsew16  lmul2-8| P P    | vlen512 vsew16  lmul0.125-0.5 | P P    |
| vlen512 vsew32 lmul1          | P P    | vlen512 vsew32  lmul2-8| P P    | vlen512 vsew32  lmul0.125-0.5 | P P    |
| vlen1024 vsew8 lmul1          | P P    | vlen1024 vsew8  lmul2-8| P P    | vlen1024 vsew8  lmul0.125-0.5 | P P    |
| vlen1024 vsew16 lmul1         | P P    | vlen1024 vsew16 lmul2-8| P P    | vlen1024 vsew16 lmul0.125-0.5 | P P    |
| vlen1024 vsew32 lmul1         | P P    | vlen1024 vsew32 lmul2-8| P P    | vlen1024 vsew32 lmul0.125-0.5 | P P    |

### Floating Points

#### vfadd, vfclass, *vfcvt*, vfdiv, vfmacc, vfmax, vfmin, vfmsac, vfmsub, vfmul, `vfncvt`, vfnmacc, vfnmadd, vfnmsac, vfnmsub, vfrdiv, vfrec7, vfredmax, vfredmin

| Config                            | vfadd | vfclass | *vfcvt* | vfdiv | vfmacc | vfmadd | vfmax | vfmin | vfmsac | vfmsub | vfmul | `vfncvt` | vfnmacc | vfnmadd | vfnmsac | vfnmsub | vfrdiv | vfrec7 | vfredmax | vfredmin |
| -----------------------------     | ----- | ------ | --------- | ----- | ------ | ------ | ----- | ----- | ------ | ------ | ----- | ---------- | ------- | ------- | ------- | ------- | ------ | ------ | -------- | -------- |
| vlen128 vsew32 lmul1(default)     | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen128 vsew64 lmul1              | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen256 vsew32 lmul1              | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen256 vsew64 lmul1              | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen512 vsew32 lmul1              | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen512 vsew64 lmul1              | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen1024 vsew32 lmul1             | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen1024 vsew64 lmul1             | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| -----------------------------     | ----- | ------ | --------- | ----- | ------ | ------ | ----- | ----- | ------ | ------ | ----- | ---------- | ------- | ------- | ------- | ------- | ------ | ------ | -------- | -------- |
| vlen128-1024 vsew32 lmul2-8       | P     | P      | -         | P     | P      | P      | P     | P     | P      | P      | P     | -          | P       | P       | P       | P       | P      | P      | P        | P        |
| vlen128-1024 vsew64 lmul2-8       | P     | P      | -         | P     | P      | P      | P     | P     | P      | P      | P     | -          | P       | P       | P       | P       | P      | P      | P        | P        |
| -----------------------------     | ----- | ------ | --------- | ----- | ------ | ------ | ----- | ----- | ------ | ------ | ----- | ---------- | ------- | ------- | ------- | ------- | ------ | ------ | -------- | -------- |
| vlen128-1024 vsew32 lmul0.125-0.5 | P     | P      | -         | P     | P      | P      | P     | P     | P      | P      | P     | -          | P       | P       | P       | P       | P      | P      | P        | P        |
| vlen128-1024 vsew64 lmul0.125-0.5 | P     | P      | -         | P     | P      | P      | P     | P     | P      | P      | P     | -          | P       | P       | P       | P       | P      | P      | P        | P        |
| -----------------------------     | ----- | ------ | --------- | ----- | ------ | ------ | ----- | ----- | ------ | ------ | ----- | ---------- | ------- | ------- | ------- | ------- | ------ | ------ | -------- | -------- |
| vlen1024-4096 vsew32 lmul0.125-8  | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |
| vlen1024-4096 vsew64 lmul0.125-8  | P P   | P P    | -         | P P   | P P    | P P    | P P   | P P   | P P    | P P    | P P   | -          | P P     | P P     | P P     | P P     | P P    | P P    | P P      | P P      |

> vfcvt, vfcvt.x.f.v, vfcvt.rtz.xu.f.v, etc. not support in Spike.

#### vfredosum, vfredusum, vfrsqrt7, vfrsub, vfsgnj, vfsgnjn, vfsgnjx, vfsqrt, vfsub

| Config                            | vfredosum | vfredusum | vfrsqrt7 | vfrsub | vfsgnj | vfsgnjn | vfsgnjx | vfsqrt | vfsub |
| -----------------------------     | --------- | --------- | -------- | ------ | ------ | ------- | ------- | ------ | ----- |
| vlen128 vsew32 lmul1(default)     | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen128 vsew64 lmul1              | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen256 vsew32 lmul1              | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen256 vsew64 lmul1              | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen512 vsew32 lmul1              | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen512 vsew64 lmul1              | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen1024 vsew32 lmul1             | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen1024 vsew64 lmul1             | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| -----------------------------     | --------- | --------- | -------- | ------ | ------ | ------- | ------- | ------ | ----- |
| vlen128-1024 vsew32 lmul2-8       | P         | P         | P        | P      | P      | P       | P       | P      | P     |
| vlen128-1024 vsew64 lmul2-8       | P         | P         | P        | P      | P      | P       | P       | P      | P     |
| -----------------------------     | --------- | --------- | -------- | ------ | ------ | ------- | ------- | ------ | ----- |
| vlen1024-4096 vsew32 lmul0.125-8  | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |
| vlen1024-4096 vsew64 lmul0.125-8  | P P       | P P       | P P      | P P    | P P    | P P     | P P     | P P    | P P   |

#### vfwadd, vfwcvt, vfwmacc, vfwmsac, vfwmul, vfwnmacc, vfwnmsac, vfwredsum, vfwsub

| Config                        | vfwadd | vfwcvt | vfwmacc | vfwmsac | vfwmul | vfwnmacc | vfwnmsac | vfwredsum | vfwsub |
| ----------------------------- | ------ | ------ | ------- | ------- | ------ | -------- | -------- | --------- | ------ |
| vlen128 vsew16 lmul1          | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen128 vsew32 lmul1(default) | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen256 vsew16 lmul1          | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen256 vsew32 lmul1          | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen512 vsew16 lmul1          | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen512 vsew32 lmul1          | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen1024 vsew16 lmul1         | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen1024 vsew32 lmul1         | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| ----------------------------- | ------ | ------ | ------- | ------- | ------ | -------- | -------- | --------- | ------ |
| vlen128 vsew16  lmul2-8       | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen128 vsew32  lmul2-8       | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen256 vsew16  lmul2-8       | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen256 vsew32  lmul2-8       | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen512 vsew16  lmul2-8       | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen512 vsew32  lmul2-8       | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen1024 vsew16 lmul2-8       | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen1024 vsew32 lmul2-8       | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| ----------------------------- | ------ | ------ | ------- | ------- | ------ | -------- | -------- | --------- | ------ |
| vlen128 vsew16  lmul0.125-0.5 | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen128 vsew32  lmul0.125-0.5 | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen256 vsew16  lmul0.125-0.5 | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen256 vsew32  lmul0.125-0.5 | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen512 vsew16  lmul0.125-0.5 | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen512 vsew32  lmul0.125-0.5 | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
| vlen1024 vsew16 lmul0.125-0.5 | /      | /      | /       | /       | /      | /        | /        | /         | /      |
| vlen1024 vsew32 lmul0.125-0.5 | P P    | P P    | P P     | P P     | P P    | P P      | P P      | P P       | P P    |
note:

- we do not have 16-bit floating point dataset
- VFWiden instructions require lmul <= 4

### Fix Points

|                                   | vaadd | vaaddu | vasub | vasubu | vnclip | vnclipu | vsmul | vssra | vssrl |
| -----------------------------     | ----- | ------ | ----- | ------ | ------ | ------- | ----- | ----- | ----- |
| vlen128 vsew8 lmul1               | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128 vsew16 lmul1              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128 vsew32 lmul1(default)     | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128 vsew64 lmul1              | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| vlen256 vsew8 lmul1               | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen256 vsew16 lmul1              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen256 vsew32 lmul1              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen256 vsew64 lmul1              | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| vlen512 vsew8 lmul1               | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen512 vsew16 lmul1              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen512 vsew32 lmul1              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen512 vsew64 lmul1              | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| vlen1024 vsew8 lmul1              | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen1024 vsew16 lmul1             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen1024 vsew32 lmul1             | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen1024 vsew64 lmul1             | P P   | P P    | P P   | P P    | /      | /       | P P   | P P   | P P   |
| -----------------------------     | ----- | ------ | ----- | ------ | ------ | ------- | ----- | ----- | ----- |
| vlen128-1024 vsew8  lmul2-8       | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128-1024 vsew16 lmul2-8       | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128-1024 vsew32 lmul2-8       | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128-1024 vsew64 lmul2-8       | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| -----------------------------     | ----- | ------ | ----- | ------ | ------ | ------- | ----- | ----- | ----- |
| vlen128-1024 vsew8  lmul0.125-0.5 | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128-1024 vsew16 lmul0.125-0.5 | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128-1024 vsew32 lmul0.125-0.5 | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |
| vlen128-1024 vsew64 lmul0.125-0.5 | P P   | P P    | P P   | P P    | P P    | P P     | P P   | P P   | P P   |

*vnclip and vnclipu not support vsew=64 and lmul=8

### LOAD

- Unable to pass the lmul==8 parameter test： vlsege32 vlssege32 vluxsegei8 vluxsegei16 vluxsegei32
- If the EMUL would be out of range (EMUL>8 or EMUL<1/8), the instruction encoding is reserved. Use `/` to represent.
- `except <eew>` means this configuration not satisfy `vemul >= 0.125 && vemul <= 8` or `vsew <= elen * lmul`

|                                   | vle8/16/32/64 | vlre8/16/32 | vlse8/16/32/64 | vls(s)ege8/16/32 | vluxei8/16/32 | vluxeiseg8/16/32 | note                                |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- | ----                                |
| vlen128-1024 vsew8 lmul1          | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul1         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul1(default)| P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul1         | P P           | P P         | P P            | P P              | P P           | P P              |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul0.125     | P P           | P P         | P P            | P P              | P P           | P P              | vle, vlse, vls(s)ege, vlre except32; vle, vlse except 64;
| vlen128-1024 vsew16 lmul0.125     | P P           | P P         | P P            | P P              | P P           | P P              | vle, vlse, vls(s)ege, vlre except32; vle, vlse except 64; vluxseg except 8
| vlen128-1024 vsew32 lmul0.125     | /             | /           | /              | /                | /             | /                |
| vlen128-1024 vsew64 lmul0.125     | /             | /           | /              | /                | /             | /                |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul0.25      | P P           | P P         | P P            | P P              | P P           | P P              | vle,vlse except 64
| vlen128-1024 vsew16 lmul0.25      | P P           | P P         | P P            | P P              | P P           | P P              | vle,vlse except 64
| vlen128-1024 vsew32 lmul0.25      | P P           | P P         | P P            | P P              | P P           | P P              | vle,vlse except 64; vluxseg except 8
| vlen128-1024 vsew64 lmul0.25      | /             | /           | /              | /                | /             | /                |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              | vluxseg except 8
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| vlen128-1024 vsew16 lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| vlen128-1024 vsew32 lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| vlen128-1024 vsew64 lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul8         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul8         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul8         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul8         | P P           | P P         | P P            | P P              | P P           | P P              |
### Store

|                                   | vse8/16/32/64 | vs1/2/4/8r  | vsse8/16/32    | vss(s)ege8/16/32 | vsuxei8/16/32 | vsuxeiseg8/16/32 | note     |
| ------------------------------    | ------------- | ----------  | -----------    | ---------------- | ------------- | ---------------- | -----    |
| vlen128-1024 vsew8 lmul1          | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul1         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul1(default)| P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul1         | P P           | P P         | P P            | P P              | P P           | P P              |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul0.125     | P P           | /           | P P            | P P              | P P           | P P              | vse, vss(s)ege except32;
| vlen128-1024 vsew16 lmul0.125     | P P           | /           | P P            | P P              | P P           | P P              | vse, vss(s)ege except32;
| vlen128-1024 vsew32 lmul0.125     | /             | /           | /              | /                | /             | /                |
| vlen128-1024 vsew64 lmul0.125     | /             | /           | /              | /                | /             | /                |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul0.25      | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul0.25      | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul0.25      | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul0.25      | /             | /           | /              | /                | /             | /                | 
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul0.5       | P P           | P P         | P P            | P P              | P P           | P P              |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| vlen128-1024 vsew16 lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| vlen128-1024 vsew32 lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| vlen128-1024 vsew64 lmul2         | P P           | P P         | P P            | P P              | P P           | x                |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul4         | P P           | P P         | P P            | P P              | P P           | P P              |
| -----------------------------     | ------------- | ----------- | -----------    | ---------------- | ------------- | ---------------- |
| vlen128-1024 vsew8  lmul8         | P P           | x           | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew16 lmul8         | P P           | x           | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew32 lmul8         | P P           | x           | P P            | P P              | P P           | P P              |
| vlen128-1024 vsew64 lmul8         | P P           | x           | P P            | P P              | P P           | P P              |

## Code Explain

### Register Alignment

- For example,  `require_noover(insn.rd(), rd_lmul, insn.rs1(), rs1_lmul)` require rs1 and rd will not overwrite each other
  - no overlap condition is **either** rightest rs1 is smaller than rd **or** rightest rd is smaller than rs1
  - `((rs1 + rs1_lmul - 1 < rd) or (rd + rd_lmul - 1 < rs1))`
  - There are many conditions like this in generating macros for different registers.

### Fill Empty Tests
```python
def print_ending(f):
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
    \n\
    TEST_VV_OP(32766, vadd.vv, 2, 1, 1)\n\
    TEST_PASSFAIL\n\
    #endif\n\
```
- The `TEST_VV_OP(32766, vadd.vv, 2, 1, 1)` is in order to fill those tests that don't have tests(For example, when emul > 8, load/store will not have tests) with one vadd test.

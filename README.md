# RISC-V Vector Automatic Tests Generator

## Prerequisite

1. RVV Compiler
   1. Set `gcc`,`objdump`, and `riscof` directory's path variables in file: `scripts/constants.py`

2. Spike
   1. Install Latest [https://github.com/riscv-software-src/riscv-isa-sim](https://github.com/riscv-software-src/riscv-isa-sim).
   2. Add `<spike_path>/build` to your PATH
   
   If the terminal can find `spike` command then it's successful

3. RISCV-ISAC RVV Support (ONLY if you need use `riscof coverage` command)
   1. `git clone https://github.com/hushenwei2000/riscv-isac-rvv`
   2. `cd riscv-isac-rvv`
   3. `git checkout vetcor`  # IMPORTANT!!!
   4. `pip install . --prefix=~/.local`  # Anywhere you want  
   5. Add `~/.local` to your PATH   
   
   If the terminal can find `riscv_isac` command then it's successful

4. Modify files in `riscof_files`
   1. Modify `riscof_files/env/test_macros_vector.h`, you can copy from `env/macros/vsewXX_lmulXX` and paste to the file
   2. Modify `riscof_files/config.ini`, write your path of RVV-ATG

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

### Generate All Tests

```
python generate_all.py
```

- This will use default parameter configuration to generate all integer instructions tests.
- **Modify `runcommand_<type>` function to run different parameter.**
- **Modyfy `main` function to run different type of instructions.**
- Test file will generate in `generate_all` folder.
- ⚠️ Because we still have bugs, those tests are not correct (i.e. **CAN'T** be used as test file) will generate `spike.log` in `generate_all` folder. You can see FAIL in the ending of these logs.

## Known Bugs
- Lack of vmerge tests
- Lack of load store eew=64 tests

## Support Configuration

| Parameter | Numbers                   | Current Support | Note                           |
| --------- | ------------------------- | --------------- | ------------------------------ |
| FLEN      | FP16, BF16, 32, 64        | 32, 64          |                                |
| vlen      | 128 ~ 2^16                | 128 ~ 1024      | Spike now support largest 4096 |
| vsew      | 8, 16, 32, 64             | All             |                                |
| lmul      | 1/8, 1/4, 1/2, 1, 2, 4, 8 | All             | lmul=8 except load/store， 1/8 except eew>=32 loadstore       |
| vta       | 0, 1                      | 0               |                                |
| vma       | 0, 1                      | 0               |                                |

### Notice of Failure Tests

- **elen = 64 for default**
  - vsew should <= elen * lmul
  - So, when lmul = 0.125, load/store eew=32+ cannot test. 

- If there are failure tests, most probably is because that configuration can not be tested on that instruction. For example test widen instruction when vsew=64, or test floating point when vsew=8/16, or the elen related restriction above.

## Current Support

- Integer Type: 
   - vsew32: lmul1, 2, 4, 8
- Floating-Point Type: 
   - vsew32: lmul1, 2, 4, 8
- Fix-Point Type: 
   - vsew32: lmul1, 2, 4, 8
- Mask Type: 
   - vsew32: lmul1, 2, 4, 8
- Permute Type: 
   - vsew32: lmul1, 2, 4, 8
- Load Store Type: 
   - vsew32: lmul1, 2, 4, 8

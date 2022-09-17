# RISC-V Vector Autometic Tests Generator
## Usage
```
python run.py -i <instruction> -t <type>
```
- The type shall be consistent with the instruction: i (integer), f (floating point), m (mask), p (permute), x (fix point), l (load store)

## Develop
### Add a instruction
1. Give a `instr` such as `vadd`, this will include `vadd.vv/x/i` tests. If it is difficult to gather them, it can also be separated.  

2. Put a yaml formatted CGF to `cgfs/<type>/` directory. The name should be `<instr>.yaml` .  

3. Add a file to `scripts/create_test_<type>/<instr>.yaml` (can copy `vadd` first).   
  You should mainly modify `generate_macros` and `generate_tests`.  
  There are two functions:
    1. `create_empty_test_vadd`: create test which only contains one test, this file is used to generate coverage report.  
    2. `create_first_test_vadd`: create test which has all operands from coverage report, but the expected answers are wrong. Used to run sail model to generate true results.  

4. Add `import` info in `scripts/lib.py`.  
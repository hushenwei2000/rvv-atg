# RISC-V Vector Autometic Tests Generator

## Usage

```
python run.py -i <instruction> -t <type> [--vlen VLEN] [--vsew VSEW]
```

- The type shall be consistent with the instruction: i (integer), f (floating point), m (mask), p (permute), x (fix point), l (load store)
  -  Supported instruction and type can be seen in `cgfs/<type>/<instrction>.yaml`
- vlen VLEN       Vector Register Length: 32, 64, 128(default), 256, 512, 1024
- vsew VSEW       Selected Element Width: 8, 16, 32(default), 64



## Support Configuration

**Currently Support**  
vlen: 128, 256, 512, 1024  
elen: = vlen   
vsew: 8, 16, 32, 64  
   
**Future support**  
lmul: 1/8, 1/4, 1/2, 1(currently), 2, 4, 8  
vta: 0(currently), 1  
vma: 0(currently), 1  

## Develop

### Add a instruction

1. Give a `instr` such as `vadd`, this will include `vadd.vv/x/i` tests. If it is difficult to gather them, it can also be separated.
2. Put a yaml formatted CGF to `cgfs/<type>/` directory. The name should be `<instr>.yaml` .
3. Add a file to `scripts/create_test_<type>/<instr>.yaml` (can copy `vadd` first).You should mainly modify `generate_macros` and `generate_tests`.There are two functions:

3. Add a file to `scripts/create_test_<type>/<instr>.yaml` (can copy `vadd` first).   
  You should mainly modify `generate_macros` and `generate_tests`.  
  There are two functions:
    1. `create_empty_test_vadd`: create test which only contains one test, this file is used to generate coverage report.  
    2. `create_first_test_vadd`: create test which has all operands from coverage report, but the expected answers are wrong. Used to run sail model to generate true results.  

4. Add `import` info in `scripts/lib.py`.  

## CheckList
- "-"   : Not test/support yet
- "P"   : Test file is correct(pass Spike), but not fully cover val_comb
- "P P" : Test file is correct and fully cover val_comb (rd, rs may not fully cover)
  - *Now cover over 99% coverage points is regarded as pass, remaining need fine tune
- Not listed instruction are not tested yet
### Mask 
#### vmand, vmandnot, vmnand, vmor, vmornot, vmxnor, vmxor; vmsbf; vpopc, vfirst; vid, viota
|  Config   | Status  |
|  ----  | ----  |
| vlen128 vsew8 lmul1            | -     |
| vlen128 vsew16 lmul1           | P    |
| vlen128 vsew32 lmul1(default)  | P P    |
| vlen128 vsew64 lmul1           | P     |
| vlen256 vsew8 lmul1            | -   |
| vlen256 vsew16 lmul1           | P    |
| vlen256 vsew32 lmul1           | P P    |
| vlen256 vsew64 lmul1           | P    |
| vlen512 vsew8 lmul1            | -    |
| vlen512 vsew16 lmul1           | P     |
| vlen512 vsew32 lmul1           | P     |
| vlen512 vsew64 lmul1           | P    |
| vlen1024 vsew8 lmul1           | -    |
| vlen1024 vsew16 lmul1          | P    |
| vlen1024 vsew32 lmul1          | P    |
| vlen1024 vsew64 lmul1          | P    |

### Permute 

#### vcompress, vmre, vmv, vrgather, vrgatherei16, vslide, vslide1, vfslide
|  Config   | Status  |
|  ----  | ----  |
| vlen128 vsew8 lmul1            | -      |
| vlen128 vsew16 lmul1           | P      |
| vlen128 vsew32 lmul1(default)  | P      |
| vlen128 vsew64 lmul1           | -      |
| vlen256 vsew8 lmul1            | -     |
| vlen256 vsew16 lmul1           | -      |
| vlen256 vsew32 lmul1           | -      |
| vlen256 vsew64 lmul1           | -      |
| vlen512 vsew8 lmul1            | -      |
| vlen512 vsew16 lmul1           | -      |
| vlen512 vsew32 lmul1           | P      |
| vlen512 vsew64 lmul1           | -     |
| vlen1024 vsew8 lmul1           | -      |
| vlen1024 vsew16 lmul1          | P     |
| vlen1024 vsew32 lmul1          | -     |
| vlen1024 vsew64 lmul1          | -     |

### Integer

#### vadc, vadd, vand, vdiv, vdivu, vmacc, vmadc, vmadd, vmax, vmaxu, vmin, vminu, vmsbc, vmseq, vmsgt, vmsgtu, vmsle, vmsleu, vmslt, vmsltu, vmsne, vmul, vmulh, vmulhsu, vmulhu

|  Config   | Status  |
|  ----  | ----  |
|vlen128 vsew8 lmul1           | - |   
|vlen128 vsew16 lmul1          | - |  
|vlen128 vsew32 lmul1(default) | P P |  
|vlen128 vsew64 lmul1          | P P |   
|vlen256 vsew8 lmul1           | - | 
|vlen256 vsew16 lmul1          | P |  
|vlen256 vsew32 lmul1          | P P |  
|vlen256 vsew64 lmul1          | P P |  
|vlen512 vsew8 lmul1           | - |  
|vlen512 vsew16 lmul1          | P |   
|vlen512 vsew32 lmul1          | P P |   
|vlen512 vsew64 lmul1          | P P | 
|vlen1024 vsew8 lmul1          | - |  
|vlen1024 vsew16 lmul1         | P | 
|vlen1024 vsew32 lmul1         | P P | 
|vlen1024 vsew64 lmul1         | P P | 

Bugs: 
- vadd lack vx and vi

#### vnmsac, vnmsub; vnsra, vnsrl; vor; vredand, vredmax, vredmaxu, vredmin, vredminu, vredor, vredsum, vredxor; vrem, vremu; vrsub; vsadd, vsaddu, vsbc 

|  Config   | Status  |
|  ----  | ----  |
|vlen128 vsew8 lmul1           | - |   
|vlen128 vsew16 lmul1          | - |  
|vlen128 vsew32 lmul1(default) | P P |  
|vlen128 vsew64 lmul1          | P P |   
|vlen256 vsew8 lmul1           | - | 
|vlen256 vsew16 lmul1          | - |  
|vlen256 vsew32 lmul1          | P P |  
|vlen256 vsew64 lmul1          | - |  
|vlen512 vsew8 lmul1           | - |  
|vlen512 vsew16 lmul1          | P |   
|vlen512 vsew32 lmul1          | P P |   
|vlen512 vsew64 lmul1          | - | 
|vlen1024 vsew8 lmul1          | - |  
|vlen1024 vsew16 lmul1         | P | 
|vlen1024 vsew32 lmul1         | P P| 
|vlen1024 vsew64 lmul1         | P P | 

Bugs:
- vnsra/l. vlen 128 vsew=64 fail


#### vsll, vsra, vsrl; vssub, vssubu; vsub; vwadd, vwaddu, vwmacc, vwmaccsu, vwmaccu, vwmaccus; vwmul, vwmulsu, vwmulu, vwredsum, vwredsumu, vwsub, vwsubu; vxor

### Floating Points
#### vfadd, vfclas, *vfcvt*, vfdiv, vfmacc, vfmax, vfmin, vfmsac, vfmsub, vfmul, `vfncvt`, vfnmacc, vfnmadd, vfnmsac, vfnmsub, vfrdiv, vfrec7, vfredmax, vfredmin
|  Config   | vfadd | vfclas | *vfcvt* | vfdiv | vfmacc | vfmax | vfmin | vfmsac | vfmsub | vfmul | `vfncvt` | vfnmacc | vfnmadd | vfnmsac | vfnmsub | vfrdiv | vfrec7 | vfredmax | vfredmin |
|  ----  | ----  | ----  |  ----  |  ----  |  ----  |  ----  |  ----  |  ----  | ----  | ----  |  ----  |  ----  |  ----  |  ----  |  ----  |  ----  |  ----  |  ----  |  ----  |
|vlen128 vsew32 lmul1(default) | P P | P P |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|vlen128 vsew64 lmul1          | x x | P P |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|vlen256 vsew32 lmul1          | P P | P P |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|vlen256 vsew64 lmul1          | x x |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|vlen512 vsew32 lmul1          | P P |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|vlen512 vsew64 lmul1          | x x |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|vlen1024 vsew32 lmul1         | P P |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|vlen1024 vsew64 lmul1         | x x |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |


### Fix Points
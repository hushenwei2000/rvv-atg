vsew32 lmul8: pass
vsew32 lmul4 vta1 vma1: pass
vsew32 lmul1 maskFalse: pass
vsew32 lmul0.5: pass

vsew64 lmul8: pass
vsew64 lmul4 vta1 vma1: pass
vsew64 lmul2 maskFalse: pass
vsew64 lmul1: pass

vsew16 lmul8: pass
vsew16 lmul4 vta1 vma1: pass
vsew16 lmul0.5 maskFalse: pass
vsew16 lmul0.25: pass

vsew8 lmul8: pass
vsew8 lmul4 maskFalse: pass
vsew8 lmul0.5 vta1 vma1: pass
vsew8 lmul0.125: pass

# Known Bug

1. When `--masked=False` -- fixed on 12.19
```
Generated file is WRONG or not exist!! Will be removed : 12-18-vfwmacc-vlen128-vsew32-lmul1.0
Generated file is WRONG or not exist!! Will be removed : 12-18-vfwmsac-vlen128-vsew32-lmul1.0
Generated file is WRONG or not exist!! Will be removed : 12-18-vfwnmacc-vlen128-vsew32-lmul1.0
Generated file is WRONG or not exist!! Will be removed : 12-18-vsuxsegei16-vlen128-vsew64-lmul2.0
Generated file is WRONG or not exist!! Will be removed : 12-18-vsuxsegei32-vlen128-vsew64-lmul2.0
Generated file is WRONG or not exist!! Will be removed : 12-18-vsuxsegei8-vlen128-vsew64-lmul2.0
```
# Usage

combination test for instruction dependency, including WAR, WAW and RAW hazard

- generate one test for a particular configuration:

```
python3 run.py  -t c [--vlen VLEN] [--vsew VSEW] [--lmul LMUL]
```

- test all legal combinations of vsew & lmul for specific xlen & vlen & elen:

```
python3 run.py  -t ca
```

**note: in this case, the "-i" will be ignored**

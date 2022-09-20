# python run.py -i vfadd -t f; # pass
# python run.py -i vfclass -t f; # pass
# python run.py -i vfcvt -t f; # failed, unrecognized opcode `vfcvt.x.f.v v14,v1'
# python run.py -i vfdiv -t f; # pass
# python run.py -i vfrdiv -t f; # pass
# python run.py -i vfmacc -t f; # pass
# python run.py -i vfmadd -t f; # pass
# python run.py -i vfmax -t f; # pass
# python run.py -i vfmerge -t f; # TODO
# python run.py -i vfmin -t f; # pass
# python run.py -i vfmsac -t f; # pass
# python run.py -i vfmsub -t f; # pass
# python run.py -i vfmul -t f; # pass
# python run.py -i vfncvt -t f; # failed, unrecognized opcode `vfncvt.x.f.v v14,v29'
# python run.py -i vfnmacc -t f; # pass
# python run.py -i vfnmadd -t f; # pass
# python run.py -i vfnmsac -t f; # pass
# python run.py -i vfnmsub -t f; # pass
python run.py -i vfrec7 -t f; # failed, the 1st instrution
# python run.py -i vfredmax -t f; # pass
# python run.py -i vfredmin -t f; # pass
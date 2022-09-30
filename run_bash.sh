if [[ -z $1 ]];
then
        echo "Please pass instrution type as a parameter!\n"
        echo "Example: bash run_bash.sh vfadd \n"
        echo "Or example: bash run_bash.sh vfclass \n"
else
        python run.py -i $1 -t f --vlen 128 --vsew 32; 
        python run.py -i $1 -t f --vlen 128 --vsew 64; 
        python run.py -i $1 -t f --vlen 256 --vsew 32; 
        python run.py -i $1 -t f --vlen 256 --vsew 64; 
        python run.py -i $1 -t f --vlen 512 --vsew 32; 
        python run.py -i $1 -t f --vlen 512 --vsew 64; 
        python run.py -i $1 -t f --vlen 1024 --vsew 32; 
        python run.py -i $1 -t f --vlen 1024 --vsew 64; 
fi
# python run.py -i vfclass -t f; # pass
# python run.py -i vfcvt -t f; # failed, illegal operands `vfcvt.rtz.x.f.v v2 v1'
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
# python run.py -i vfncvt -t f; # failed, junk at end of line, first unrecognized character is `F'
# python run.py -i vfnmacc -t f; # pass
# python run.py -i vfnmadd -t f; # pass
# python run.py -i vfnmsac -t f; # pass
# python run.py -i vfnmsub -t f; # pass
# python run.py -i vfrec7 -t f; # pass
# python run.py -i vfredmax -t f; # pass
# python run.py -i vfredmin -t f; # pass
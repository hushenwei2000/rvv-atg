#!/bin/bash

# following is another way to find directory, according to modified time, which could lead problems when run this scripts in multie terminals
# find . -type d -mmin 0

# $1 is the instructuion name
# $2 is vsew
# $3 is vlen
# $4 is the instruction type

# $root_path is for environment configuration
root_path=$(pwd)                                

# following variables can be easily understood by name
ins_name=$1
vsew=$2
vlen=$3
ele_num=$(($vlen/$vsew))
cd ..

# to create a folder to save intermediate results 
if [ ! -d $root_path/outputs/ ]; then        
    mkdir -p $root_path/outputs 
fi

# excute testing command and cd to target directory
date=`date +"%m-%d"`
rm $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
python3 run.py -i $ins_name -t $4 --vsew $vsew --vlen $vlen --agnostic 1 --vma 1            #! run.py need to change
dir_path=`find . -name $date-$ins_name-vlen$3-vsew$2* `
find . -name $date-$ins_name-vlen$3-vsew$2*
if [ $? -ne 0 ]; then
    echo finding directory error!!!
fi
cd $dir_path
log_path=`find . -name spike_$ins_name\_final.log`

# to get mask data
mask_data_orign=(`grep "e$vsew m1 l$ele_num v0" $log_path | grep -v "0: 3"`)
mask_data=${mask_data_orign[9]} #0x20219a51429ede3d86569d2711111111
echo -e "$mask_data" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt

# target row is the row under the target instructions, which displays the spike results of destination register  
mapfile -t array_spk < <(grep -n "$ins_name" $log_path | awk -F: '{print $1}' )
targ_row=$((array_spk[0]+1))

# for destination register, rd2 is uesd when verifying widden instruction
rd_num=$(grep -o -E "$ins_name(\.[a-z]*)*\s+([a-z]*[0-9]*)" $log_path | awk '{print $2}')       
rd_pure_num=$(echo $rd_num | grep -o "[0-9]\+")
rd2_pure_num=$(expr 1 + $rd_pure_num)
rd2_num=$(echo $rd_num | sed "s/[0-9]\+/$rd2_pure_num/g")

# to get original value, in case when rd registers don't change, often occurs when testing widen instructions
mapfile -t array_orign < <(grep -n "e$vsew m1 l$ele_num $rd_num" $log_path | awk -F: '{print $3}' )           
rd_data_orign_1=$(echo $array_orign | grep -o  "$rd_num.*" | awk '{print $2}' )
rd_data_orign_2=$(echo $array_orign | grep -o  "$rd2_num.*" | awk '{print $2}' )


# for vw instructions to get mask data, spike results and modified results and send to python script to check out results
if [[ ${ins_name:0:2} = "vw" ]];then
    #the combination of head and tail displays the target row content
    rd_data_spike_1=$(head -$targ_row $log_path | tail -1 | grep -o  "$rd_num.*" | awk '{print $2}')
    rd_data_spike_2=$(head -$targ_row $log_path | tail -1 | grep -o  "$rd_num.*" | awk '{print $4}')
    # for special situation when rds don't change
    if [[ $rd_data_spike_2 = ""  ]]; then
        rd_data_spike_2=$rd_data_orign_2
    elif [[ $rd_data_spike_2 = "" ]]; then
        rd_data_spike_1=$rd_data_orign_1
    fi
    mapfile -t array_chg1 < <(grep -n "e$vsew m1 l$ele_num v8" $log_path | grep -v "0: 3" | awk -F: '{print $3}' )  
    change1_temp=(${array_chg1[1]})                                       
    rd_data_change1_1=${change1_temp[7]}
    rd_data_change1_2=${change1_temp[9]}
    echo -e "mask data\t=\t$mask_data"
    echo -e "spike results\t=\t$rd_data_spike_1\t$rd_data_spike_2"
    echo -e "modified results=\t$rd_data_change1_1\t$rd_data_change1_2"
    echo -e "$rd_data_spike_1" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
    echo -e "$rd_data_spike_2" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
    echo -e "$rd_data_change1_1" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
    echo -e "$rd_data_change1_2" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt

# for vfw instructions to get mask data, spike results and modified results and send to python script to check out results
elif [[ ${ins_name:0:3} = "vfw" ]]; then
    rd_data_spike_1=$(head -$targ_row $log_path | tail -1 | grep -o  "$rd_num.*" | awk '{print $2}')
    rd_data_spike_2=$(head -$targ_row $log_path | tail -1 | grep -o  "$rd_num.*" | awk '{print $4}')
    if [[ $rd_data_spike_2 = ""  ]]; then
        rd_data_spike_2=$rd_data_orign_2
    elif [[ $rd_data_spike_2 = "" ]]; then      
        rd_data_spike_1=$rd_data_orign_1
    fi
    mapfile -t array_chg1 < <(grep -n "e$vsew m1 l$ele_num v8" $log_path | grep -v "0: 3" | awk -F: '{print $3}' )
    change1_temp=(${array_chg1[1]})
    rd_data_change1_1=${change1_temp[7]}
    rd_data_change1_2=${change1_temp[9]}
    echo -e "mask data\t=\t$mask_data"
    echo -e "spike results\t=\t$rd_data_spike_1\t$rd_data_spike_2"
    echo -e "modified results=\t$rd_data_change1_1\t$rd_data_change1_2"
    echo -e "$rd_data_spike_1" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
    echo -e "$rd_data_spike_2" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt9
    echo -e "$rd_data_change1_1" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
    echo -e "$rd_data_change1_2" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt

# for normal instructions to get mask data, spike results and modified result sand send to python script to check out results
else                                
    rd_data_spike=$(head -$targ_row $log_path | tail -1 | grep -o  "$rd_num.*" | awk '{print $2}')  
    # for vfslide vslide vslide1, the real instruction name isn't these names, so use position to get the results
    if [[ $ins_name = "vfslide" ]] || [[ $ins_name = "vslide" ]] || [[ $ins_name = "vslide1" ]]; then
        rd_data_spike=$(head -$targ_row $log_path | tail -1 | awk '{print $12}')
    fi
    mapfile -t array_chg1 < <(grep -n "e$vsew m1 l$ele_num v8" $log_path | grep -v "0: 3" | awk -F: '{print $3}' )
    change1_temp=(${array_chg1[1]})
    rd_data_change1=${change1_temp[7]}
    echo -e "mask data\t=\t$mask_data"
    echo -e "spike results\t=\t$rd_data_spike"
    echo -e "modified results=\t$rd_data_change1"
    echo -e "$rd_data_spike" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
    echo -e "$rd_data_change1" >> $root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
fi

# excute python script
cd $root_path/
work_path=$root_path/outputs/$date-$ins_name-vlen$3-vsew$2.txt
python3 check_masked_results.py $ins_name $vsew $vlen $work_path
# INTRODUCTION
The folder, for_masked_elem_retain1 contains automation checking masked elements results, because spike doesn't support set masked elements to 1, so it's necessary to check modified results another way.

# USAGE
First, set the current working path to for_masked_elem_retain1  
`cd $PRJ_ROOT/rvv-atg/for_masked_elem_retain1`  
Then run `check_masked_results.sh` shell script,the first parameter is the `instructuion name`, the second is `vsew`, the third is `vlen`, the fourth is the `instruction type`. Following is an instance:  
`source check_masked_results.sh  vfwadd 32  128 f `  
The results will display as follows  
`mask data       =       0x20219a51429ede3d86569d2711111111`   
`spike results   =       0x67f9ab29fd2ce83ff682191afffffffc`    
`modified results=       0x000000010000000100000001fffffffc`  
If successfuly replaced, it will show  
`SUCCESS!! The results has been successfully replaced`  


# RANGE  
The following chart displays the availible and inavailible instructions of changing masked elements into 1. 
And the support instructions are stored in the folder named by instruction type, such as `f i m p x`

|                        | f                                               | i                                                                                                                                                   | l           | m                                                                                       | p                  | x                      |
| ---------------------- |:----------------------------------------------- |:---------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------:|:---------------------------------------------------------------------------------------:|:------------------:|:----------------------:|
| check results fail     | none                              | none                                                                                                                                  |             | vid results can't be checked by script                                                                            | none | none     |  under modifying
| **successful_replaced** but will be stuck in a loop | vfclass vfrec7 vfrsqrt7 vfsqrt vfwcvt           |                                                                                                                                                     |             |                                                                                         |                    |                        |
| rd is destination mask register(each bit represents an element)       | vfredmax vfredmin vfredosum vfredusum vfwredsum | vmadc vmsbc vmseq vmsgtu vmsgt vmsleu vmsle vmsltu vmslt vredand vmsne  vredmaxu vredmax vredminu vredmin vredor vredsum vredxor vwredsumu vwredsum |             | vfirst vmand vmandnot vmnand vmnor vmnxnor vmnxor vmor vmornot vmsbf vmxnor vmxor vpopc |                    |                        |
| vm field is 1(unmasked)       | vfmv                                            |                                                                                                                                                     | t |                                                                                         | vmv vmre vcompress |                        |
| special mask instructions                 | vfmerge                                         |                                                                                                                                                     |             |                                                                                         |                    |                        |
| not support in spike               | vfncvt和vfcvt                                    | vsew=64 vnsra vnsrl                                                                                                                                 |             |                                                                                         | vsew=8,16 vfslide  | vsew=64 vnclipu vnclip |





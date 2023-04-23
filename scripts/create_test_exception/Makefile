
TEST:=vs
TYPE:=misaligned_address
# illegal_instruction

$(shell mkdir -p build)

run:compile objdump run-spike

compile:
	/work/home/jjliu/riscv-gnu-toolchain/installed-tools/bin/riscv64-unknown-elf-gcc -march=rv64gv  -g   -w   \
	-static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles        \
	-T /work/home/jjliu/rvv-atg/env/p/link.ld         \
	-I /work/home/jjliu/rvv-atg/env/macros/vsew32_lmul1_nofail         \
	-I /work/home/jjliu/rvv-atg/scripts/create_test_exception/p         \
	-I /work/home/jjliu/rvv-atg/env         \
	-I /work/home/jjliu/rvv-atg/env/sail_cSim -mabi=lp64  \
	./create_test_exception_$(TYPE)/exception_$(TEST).S -o ./build/ELF_$(TEST).elf -DTEST_CASE_1=True -DXLEN=64 -DFLEN=32;

objdump:
	/work/home/jjliu/riscv-gnu-toolchain/installed-tools/bin/riscv64-unknown-elf-objdump -D ./build/ELF_$(TEST).elf > ./build/dump_$(TEST).disass;

run-spike:
	spike --isa rv64ghv_zfh -l --log-commits -d  --varch=vlen:128,elen:128 ./build/ELF_$(TEST).elf > ./build/spike_$(TEST).log 


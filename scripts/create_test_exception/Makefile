
TEST:=vs
TYPE:=misaligned_address

GCC:=
OBJ:=
BUILD:=./build/
DEBUG:=0


$(shell mkdir -p $(BUILD))

run:compile objdump run-spike

compile:
	$(GCC) -march=rv64gv  -g   -w   \
	-static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles        \
	-T ./p/link.ld         \
	-I ../../env/macros/vsew32_lmul1_nofail         \
	-I ./p         \
	-I ../../env         \
	-I ../../env/sail_cSim -mabi=lp64  \
	./create_test_exception_$(TYPE)/exception_$(TEST).S -o $(BUILD)/ELF_$(TEST).elf -DTEST_CASE_1=True -DXLEN=64 -DFLEN=32;

objdump:
	$(OBJ) -D $(BUILD)/ELF_$(TEST).elf > $(BUILD)/dump_$(TEST).disass;


run-spike:
ifeq ($(DEBUG), 0)
	spike --isa rv64ghv_zfh -l --log-commits -d  --varch=vlen:128,elen:128 $(BUILD)/ELF_$(TEST).elf > $(BUILD)/spike_$(TEST).log
else
	spike --isa rv64ghv_zfh -l --log-commits -d  --varch=vlen:128,elen:128 $(BUILD)/ELF_$(TEST).elf > $(BUILD)/spike_$(TEST).log 2>&1
endif


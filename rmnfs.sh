#!/bin/bash
date="10-31*"
kill -9 `pgrep spike`
kill -9 `pgrep riscv_isac`
rm -rf $date
import os
rs1_val = ["0x00000000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000",
           "0x00800000", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", ]
rs2_val = ["0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000",
           "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", ]

rs1_val_64 = ['0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x0000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x8000000000000000', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x0000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001', '0x8000000000000001',
              '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x0000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF',
              '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x0010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x8010000000000000', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x0010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002', '0x8010000000000002',
              '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0x3FF0000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', '0xBF80000000000000', ]
rs2_val_64 = ['0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000',
              '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000',
              '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000',
              '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', '0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', ]


def valid_aligned_regs(reg):
    i = reg // 8
    if i == 0 or i == 3:
        return 8, 16
    elif i == 1:
        return 16, 24
    else:
        return 24, 8


def generate_macros(f, vsew, lmul, test_vv=True, test_vf=True, test_rv=False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FP_VV_OP \n\
#define TEST_FP_VV_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    print("#undef TEST_FP_VF_OP \n\
#define TEST_FP_VF_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,    \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7); "%vsew + " \\\n\
        la x7, val2; \\\n\
        fl%s f1, (x7); "%('d' if vsew == 64 else 'w') + " \\\n\
        inst v24, v8, f1%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    if test_vv:
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            rs2, rd = valid_aligned_regs(n)
            print("#define TEST_FP_VV_OP_1%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7); \\\n\
                %s "%(n, rd, vsew, rd, "la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7); \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7); \\\n\
                inst v%d, v%d, v%d%s; \\\n\
            )" % (vsew, rs2, vsew, n, rd, rs2, n, ", v0.t" if masked else ""), file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            rs1, rs2 = valid_aligned_regs(n)
            print("#define TEST_FP_VV_OP_rd%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7); \\\n\
                %s "%(n, n, vsew, n, "la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7); \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7); \\\n\
                inst v%d, v%d, v%d%s; \\\n\
            )" % (vsew, rs2, vsew, rs1, n, rs2, rs1, ", v0.t" if masked else ""), file=f)
    if test_vf:
        for n in range(1,32):
            if n == 2 or n % lmul != 0:
                continue
            print("#define TEST_FP_VF_OP_rs1_%d( testnum, inst, flags, result, val1, val2 )"%n + " \\\n\
                TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,   \\\n\
                    VSET_VSEW_4AVL \\\n\
                    la x7, rd_origin_data; \\\n\
                    vle%d.v v24, (x7);"%vsew + " \\\n\
                    %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                    la x7, val1; \\\n\
                    vle%d.v v8, (x7);"%(vsew) + " \\\n\
                    la x7, val2; \\\n\
                    fl%s f%d, (x7);"%(('d' if vsew == 64 else 'w'), n) + " \\\n\
                    inst v24, v8, f%d%s; "%(n, ", v0.t" if masked else "") + " \\\n\
                )", file=f)
        for n in range(1,32):
            if n == 1 or n % lmul != 0:
                continue
            print("#define TEST_FP_VF_OP_rd_%d( testnum, inst, flags, result, val1, val2 ) "%n + "\\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8, "%n + "    \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                la x7, val2; \\\n\
                fl%s f1, (x7);"%('d' if vsew == 64 else 'w') + " \\\n\
                inst v%d, v8, f1%s; "%(n, ", v0.t" if masked else "") +" \\\n\
            )", file=f)
    if test_rv:
        for n in range(1,32):
            if n ==14 or n % lmul != 0:
                continue
            print("#define TEST_FP_VF_OP_RV_rs1_%d( testnum, inst, flags, result, val1, val2 )"%n + " \\\n\
                TEST_CASE_FP( testnum, v24, flags, result, val1, val2,   \\\n\
                    fl%s f0, 0(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
                    fl%s f1, 4(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
                    vfmv.s.f v%d, f0; "%n + "\\\n\
                    fl%s f2, 8(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
                    inst v24, f1, v%d; "%n + " \\\n\
                )", file=f)
        for n in range(1,32):
            if n == 1 or n == 8 or n % lmul != 0:
                continue
            print("#define TEST_FP_VF_OP_RV_rd_%d( testnum, inst, flags, result, val1, val2 ) "%n + "\\\n\
                TEST_CASE_FP( testnum, v%d, flags, result, val1, val2, "%n + "    \\\n\
                    fl%s f0, 0(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
                    fl%s f1, 4(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
                    vfmv.s.f v8, f0; \\\n\
                    fl%s f2, 8(a0);"%('d' if vsew == 64 else 'w') + " \\\n\
                    inst v%d, f1, v8; "%n +" \\\n\
                )", file=f)

def generate_macros_v_op(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    lmul = 1 if lmul < 1 else int(lmul)
    print("#undef TEST_FP_V_OP \n\
#define TEST_FP_V_OP( testnum, inst, flags, result, val1 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_FP_V_OP_rs1_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v%d%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_FP_V_OP_rd_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                inst v%d, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)

def generate_macros_vfmacc(f, vsew, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FP_VV_FUSED_OP \n\
#define TEST_FP_VV_FUSED_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    print("#undef TEST_FP_VF_FUSED_OP_RV \n\
#define TEST_FP_VF_FUSED_OP_RV( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        fl%s f1, (x7);"%(('d' if vsew == 64 else 'w')) + " \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        inst v24, f1, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        rs2, rd = valid_aligned_regs(n)
        print("#define TEST_FP_VV_FUSED_OP_1%d( testnum, inst, flags, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8,"%rd + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, rs2) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, rd) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                inst v%d, v%d, v%d%s;"%(rd, rs2, n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_FP_VV_FUSED_OP_rd%d( testnum, inst, flags, result, val1, val2 ) "%n + "\\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8,"%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, rs2) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, rs1) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                inst v%d, v%d, v%d%s;"%(n, rs2, rs1, ", v0.t" if masked else "") + " \\\n\
        )", file=f)
    # vf
    for n in range(1,32):
        if n == 2 or n % lmul != 0:
            continue
        print("#define TEST_FP_VF_FUSED_OP_RV_rs1_%d( testnum, inst, flags, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,   \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                la x7, val2; \\\n\
                fl%s f%d, (x7);"%(('d' if vsew == 64 else 'w'), n) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%(vsew) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                inst v24, f%d, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file=f)
    for n in range(1,32):
        if n == 1 or n % lmul != 0:
            continue
        print("#define TEST_FP_VF_FUSED_OP_RV_rd_%d( testnum, inst, flags, result, val1, val2 ) "%n + "\\\n\
        TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8, "%n + "    \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%(vsew) + " \\\n\
            la x7, val2; \\\n\
            fl%s f1, (x7);"%('d' if vsew == 64 else 'w') + " \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            inst v%d, f1, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)

def generate_macros_vfwmacc(f, vsew, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FP_W_VV_FUSED_OP \n\
#define TEST_FP_W_VV_FUSED_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    print("#undef TEST_FP_W_VF_FUSED_OP_RV \n\
#define TEST_FP_W_VF_FUSED_OP_RV( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        fl%s f1, (x7);"%(('d' if vsew == 64 else 'w')) + " \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        inst v24, f1, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        rs2, rd = valid_aligned_regs(n)
        print("#define TEST_FP_W_VV_FUSED_OP_1%d( testnum, inst, flags, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_LOOP_W_FP( testnum, v%d, flags, result, v8,"%rd + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, rs2) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew*2, rd) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                inst v%d, v%d, v%d%s;"%(rd, rs2, n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_FP_W_VV_FUSED_OP_rd%d( testnum, inst, flags, result, val1, val2 ) "%n + "\\\n\
            TEST_CASE_LOOP_W_FP( testnum, v%d, flags, result, v8,"%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, rs2) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, rs1) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew*2, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                inst v%d, v%d, v%d%s;"%(n, rs2, rs1, ", v0.t" if masked else "") + " \\\n\
        )", file=f)
    # vf
    for n in range(1,32):
        if n == 2 or n % lmul != 0:
            continue
        print("#define TEST_FP_W_VF_FUSED_OP_RV_rs1_%d( testnum, inst, flags, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,   \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                la x7, val2; \\\n\
                fl%s f%d, (x7);"%(('d' if vsew == 64 else 'w'), n) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%(vsew*2) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                inst v24, f%d, v8%s;"%(n, ", v0.t" if masked else "") + " \\\n\
            )", file=f)
    for n in range(1,32):
        if n == 1 or n % lmul != 0:
            continue
        print("#define TEST_FP_W_VF_FUSED_OP_RV_rd_%d( testnum, inst, flags, result, val1, val2 ) "%n + "\\\n\
        TEST_CASE_LOOP_W_FP( testnum, v%d, flags, result, v8, "%n + "    \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%(vsew) + " \\\n\
            la x7, val2; \\\n\
            fl%s f1, (x7);"%('d' if vsew == 64 else 'w') + " \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew*2, n) + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            inst v%d, f1, v8%s;"%(n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)

def generate_macros_vfred(f, vsew, lmul, test_vv=True, test_vf=True, test_rv=False):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#define TEST_FPRED_VV_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
        TEST_CASE_FP( testnum, v24, flags, result, val1, val2,    \\\n\
            fl%s f0, 0(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
            fl%s f1, %d(a0); "%(('d' if vsew == 64 else 'w'), (8 if vsew == 64 else 4)) + "\\\n\
            vfmv.s.f v8, f0; \\\n\
            vfmv.s.f v16, f1; \\\n\
            fl%s f2, %d(a0); "%(('d' if vsew == 64 else 'w'), (16 if vsew == 64 else 8)) + "\\\n\
            inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    print("#define TEST_FPRED_VF_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
        TEST_CASE_FP( testnum, v24, flags, result, val1, val2,    \\\n\
            fl%s f0, 0(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
            fl%s f1, %d(a0); "%(('d' if vsew == 64 else 'w'), (8 if vsew == 64 else 4)) + "\\\n\
            vfmv.s.f v8, f0; \\\n\
            fl%s f2, %d(a0); "%(('d' if vsew == 64 else 'w'), (16 if vsew == 64 else 8)) + " \\\n\
            inst v24, v8, f1%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    # lmul = 1 if lmul < 1 else int(lmul)
    if test_vv:
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            rs2, rd = valid_aligned_regs(n)
            print("#define TEST_FPRED_VV_OP_1%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_FP( testnum, v%d, flags, result, val1, val2, \\\n\
                fl%s f0, 0(a0); \\\n\
                fl%s f1, %d(a0); \\\n\
                vfmv.s.f v%d, f0; \\\n\
                vfmv.s.f v%d, f1; \\\n\
                fl%s f2, %d(a0); \\\n\
                inst v%d, v%d, v%d%s; \\\n\
            )" % (n, rd, ('d' if vsew == 64 else 'w'), ('d' if vsew == 64 else 'w'), (8 if vsew == 64 else 4), rs2,  n, ('d' if vsew == 64 else 'w'), (16 if vsew == 64 else 8), rd, rs2, n, ", v0.t" if masked else ""), file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            rs1, rs2 = valid_aligned_regs(n)
            print("#define TEST_FPRED_VV_OP_rd%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_FP( testnum, v%d, flags, result, val1, val2, \\\n\
                fl%s f0, 0(a0); \\\n\
                fl%s f1, %d(a0); \\\n\
                vfmv.s.f v%d, f0; \\\n\
                vfmv.s.f v%d, f1; \\\n\
                fl%s f2, %d(a0); \\\n\
                inst v%d, v%d, v%d%s; \\\n\
            )" % (n,  n, ('d' if vsew == 64 else 'w'), ('d' if vsew == 64 else 'w'), (8 if vsew == 64 else 4), rs2, rs1, ('d' if vsew == 64 else 'w'), (16 if vsew == 64 else 8), n, rs2, rs1, ", v0.t" if masked else ""), file=f)
    if test_vf:
        for n in range(1,32):
            if n == 2 or n % lmul != 0:
                continue
            print("#define TEST_FPRED_VF_OP_rs1_%d( testnum, inst, flags, result, val1, val2 )"%n + " \\\n\
                TEST_CASE_FP( testnum, v24, flags, result, val1, val2,   \\\n\
                    fl%s f0, 0(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
                    fl%s f%d, %d(a0);"%(('d' if vsew == 64 else 'w'), (8 if vsew == 64 else 4)) + " \\\n\
                    vfmv.s.f v8, f0; \\\n\
                    fl%s f2, %d(a0); "%(('d' if vsew == 64 else 'w'), (16 if vsew == 64 else 8)) + "\\\n\
                    inst v24, v8, f%d%s; "%(n,n, ", v0.t" if masked else "") + " \\\n\
                )", file=f)
        for n in range(1,32):
            if n == 1 or n % lmul != 0:
                continue
            print("#define TEST_FPRED_VF_OP_rd_%d( testnum, inst, flags, result, val1, val2 ) "%n + "\\\n\
            TEST_CASE_FP( testnum, v%d, flags, result, val1, val2,     \\\n\
                fl%s f0, 0(a0); "%('d' if vsew == 64 else 'w') + "\\\n\
                fl%s f1, %d(a0); "%(('d' if vsew == 64 else 'w'), (8 if vsew == 64 else 4)) + "\\\n\
                vfmv.s.f v8, f0; \\\n\
                fl%s f2, %d(a0); "%(('d' if vsew == 64 else 'w'), (16 if vsew == 64 else 8)) + "\\\n\
                inst v%d, v8, f1%s; "%(n, ", v0.t" if masked else "") +" \\\n\
            )", file=f)

def generate_macros_widen(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#undef TEST_W_FP_VV_OP \n\
#define TEST_W_FP_VV_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    print("#undef TEST_W_FP_VF_OP \n\
#define TEST_W_FP_VF_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,    \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7); "%vsew + " \\\n\
        la x7, val2; \\\n\
        fl%s f1, (x7); "%('d' if vsew == 64 else 'w') + " \\\n\
        inst v24, v8, f1%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    print("#undef TEST_W_FP_WV_OP \n\
#define TEST_W_FP_WV_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    print("#undef TEST_W_FP_WF_OP \n\
#define TEST_W_FP_WF_OP( testnum, inst, flags, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,    \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7); "%(vsew*2 if vsew < 64 else 64) + " \\\n\
        la x7, val2; \\\n\
        fl%s f1, (x7); "%('d' if vsew == 64 else 'w') + " \\\n\
        inst v24, v8, f1%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    # lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        rs2, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_1%d( testnum, inst, flags, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP_W_FP( testnum, v%d, flags, result, v8, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7); \\\n\
            %s "%(n, rd, vsew*2 if vsew < 64 else 64, rd,  "la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v%d, (x7); \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7); \\\n\
            inst v%d, v%d, v%d%s; \\\n\
        )" % (vsew, rs2, vsew, n, rd, rs2, n, ", v0.t" if masked else ""), file=f)
    for n in range(1, 32):
        if n % (2*lmul) != 0:
            continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_rd%d( testnum, inst, flags, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP_W_FP( testnum, v%d, flags, result, v8, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7); \\\n\
            %s "%(n, n, vsew*2 if vsew < 64 else 64, n, "la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v%d, (x7); \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7); \\\n\
            inst v%d, v%d, v%d%s; \\\n\
        )" % (vsew, rs2, vsew, rs1, n, rs2, rs1, ", v0.t" if masked else ""), file=f)


def generate_macros_widen_rs2(f, lmul):
    # lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        rs1, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_2%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )" % (n, rd, rs1, n, rd, rd, rs1, n), file=f)
    for n in range(1, 32):
        if n % (2*lmul) != 0:
            continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_rd%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )" % (n, n, rs1, rs2, n, n, rs1, rs2), file=f)


def generate_macros_widen_rs2_neg(f, lmul):
    # lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        rs1, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_NEGRESULT_2%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            fneg.d f2, f2; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )" % (n, rd, rs1, n, rd, rd, rs1, n), file=f)
    for n in range(1, 32):
        if n % (2*lmul) != 0:
            continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_NEGRESULT_rd%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            fneg.d f2, f2; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )" % (n, n, rs1, rs2, n, n, rs1, rs2), file=f)


def generate_tests(instr, f, vsew, lmul, suffix="vv", test_vv=True, test_vf=True, test_rv=False):
    # lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64

    if instr == "vfdiv" or instr == "vfrdiv" or instr == "vfrec7":
        # For the divison instruction, the operands cannot be zero
        # So we need to delete it
        while (rs1_val.count("0x00000000")):
            rs1_val.remove("0x00000000")
        while (rs2_val.count("0x00000000")):
            rs2_val.remove("0x00000000")

        # `0x80000000` is represented as `-0` in floating point
        # So we need to delete it
        while (rs1_val.count("0x80000000")):
            rs1_val.remove("0x80000000")
        while (rs2_val.count("0x80000000")):
            rs2_val.remove("0x80000000")

        # For the divison instruction, the operands cannot be zero
        # So we need to delete it
        while (rs1_val.count("0x0000000000000000")):
            rs1_val.remove("0x0000000000000000")
        while (rs2_val.count("0x0000000000000000")):
            rs2_val.remove("0x0000000000000000")

        # `0x8000000000000000` is represented as `-0` in floating point
        # So we need to delete it
        while (rs1_val.count("0x8000000000000000")):
            rs1_val.remove("0x8000000000000000")
        while (rs2_val.count("0x8000000000000000")):
            rs2_val.remove("0x8000000000000000")

    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0

    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    if test_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("TEST_FP_VV_OP( %d,  %s.%s, 0xff100, rd_data_vv+%d, rs2_data+%d, rs1_data+%d);" % (
                n, instr, suffix, i*step_bytes, i*step_bytes, i*step_bytes), file=f)

        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests (different register)", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(min(32, loop_num)):
            k = i % 31 + 1
            if k == 8 or k == 16 or k == 24 or k % lmul != 0:
                continue
            n += 1
            print("  TEST_FP_VV_OP_rd%d( " % k+str(n)+",  %s.%s, 0xff100, " %
                  (instr, suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
            n += 1
            print("  TEST_FP_VV_OP_1%d( " % k+str(n)+",  %s.%s, 0xff100, " %
                  (instr, suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
    vv_test_num = n
    
    if test_vf:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VF Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("TEST_FP_VF_OP( %d,  %s.vf, 0xff100, rd_data_vf+%d, rs2_data+%d, rs1_data+%d);" % (
                n, instr, i*step_bytes, i*step_bytes, i*step_bytes), file=f)

        print("  #-------------------------------------------------------------",file=f)
        print("  # VF Tests (different register)",file=f)
        print("  #-------------------------------------------------------------",file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)",file=f)
        for i in range(min(32, loop_num)):     
            k = i%31+1        
            if k == 1 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
                continue  
            n += 1
            print("  TEST_FP_VF_OP_rd_%d( "%k+str(n)+",  %s.vf, 0xff100, "%instr+"rd_data_vf+%d, rs2_data+%d, rs1_data+%d);" % (i*step_bytes, i*step_bytes, i*step_bytes),file=f)
            
            k = i%31+1
            if k == 2 or k % lmul != 0:
                continue        
            n += 1
            print("  TEST_FP_VF_OP_rs1_%d( "%k+str(n)+",  %s.vf, 0xff100, "%instr+"rd_data_vf+%d, rs2_data+%d, rs1_data+%d);" % (i*step_bytes, i*step_bytes, i*step_bytes),file=f)
    vf_test_num = n - vv_test_num

    if test_rv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VF Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("TEST_FP_VF_OP_RV( %d,  %s.vf, 0xff100,               5201314,        %s,        %s );" % (
                n, instr, rs1_val[i], rs2_val[i]), file=f)

        print("  #-------------------------------------------------------------",file=f)
        print("  # VF Tests (different register)",file=f)
        print("  #-------------------------------------------------------------",file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
        for i in range(min(32, loop_num)):
            k = i%31+1
            if k == 1 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
                continue
            n += 1
            print("  TEST_FP_VF_OP_RV_rd_%d( "%k+str(n)+",  %s.vf, 0xff100, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );",file=f)

            k = i%31+1
            if k == 14 or k % lmul != 0:
                continue
            n += 1
            print("  TEST_FP_VF_OP_RV_rs1_%d( "%k+str(n)+",  %s.vf, 0xff100, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );",file=f)
    rv_test_num = n - vf_test_num - vv_test_num
    
    return (vv_test_num, vf_test_num, rv_test_num)

def generate_tests_v_op(instr, f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    rs1_val = list(set(rs1_val))
    rs2_val = list(set(rs2_val))
    if instr == "vfdiv" or instr == "vfrdiv" or instr == "vfrec7":
        # For the divison instruction, the operands cannot be zero
        # So we need to delete it
        while (rs1_val.count("0x00000000")):
            rs1_val.remove("0x00000000")
        while (rs2_val.count("0x00000000")):
            rs2_val.remove("0x00000000")

        # `0x80000000` is represented as `-0` in floating point
        # So we need to delete it
        while (rs1_val.count("0x80000000")):
            rs1_val.remove("0x80000000")
        while (rs2_val.count("0x80000000")):
            rs2_val.remove("0x80000000")

        # For the divison instruction, the operands cannot be zero
        # So we need to delete it
        while (rs1_val.count("0x0000000000000000")):
            rs1_val.remove("0x0000000000000000")
        while (rs2_val.count("0x0000000000000000")):
            rs2_val.remove("0x0000000000000000")

        # `0x8000000000000000` is represented as `-0` in floating point
        # So we need to delete it
        while (rs1_val.count("0x8000000000000000")):
            rs1_val.remove("0x8000000000000000")
        while (rs2_val.count("0x8000000000000000")):
            rs2_val.remove("0x8000000000000000")

    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfclass.v Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(loop_num):        
        print("TEST_FP_V_OP( %d,  %s.v, 0xff100, "%(n, instr) + "rd_data_vv+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes), file=f)
        n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfclass.v Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8:
            continue
        print("  TEST_FP_V_OP_rd_%d( "%k+str(n)+",  %s.v, 0xff100, rd_data_vv+%d, rs1_data+%d);"%(instr, i*step_bytes, i*step_bytes),file=f)
        n += 1

        k = i % 31 + 1
        if k % lmul != 0 or k == 24:
            continue
        print("  TEST_FP_V_OP_rs1_%d( "%k+str(n)+",  %s.v, 0xff100, rd_data_vv+%d, rs1_data+%d);"%(instr, i*step_bytes, i*step_bytes),file=f)
        n += 1
    return (n, 0, 0)



def generate_tests_vfmacc(instr, f, vsew, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    rs1_val = list(set(rs1_val))
    rs2_val = list(set(rs2_val))
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
 
    # VV
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("TEST_FP_VV_FUSED_OP( %d,  %s.vv, 0xff100,  rd_data_vv+%d, rs2_data+%d, rs1_data+%d);" % (
            n, instr, i*step_bytes, i*step_bytes, i*step_bytes), file=f)

    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n += 1
        print("  TEST_FP_VV_FUSED_OP_rd%d( " % k+str(n)+",  %s.vv, 0xff100, " %
                (instr)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
        n += 1
        print("  TEST_FP_VV_FUSED_OP_1%d( " % k+str(n)+",  %s.vv, 0xff100, " %
                (instr)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
    
    vv_test_num = n
    # VF
    print("  #-------------------------------------------------------------", file=f)
    print("  # VF Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("TEST_FP_VF_FUSED_OP_RV( %d,  %s.vf, 0xff100, rd_data_vf+%d, rs2_data+%d, rs1_data+%d);"  % (
            n, instr, i*step_bytes, i*step_bytes, i*step_bytes), file=f)
    vf_test_num = n - vv_test_num
    return (vv_test_num, vf_test_num, 0)

def generate_tests_vfwmacc(instr, f, vsew, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    rs1_val = list(set(rs1_val))
    rs2_val = list(set(rs2_val))
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
 
    # VV
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("TEST_FP_W_VV_FUSED_OP( %d,  %s.vv, 0xff100,  rd_data_vv+%d, rs2_data+%d, rs1_data+%d);" % (
            n, instr, i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)

    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if not (k == 8 or k == 16 or k == 24 or k % (2*lmul) != 0):
            n += 1
            print("  TEST_FP_W_VV_FUSED_OP_rd%d( " % k+str(n)+",  %s.vv, 0xff100, " %
                    (instr)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d);"%(i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)
        if not (k == 8 or k == 16 or k == 24 or k % lmul != 0):
            n += 1
            print("  TEST_FP_W_VV_FUSED_OP_1%d( " % k+str(n)+",  %s.vv, 0xff100, " %
                    (instr)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d);"%(i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)
    
    vv_test_num = n
    # VF
    print("  #-------------------------------------------------------------", file=f)
    print("  # VF Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("TEST_FP_W_VF_FUSED_OP_RV( %d,  %s.vf, 0xff100, rd_data_vf+%d, rs2_data+%d, rs1_data+%d);"  % (
            n, instr, i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)
    vf_test_num = n - vv_test_num
    return (vv_test_num, vf_test_num, 0)

def generate_tests_vfred(instr, f, vsew, lmul, suffix="vf", test_vv=True, test_vf=True, test_rv=False):
    # lmul = 1 if lmul < 1 else int(lmul)

    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64

    if instr == "vfdiv" or instr == "vfrdiv" or instr == "vfrec7":
        # For the divison instruction, the operands cannot be zero
        # So we need to delete it
        while (rs1_val.count("0x00000000")):
            rs1_val.remove("0x00000000")
        while (rs2_val.count("0x00000000")):
            rs2_val.remove("0x00000000")

        # `0x80000000` is represented as `-0` in floating point
        # So we need to delete it
        while (rs1_val.count("0x80000000")):
            rs1_val.remove("0x80000000")
        while (rs2_val.count("0x80000000")):
            rs2_val.remove("0x80000000")

        # For the divison instruction, the operands cannot be zero
        # So we need to delete it
        while (rs1_val.count("0x0000000000000000")):
            rs1_val.remove("0x0000000000000000")
        while (rs2_val.count("0x0000000000000000")):
            rs2_val.remove("0x0000000000000000")

        # `0x8000000000000000` is represented as `-0` in floating point
        # So we need to delete it
        while (rs1_val.count("0x8000000000000000")):
            rs1_val.remove("0x8000000000000000")
        while (rs2_val.count("0x8000000000000000")):
            rs2_val.remove("0x8000000000000000")

    n = 1
    if test_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(len(rs1_val)):
            print("TEST_FPRED_VV_OP( %d,  %s.%s, 0xff100,               5201314,        %s,        %s );" % (
                n, instr, suffix, rs1_val[i], rs2_val[i]), file=f)
            n += 1

        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests (different register)", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)

        for i in range(len(rs1_val)):
            k = i % 31 + 1
            if k == 8 or k == 16 or k == 24 or k % lmul != 0:
                continue
            print("  TEST_FPRED_VV_OP_rd%d( " % k+str(n)+",  %s.%s, 0xff100, " %
                  (instr, suffix)+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
            n += 1
            print("  TEST_FPRED_VV_OP_1%d( " % k+str(n)+",  %s.%s, 0xff100, " %
                  (instr, suffix)+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
            n += 1

    if test_vf:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VF Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            print("TEST_FPRED_VF_OP( %d,  %s.vf, 0xff100,               5201314,        %s,        %s );" % (
                n, instr, rs1_val[i], rs2_val[i]), file=f)
            n += 1

        print("  #-------------------------------------------------------------",file=f)
        print("  # VF Tests (different register)",file=f)
        print("  #-------------------------------------------------------------",file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)",file=f)
        n = n+1
        for i in range(len(rs1_val)):     
            k = i%31+1        
            if k == 1 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
                continue  
            print("  TEST_FPRED_VF_OP_rd_%d( "%k+str(n)+",  %s.vf, 0xff100, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );",file=f)
            n+=1
            
            k = i%31+1
            if k == 2 or k % lmul != 0:
                continue        
            print("  TEST_FPRED_VF_OP_rs1_%d( "%k+str(n)+",  %s.vf, 0xff100, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );",file=f)
            n +=1



def generate_tests_widen(instr, f, vsew, lmul,  test_wvwf = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    rs1_val = list(set(rs1_val))
    rs2_val = list(set(rs2_val))
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2

    print("  #-------------------------------------------------------------",file=f)
    print("  # VV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_W_FP_VV_OP( "+str(n)+",  %s.vv,  "%instr+"0xff100, "+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes),file=f)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(min( 32, loop_num)):
        k = i % 31 + 1
        if k % lmul == 0:
            n += 1
            print("  TEST_W_FP_VV_OP_1%d( "%k + str(n) + ",  %s.vv, "%instr + "0xff100, rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)

        if k % (2*lmul) == 0:
            n += 1
            print("  TEST_W_FP_VV_OP_rd%d( "%k + str(n)+ ",  %s.vv, "%instr + "0xff100, rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)
    vv_test_num = n

    print("  #-------------------------------------------------------------",file=f)
    print("  # VF Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_W_FP_VF_OP( "+str(n)+",  %s.vf, "%instr+"0xff100, "+"rd_data_vf+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes),file=f)
    vf_test_num = n - vv_test_num

    wv_test_num = 0
    wf_test_num = 0
    if test_wvwf:
        print("  #-------------------------------------------------------------",file=f)
        print("  # WV Tests",file=f)
        print("  #-------------------------------------------------------------",file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_W_FP_WV_OP( "+str(n)+",  %s.wv, "%instr+"0xff100, "+"rd_data_wv+%d, rs2_data_widen+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes_double, i*step_bytes),file=f)
        wv_test_num = n - vf_test_num - vv_test_num

        print("  #-------------------------------------------------------------",file=f)
        print("  # WF Tests",file=f)
        print("  #-------------------------------------------------------------",file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_W_FP_WF_OP( "+str(n)+",  %s.wf, "%instr+"0xff100, "+"rd_data_wf+%d, rs2_data_widen+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes_double, i*step_bytes),file=f)
        wf_test_num = n - vf_test_num - vv_test_num - wv_test_num
    return (vv_test_num, vf_test_num, wv_test_num, wf_test_num)


    

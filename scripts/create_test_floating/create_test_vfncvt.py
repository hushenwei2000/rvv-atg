import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *
import re

instr = 'vfncvt'
rs1_val = ["0x00000000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000",
           "0x00800000", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", 
           '0xd5173d3b', '0x1c954c88', '0xae8f2f8a', '0xe18cd6d3', '0xe7128ead', '0x430c45f2', '0x1fece821', '0xdbe8db2f', '0x9deac411', '0xd578536b', '0x5a2112c5', '0x33755502', '0x41f512c8', '0x5b07c90e', '0x30e95eba', '0xdc43d0d7', '0xce250988', '0x546ef0b9', '0x7c69a228', '0x540da0bc', '0xb917bde6', '0x2b14a548', '0x5c51c72f', '0xe66cd16e', '0xf8e67fb0', '0x45b5c5f1', '0x6bd9ba9a', '0x9c1e8667', '0x8a2c7d45', '0xaf61ac13', '0xcc06f22d', '0x6ac84f04', '0x581f3afc', '0x6122b26e', '0xff4914a8', '0xf0a80a4a', '0x44577dfa', '0xe31172b1', '0x30b00f6c', '0x9cd4367e', '0x53266571', '0x39a2b9a9', '0xf628feb7', '0x519a8397', '0xd949e747', '0xfe0b7d68', '0xd2ec6f9d', '0x7b9f0a06', '0xe25828a9', '0x6ff72e08', '0xae72d34d', '0xf61fde3e', '0x1cb57d88', '0x3bb5e465', '0x89b4574b', '0xae23f858', '0x32b4b342', '0x9c5034c7', '0x6129cabb', '0x9af4bc9a', '0xc729acef', '0x7d485219', '0x4a3b445a', '0x276f4a82', '0xdd7bf9fc', '0x6797c5aa', '0x9c739bc0', '0x37e6587a', '0x292fa2d6', '0x57b6f48d', '0xa87ebd39', '0xda3b9803', '0xcf98db80', '0xa1993841', '0x214c72b3', '0x4a289aa8', '0x3d7777d1', '0x579e0114', '0x13d30cfc', '0x8a19a62b', '0x07041e7d', '0x3b192289', '0xb8f72c52', '0x3a7c4f91', '0x2eadf0ac', '0xdbfec094', '0x8c1ae516', '0xbb97f344', '0x2d614a74', '0xdbb7bc69', '0x75160c80', '0x026513b2', '0xb3301eb1', '0x513b24cd', '0xd2d18754', '0x0fccea6a', '0xb4e15b15', '0xb546b05b', '0x0f952852', '0x7dbe9d89', '0xf8791ac8', '0xd924a386', '0xdf5f99f4', '0x6618d504', '0x8849a498', '0xf2961261', '0xe303d466', '0xd9d90f64', '0x9ceb7bc1', '0x07b60686', '0x92dc0a8a', '0x93997373', '0xe19d8f2e', '0xdd4ad4c7', '0x0b3419eb', '0x46365e84', '0x92db17e9', '0x65cdd905', '0xdd60629d', '0x16478c58', '0xd11c290e', '0x0d899e08', '0xc9770a1f', '0xac39d155', '0x0f7a7733', '0xa946bce1', '0x4e00d0f3', '0x3aa41dc4', 
           '0x0a9f9511', '0x5398487b', '0xf3782028', '0x69b76600', '0x8ca3efb3', '0xcb7da0de', '0x552d23d2', '0x3436f14c', '0x6f5f3f35', '0x53b5a207', '0xd20dfb9f', '0x8723b674', '0x0f348d99', '0x3886ab90', '0x0334f85a', '0xea1670df', '0xd13744b3', '0x883fe017', '0x1daf3b01', '0xa9c63a58', '0xec747b1c', '0x0c6eccf7', '0x4cad30bc', '0x477b3771', '0xaeef6b3d', '0x1555f68c', '0xb7e378a2', '0xb602bd3e', '0xaf130fb6', '0x31a4314a', '0xc723b3d7', '0x7015aa42', '0x0928aa3e', '0x22ef3704', '0xf352256b', '0x4da52bc4', '0x546d8880', '0xf78ee9c7', '0xc95bd691', '0x5239bc94', '0xb48c2fbf', '0x67e301b5', '0x240451c9', '0x27c6864f', '0x26c6f274', '0x25f55d4e', '0x5d2eb86f', '0x828a97e7', '0x67e912e1', '0x3d4617ee', '0x09322d7d', '0x1eca00ff', '0x2ecc47d2', '0xf3bb23d6', '0xab05bda1', '0xbebbadd8', '0x76ca2ed2', '0x2b20cd36', '0x524f229d', '0x5254e959', '0x2aef92ad', '0x31229858', '0xb06bc8f6', '0x5dcce032', '0x310e5031', '0xf2069096', '0x072a3060', '0x9c33042c', '0x06dd7d38', '0xe4b100b8', '0x04c5e517', '0x3b50cc02', '0x6f0086f2', '0xc583b3da', '0xae6ff135', '0x7815f9b0', '0x5cc84607', '0x754bced3', '0xaec59a2a', '0x8542dc85', '0x3af43c9d', '0xae8c12b8', '0x67be397d', '0x8758cfc4', '0x1de4f6af', '0x1a455288', '0x88db7d8c', '0xf937aafa', '0xca3650e2', '0xc7044eb3', '0x58933db0', '0x0545acbb', '0xb379a614', '0x9b3eb4cc', '0xe9519192', '0x2eb0d339', '0xf575e7bb', '0xee907664', '0x53960a4c', '0x87973a27', '0xa925b817', '0x1c1a1e45', '0x20dcdbeb', '0x2d3e0667', '0x53d05d72', '0xb822ad39', '0x4ffe6390', '0x9ef29035', '0xd0450fa2', '0x0d89744e', '0x346489f5', '0xd48dd733', '0x5d857c31', '0x9b185404', '0x41059de4', '0x12d11883', '0xa647e794', '0xd5710481', '0xcca75bc9', '0x28ea8990', '0x4914fd85', '0x9edd447a', '0x1a012a8e', '0x697d2a85', '0x0e3deb9d', '0x9da1bcd6', '0x5254ddf9', '0x0c3eab36',]
rs2_val = ["0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000",
           "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", 
           '0x16b77bce', '0x85a8a33c', '0xbe82002a', '0x6b4eed81', '0xfcf2b7b2', '0xb1a3f397', '0x81815039', '0x7df4c24f', '0x0827c929', '0xe1f1c6ec', '0x9b111081', '0x08c53c5a', '0x16e35174', '0x20553b83', '0xf4ed3db2', '0x5879b2ca', '0xf80d83b9', '0x7b48384f', '0x89a6c1a0', '0x31fe5439', '0x6ee2f5aa', '0x330f5715', '0x9f46020f', '0xb697e1c3', '0xf518acf6', '0x3958ea56', '0x56a29c95', '0xef286e01', '0xf6cad350', '0xe95400f6', '0x0b2ac811', '0x3ced78db', '0x75809524', '0xc5e59fb2', '0xdd81fa0a', '0xec9fb18d', '0x30e1830a', '0x21d2bbb0', '0x731a1760', '0x19167ebd', '0x7e537a04', '0xcf9dc475', '0x17f847a1', '0x5f4e2f05', '0x11065906', '0xa9663dbb', '0xb6d5707b', '0xef201e7b', '0xb4a84974', '0xc9feb8d1', '0xba38c7b1', '0x1877b042', '0x91778cbb', '0x2e715ec9', '0xebc88fd7', '0x6947de05', '0xaec12b86', '0x6164c29e', '0xba68fa1d', '0x17a54142', '0xbb7b049e', '0x08fab1e5', '0x1af6bb18', '0x74348a1d', '0xf41f5f9b', '0x604f267a', '0x8543a485', '0x17fca002', '0x3777625d', '0xca42df1f', '0xe9591298', '0x655428d1', '0x678995cf', '0x7ea84660', '0x049f1faf', '0x9a6ccdab', '0xf75264e4', '0x5b832e4f', '0x047e6b3b', '0xc18c4e25', '0x6676bf0e', '0x86738089', '0x1ee4a5ed', '0xb9545c29', '0x2c7cb95f', '0x8ab6881d', '0x32dc44c0', '0x7915e449', '0xb68216c7', '0x53c4ffc4', '0xc01a2b07', '0x6d56c00d', '0x231896cb', '0x3a6c685c', '0xe57e27bd', '0x3e6f7cbe', '0x8e74e2da', '0xfcea6243', '0x80eedc35', '0x048d92fb', '0xe8e803f4', '0x12c54b7b', '0x2d633cae', '0xbe8c5af3', '0x379def6c', '0xe298ae9a', '0x626b7cc5', '0x8f61b3a5', '0xe4219193', '0x01b8cfcd', '0x04bfcdf8', '0xd6cbbf81', '0x4bd075af', '0xe291d09b', '0xf0503b64', '0x21124d60', '0x17d5856b', '0x7989bf32', '0x6b84a91f', '0x3019a087', '0x01c79214', '0xea939be7', '0xc375122d', '0x116ec3d2', '0x2d7eeffe', '0xe013be07', '0xb45484fc', '0x2dcda7f1', 
           '0x2e2151fa', '0x500c5f17', '0x984b6942', '0x9960c98a', '0xc0c7c26a', '0xc714bae1', '0x7c086243', '0x9a4397f5', '0xb02b37fb', '0xec0ac4f0', '0xabb5045d', '0x4de1938f', '0x4ef87036', '0x477553ed', '0xdf884a52', '0xe364a2c3', '0x5e3d04d3', '0xa37172c6', '0x39c33e1d', '0x5fa55642', '0xc6588c96', '0x57aa9ec7', '0x52a373c8', '0x868a5027', '0xafc3fa5e', '0x804beeba', '0xbf812338', '0x53cf2324', '0x1c2a2099', '0x77275ab3', '0x8f53143f', '0x7868d163', '0x3362ef56', '0xf5c4c30d', '0x3413c9a6', '0xbae49486', '0x4d195ecf', '0x55085e69', '0x497af66c', '0x776d41f0', '0x6b06fcef', '0xec9c3cae', '0xbbcdcd90', '0xa78b9e5d', '0xb517d569', '0x58ecb82f', '0x897683b0', '0x017fed42', '0x7ac46a81', '0x6b3424e3', '0xf78c7be0', '0x225c9001', '0x716f74e5', '0x5ea07308', '0x9cb1f841', '0x69773182', '0xba7c2bc1', '0x3615b6cd', '0xb7cbdb1c', '0x57503bd7', '0x08d9043f', '0xde4c459d', '0x7a26c712', '0x563028c3', '0x795e33bf', '0xf2d19a38', '0xf20bed88', '0x7e91e990', '0x28403d8f', '0xe451d935', '0x6cbd6936', '0x4bb4197f', '0xb2301f0d', '0xc0fe2faf', '0x16598049', '0x8b074d85', '0xb3044c5f', '0x52e624b8', '0xe4b5a3ae', '0x223b3100', '0x60e69e76', '0x7b1ae2f0', '0x8837caa2', '0xa64768d4', '0xe3cafbaa', '0x409e0a27', '0x8bca7953', '0x54110db1', '0xdd376b5e', '0x82997f29', '0x355719f2', '0x409cf5f2', '0xd0f04044', '0xb1f11cd7', '0xde5e4fa6', '0xd82dd4fd', '0xe58d530d', '0x4949dc26', '0x8e5f9ede', '0x8e4a63c9', '0x3e0b7f6a', '0x721e2d49', '0xb9420e82', '0x9f300bb4', '0xdaf09bbc', '0x33939602', '0x22d815c2', '0xdd6461b8', '0xa0c1de71', '0x8412c769', '0xe03a03d1', '0x1d7e0df1', '0xaa1ba77a', '0x1fd16c33', '0xe6b2620f', '0xd80b4e8d', '0x8c57dfcc', '0x72d00ff0', '0x8d71f3bd', '0x90df5366', '0x65e2e213', '0xd4af903f', '0x0b402769', '0xe520a1a5', '0x2fd98a32', '0x8d31c277', '0x431be53f', '0x163af993',]


def generate_fdat_seg(f):
    print("fdat_rs1:", file=f)
    for i in range(len(rs1_val)):
        print("fdat_rs1_" + str(i) + ":  .word " + rs1_val[i], file=f)
    print("", file=f)
    print("fdat_rs2:", file=f)
    for i in range(len(rs2_val)):
        print("fdat_rs2_" + str(i) + ":  .word " + rs2_val[i], file=f)


def generate_macros_vfncvt(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FP_N_V_OP \n\
#define TEST_FP_N_V_OP( testnum, inst, flags, result, val1 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew*2 + " \\\n\
        inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_FP_N_V_OP_rs1_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew*2, n) + " \\\n\
                inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_FP_N_V_OP_rd_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew*2) + " \\\n\
                inst v%d, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)



def extract_operands(f, rpt_path):
    # Floating pooints tests don't need to extract operands, rs1 and rs2 are fixed
    return 0


def generate_tests_vfncvt(instr, f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 32:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    # rs1_val = list(set(rs1_val))
    # rs2_val = list(set(rs2_val))

    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    # print("loop_num = ", loop_num);
    # print("vlen = ", vlen, ", vsew = ", vsew, ", len(rs1_val) = ", len(rs1_val), ", len(rs2_val) = ", len(rs2_val));
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    # for i in range(loop_num):
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.xu.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.x.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.rtz.xu.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.rtz.x.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.f.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.rod.f.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    
    # for i in range(loop_num):
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.f.xu.w') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, 0xff100, "%(n, 'vfncvt.f.x.w') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
    #     n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % (2*lmul) == 0 and k != 8:
            for i in range(loop_num):
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.xu.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.x.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.rtz.xu.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.rtz.x.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.f.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.rod.f.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1
            for i in range(loop_num):
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.f.xu.w') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.f.x.w') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
                n += 1

        k = i % 31 + 1
        if k % lmul != 0 or k == 8:
            continue
        for i in range(loop_num):
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.xu.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.x.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.rtz.xu.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.rtz.x.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.f.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.rod.f.f.w') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
        for i in range(loop_num):
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.f.xu.w') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfncvt.f.x.w') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes_double), file=f)
            n += 1
    return (n, 0)

def print_ending(f):
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
    \n\
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)\n\
    TEST_PASSFAIL\n\
    #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    ", file=f)

    generate_fdat_seg(f)

    print("signature_x12_0:\n\
        .fill 0,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x12_1:\n\
        .fill 32,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_0:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_1:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_2:\n\
        .fill 376,4,0xdeadbeef\n\
    \n\
    #ifdef rvtest_mtrap_routine\n\
    \n\
    mtrap_sigptr:\n\
        .fill 128,4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    #ifdef rvtest_gpr_save\n\
    \n\
    gpr_save:\n\
        .fill 32*(XLEN/32),4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    RVTEST_DATA_END\n\
    ", file=f)


def create_empty_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VFMVF_OP( 1,  fdat_rs1_0 );", file=f)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vfncvt(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_vfncvt(instr, f, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs2_val, num_tests_tuple, vsew, f, is_narrow = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path

#!/usr/bin/env python3
"""
UmaDecryptor 解密算法Python实现
从 https://github.com/RanKaeder/UmaDecryptor 移植
用于分析赛马娘游戏加密数据

用法：
  python3 uma_decrypt.py decrypt-db <meta_file> <output_file> [--region japan|global]
  python3 uma_decrypt.py decrypt-dat <input_dir> <output_dir> <meta_db>
"""

import struct
import os
import sys
import sqlite3

# ========== 数据库解密 ==========
DB_BASE_KEY = bytes([0xF1, 0x70, 0xCE, 0xA4, 0xDF, 0xCE, 0xA3, 0xE1, 0xA5, 0xD8, 0xC7, 0x0B, 0xD1, 0x00, 0x00, 0x00])

DATABASE_KEY_JAPAN = bytes([
    0x6D, 0x5B, 0x65, 0x33, 0x63, 0x36, 0x63, 0x25, 0x54, 0x71, 0x2D, 0x73,
    0x50, 0x53, 0x63, 0x38, 0x6D, 0x34, 0x37, 0x7B, 0x35, 0x63, 0x70, 0x23,
    0x37, 0x34, 0x53, 0x29, 0x73, 0x43, 0x36, 0x33
])

DATABASE_KEY_GLOBAL = bytes([
    0x56, 0x63, 0x6B, 0x63, 0x42, 0x72, 0x37, 0x76, 0x65, 0x70, 0x41, 0x62
])

def generate_db_key(region='japan'):
    """生成数据库最终解密密钥"""
    base_key = DATABASE_KEY_JAPAN if region == 'japan' else DATABASE_KEY_GLOBAL
    final_key = bytearray(len(base_key))
    for i in range(len(base_key)):
        final_key[i] = base_key[i] ^ DB_BASE_KEY[i % 13]
    return bytes(final_key)

# ========== 资源文件解密 ==========
DEFAULT_BASE_KEYS = bytes([0x53, 0x2B, 0x46, 0x31, 0xE4, 0xA7, 0xB9, 0x47, 0x3E, 0x7C, 0xFB])
DEFAULT_KEY = -7673907454518172050  # 0x958F6B5A3D2E1C2E

def generate_xor_keys(base_keys=DEFAULT_BASE_KEYS, key=DEFAULT_KEY):
    """生成XOR密钥数组"""
    key_bytes = struct.pack('<q', key)  # 8字节小端
    keys = bytearray(len(base_keys) * 8)
    for i in range(len(base_keys)):
        base_offset = i * 8
        for j in range(8):
            keys[base_offset + j] = base_keys[i] ^ key_bytes[j]
    return bytes(keys)

def decrypt_asset(data, base_keys=DEFAULT_BASE_KEYS, key=DEFAULT_KEY):
    """解密资源文件数据"""
    if len(data) <= 256:
        return data
    
    keys = generate_xor_keys(base_keys, key)
    result = bytearray(data)
    for i in range(256, len(result)):
        result[i] ^= keys[i % len(keys)]
    return bytes(result)

def decrypt_asset_file(input_path, output_path):
    """解密资源文件"""
    with open(input_path, 'rb') as f:
        data = f.read()
    decrypted = decrypt_asset(data)
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(decrypted)
    print(f"Decrypted: {input_path} -> {output_path} ({len(decrypted)} bytes)")

# ========== 主入口 ==========
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'decrypt-db':
        if len(sys.argv) < 4:
            print("Usage: decrypt-db <input> <output> [--region japan|global]")
            sys.exit(1)
        region = 'japan'
        if '--region' in sys.argv:
            idx = sys.argv.index('--region')
            region = sys.argv[idx + 1]
        final_key = generate_db_key(region)
        print(f"Database key ({region}): {final_key.hex()}")
        print("Note: Full SQLCipher decryption requires sqlite3mc library")
        
    elif cmd == 'decrypt-dat':
        if len(sys.argv) < 4:
            print("Usage: decrypt-dat <input_dir> <output_dir> <meta_db>")
            sys.exit(1)
        input_dir = sys.argv[2]
        output_dir = sys.argv[3]
        for root, dirs, files in os.walk(input_dir):
            for fname in files:
                input_path = os.path.join(root, fname)
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                decrypt_asset_file(input_path, output_path)
    
    elif cmd == 'generate-keys':
        keys = generate_xor_keys()
        print(f"XOR Keys ({len(keys)} bytes): {keys.hex()}")
        print(f"BaseKeys: {DEFAULT_BASE_KEYS.hex()}")
        print(f"Key (int64): {DEFAULT_KEY}")
        print(f"Key (hex): 0x{DEFAULT_KEY & 0xFFFFFFFFFFFFFFFF:016X}")
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

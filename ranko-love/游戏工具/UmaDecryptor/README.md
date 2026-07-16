# UmaDecryptor - UMA赛马娘游戏数据解密工具

**日期**：2025-09-29（更新：2026-04-19）
**分类**：游戏工具
**标签**：赛马娘, 解密工具, .NET
**原文链接**：https://ranko.love/2025/09/29/2025-09-29UmaDecryptor/
**GitHub**：https://github.com/RanKaeder/UmaDecryptor

## 概述

UMA赛马娘游戏数据解密工具 - 一个功能完整的.NET 8控制台应用程序，支持解密UMA游戏的数据库文件和资源文件。

## 功能特性

### 核心能力
- **完整数据库解密**：解密 meta 数据库，保留所有表结构和数据
- **多区域支持**：支持日服和Global国际服
- **资源文件解密**：解密游戏资源文件（AssetBundle等）
- **目录批处理**：一键处理整个游戏数据目录
- **增量更新**：智能跳过已存在文件
- **多线程并行**：高效处理大量文件

### 三大命令

#### 1. uma-dir - 一站式目录处理
处理完整的UMA游戏目录，自动解密所有类型的数据文件。

```bash
# 日服解密
UmaDecryptor.exe uma-dir -i "C:\Users\User\AppData\LocalLow\Cygames\umamusume" -o "C:\UMA_Decrypted"

# Global国际服
UmaDecryptor.exe uma-dir -i "C:\Games\UMA_Global" -o "C:\Games\UMA_Global_Decrypted" -r Global

# 全量模式（覆盖）
UmaDecryptor.exe uma-dir -i "C:\Games\UMA" -o "C:\Games\UMA_Decrypted" --overwrite

# 多线程
UmaDecryptor.exe uma-dir -i "C:\Games\UMA" -o "C:\Games\UMA_Decrypted" -t 8
```

**自动处理流程：**
1. 解密 meta 数据库（读取所有表）
2. 拷贝 master 文件夹（保持完整性，支持增量）
3. 解密 dat 文件夹（所有资源文件，保持目录结构）

#### 2. decrypt-db - 数据库解密
解密单个数据库文件，输出完整的SQLite数据库。

```bash
UmaDecryptor.exe decrypt-db -i meta -o meta_decrypted
UmaDecryptor.exe decrypt-db -i meta -o meta_global -r Global
```

#### 3. decrypt-dat - 资源文件解密
解密资源文件夹，支持任意目录结构。

```bash
UmaDecryptor.exe decrypt-dat -i "C:\Game\dat" -o "C:\Game\dat_decrypted" -m "meta_decrypted"
```

## 解密算法

### 数据库解密
- 使用 sqlite3mc 处理 SQLCipher 加密的数据库
- 日服密钥：32字节，与DB_BASE_KEY进行XOR运算
- Global服密钥：12字节
- DB_BASE_KEY：`0xF1, 0x70, 0xCE, 0xA4, 0xDF, 0xCE, 0xA3, 0xE1, 0xA5, 0xD8, 0xC7, 0x0B, 0xD1, 0x00, 0x00, 0x00`

### 资源文件解密
- 前256字节保持原样
- 从256字节开始使用密钥循环异或解密
- 支持负数密钥（小端序处理）
- DefaultBaseKeys: `0x53, 0x2B, 0x46, 0x31, 0xE4, 0xA7, 0xB9, 0x47, 0x3E, 0x7C, 0xFB`
- DefaultKey: `-7673907454518172050L`

## 输出结构

```
输出目录/
├── meta          # 解密后的完整数据库
├── master/       # 原封不动拷贝
└── dat/          # 解密后的资源文件
    ├── 2A/
    ├── 3B/
    └── ...
```

## 项目架构

```
UmaDecryptor/
├── Commands/         # CLI命令定义
├── Core/             # 核心验证组件
├── Crypto/           # 加密解密算法
├── Database/         # 数据库处理
├── Services/         # 业务逻辑服务
├── Program.cs        # 程序入口
├── sqlite3mc_x64.dll # SQLite加密扩展
└── UmaDecryptor.csproj
```

## 技术栈

- .NET 8
- CommandLineParser (CLI参数解析)
- System.Data.SQLite (数据库操作)
- Microsoft.Extensions.Logging (结构化日志)
- sqlite3mc (SQLite加密扩展)

## 许可证

MIT

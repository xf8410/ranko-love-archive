# Hachimi 0.15 + Mod性能优化版本

**日期**：2025-09-29
**分类**：游戏工具
**标签**：赛马娘, Mod, Hachimi, 游戏工具
**原文链接**：https://ranko.love/2025/09/29/2025-09-29Hachimi/
**GitHub**：https://github.com/RanKaeder/Hachimi

## 概述

Hachimi Edge是一个游戏增强和翻译Mod，用于UM:PD（赛马娘）。由Rust编写，支持Windows和Android。博主的优化版本提升了Mod的兼容性和性能。

## 为什么要做这个插件？

游戏频繁更新导致mod失效是个老问题，每次都要等作者更新适配。博主研究Hachimi的机制，通过优化提升mod的兼容性和性能表现。

## 安装指南

### 1. 安装原版 Hachimi
- 下载最新的 `hachimi_installer.exe`
- 在 Target 一栏中选择 `UnityPlayer.dll`
- 点击 Install，安装 Hachimi 0.15 原版

### 2. 替换优化版DLL
- 启动一次游戏，让Hachimi完成初始化
- 进入游戏安装目录
- 找到 `umamusume.exe.local` 文件夹
- 将优化版DLL文件复制并覆盖到该文件夹中

### 3. 安装Mod文件
- 在游戏安装目录下找到 `hachimi` 文件夹
- 在该文件夹内新建 `mods` 文件夹
- 将mod文件放入 `mods` 文件夹

## Hachimi Edge 特性

- **高质量翻译**：支持复数形式、序数词等，UI文本/mdb/剧情/歌词/纹理替换
- **即插即用**：所有设置均在游戏内完成
- **翻译自动更新**：内置更新器，无需重启
- **内置GUI**：游戏内配置编辑器
- **图形设置**：FPS解锁、分辨率缩放
- **跨平台**：Windows + Android

## 技术栈

- **语言**：Rust
- **平台**：Windows (DLL注入) + Android (Zygisk)
- **许可证**：GNU GPLv3

## 特别致谢

- Trainers' Legend G
- umamusume-localify-android
- umamusume-localify
- Carotenify
- umamusu-translate
- frida-il2cpp-bridge

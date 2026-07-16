# 如何定位插件所需的 START_RVA 地址

**日期**：2025-10-11（更新：2026-04-19）
**分类**：游戏开发 → 插件制作
**标签**：逆向工程, Unity, IL2CPP, RVA
**原文链接**：https://ranko.love/2025/10/11/2025-10-11-how-to-locate-start-rva/

## 什么是 START_RVA

START_RVA 是 IL2CPP 二进制文件中符号表的起始 RVA 偏移。它允许开发者定位和调用 IL2CPP API 函数，如 `il2cpp_init`、`il2cpp_class_from_name` 等。在插件开发中，准确获取 START_RVA 是绕过混淆和定位函数的基础。

## 获取 PDB 文件

### 安装 Windows SDK
前往 [微软官方下载页面](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/) 下载 Windows SDK，仅勾选「Debugging Tools for Windows」。

### 设置符号路径环境变量
```cmd
set _NT_SYMBOL_PATH=srv*C:\Symbols*http://symbolserver.unity3d.com
```

### 使用 cdb 打开目标 DLL
```cmd
"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\cdb.exe" -z "E:\Documents\umamusume\UnityPlayer.dll"
```
输入 `.reload /f` 下载并加载 PDB 文件。

## 分析 DLL 文件

### 步骤1: 加载到 IDA Pro 或 Ghidra
使用 IDA Pro 或 Ghidra 打开 UnityPlayer.dll。

### 步骤2: 定位 LoadIl2cpp 函数
- 在符号视图中搜索 "LoadIl2cpp"
- 如果 PDB 加载成功，可以直接跳转到函数
- 参考教程：https://katyscode.wordpress.com/2021/02/23/il2cpp-finding-obfuscated-global-metadata/

### 使用 IDA Pro 定位
1. 打开 UnityPlayer.dll，等待加载完毕
2. 在左侧 Functions 窗口过滤找到 Loadil2Cpp
3. 找到 il2cpp_init 部分，相当于：
```c
void* addr = LookupSymbol(module, "dc1f72af605f19e6b916349", 1);
il2cpp_init = addr;
```
4. 右键选择 TextView，选中字符串，切换到 hex 视图
5. 取后四个字节，即字符串的地址
6. 减去 ImageBase (0x180000000)，拿到 RVA

## 工具和脚本推荐

- **IDA Pro / Ghidra**：反汇编和分析二进制文件
- **cdb / windbg**：下载和加载 PDB 符号
- **Python pefile**：解析 PE 文件头和 RVA
- **自定义脚本**：遍历符号表，验证 RVA

## 结论

获取 START_RVA 需要结合符号调试和逆向工程。通过 PDB 文件和调试工具，可以准确定位 IL2CPP 符号表，为插件开发奠定基础。不同 Unity 版本的 RVA 可能不同，建议验证后使用。

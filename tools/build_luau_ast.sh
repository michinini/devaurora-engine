#!/bin/bash
# Build luau-ast from the existing patched Luau 0.739 source tree
# (mirrors the flags of deobf/build_luau.py: gcc, -O3 -flto -march=native, static)
set -e
SRC=/tmp/luau-src/luau-0.739
BUILD=$SRC/build-deobf
BIN=/home/z/my-project/engine/Deobfuscator/deobf/bin

cmake -S "$SRC" -B "$BUILD" -DCMAKE_BUILD_TYPE=Release \
  -DLUAU_BUILD_TESTS=OFF -DLUAU_STATIC_CRT=ON -G Ninja \
  -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ \
  -DCMAKE_C_FLAGS_RELEASE="-O3 -flto -march=native -DNDEBUG" \
  -DCMAKE_CXX_FLAGS_RELEASE="-O3 -flto -march=native -DNDEBUG" \
  -DCMAKE_EXE_LINKER_FLAGS="-static -O3 -flto -march=native"

cmake --build "$BUILD" --config Release --target Luau.Ast.CLI --parallel 2>&1 | tail -5

for cand in "$BUILD/luau-ast" "$BUILD/Release/luau-ast"; do
  if [ -f "$cand" ]; then
    mkdir -p "$BIN"
    cp -f "$cand" "$BIN/luau-ast"
    chmod +x "$BIN/luau-ast"
    echo "[+] wrote $BIN/luau-ast"
    "$BIN/luau-ast" --help 2>&1 | head -3 || true
    exit 0
  fi
done
echo "[!] luau-ast binary not found under $BUILD"; exit 1

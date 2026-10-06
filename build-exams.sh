#!/usr/bin/env bash
# ============================================================
# build-exams.sh — 编译仓库内所有试卷/答案 tex
#
# 用法:
#   ./build-exams.sh                     # 编译全部（两次，解析 LastPage）
#   ./build-exams.sh 341                 # 只编译路径含 "341" 的文件
#   ./build-exams.sh --tex 341信息化      # 只编译文件名含该子串的文件
#   ./build-exams.sh --force             # 忽略时间戳，全部重编
#
# 产物: <目录>/out/<文件名>/<文件名>.pdf 与 <目录>/<文件名>.pdf
# ============================================================
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
# 把仓库根目录加入 TEXINPUTS 的 basename 搜索路径：新版 kpathsea 不解析
# 文件名里的 ".."，形如 \usepackage{../../notestyle} 的旧文件由此兜底
export TEXINPUTS=".:./exam-template:${ROOT}:${TEXINPUTS:-}"

pat=""
force=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) force=1; shift ;;
    --tex) pat="$2"; shift 2 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) pat="$1"; shift ;;
  esac
done

mapfile -t texfiles < <(
  find . -name "*.tex" \
    -not -path "./tmp/*" -not -path "./.git/*" -not -path "./.kilo/*" -not -path "./.kilo" \
    -not -path "*/out/*" -not -path "./exam-template/*" \
    | sort
)

fail=0
for tex in "${texfiles[@]}"; do
  [[ -n "$pat" && "$tex" != *"$pat"* ]] && continue
  dir="$(dirname "$tex")"
  base="$(basename "$tex" .tex)"
  outdir="$dir/out/$base"
  pdf="$outdir/$base.pdf"

  if [[ $force -eq 0 && -f "$pdf" && "$pdf" -nt "$tex" && "$pdf" -nt "$dir/../notestyle.sty" ]]; then
    echo "== skip  $tex (已是最新)"
    continue
  fi

  mkdir -p "$outdir"
  ok=1
  for pass in 1 2; do
    if ! xelatex -interaction=nonstopmode -halt-on-error \
         -output-directory="$outdir" "$tex" >"$outdir/build.log" 2>&1; then
      ok=0
      break
    fi
  done

  if [[ $ok -eq 1 && -f "$pdf" ]]; then
    cp -f "$pdf" "$dir/$base.pdf"
    echo "== ok    $tex -> $dir/$base.pdf"
  else
    fail=$((fail + 1))
    echo "== FAIL  $tex"
    grep -nE "^!|^l\.[0-9]+" "$outdir/build.log" | head -12
  fi
done

if [[ $fail -gt 0 ]]; then
  echo "有 $fail 个文件编译失败"
  exit 1
fi
echo "全部完成"

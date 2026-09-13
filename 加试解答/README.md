# 2026 高联预赛 A 卷加试解答

`加试解答.tex` 包含试卷第二页四道加试题的题目和完整证明。

第二题采用纯平面几何证明：取斜边中点将倍角条件化为四点共圆，
再利用九点圆、反射和位似转移相切关系。正文配有展示辅助圆、辅助线及切线的 TikZ 图。

在本文件夹内运行两次：

```bash
xelatex -interaction=nonstopmode -halt-on-error 加试解答.tex
```

然后将 PDF 复制到项目顶层：

```bash
cp 加试解答.pdf ../2026高联预赛A卷加试解答.pdf
```

所有编译中间文件均保留在本文件夹内。

`check_s_shapes.py` 是第四题的小规模线性规划辅助核验脚本，可以用以下命令运行：

```bash
uv run --with scipy python check_s_shapes.py 2 3 4 5 6 7 8 9 10 11 12
```

脚本输出不是数学证明的依据；PDF 中的下界证明和取等构造对所有允许的整数 `n` 成立。

# Top-10 词频统计示例

这是一个简单的 Python 小程序：统计英文文本中出现次数最多的 10 个单词，并将结果保存为 PDF 矢量柱状图。

生成文件：`figures/word_freq.pdf`

## 1. 安装依赖

```bash
python -m pip install -r requirements.txt
```

## 2. 运行示例

直接运行程序会使用内置示例文本：

```bash
python word_freq.py
```

也可以传入自己的 UTF-8 文本文件：

```bash
python word_freq.py input.txt
```

程序只统计由英文字母组成的单词，自动忽略大小写，并过滤少量常见停用词。

## 3. 在 LaTeX 报告中插图

首先在导言区加载 `graphicx`：

```latex
\usepackage{graphicx}
```

如果报告已经定义了 `\reportfig` 命令，可以直接写：

```latex
如图~\ref{fig:wordfreq} 所示，实验结果图使用 PDF 矢量格式保存，
可以在缩放后保持较好的文字和图形清晰度。

\reportfig{figures/word_freq.pdf}{词频统计实验结果}{fig:wordfreq}
```

也可以使用标准的 `figure` 环境：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{figures/word_freq.pdf}
  \caption{词频统计实验结果}
  \label{fig:wordfreq}
\end{figure}
```

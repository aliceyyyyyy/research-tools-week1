"""Count the top English words and export a vector PDF bar chart."""

from collections import Counter
from pathlib import Path
import re
import sys

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


SAMPLE_TEXT = """
Data analysis uses data to build a model. A good model learns useful features
from training data. The learning method affects model performance, while clear
analysis helps explain each result. Data, model, learning, analysis, feature,
training, method, system, result, and performance are common experiment words.
The data system compares model results and reports model performance.
"""

STOP_WORDS = {"a", "an", "and", "are", "from", "in", "of", "the", "to", "while"}


def top_words(text: str, limit: int = 10) -> list[tuple[str, int]]:
    words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())
    useful_words = [word for word in words if word not in STOP_WORDS]
    return Counter(useful_words).most_common(limit)


def draw_chart(items: list[tuple[str, int]], output: Path) -> None:
    if not items:
        raise ValueError("No English words were found in the input text.")

    output.parent.mkdir(parents=True, exist_ok=True)
    page_w, page_h = 515, 322
    left, right = 95, 34
    chart_top, chart_bottom = 225, 48
    chart_w = page_w - left - right
    row_gap = (chart_top - chart_bottom) / max(len(items) - 1, 1)
    bar_h = min(10.5, row_gap * 0.58)
    largest = items[0][1]
    axis_max = max(largest * 1.12, 1)

    pdf = canvas.Canvas(str(output), pagesize=(page_w, page_h), pageCompression=1)
    pdf.setTitle("Top 10 Word Frequencies")
    pdf.setCreator("word_freq.py")

    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#101828"))
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(24, 286, "Top 10 Word Frequencies")
    pdf.setFillColor(HexColor("#667085"))
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(24, 270, "Word-frequency experiment result")

    pdf.setFillColor(HexColor("#F7F9FC"))
    pdf.roundRect(20, 26, page_w - 40, 226, 7, fill=1, stroke=0)

    for part in range(5):
        value = largest * part / 4
        x = left + chart_w * value / axis_max
        pdf.setStrokeColor(HexColor("#DCE3EC"))
        pdf.setLineWidth(0.55)
        pdf.line(x, chart_bottom - 6, x, chart_top + 8)
        label = str(round(value))
        pdf.setFillColor(HexColor("#667085"))
        pdf.setFont("Helvetica", 7.5)
        pdf.drawString(x - stringWidth(label, "Helvetica", 7.5) / 2, 34, label)

    start_blue = (23, 92, 211)
    end_blue = (189, 222, 242)
    color_steps = max(len(items) - 1, 1)

    for index, (word, count) in enumerate(items):
        y = chart_top - index * row_gap
        ratio = index / color_steps
        rgb = tuple(round(a + (b - a) * ratio) for a, b in zip(start_blue, end_blue))
        color = HexColor("#%02X%02X%02X" % rgb)
        bar_w = chart_w * count / axis_max

        pdf.setFillColor(HexColor("#1D2939"))
        pdf.setFont("Helvetica", 8.2)
        label_w = stringWidth(word, "Helvetica", 8.2)
        pdf.drawString(left - 10 - label_w, y - 2.7, word)

        pdf.setFillColor(color)
        pdf.roundRect(left, y - bar_h / 2, bar_w, bar_h, bar_h / 2, fill=1, stroke=0)

        pdf.setFillColor(HexColor("#344054"))
        pdf.setFont("Helvetica-Bold", 7.8)
        pdf.drawString(left + bar_w + 5, y - 2.6, str(count))

    pdf.setFillColor(HexColor("#344054"))
    pdf.setFont("Helvetica", 8.2)
    axis_label = "Frequency"
    pdf.drawString(
        left + chart_w / 2 - stringWidth(axis_label, "Helvetica", 8.2) / 2,
        15,
        axis_label,
    )
    pdf.showPage()
    pdf.save()


def main() -> None:
    text = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else SAMPLE_TEXT
    output = Path("figures/word_freq.pdf")
    draw_chart(top_words(text), output)
    print(f"Created: {output.resolve()}")


if __name__ == "__main__":
    main()

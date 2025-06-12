# Order Blocks & Imbalances Detector

Detects hourly **order blocks** and price **imbalances** inside one trading session and
exports the results to an Excel workbook.
---

## ✨ Features

| Stage | Description |
|-------|-------------|
| 1️⃣ **Parse** | Reads *correct.csv* (minute bars) and converts timestamps. |
| 2️⃣ **Detect** | Finds hourly order‑blocks (bullish / bearish) and 1‑hour imbalances. |
| 3️⃣ **Nest** | Searches for 15‑minute imbalances that lie inside every detected block. |
| 4️⃣ **Export** | Writes a styled `result.xlsx` with hierarchical numbering and Russian headers. |

Order‑block / imbalance **direction** is set automatically:

* **Bullish** — upper bound `>` lower bound  
* **Bearish** — lower bound `>` upper bound  
* **Neutral** — bounds are equal

---

## 📂 Project layout

```
├── order_blocks_and_imbalances.py  # main script
├── correct.csv                     # minute bars (input)
├── result.xlsx                     # generated report (output)
└── README.md                       # this file
```

---

## 🚀 Quick start

```bash
# 1. Install dependencies
pip install pandas openpyxl

# 2. Drop your minute‑level data into `correct.csv`
# 3. Run the pipeline
python order_blocks_and_imbalances.py
```

> The script prints a short progress log and creates **result.xlsx** in the same folder.

---

## ⚙️ Configuration

Open **order_blocks_and_imbalances.py** and tweak the constants at the top if needed:

| Name          | Default | Meaning |
|---------------|---------|---------|
| `INPUT_CSV`   | `correct.csv` | Path to minute bar file. |
| `OUTPUT_XLSX` | `result.xlsx` | Destination workbook for the report. |
| `TOLERANCE`   | `0.001` | ± 0.1 % extra range used when nesting imbalances inside a block. |

---

## 📊 Output structure

Column | Description
-------|------------
`Порядковый номер` | Hierarchical index, e.g. `3` (block) or `3.2` (embedded imbalance).
`Формация`         | “Ордер блок” / “Имбаланс”.
`Направление`      | “Бычий”, “Медвежий” or “Нейтральный”.
`Дата и время`     | Opening time of the candlestick that **closed** the structure.
`Диапазон цен`     | Formatted as `low$‑high$` (2 decimal places).

---

## 🧮 Algorithm in a nutshell

1. **Order block** appears when a bearish candle is followed by a bullish one  
   *(or vice‑versa for bearish blocks)*.
2. **Imbalance** is a gap between consecutive candles:
   * bullish → `low₁ > high₂`
   * bearish → `high₁ < low₂`
3. When nesting, only imbalances **of the same type** as the parent block are considered,
   and their range is clipped to fit completely inside the block
   (with the configurable tolerance).

Full implementation lives in `detect_order_blocks`, `detect_imbalances`
and `clip_imbalance` functions of the script.

---

## 🤝 Contributing

Pull‑requests and issue reports are welcome!  
Feel free to fork the repository and propose improvements.

---

## 🪪 License

Released under the **MIT License** — see [`LICENSE`](LICENSE) for details.

import pandas as pd
from datetime import datetime


def parse_datetime(dt_str):
    # dt_str: '20250319 040000'
    return datetime.strptime(dt_str.strip(), "%Y%m%d %H%M%S")


def format_datetime(dt):
    return dt.strftime("%H:%M %d.%m.%Y")


def format_price_range(low, high):
    return f"{low:.2f}$-{high:.2f}$"


def find_order_blocks(df):
    blocks = []
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]
        if prev[4] < prev[1] and curr[4] > curr[1]:
            blocks.append(
                {
                    "type": "bullish",
                    "time": curr["date_time"],
                    "low": prev[3],
                    "high": prev[2],
                }
            )
        if prev[4] > prev[1] and curr[4] < curr[1]:
            blocks.append(
                {
                    "type": "bearish",
                    "time": curr["date_time"],
                    "low": prev[3],
                    "high": prev[2],
                }
            )
    return blocks


def find_imbalances(df):
    imbalances = []
    for i in range(len(df) - 1):
        curr = df.iloc[i]
        next_ = df.iloc[i + 1]
        if curr[3] > next_[2]:
            imbalances.append(
                {
                    "type": "bullish",
                    "time": next_["date_time"],
                    "low": next_[2],
                    "high": curr[3],
                }
            )
        if curr[2] < next_[3]:
            imbalances.append(
                {
                    "type": "bearish",
                    "time": next_["date_time"],
                    "low": curr[2],
                    "high": next_[3],
                }
            )
    return imbalances


def clip_imbalance_to_block(imb, block):
    low = max(imb["low"], block["low"])
    high = min(imb["high"], block["high"])
    return {**imb, "low": low, "high": high}


def main():
    print("=" * 40)
    print("ЭТАП 1: Поиск ордер блоков и имбалансов на H1")
    print("=" * 40)
    df = pd.read_csv("correct.csv", header=None)
    df["date_time"] = df[0].apply(parse_datetime)
    for col in [1, 2, 3, 4, 5]:
        df[col] = df[col].astype(float)

    order_blocks = find_order_blocks(df)
    imbalances = find_imbalances(df)

    print("\n" + "=" * 40)
    print("ЭТАП 2: Имбалансы внутри ордер блоков")
    print("=" * 40)

    print("\n" + "=" * 40)
    print("ЭТАП 3: Формирование итоговой таблицы и экспорт в Excel")
    print("=" * 40)
    PRICE_TOLERANCE = 0.001

    columns = [
        "Порядковый номер",
        "Формация (ордер блок или имбаланс)",
        "Направление (тип)",
        "Дата и время формирования",
        "Диапазон цен",
    ]
    result_rows = []
    row_number = 1
    for idx, block in enumerate(order_blocks, 1):
        result_rows.append(
            {
                "Порядковый номер": str(row_number),
                "Формация (ордер блок или имбаланс)": "Ордер блок",
                "Направление (тип)": (
                    "Бычий" if block["type"] == "bullish" else "Медвежий"
                ),
                "Дата и время формирования": format_datetime(block["time"]),
                "Диапазон цен": format_price_range(block["low"], block["high"]),
            }
        )
        imb_count = 1
        for imb in imbalances:
            if imb["type"] != block["type"]:
                continue
            tol_low = block["low"] - abs(block["low"]) * PRICE_TOLERANCE
            tol_high = block["high"] + abs(block["high"]) * PRICE_TOLERANCE
            if imb["high"] < tol_low or imb["low"] > tol_high:
                continue
            clipped = clip_imbalance_to_block(imb, block)
            result_rows.append(
                {
                    "Порядковый номер": f"{row_number}.{imb_count}",
                    "Формация (ордер блок или имбаланс)": "Имбаланс",
                    "Направление (тип)": (
                        "Бычий" if imb["type"] == "bullish" else "Медвежий"
                    ),
                    "Дата и время формирования": format_datetime(imb["time"]),
                    "Диапазон цен": format_price_range(clipped["low"], clipped["high"]),
                }
            )
            imb_count += 1
        row_number += 1

    result_df = pd.DataFrame(result_rows, columns=columns)
    result_df.to_excel("result.xlsx", index=False)
    print("Результат сохранён в result.xlsx")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Сборка проекта для ДЭ 09.02.07, Модуль 1.
Создаёт:
  - ERD_module_1.pdf  (ER-диаграмма)
  - db.sqlite         (база данных SQLite)
  - импортирует данные из xlsx, если они есть рядом
Запуск:
    python build_project.py
"""

import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite")
ERD_PATH = os.path.join(BASE_DIR, "ERD_module_1.pdf")

# ---------------------------------------------------------------------------
# 1. ER-диаграмма
# ---------------------------------------------------------------------------

ERD_DOT = """
digraph ERD {
    rankdir=LR;
    node [shape=plaintext, fontname="Arial"];
    edge [fontname="Arial", fontsize=10];

    roles [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#cccccc"><B>roles</B></TD></TR>
        <TR><TD PORT="role_id">role_id (PK)</TD></TR>
        <TR><TD>role_name</TD></TR>
    </TABLE>>];

    users [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#cccccc"><B>users</B></TD></TR>
        <TR><TD PORT="user_id">user_id (PK)</TD></TR>
        <TR><TD>last_name</TD></TR>
        <TR><TD>first_name</TD></TR>
        <TR><TD>middle_name</TD></TR>
        <TR><TD>login</TD></TR>
        <TR><TD PORT="role_id">role_id (FK)</TD></TR>
    </TABLE>>];

    products [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#cccccc"><B>products</B></TD></TR>
        <TR><TD PORT="product_id">product_id (PK)</TD></TR>
        <TR><TD>category</TD></TR>
        <TR><TD>subcategory</TD></TR>
        <TR><TD>image_path</TD></TR>
        <TR><TD>product_name</TD></TR>
        <TR><TD>manufacturer</TD></TR>
        <TR><TD>description</TD></TR>
        <TR><TD>composition</TD></TR>
        <TR><TD>price</TD></TR>
    </TABLE>>];

    sizes [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#cccccc"><B>sizes</B></TD></TR>
        <TR><TD PORT="size_id">size_id (PK)</TD></TR>
        <TR><TD>size_value</TD></TR>
    </TABLE>>];

    stock_items [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#cccccc"><B>stock_items</B></TD></TR>
        <TR><TD PORT="stock_item_id">stock_item_id (PK)</TD></TR>
        <TR><TD PORT="product_id">product_id (FK)</TD></TR>
        <TR><TD PORT="size_id">size_id (FK)</TD></TR>
        <TR><TD>quantity_available</TD></TR>
    </TABLE>>];

    orders [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#cccccc"><B>orders</B></TD></TR>
        <TR><TD PORT="order_id">order_id (PK)</TD></TR>
        <TR><TD>order_date</TD></TR>
        <TR><TD PORT="user_id">user_id (FK)</TD></TR>
    </TABLE>>];

    order_items [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD BGCOLOR="#cccccc"><B>order_items</B></TD></TR>
        <TR><TD PORT="order_item_id">order_item_id (PK)</TD></TR>
        <TR><TD PORT="order_id">order_id (FK)</TD></TR>
        <TR><TD PORT="product_id">product_id (FK)</TD></TR>
        <TR><TD PORT="size_id">size_id (FK)</TD></TR>
        <TR><TD>quantity</TD></TR>
        <TR><TD>price</TD></TR>
    </TABLE>>];

    roles:role_id -> users:role_id [label="1 : M"];
    users:user_id -> orders:user_id [label="1 : M"];
    orders:order_id -> order_items:order_id [label="1 : M"];
    products:product_id -> stock_items:product_id [label="1 : M"];
    sizes:size_id -> stock_items:size_id [label="1 : M"];
    products:product_id -> order_items:product_id [label="1 : M"];
    sizes:size_id -> order_items:size_id [label="1 : M"];
}
"""


def build_erd():
    """Пытается собрать ERD_module_1.pdf через graphviz, иначе через matplotlib."""
    try:
        from graphviz import Source
        src = Source(ERD_DOT)
        src.render(
            filename=os.path.splitext(os.path.basename(ERD_PATH))[0],
            directory=BASE_DIR,
            format="pdf",
            cleanup=True,
        )
        print(f"[OK] ER-диаграмма: {ERD_PATH}")
        return
    except Exception as e:
        print(f"[i] graphviz недоступен ({e}), рисую через matplotlib...")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

        tables = {
            "roles":       ["role_id (PK)", "role_name"],
            "users":       ["user_id (PK)", "last_name", "first_name",
                            "middle_name", "login", "role_id (FK)"],
            "products":    ["product_id (PK)", "category", "subcategory",
                            "image_path", "product_name", "manufacturer",
                            "description", "composition", "price"],
            "sizes":       ["size_id (PK)", "size_value"],
            "stock_items": ["stock_item_id (PK)", "product_id (FK)",
                            "size_id (FK)", "quantity_available"],
            "orders":      ["order_id (PK)", "order_date", "user_id (FK)"],
            "order_items": ["order_item_id (PK)", "order_id (FK)",
                            "product_id (FK)", "size_id (FK)",
                            "quantity", "price"],
        }

        positions = {
            "roles":       (0.05, 0.80),
            "users":       (0.30, 0.80),
            "orders":      (0.55, 0.80),
            "order_items": (0.80, 0.80),
            "products":    (0.05, 0.30),
            "sizes":       (0.35, 0.30),
            "stock_items": (0.65, 0.30),
        }

        fig, ax = plt.subplots(figsize=(18, 10))
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

        boxes = {}
        row_h = 0.035
        for name, cols in tables.items():
            x, y = positions[name]
            h = row_h * (len(cols) + 1)
            w = 0.18
            box = FancyBboxPatch((x, y - h), w, h,
                                 boxstyle="round,pad=0.005",
                                 linewidth=1.2, edgecolor="black",
                                 facecolor="#f5f5f5")
            ax.add_patch(box)
            ax.text(x + w / 2, y - row_h / 2, name, ha="center",
                    va="center", fontsize=11, fontweight="bold")
            for i, col in enumerate(cols):
                ax.text(x + 0.01, y - row_h * (i + 1.5), col,
                        ha="left", va="center", fontsize=8)
            boxes[name] = (x, y, w, h)

        def link(a, b, label):
            xa, ya, wa, ha = boxes[a]
            xb, yb, wb, hb = boxes[b]
            ax.add_patch(FancyArrowPatch(
                (xa + wa, ya - ha / 2), (xb, yb - hb / 2),
                arrowstyle="-|>", mutation_scale=12,
                linewidth=1, color="#444"))
            ax.text((xa + wa + xb) / 2, (ya - ha / 2 + yb - hb / 2) / 2,
                    label, fontsize=8, color="#444")

        link("roles", "users", "1:M")
        link("users", "orders", "1:M")
        link("orders", "order_items", "1:M")
        link("products", "stock_items", "1:M")
        link("sizes", "stock_items", "1:M")
        link("products", "order_items", "1:M")
        link("sizes", "order_items", "1:M")

        plt.savefig(ERD_PATH, bbox_inches="tight")
        plt.close()
        print(f"[OK] ER-диаграмма: {ERD_PATH}")
    except Exception as e:
        print(f"[!] Не удалось создать ER-диаграмму: {e}")


# ---------------------------------------------------------------------------
# 2. Создание БД
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS stock_items;
DROP TABLE IF EXISTS sizes;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    role_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name   VARCHAR(50) NOT NULL,
    first_name  VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    login       VARCHAR(50) NOT NULL UNIQUE,
    role_id     INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category     VARCHAR(50),
    subcategory  VARCHAR(50),
    image_path   VARCHAR(255),
    product_name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    description  TEXT,
    composition  TEXT,
    price        NUMERIC(10,2) NOT NULL
);

CREATE TABLE sizes (
    size_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    size_value VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE stock_items (
    stock_item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id         INTEGER NOT NULL,
    size_id            INTEGER NOT NULL,
    quantity_available INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (size_id)    REFERENCES sizes(size_id),
    UNIQUE (product_id, size_id)
);

CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date DATE NOT NULL,
    user_id    INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    size_id       INTEGER NOT NULL,
    quantity      INTEGER NOT NULL,
    price         NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (size_id)    REFERENCES sizes(size_id)
);
"""

SEED_SQL = """
INSERT INTO roles (role_name) VALUES ('admin'), ('client');

INSERT INTO users (last_name, first_name, middle_name, login, role_id) VALUES
('Иванов','Иван','Иванович','ivanov',2),
('Петров','Пётр','Петрович','petrov',2),
('Админов','Админ',NULL,'admin',1);

INSERT INTO products
(category, subcategory, image_path, product_name, manufacturer, description, composition, price) VALUES
('Обувь','Кроссовки','img/sneaker1.png','Кроссовки RunFast','RunCo','Лёгкие беговые','Текстиль',5990.00),
('Обувь','Ботинки','img/boot1.png','Ботинки WinterPro','WinterCo','Тёплые','Кожа',8990.00);

INSERT INTO sizes (size_value) VALUES ('39'),('40'),('41'),('42'),('43');

INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES
(1,1,10),(1,2,5),(1,3,0),(1,4,7),
(2,3,4),(2,4,3),(2,5,2);

INSERT INTO orders (order_date, user_id) VALUES
('2026-10-10', 1),
('2026-10-11', 2);

INSERT INTO order_items (order_id, product_id, size_id, quantity, price) VALUES
(1,1,2,1,5990.00),
(1,2,4,1,8990.00),
(2,1,4,2,5990.00);
"""


def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)
    conn.executescript(SEED_SQL)
    conn.commit()
    conn.close()
    print(f"[OK] База данных: {DB_PATH}")


# ---------------------------------------------------------------------------
# 3. Импорт xlsx
# ---------------------------------------------------------------------------

IMPORT_MAP = [
    # (файл, таблица, приоритет)
    ("Sizes_import.xlsx",       "sizes",       1),
    ("Products_import.xlsx",    "products",    1),
    ("Users_import.xlsx",       "users",       1),
    ("Stock_Items_import.xlsx", "stock_items", 2),
    ("Orders_import.xlsx",      "orders",      2),
]


def import_xlsx():
    try:
        import pandas as pd
    except ImportError:
        print("[!] pandas не установлен — импорт xlsx пропущен. "
              "Установите: pip install pandas openpyxl")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    # Сначала очищаем таблицы, куда будем лить из xlsx,
    # чтобы не смешивать тестовые данные с реальными.
    order_of_clear = [
        "order_items", "orders", "stock_items",
        "users", "products", "sizes",
    ]
    for t in order_of_clear:
        conn.execute(f"DELETE FROM {t};")
    conn.execute("DELETE FROM roles;")
    conn.execute("INSERT INTO roles (role_name) VALUES ('admin'), ('client');")
    conn.commit()

    for filename, table, _prio in IMPORT_MAP:
        path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(path):
            print(f"[i] нет файла {filename}, пропуск")
            continue
        try:
            df = pd.read_excel(path)
            df.to_sql(table, conn, if_exists="append", index=False)
            print(f"[OK] Импорт {filename} -> {table} ({len(df)} строк)")
        except Exception as e:
            print(f"[!] Ошибка импорта {filename}: {e}")

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    print("=== Сборка проекта Модуль 1 ===")
    build_erd()
    build_db()
    import_xlsx()

    print()
    print("Готово. Файлы рядом со скриптом:")
    print(f"  - {os.path.basename(ERD_PATH)}")
    print(f"  - {os.path.basename(DB_PATH)}")
    print()
    print("Дальше:")
    print("  1. Откройте «Автотест», выберите Модуль 1.")
    print("  2. Укажите папку проекта (где лежит db.sqlite).")
    print("  3. Прогоните все проверки и впишите контрольные суммы.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[X] Критическая ошибка: {e}")
        sys.exit(1)
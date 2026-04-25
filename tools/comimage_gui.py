#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コマンド画像 D&Dツール  (tools/comimage_gui.py)

各コマンドスロットに画像をドラッグ＆ドロップするだけで
  resources/chara_XX/<stem>[<suffix>].ext
に自動コピーします。

【依存ライブラリ】Windowsで pip install:
  pip install tkinterdnd2 Pillow

  tkinterdnd2 がなければダブルクリックでファイルダイアログ（DnD不可）
  Pillow     がなければサムネイル非表示（色でファイル有無を表示）

【起動】
  python tools/comimage_gui.py
"""

import sys
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES  # type: ignore
    _HAS_DND = True
except ImportError:
    _HAS_DND = False

try:
    from PIL import Image, ImageTk  # type: ignore
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

sys.path.insert(0, str(Path(__file__).parent))
from rename_comimg import COMMANDS, VALID_EXTS  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent


def _chara_dir(cno: int) -> Path:
    return REPO_ROOT / "resources" / f"chara_{cno:02d}"


# ── キャラ一覧 ──────────────────────────────────────────────────
CHARAS: list[tuple[int, str]] = [
    (1,  "三善かなえ"),  (2,  "北川ゆき"),    (3,  "小野ちよ"),    (4,  "早川きこ"),
    (5,  "桃智あすか"),  (6,  "藍乃あいか"),  (7,  "高原ちあき"),  (8,  "丸子みさき"),
    (9,  "月永るか"),    (10, "木之下ゆゆ"),  (11, "氷野くるみ"),  (12, "神樹いちか"),
    (13, "羽森つばさ"),  (14, "花音ことり"),  (15, "長町やえ"),    (16, "大虎いさみ"),
    (17, "小鳩あずさ"),  (18, "熊沢ひめの"),  (19, "猫塚みけ"),    (20, "藤猪しずく"),
    (21, "雉子すみれ"),  (22, "鯱いかり"),    (23, "鶯木こはる"),  (24, "三波なつみ"),
    (25, "八朔つゆり"),  (26, "堀田さあや"),  (27, "夏野ゆり"),    (28, "星海こよい"),
    (29, "春風なな"),    (30, "長居ゆう"),    (31, "夢路まりあ"),  (32, "安条まい"),
    (33, "柊るな"),      (34, "桐島かいり"),  (35, "梅園かな"),    (36, "遠見ちか"),
    (37, "龍泉寺レンレン"), (38, "クー・カロア"), (39, "冴木もも"), (40, "夜霧はやて"),
    (41, "悠木ともこ"),  (42, "榊むつみ"),    (43, "砂賀みどり"),  (44, "笹芽ひよの"),
    (45, "円城寺れいか"), (46, "双葉みづき"), (47, "双葉みなづき"), (48, "四方みつる"),
    (49, "小松ぼたん"),  (50, "山條ぎん"),    (51, "御影かすみ"),  (52, "湖南やこ"),
    (53, "花丘まり"),    (54, "久坂あやめ"),  (55, "伊藤さくら"),  (56, "八壁ひかる"),
    (57, "岩戸サン"),    (58, "天宮るり"),    (59, "水嶌うしお"),  (60, "瀬川かえで"),
    (61, "鶴海ひまり"),  (62, "黒森すず"),    (63, "八雲ちづる"),  (64, "峰山しおん"),
    (65, "時国そら"),    (66, "曽根セイラ"),  (67, "日滝ましろ"),  (68, "深鳥ふみ"),
    (69, "神樹はじめ"),  (70, "神無月ほとり"), (71, "棗ひびき"),
]

VARIANTS: list[tuple[str, str]] = [
    ("通常",    ""),
    ("_1",     "_1"),
    ("_2",     "_2"),
    ("恋慕",   "_renbo"),
]

CATEGORIES: list[tuple[str, list]] = [
    ("純愛コミュニケーション系  COM300〜399",
     [c for c in COMMANDS if 300 <= c[0] <= 399]),
    ("ウフフ通常系  COM0〜257",
     [c for c in COMMANDS if 0 <= c[0] <= 257]),
    ("独自コマンド",
     [c for c in COMMANDS if (280 <= c[0] <= 284) or (c[0] >= 410)]),
]

THUMB_W, THUMB_H = 80, 80
COLS = 5

# カラーパレット（ダーク）
C_BG       = "#1e1e1e"
C_BAR      = "#252526"
C_SLOT     = "#2d2d30"
C_SLOT_H   = "#3e3e42"   # hover
C_SLOT_S   = "#1e3320"   # 画像あり
C_SLOT_SH  = "#2e4330"   # 画像あり + hover
C_CAT      = "#3c3c3c"
C_FG       = "#d4d4d4"
C_DIM      = "#888888"
C_OK       = "#4ec994"
C_WARN     = "#ce9178"


def _parse_drop(data: str) -> list[str]:
    """tkinterdnd2 ドロップデータ → ファイルパスリスト"""
    paths: list[str] = []
    data = data.strip()
    while data:
        if data.startswith("{"):
            end = data.find("}")
            if end < 0:
                paths.append(data[1:])
                break
            paths.append(data[1:end])
            data = data[end + 1:].strip()
        else:
            paths.extend(data.split())
            break
    return [p for p in paths if p]


# ──────────────────────────────────────────────────────────────────
class SlotWidget(tk.Frame):
    """1コマンド分のスロット（サムネイル + 名前ラベル）"""

    def __init__(self, parent: tk.Widget, cid: int, jname: str, stem: str,
                 app: "App", **kw):
        super().__init__(parent, bg=C_SLOT, bd=1, relief=tk.FLAT,
                         padx=3, pady=3, **kw)
        self.cid, self.jname, self.stem, self.app = cid, jname, stem, app
        self._has_img = False
        self._photo = None  # GC対策

        # サムネイルキャンバス
        self.cnv = tk.Canvas(self, width=THUMB_W, height=THUMB_H,
                             bg="#111111", highlightthickness=1,
                             highlightbackground="#555", cursor="hand2")
        self.cnv.pack()

        # コマンド名ラベル
        short = jname[:8] + "…" if len(jname) > 9 else jname
        self.lbl = tk.Label(self, text=f"COM{cid}\n{short}",
                            font=("", 7), bg=C_SLOT, fg=C_DIM,
                            wraplength=THUMB_W + 2, justify=tk.CENTER)
        self.lbl.pack(fill=tk.X)

        self._bind_all()
        self.refresh()

    def _bind_all(self):
        ws = [self, self.cnv, self.lbl]
        if _HAS_DND:
            for w in ws:
                w.drop_target_register(DND_FILES)
                w.dnd_bind("<<Drop>>", self._on_drop)
        for w in ws:
            w.bind("<Double-Button-1>", self._on_dblclick)
            w.bind("<Enter>",           self._on_enter)
            w.bind("<Leave>",           self._on_leave)

    # ── hover ──
    def _set_bg(self, bg: str):
        self.config(bg=bg)
        self.lbl.config(bg=bg)

    def _on_enter(self, _=None):
        self._set_bg(C_SLOT_SH if self._has_img else C_SLOT_H)

    def _on_leave(self, _=None):
        self._set_bg(C_SLOT_S if self._has_img else C_SLOT)

    # ── DnD / ダブルクリック ──
    def _on_drop(self, event):
        paths = _parse_drop(event.data)
        if paths:
            self._place(Path(paths[0]))

    def _on_dblclick(self, _=None):
        p = filedialog.askopenfilename(
            title=f"COM{self.cid} {self.jname} の画像を選択",
            filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.bmp"),
                       ("すべてのファイル", "*.*")],
        )
        if p:
            self._place(Path(p))

    # ── ファイル配置 ──
    def _dst(self, src_ext: str) -> Path:
        return _chara_dir(self.app.cno) / (
            self.stem + self.app.variant_suffix + src_ext.lower()
        )

    def _find_existing(self):
        d = _chara_dir(self.app.cno)
        base = self.stem + self.app.variant_suffix
        for ext in (".png", ".jpg", ".jpeg", ".bmp"):
            p = d / (base + ext)
            if p.exists():
                return p
        return None

    def _place(self, src: Path):
        if src.suffix.lower() not in VALID_EXTS:
            self.app.status(f"⚠  未対応の拡張子: {src.suffix}  ({src.name})", warn=True)
            return
        dst = self._dst(src.suffix)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        self.app.status(f"✓  {src.name}  →  {dst.relative_to(REPO_ROOT)}")
        self.refresh()

    # ── サムネイル更新 ──
    def refresh(self):
        p = self._find_existing()
        self._has_img = p is not None
        self._set_bg(C_SLOT_S if self._has_img else C_SLOT)
        self.cnv.delete("all")
        self._photo = None

        if p and _HAS_PIL:
            try:
                img = Image.open(p)
                img.thumbnail((THUMB_W, THUMB_H), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self._photo = photo
                self.cnv.config(bg="#111111")
                self.cnv.create_image(THUMB_W // 2, THUMB_H // 2,
                                      image=photo, anchor=tk.CENTER)
                return
            except Exception:
                pass

        cx, cy = THUMB_W // 2, THUMB_H // 2
        if self._has_img:
            self.cnv.config(bg="#1a3a1a")
            self.cnv.create_text(cx, cy, text="画像あり",
                                 fill=C_OK, font=("", 8))
        else:
            self.cnv.config(bg="#111111")
            hint = ("D&D\nまたは\nダブルクリック" if _HAS_DND
                    else "ダブルクリックで\nファイル選択")
            self.cnv.create_text(cx, cy, text=hint,
                                 fill="#555555", font=("", 7), justify=tk.CENTER)


# ──────────────────────────────────────────────────────────────────
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("コマンド画像 D&Dツール — eraあんガル")
        root.geometry("980x740")
        root.configure(bg=C_BG)
        root.option_add("*TCombobox*Listbox.font", ("", 9))

        self.cno: int = 1
        self.variant_suffix: str = ""
        self._slots: list[SlotWidget] = []

        self._build_topbar()
        self._build_main()
        self._build_statusbar()
        self._build_slots()

    # ── UI構築 ──────────────────────────────────────────────
    def _build_topbar(self):
        bar = tk.Frame(self.root, bg=C_BAR, pady=6)
        bar.pack(fill=tk.X)

        tk.Label(bar, text="キャラ:", bg=C_BAR, fg=C_FG,
                 font=("", 9)).pack(side=tk.LEFT, padx=(10, 2))

        chara_vals = [f"{n:02d}  {nm}" for n, nm in CHARAS]
        self._chara_var = tk.StringVar(value=chara_vals[0])
        cb = ttk.Combobox(bar, textvariable=self._chara_var,
                          values=chara_vals, state="readonly",
                          width=20, font=("", 9))
        cb.pack(side=tk.LEFT, padx=4)
        cb.bind("<<ComboboxSelected>>", self._on_chara)

        tk.Label(bar, text="バリアント:", bg=C_BAR, fg=C_FG,
                 font=("", 9)).pack(side=tk.LEFT, padx=(18, 4))
        self._var_var = tk.StringVar(value="")
        for label, suffix in VARIANTS:
            rb = tk.Radiobutton(bar, text=label, variable=self._var_var,
                                value=suffix, bg=C_BAR, fg=C_FG,
                                selectcolor="#444", activebackground=C_BAR,
                                activeforeground=C_FG, font=("", 9),
                                command=self._on_variant)
            rb.pack(side=tk.LEFT, padx=3)

        tk.Button(bar, text="↺ 更新", bg="#404040", fg=C_FG,
                  relief=tk.FLAT, padx=6, font=("", 8), cursor="hand2",
                  command=self._refresh_all).pack(side=tk.LEFT, padx=(14, 0))

        dnd_text = "● DnD有効" if _HAS_DND else "○ DnD無効  (pip install tkinterdnd2)"
        dnd_fg   = C_OK if _HAS_DND else C_WARN
        tk.Label(bar, text=dnd_text, bg=C_BAR, fg=dnd_fg,
                 font=("", 8)).pack(side=tk.RIGHT, padx=10)

    def _build_main(self):
        outer = tk.Frame(self.root, bg=C_BG)
        outer.pack(fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(outer, bg=C_BG, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient=tk.VERTICAL,
                            command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(fill=tk.BOTH, expand=True)

        self._inner = tk.Frame(self._canvas, bg=C_BG)
        self._cwin = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw")
        self._inner.bind(
            "<Configure>",
            lambda e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")))
        self._canvas.bind(
            "<Configure>",
            lambda e: self._canvas.itemconfig(self._cwin, width=e.width))
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self._canvas.bind(seq, self._on_scroll)

    def _build_statusbar(self):
        self._status_var = tk.StringVar(value="準備完了")
        self._status_lbl = tk.Label(
            self.root, textvariable=self._status_var,
            bg="#111111", fg=C_DIM, anchor=tk.W, padx=10, font=("", 8))
        self._status_lbl.pack(fill=tk.X, side=tk.BOTTOM)

    def _build_slots(self):
        for w in self._inner.winfo_children():
            w.destroy()
        self._slots.clear()

        row = 0
        for cat_name, cmds in CATEGORIES:
            if not cmds:
                continue
            hdr = tk.Label(self._inner, text=cat_name,
                           bg=C_CAT, fg=C_FG, font=("", 9, "bold"),
                           anchor=tk.W, padx=10, pady=4)
            hdr.grid(row=row, column=0, columnspan=COLS,
                     sticky="ew", pady=(10, 2))
            row += 1

            col = 0
            for cid, jname, stem in sorted(cmds, key=lambda x: x[0]):
                slot = SlotWidget(self._inner, cid, jname, stem, self)
                slot.grid(row=row, column=col, padx=3, pady=3)
                self._slots.append(slot)
                col += 1
                if col >= COLS:
                    col = 0
                    row += 1
            if col:
                row += 1

        for c in range(COLS):
            self._inner.columnconfigure(c, weight=1)

    # ── イベント ─────────────────────────────────────────────
    def _on_chara(self, _=None):
        val = self._chara_var.get()
        self.cno = int(val.split()[0])
        self._refresh_all()
        self.status(f"キャラ切替: {val.strip()}")

    def _on_variant(self):
        self.variant_suffix = self._var_var.get()
        self._refresh_all()
        label = next(l for l, s in VARIANTS if s == self.variant_suffix)
        self.status(f"バリアント: {label}")

    def _refresh_all(self):
        for s in self._slots:
            s.refresh()

    def _on_scroll(self, event):
        if event.num == 4:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self._canvas.yview_scroll(1, "units")
        else:
            self._canvas.yview_scroll(int(-event.delta / 120), "units")

    def status(self, msg: str, warn: bool = False):
        self._status_var.set(msg)
        self._status_lbl.config(fg=C_WARN if warn else C_OK)
        self.root.update_idletasks()


# ──────────────────────────────────────────────────────────────────
def main():
    if _HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コマンド画像 / 顔グラ D&Dツール  (tools/comimage_gui.py)

【依存ライブラリ】Windowsで pip install:
  pip install tkinterdnd2 Pillow
"""

import sys
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog

_DND_ERR = ""
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES  # type: ignore
    _HAS_DND = True
except Exception as _e:
    _HAS_DND = False
    _DND_ERR = str(_e)

try:
    from PIL import Image, ImageTk  # type: ignore
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

sys.path.insert(0, str(Path(__file__).parent))
from rename_comimg import COMMANDS, VALID_EXTS  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent
RESOURCES  = REPO_ROOT / "resources"
FACE_CSV   = RESOURCES / "face.csv"


def _chara_dir(cno: int) -> Path:
    return RESOURCES / f"chara_{cno:02d}"


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
    ("通常_1", "_1"),
    ("通常_2", "_2"),
    ("通常_3", "_3"),
    ("恋慕_1", "_renbo_1"),
    ("恋慕_2", "_renbo_2"),
    ("恋慕_3", "_renbo_3"),
]

CATEGORIES: list[tuple[str, list]] = [
    ("純愛コミュニケーション系  COM300〜399",
     [c for c in COMMANDS if 300 <= c[0] <= 399]),
    ("ウフフ通常系  COM0〜257",
     [c for c in COMMANDS if 0 <= c[0] <= 257]),
    ("独自コマンド",
     [c for c in COMMANDS if (280 <= c[0] <= 284) or (c[0] >= 410)]),
]

THUMB_W, THUMB_H = 96, 96
FACE_W,  FACE_H  = 110, 130   # 顔グラスロットサイズ
COLS     = 5
FACE_COLS = 8

C_BG       = "#1e1e1e"
C_BAR      = "#252526"
C_SLOT     = "#2d2d30"
C_SLOT_H   = "#3e3e42"
C_SLOT_S   = "#1e3320"
C_SLOT_SH  = "#2e4330"
C_CAT      = "#3c3c3c"
C_FG       = "#d4d4d4"
C_DIM      = "#888888"
C_OK       = "#4ec994"
C_WARN     = "#ce9178"
C_TAB_ACT  = "#007acc"
C_TAB_INACT= "#3c3c3c"


def _parse_drop(data: str) -> list[str]:
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


def _load_face_csv() -> dict[int, str]:
    """face.csv を読み込み {cno: filename} を返す"""
    mapping: dict[int, str] = {}
    if not FACE_CSV.exists():
        return mapping
    with open(FACE_CSV, "rb") as f:
        text = f.read().decode("cp932")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        parts = line.split(",")
        if len(parts) < 2:
            continue
        resource = parts[0].strip()   # "face_01"
        filename = parts[1].strip()   # "face_37.png"
        # resource名からcnoを抽出
        if resource.startswith("face_"):
            try:
                cno = int(resource[5:])
                mapping[cno] = filename
            except ValueError:
                pass
    return mapping


def _save_face_csv(mapping: dict[int, str]):
    """face.csv を書き出す"""
    lines = [
        ";eraあんガル 顔グラフィックスプライト定義",
        ";リソース名,ファイル名（ファイルはcno順＝ゲーム内ID順で命名されている前提）",
    ]
    for cno in sorted(mapping.keys()):
        resource = f"face_{cno:02d}"
        lines.append(f"{resource},{mapping[cno]}")
    text = "\r\n".join(lines) + "\r\n"
    with open(FACE_CSV, "wb") as f:
        f.write(text.encode("cp932"))


# ──────────────────────────────────────────────────────────────────
class SlotWidget(tk.Frame):
    """コマンド画像スロット"""

    def __init__(self, parent, cid, jname, stem, app, **kw):
        super().__init__(parent, bg=C_SLOT, bd=1, relief=tk.FLAT,
                         padx=3, pady=3, **kw)
        self.cid, self.jname, self.stem, self.app = cid, jname, stem, app
        self._has_img = False
        self._photo = None

        self.cnv = tk.Canvas(self, width=THUMB_W, height=THUMB_H,
                             bg="#111111", highlightthickness=1,
                             highlightbackground="#555", cursor="hand2")
        self.cnv.pack()

        short = jname[:8] + "…" if len(jname) > 9 else jname
        self.lbl = tk.Label(self, text=f"COM{cid}\n{short}",
                            font=("", 10), bg=C_SLOT, fg=C_DIM,
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

    def _set_bg(self, bg):
        self.config(bg=bg)
        self.lbl.config(bg=bg)

    def _on_enter(self, _=None):
        self._set_bg(C_SLOT_SH if self._has_img else C_SLOT_H)

    def _on_leave(self, _=None):
        self._set_bg(C_SLOT_S if self._has_img else C_SLOT)

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

    def _dst(self, src_ext):
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

    def _place(self, src):
        if src.suffix.lower() not in VALID_EXTS:
            self.app.status(f"⚠  未対応の拡張子: {src.suffix}", warn=True)
            return
        dst = self._dst(src.suffix)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        self.app.status(f"✓  {src.name}  →  {dst.relative_to(REPO_ROOT)}")
        self.refresh()

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
            self.cnv.create_text(cx, cy, text="画像あり", fill=C_OK, font=("", 11))
        else:
            self.cnv.config(bg="#111111")
            hint = ("D&D\nまたは\nダブルクリック" if _HAS_DND
                    else "ダブルクリックで\nファイル選択")
            self.cnv.create_text(cx, cy, text=hint,
                                 fill="#555555", font=("", 10), justify=tk.CENTER)


# ──────────────────────────────────────────────────────────────────
class FaceSlotWidget(tk.Frame):
    """顔グラスロット（キャラ1人分）"""

    def __init__(self, parent, cno: int, name: str, app: "App", **kw):
        super().__init__(parent, bg=C_SLOT, bd=1, relief=tk.FLAT,
                         padx=2, pady=2, **kw)
        self.cno, self.name, self.app = cno, name, app
        self._has_img = False
        self._photo = None

        self.cnv = tk.Canvas(self, width=FACE_W, height=FACE_H,
                             bg="#111111", highlightthickness=1,
                             highlightbackground="#555", cursor="hand2")
        self.cnv.pack()

        short = name[3:] if len(name) > 4 else name  # 姓を省く
        self.lbl = tk.Label(self, text=f"No.{cno:02d}\n{short}",
                            font=("", 9), bg=C_SLOT, fg=C_DIM,
                            wraplength=FACE_W, justify=tk.CENTER)
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
            w.bind("<Button-3>",        self._on_rclick)

    def _set_bg(self, bg):
        self.config(bg=bg)
        self.lbl.config(bg=bg)

    def _on_enter(self, _=None):
        self._set_bg(C_SLOT_SH if self._has_img else C_SLOT_H)

    def _on_leave(self, _=None):
        self._set_bg(C_SLOT_S if self._has_img else C_SLOT)

    def _on_drop(self, event):
        paths = _parse_drop(event.data)
        if paths:
            self._place(Path(paths[0]))

    def _on_dblclick(self, _=None):
        p = filedialog.askopenfilename(
            title=f"No.{self.cno:02d} {self.name} の顔グラを選択",
            filetypes=[("PNG", "*.png"), ("画像ファイル", "*.jpg *.jpeg *.bmp"),
                       ("すべてのファイル", "*.*")],
        )
        if p:
            self._place(Path(p))

    def _on_rclick(self, _=None):
        """右クリック → 現在の設定を確認"""
        mapping = _load_face_csv()
        fname = mapping.get(self.cno, "(未設定)")
        exists = (RESOURCES / fname).exists() if fname != "(未設定)" else False
        status = "✓ ファイルあり" if exists else "✗ ファイルなし"
        self.app.status(
            f"No.{self.cno:02d} {self.name}  →  {fname}  [{status}]"
        )

    def _place(self, src: Path):
        if src.suffix.lower() not in VALID_EXTS:
            self.app.status(f"⚠  未対応の拡張子: {src.suffix}", warn=True)
            return

        mapping = _load_face_csv()
        # 既存マッピングがあればそのファイル名を使う。なければ face_NN.png を生成
        if self.cno in mapping:
            target_name = mapping[self.cno]
            # 拡張子を合わせる（元が.pngでないなら変更）
            stem = Path(target_name).stem
            target_name = stem + src.suffix.lower()
            mapping[self.cno] = target_name
        else:
            target_name = f"face_{self.cno:02d}{src.suffix.lower()}"
            mapping[self.cno] = target_name

        dst = RESOURCES / target_name
        RESOURCES.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        _save_face_csv(mapping)
        self.app.status(
            f"✓  {src.name}  →  resources/{target_name}  (face.csv 更新済み)"
        )
        self.refresh()

    def _find_existing(self) -> Path | None:
        mapping = _load_face_csv()
        fname = mapping.get(self.cno)
        if fname:
            p = RESOURCES / fname
            if p.exists():
                return p
            # 同stemで別拡張子も試す
            stem = Path(fname).stem
            for ext in (".png", ".jpg", ".jpeg", ".bmp"):
                p2 = RESOURCES / (stem + ext)
                if p2.exists():
                    return p2
        return None

    def refresh(self):
        p = self._find_existing()
        self._has_img = p is not None
        self._set_bg(C_SLOT_S if self._has_img else C_SLOT)
        self.cnv.delete("all")
        self._photo = None

        if p and _HAS_PIL:
            try:
                img = Image.open(p)
                img.thumbnail((FACE_W, FACE_H), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self._photo = photo
                self.cnv.config(bg="#111111")
                self.cnv.create_image(FACE_W // 2, FACE_H // 2,
                                      image=photo, anchor=tk.CENTER)
                return
            except Exception:
                pass

        cx, cy = FACE_W // 2, FACE_H // 2
        if self._has_img:
            self.cnv.config(bg="#1a3a1a")
            self.cnv.create_text(cx, cy, text="画像あり", fill=C_OK, font=("", 11))
        else:
            self.cnv.config(bg="#111111")
            hint = ("D&D / ダブルクリック" if _HAS_DND else "ダブルクリック")
            self.cnv.create_text(cx, cy, text=hint,
                                 fill="#555555", font=("", 9), justify=tk.CENTER)


# ──────────────────────────────────────────────────────────────────
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("コマンド画像 / 顔グラ D&Dツール — eraあんガル")
        root.geometry("1280x900")
        root.configure(bg=C_BG)
        root.option_add("*TCombobox*Listbox.font", ("", 12))

        self.cno: int = 1
        self.variant_suffix: str = "_1"
        self._slots: list[SlotWidget] = []
        self._face_slots: list[FaceSlotWidget] = []
        self._active_tab = tk.StringVar(value="com")

        self._build_tabbar()
        self._build_com_frame()
        self._build_face_frame()
        self._build_statusbar()
        self._switch_tab("com")
        # スクロールは1か所でまとめてバインド（bind_allの上書き問題を回避）
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.root.bind_all(seq, self._on_scroll)

    # ── タブバー ──────────────────────────────────────────────
    def _build_tabbar(self):
        self._tabbar = tk.Frame(self.root, bg=C_BAR, pady=0)
        self._tabbar.pack(fill=tk.X, side=tk.TOP)

        self._tab_btns: dict[str, tk.Button] = {}
        for key, label in [("com", "📷  コマンド画像"), ("face", "🖼  顔グラ")]:
            btn = tk.Button(
                self._tabbar, text=label, bg=C_TAB_INACT, fg=C_FG,
                relief=tk.FLAT, padx=16, pady=6, font=("", 12, "bold"),
                cursor="hand2", bd=0, activebackground=C_TAB_ACT,
                command=lambda k=key: self._switch_tab(k),
            )
            btn.pack(side=tk.LEFT)
            self._tab_btns[key] = btn

        if _HAS_DND:
            dnd_text, dnd_fg = "● DnD有効", C_OK
        elif _DND_ERR:
            dnd_text = f"○ DnD無効  ({_DND_ERR[:60]})"
            dnd_fg = C_WARN
        else:
            dnd_text, dnd_fg = "○ DnD無効  (pip install tkinterdnd2)", C_WARN
        tk.Label(self._tabbar, text=dnd_text, bg=C_BAR, fg=dnd_fg,
                 font=("", 11)).pack(side=tk.RIGHT, padx=12)

    def _switch_tab(self, key: str):
        self._active_tab.set(key)
        for k, btn in self._tab_btns.items():
            btn.config(bg=C_TAB_ACT if k == key else C_TAB_INACT)
        if key == "com":
            self._face_outer.pack_forget()
            self._com_outer.pack(fill=tk.BOTH, expand=True)
        else:
            self._com_outer.pack_forget()
            self._face_outer.pack(fill=tk.BOTH, expand=True)

    # ── コマンド画像ペイン ────────────────────────────────────
    def _build_com_frame(self):
        self._com_outer = tk.Frame(self.root, bg=C_BG)

        # トップバー
        bar = tk.Frame(self._com_outer, bg=C_BAR, pady=6)
        bar.pack(fill=tk.X)

        tk.Label(bar, text="キャラ:", bg=C_BAR, fg=C_FG,
                 font=("", 12)).pack(side=tk.LEFT, padx=(10, 2))
        chara_vals = [f"{n:02d}  {nm}" for n, nm in CHARAS]
        self._chara_var = tk.StringVar(value=chara_vals[0])
        cb = ttk.Combobox(bar, textvariable=self._chara_var,
                          values=chara_vals, state="readonly",
                          width=24, font=("", 12))
        cb.pack(side=tk.LEFT, padx=4)
        cb.bind("<<ComboboxSelected>>", self._on_chara)

        tk.Label(bar, text="バリアント:", bg=C_BAR, fg=C_FG,
                 font=("", 12)).pack(side=tk.LEFT, padx=(18, 4))
        self._var_var = tk.StringVar(value="_1")
        sep = True
        for label, suffix in VARIANTS:
            if sep and suffix.startswith("_renbo"):
                tk.Label(bar, text="|", bg=C_BAR, fg="#666").pack(side=tk.LEFT, padx=2)
                sep = False
            rb = tk.Radiobutton(bar, text=label, variable=self._var_var,
                                value=suffix, bg=C_BAR, fg=C_FG,
                                selectcolor="#444", activebackground=C_BAR,
                                activeforeground=C_FG, font=("", 11),
                                command=self._on_variant)
            rb.pack(side=tk.LEFT, padx=2)

        tk.Button(bar, text="↺ 更新", bg="#404040", fg=C_FG,
                  relief=tk.FLAT, padx=6, font=("", 11), cursor="hand2",
                  command=self._refresh_com).pack(side=tk.LEFT, padx=(14, 0))

        # スクロールエリア
        outer2 = tk.Frame(self._com_outer, bg=C_BG)
        outer2.pack(fill=tk.BOTH, expand=True)
        self._com_canvas = tk.Canvas(outer2, bg=C_BG, highlightthickness=0)
        vsb = ttk.Scrollbar(outer2, orient=tk.VERTICAL,
                            command=self._com_canvas.yview)
        self._com_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._com_canvas.pack(fill=tk.BOTH, expand=True)
        self._com_inner = tk.Frame(self._com_canvas, bg=C_BG)
        cwin = self._com_canvas.create_window((0, 0), window=self._com_inner, anchor="nw")
        self._com_inner.bind(
            "<Configure>",
            lambda e: self._com_canvas.configure(
                scrollregion=self._com_canvas.bbox("all")))
        self._com_canvas.bind(
            "<Configure>",
            lambda e: self._com_canvas.itemconfig(cwin, width=e.width))
        self._build_com_slots()

    def _build_com_slots(self):
        for w in self._com_inner.winfo_children():
            w.destroy()
        self._slots.clear()
        row = 0
        for cat_name, cmds in CATEGORIES:
            if not cmds:
                continue
            hdr = tk.Label(self._com_inner, text=cat_name,
                           bg=C_CAT, fg=C_FG, font=("", 12, "bold"),
                           anchor=tk.W, padx=10, pady=4)
            hdr.grid(row=row, column=0, columnspan=COLS,
                     sticky="ew", pady=(10, 2))
            row += 1
            col = 0
            for cid, jname, stem in sorted(cmds, key=lambda x: x[0]):
                slot = SlotWidget(self._com_inner, cid, jname, stem, self)
                slot.grid(row=row, column=col, padx=3, pady=3)
                self._slots.append(slot)
                col += 1
                if col >= COLS:
                    col = 0
                    row += 1
            if col:
                row += 1
        for c in range(COLS):
            self._com_inner.columnconfigure(c, weight=1)

    # ── 顔グラペイン ──────────────────────────────────────────
    def _build_face_frame(self):
        self._face_outer = tk.Frame(self.root, bg=C_BG)

        # 説明バー
        bar = tk.Frame(self._face_outer, bg=C_BAR, pady=8)
        bar.pack(fill=tk.X)
        tk.Label(bar,
                 text="顔グラ設定  —  各スロットにD&Dまたはダブルクリックで画像を配置  |  右クリック：ファイル情報表示",
                 bg=C_BAR, fg=C_FG, font=("", 12)).pack(side=tk.LEFT, padx=12)
        tk.Button(bar, text="↺ 更新", bg="#404040", fg=C_FG,
                  relief=tk.FLAT, padx=6, font=("", 11), cursor="hand2",
                  command=self._refresh_face).pack(side=tk.LEFT, padx=8)
        # face.csv統計
        self._face_stat = tk.Label(bar, text="", bg=C_BAR, fg=C_DIM, font=("", 11))
        self._face_stat.pack(side=tk.RIGHT, padx=12)

        # スクロールエリア
        outer2 = tk.Frame(self._face_outer, bg=C_BG)
        outer2.pack(fill=tk.BOTH, expand=True)
        self._face_canvas = tk.Canvas(outer2, bg=C_BG, highlightthickness=0)
        vsb = ttk.Scrollbar(outer2, orient=tk.VERTICAL,
                            command=self._face_canvas.yview)
        self._face_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._face_canvas.pack(fill=tk.BOTH, expand=True)
        self._face_inner = tk.Frame(self._face_canvas, bg=C_BG)
        cwin = self._face_canvas.create_window((0, 0), window=self._face_inner, anchor="nw")
        self._face_inner.bind(
            "<Configure>",
            lambda e: self._face_canvas.configure(
                scrollregion=self._face_canvas.bbox("all")))
        self._face_canvas.bind(
            "<Configure>",
            lambda e: self._face_canvas.itemconfig(cwin, width=e.width))
        self._build_face_slots()

    def _build_face_slots(self):
        for w in self._face_inner.winfo_children():
            w.destroy()
        self._face_slots.clear()

        for idx, (cno, name) in enumerate(CHARAS):
            row, col = divmod(idx, FACE_COLS)
            slot = FaceSlotWidget(self._face_inner, cno, name, self)
            slot.grid(row=row, column=col, padx=3, pady=3)
            self._face_slots.append(slot)

        for c in range(FACE_COLS):
            self._face_inner.columnconfigure(c, weight=1)

        self._update_face_stat()

    def _update_face_stat(self):
        mapping = _load_face_csv()
        total = len(CHARAS)
        exists = sum(1 for cno, _ in CHARAS
                     if any((RESOURCES / f).exists()
                            for f in [mapping.get(cno, "")]
                            if f))
        self._face_stat.config(text=f"設定済み: {exists} / {total}")

    # ── ステータスバー ────────────────────────────────────────
    def _build_statusbar(self):
        self._status_var = tk.StringVar(value="準備完了")
        self._status_lbl = tk.Label(
            self.root, textvariable=self._status_var,
            bg="#111111", fg=C_DIM, anchor=tk.W, padx=10, font=("", 11))
        self._status_lbl.pack(fill=tk.X, side=tk.BOTTOM)

    # ── イベント ─────────────────────────────────────────────
    def _on_chara(self, _=None):
        val = self._chara_var.get()
        self.cno = int(val.split()[0])
        self._refresh_com()
        self.status(f"キャラ切替: {val.strip()}")

    def _on_variant(self):
        self.variant_suffix = self._var_var.get()
        self._refresh_com()
        label = next(l for l, s in VARIANTS if s == self.variant_suffix)
        self.status(f"バリアント: {label}")

    def _refresh_com(self):
        for s in self._slots:
            s.refresh()

    def _refresh_face(self):
        for s in self._face_slots:
            s.refresh()
        self._update_face_stat()
        self.status("顔グラ一覧を更新しました")

    def _on_scroll(self, event):
        delta = -1 if event.num == 4 else (1 if event.num == 5 else int(-event.delta / 120))
        canvas = self._com_canvas if self._active_tab.get() == "com" else self._face_canvas
        canvas.yview_scroll(delta, "units")

    def status(self, msg: str, warn: bool = False):
        self._status_var.set(msg)
        self._status_lbl.config(fg=C_WARN if warn else C_OK)
        self.root.update_idletasks()


# ──────────────────────────────────────────────────────────────────
def main():
    if _HAS_DND:
        try:
            root = TkinterDnD.Tk()
        except Exception as e:
            print(f"[DnD] TkinterDnD.Tk() 失敗: {e}", file=sys.stderr)
            root = tk.Tk()
    else:
        if _DND_ERR:
            print(f"[DnD] インポート失敗: {_DND_ERR}", file=sys.stderr)
        root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

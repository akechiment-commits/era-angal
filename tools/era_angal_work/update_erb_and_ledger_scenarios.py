# -*- coding: utf-8 -*-

def update_all():
    # 1. Update ERB
    with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
        text = f.read()

    # Replacement for CHAR_58 天宮るり
    ruri_block_old = """\t\tCASE 58
\t\t\t;天宮るり (3-B / 天文部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生のひと / 弟のひと / 素:転校生くん) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生のひと"
\t\t\t\t;--- 最重要親友・幼馴染（ほとりのひと / ほとりちゃん） ---
\t\t\t\tCASE 70
\t\t\t\t\t;神無月ほとり (最愛の幼馴染・副部長)
\t\t\t\t\tRESULTS '= @"ほとりのひと"
\t\t\t\t;--- 生徒会長 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (生徒会長のひと)
\t\t\t\t\tRESULTS '= @"生徒会長のひと"
\t\t\t\t;--- 独自呼称 ---
\t\t\t\tCASE 10
\t\t\t\t\t;木之下ゆゆ (文芸部)
\t\t\t\t\tRESULTS '= @"ゆゆゆのひと"
\t\t\t\tCASE 51
\t\t\t\t\t;御影かすみ
\t\t\t\t\tRESULTS '= @"魔人のひと"
\t\t\t\tCASE 27
\t\t\t\t\t;夏野ゆり
\t\t\t\t\tRESULTS '= @"桃太郎のひと"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT"""

    ruri_block_new = """\t\tCASE 58
\t\t\t;天宮るり (3-B / 天文部部長 / 宇宙人観測者)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (基本:「転校生のひと」/理屈呼び:「弟のひと」/素:「転校生くん」) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生のひと"
\t\t\t\t;--- 最重要親友・幼馴染（ほとりのひと / 素:ほとりちゃん） ---
\t\t\t\tCASE 70
\t\t\t\t\t;神無月ほとり (最愛の幼馴染・副部長)
\t\t\t\t\tRESULTS '= @"ほとりのひと"
\t\t\t\t;--- 天文部・部活仲間 ---
\t\t\t\tCASE 28
\t\t\t\t\t;星海こよい (天文部後輩・27回登場)
\t\t\t\t\tRESULTS '= @"こよいのひと"
\t\t\t\tCASE 30
\t\t\t\t\t;長居ゆう (夜空の一等星)
\t\t\t\t\tRESULTS '= @"ゆうのひと"
\t\t\t\t;--- 生徒会長 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (生徒会長のひと・11回登場)
\t\t\t\t\tRESULTS '= @"生徒会長のひと"
\t\t\t\t;--- 親しい後輩・友人 ---
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか (23回登場)
\t\t\t\t\tRESULTS '= @"あいかのひと"
\t\t\t\tCASE 12
\t\t\t\t\t;神樹いちか (10回登場)
\t\t\t\t\tRESULTS '= @"いちかのひと"
\t\t\t\tCASE 25
\t\t\t\t\t;八朔つゆり
\t\t\t\t\tRESULTS '= @"つゆりのひと"
\t\t\t\t;--- 固有命名呼称（scenarios完全抽出） ---
\t\t\t\tCASE 10
\t\t\t\t\t;木之下ゆゆ (文芸部)
\t\t\t\t\tRESULTS '= @"ゆゆゆのひと"
\t\t\t\tCASE 27
\t\t\t\t\t;夏野ゆり (桃太郎のひと)
\t\t\t\t\tRESULTS '= @"桃太郎のひと"
\t\t\t\tCASE 51
\t\t\t\t\t;御影かすみ (魔人のひと)
\t\t\t\t\tRESULTS '= @"魔人のひと"
\t\t\t\tCASE 65
\t\t\t\t\t;時国そら (ゆんゆんのひと / 耳がいいだけのひと)
\t\t\t\t\tRESULTS '= @"ゆんゆんのひと"
\t\t\t\tCASE 68
\t\t\t\t\t;深鳥ふみ (新聞部のひと)
\t\t\t\t\tRESULTS '= @"新聞部のひと"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (生き神のひと)
\t\t\t\t\tRESULTS '= @"生き神のひと"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT"""

    if ruri_block_old in text:
        text = text.replace(ruri_block_old, ruri_block_new)
        print('ERB Ruri block updated successfully!')
    else:
        print('WARNING: ruri_block_old not found directly!')

    # Replacement for CHAR_61 鶴海ひまり
    himari_block_old = """\t\tCASE 61
\t\t\t;鶴海ひまり (3-B / 現生徒会長・合唱部 / 渾名付けが趣味！)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (渾名「下僕くん」原作230回登場！) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"下僕くん"
\t\t\t\t;--- 敬愛する前会長（183回登場！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (敬愛する前会長)
\t\t\t\t\tRESULTS '= @"れいか先輩"
\t\t\t\t;--- 生徒会長の固有あだ名（公式設定・高頻度登場） ---
\t\t\t\tCASE 41
\t\t\t\t\t;悠木ともこ (剣道部・110回登場！)
\t\t\t\t\tRESULTS '= @"ユッキー"
\t\t\t\tCASE 48
\t\t\t\t\t;四方みつる (生徒会副会長・王子様・105回登場！)
\t\t\t\t\tRESULTS '= @"ミッチー"
\t\t\t\tCASE 24
\t\t\t\t\t;三波なつみ (演劇部・34回登場！)
\t\t\t\t\tRESULTS '= @"みなみん"
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず (軽音部・16回登場！※くろりんは0件誤記)
\t\t\t\t\tRESULTS '= @"クロちゃん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (大親友愛称！17回登場)
\t\t\t\t\tRESULTS '= @"アンジー"
\t\t\t\t;--- 親しい友人・後輩への愛称 ---
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか (合唱部相棒・168回登場！)
\t\t\t\t\tRESULTS '= @"あいかちゃん"
\t\t\t\tCASE 54
\t\t\t\t\t;久坂あやめ (80回登場！)
\t\t\t\t\tRESULTS '= @"あやめちゃん"
\t\t\t\tCASE 53
\t\t\t\t\t;花丘まり (50回登場！)
\t\t\t\t\tRESULTS '= @"まりちゃん"
\t\t\t\tCASE 60
\t\t\t\t\t;瀬川かえで (30回登場！)
\t\t\t\t\tRESULTS '= @"かえでちゃん"
\t\t\t\tCASE 10
\t\t\t\t\t;木之下ゆゆ (文芸部・27回登場！)
\t\t\t\t\tRESULTS '= @"ゆゆちゃん"
\t\t\t\tCASE 40
\t\t\t\t\t;夜霧はやて (5回登場！)
\t\t\t\t\tRESULTS '= @"はやてちゃん"
\t\t\t\tCASE 55
\t\t\t\t\t;伊藤さくら (5回登場！)
\t\t\t\t\tRESULTS '= @"さくらちゃん"
\t\t\t\tCASE 51
\t\t\t\t\t;御影かすみ (4回登場！)
\t\t\t\t\tRESULTS '= @"かすみちゃん"
\t\t\tENDSELECT"""

    himari_block_new = """\t\tCASE 61
\t\t\t;鶴海ひまり (3-B / 現生徒会長・合唱部 / 渾名付けが趣味！)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (渾名「下僕くん」原作230回登場！) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"下僕くん"
\t\t\t\t;--- 敬愛する前会長（183回登場！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (敬愛する前会長)
\t\t\t\t\tRESULTS '= @"れいか先輩"
\t\t\t\t;--- 生徒会長の固有あだ名（公式設定・scenarios完全抽出） ---
\t\t\t\tCASE 41
\t\t\t\t\t;悠木ともこ (剣道部・110回登場！)
\t\t\t\t\tRESULTS '= @"ユッキー"
\t\t\t\tCASE 48
\t\t\t\t\t;四方みつる (生徒会副会長・王子様・105回登場！)
\t\t\t\t\tRESULTS '= @"ミッチー"
\t\t\t\tCASE 24
\t\t\t\t\t;三波なつみ (演劇部・34回登場！)
\t\t\t\t\tRESULTS '= @"みなみん"
\t\t\t\tCASE 25
\t\t\t\t\t;八朔つゆり (大奥つゆりん)
\t\t\t\t\tRESULTS '= @"つゆりん"
\t\t\t\tCASE 50
\t\t\t\t\t;山條ぎん
\t\t\t\t\tRESULTS '= @"ぎんぎん"
\t\t\t\tCASE 56
\t\t\t\t\t;八壁ひかる (柔道部)
\t\t\t\t\tRESULTS '= @"ひかるんるん"
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず (軽音部・16回登場！)
\t\t\t\t\tRESULTS '= @"クロちゃん"
\t\t\t\tCASE 67
\t\t\t\t\t;日滝ましろ (新聞部・運動部・8回登場！)
\t\t\t\t\tRESULTS '= @"ましろん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (大親友愛称！17回登場)
\t\t\t\t\tRESULTS '= @"アンジー"
\t\t\t\t;--- 親しい友人・後輩への愛称 ---
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか (合唱部相棒・168回登場！)
\t\t\t\t\tRESULTS '= @"あいかちゃん"
\t\t\t\tCASE 10
\t\t\t\t\t;木之下ゆゆ (文芸部・27回登場！)
\t\t\t\t\tRESULTS '= @"ゆゆちゃん"
\t\t\t\tCASE 40
\t\t\t\t\t;夜霧はやて (5回登場！)
\t\t\t\t\tRESULTS '= @"はやてちゃん"
\t\t\t\tCASE 51
\t\t\t\t\t;御影かすみ (4回登場！)
\t\t\t\t\tRESULTS '= @"かすみちゃん"
\t\t\t\tCASE 53
\t\t\t\t\t;花丘まり (50回登場！)
\t\t\t\t\tRESULTS '= @"まりちゃん"
\t\t\t\tCASE 54
\t\t\t\t\t;久坂あやめ (80回登場！)
\t\t\t\t\tRESULTS '= @"あやめちゃん"
\t\t\t\tCASE 55
\t\t\t\t\t;伊藤さくら (5回登場！)
\t\t\t\t\tRESULTS '= @"さくらちゃん"
\t\t\t\tCASE 60
\t\t\t\t\t;瀬川かえで (30回登場！)
\t\t\t\t\tRESULTS '= @"かえでちゃん"
\t\t\t\tCASE 66
\t\t\t\t\t;曽根セイラ
\t\t\t\t\tRESULTS '= @"セイラちゃん"
\t\t\tENDSELECT"""

    if himari_block_old in text:
        text = text.replace(himari_block_old, himari_block_new)
        print('ERB Himari block updated successfully!')
    else:
        print('WARNING: himari_block_old not found directly!')

    # Normalize line endings to CRLF
    text = text.replace('\r\n', '\n').replace('\n', '\r\n')

    with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
        f.write(text.encode('cp932'))

    print('ERB fully updated!')

    # 2. Update Ledger
    with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'r', encoding='utf-8') as f:
        ledger = f.read()

    ledger_ruri_old = """### CHAR_58 天宮るり (3年B組 / 部活: 天文部部長)
- **一人称**: **三段構造**
  - (1) **るり**（三人称・基本/観測者モード・丁寧語）＝最頻！
  - (2) **あたし**（素・親密モード・原作146回）＝ほとりや心を許した相手の前、天体観測に誘う時
  - (3) **『わたし』**（ひらがな・括弧付き・深い孤独・原作7回）＝心の声で孤独を語る最深層
  ※漢字「私」「僕」は厳禁！
- **二人称**: **あなた**（115回登場）
- **口調**: 宇宙・物理用語を日常に織り交ぜる観測者（「るるる……♪」「大宇宙〜☆」「重力」「特異点」「〜ですね？」「〜ですか？」）
- **主人公の呼び方**: **転校生のひと**（最頻42回・基本観測者モード） / **弟のひと**（理屈呼び） / **転校生くん**（あたしモード）
- **既定ルール**:
  - 全学年: **`%CALLNAME:AI%のひと`**（★最大の個性！人を「〜のひと」と呼ぶ命名癖・原作189回登場）
- **特別呼称（セリフ抽出）**:
  - **主人公（転校生）**:
    - 00 主人公: **「転校生のひと」**（基本） / 「転校生くん」（親密） / 「弟のひと」
  - **最重要親友・幼馴染（111回登場・副部長）**:
    - 70 神無月ほとり: **「ほとりのひと」**（観測者モード） / **「ほとりちゃん」**（あたしモード）
  - **生徒会長**:
    - 61 鶴海ひまり: **「生徒会長のひと」**（11回登場）
  - **独自命名呼称**:
    - 10 木之下ゆゆ: **「ゆゆゆのひと」**（文芸部）
    - 51 御影かすみ: **「魔人のひと」**
    - 27 夏野ゆり: **「桃太郎のひと」**
    - 06 藍乃あいか: **「あいかのひと**（15回登場）
    - 12 神樹いちか: **「いちかのひと」**（10回登場）
    - 28 星海こよい: **「こよいのひと」**（14回登場）
    - 72 あんず: **「あんずさん」**"""

    ledger_ruri_new = """### CHAR_58 天宮るり (3年B組 / 部活: 天文部部長)
- **一人称**: **三段構造**
  - (1) **るり**（三人称・基本/観測者モード・丁寧語）＝最頻！
  - (2) **あたし**（素・親密モード・原作146回）＝ほとりや心を許した相手の前、天体観測に誘う時
  - (3) **『わたし』**（ひらがな・括弧付き・深い孤独・原作7回）＝心の声で孤独を語る最深層
  ※漢字「私」「僕」は厳禁！
- **二人称**: **あなた**（115回登場）
- **口調**: 宇宙・物理用語を日常に織り交ぜる観測者（「るるる……♪」「大宇宙〜☆」「重力」「特異点」「〜ですね？」「〜ですか？」）
- **主人公の呼び方**: **転校生のひと**（最頻42回・基本観測者モード） / **弟のひと**（理屈呼び） / **転校生くん**（あたしモード）
- **既定ルール**:
  - 全学年: **`%CALLNAME:AI%のひと`**（★最大の個性！人を「〜のひと」と呼ぶ命名癖・原作189回登場）
- **特別呼称（scenarios全網羅抽出）**:
  - **主人公（転校生）**:
    - 00 主人公: **「転校生のひと」**（基本） / 「弟のひと」 / 「転校生くん」
  - **最重要親友・幼馴染（副部長）**:
    - 70 神無月ほとり: **「ほとりのひと」**（観測者モード） / **「ほとりちゃん」**（あたしモード・51回登場）
  - **天文部仲間**:
    - 28 星海こよい: **「こよいのひと」**（27回登場） / **「こよいちゃん」**
    - 30 長居ゆう: **「ゆうのひと」** / **「ゆうちゃん」**
  - **生徒会長**:
    - 61 鶴海ひまり: **「生徒会長のひと」**（11回登場）
  - **親しい後輩・友人**:
    - 06 藍乃あいか: **「あいかのひと」**（23回登場）
    - 12 神樹いちか: **「いちかのひと」**（10回登場）
    - 25 八朔つゆり: **「つゆりのひと」**
  - **独自命名呼称（scenarios抽出）**:
    - 10 木之下ゆゆ: **「ゆゆゆのひと」**（文芸部）
    - 27 夏野ゆり: **「桃太郎のひと」**
    - 51 御影かすみ: **「魔人のひと」**
    - 65 時国そら: **「ゆんゆんのひと」** / **「耳がいいだけのひと」**
    - 68 深鳥ふみ: **「新聞部のひと」**
    - 69 神樹はじめ: **「生き神のひと」**
    - 72 あんず: **「あんずさん」**"""

    if ledger_ruri_old in ledger:
        ledger = ledger.replace(ledger_ruri_old, ledger_ruri_new)
        print('Ledger Ruri updated!')
    else:
        # replace looser
        import re
        ledger = re.sub(r'### CHAR_58 天宮るり.*?(?=### CHAR_59)', ledger_ruri_new + '\n\n', ledger, flags=re.DOTALL)
        print('Ledger Ruri updated via regex!')

    ledger_himari_new = """### CHAR_61 鶴海ひまり (3年B組 / 現生徒会長・合唱部)
- **一人称**: **私**（587回登場・漢字「私」！※あたし/わたし/僕は厳禁！）
- **二人称**: **おまえ**（131回登場・ひらがな「おまえ」！）
- **口調**: 熱血・快活・頼れる生徒会長（「〜のだあーっ！」「〜ぞお！」「〜だな！」「ふはは！」「せえとかいちょお！」）
- **主人公の呼び方**: **下僕くん**（原作230回登場！生徒会長の固有渾名！）
- **既定ルール**:
  - 全学年: **`%CALLNAME:AI%`**（基本は親しみを込めた名前呼び捨て）
  - ★**公式設定：全校生徒の顔と名前を覚え、渾名（あだ名）をつけるのが趣味！**
- **特別呼称（生徒会長の固有あだ名・scenarios完全網羅抽出）**:
  - **主人公（転校生）**:
    - 00 主人公: **「下僕くん」**（230回登場！主人公への絶対的固有あだ名！）
  - **生徒会長の重要固有あだ名**:
    - 41 悠木ともこ: **「ユッキー」**（110回登場！剣道部・大親友！）
    - 48 四方みつる: **「ミッチー」**（105回登場！生徒会副会長・王子様！）
    - 24 三波なつみ: **「みなみん」**（34回登場！演劇部！）
    - 25 八朔つゆり: **「つゆりん」**（大奥つゆりん・5回登場！）
    - 50 山條ぎん: **「ぎんぎん」**
    - 56 八壁ひかる: **「ひかるんるん」**
    - 62 黒森すず: **「クロちゃん」**（16回登場！軽音部！）
    - 67 日滝ましろ: **「ましろん」**（8回登場！新聞部・運動部）
    - 72 あんず: **「アンジー」**（17回登場！元茶道部部長・大親友！）
  - **敬愛する前会長（183回登場！）**:
    - 45 円城寺れいか: **「れいか先輩」**（生徒会長再任選挙の因縁・敬愛する前会長！）
  - **親しい友人・後輩への愛称**:
    - 06 藍乃あいか: **「あいかちゃん」**（168回登場！合唱部相棒！） / 「あいか姫」
    - 10 木之下ゆゆ: **「ゆゆちゃん」**（27回登場！文芸部！） / 「ゆゆ姫」
    - 40 夜霧はやて: **「はやてちゃん」**（5回登場！）
    - 51 御影かすみ: **「かすみちゃん」**（4回登場！）
    - 53 花丘まり: **「まりちゃん」**（50回登場！テニス部）
    - 54 久坂あやめ: **「あやめちゃん」**（80回登場！生物部・魔王）
    - 55 伊藤さくら: **「さくらちゃん」**（5回登場！園芸部）
    - 60 瀬川かえで: **「かえでちゃん」**（30回登場！弓道部）
    - 66 曽根セイラ: **「セイラちゃん」**"""

    import re
    ledger = re.sub(r'### CHAR_61 鶴海ひまり.*?(?=### CHAR_62)', ledger_himari_new + '\n\n', ledger, flags=re.DOTALL)
    print('Ledger Himari updated via regex!')

    with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'w', encoding='utf-8') as f:
        f.write(ledger)

    print('Ledger fully written!')

if __name__ == '__main__':
    update_all()

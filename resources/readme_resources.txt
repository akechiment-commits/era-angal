このフォルダはEmuera1824以降（EmueraEM+EE推奨）で使用する画像リソースを置く場所です。

■ 対応フォーマット
  bmp / jpg / png

■ ファイル命名規則（予定）
  face_XX.png   … キャラNO:XXの顔グラ（例: face_01.png = Chara1）
  bg_classroom.png … 背景画像
  card_XXXX.png … カードID:XXXXの絵

■ 使用するには
  Emuera1820.exe を EmueraEM+EE の exe に差し替えてください。
  DL先: https://osdn.net/projects/emuera/
  （Emuera1824.zip が公式最終版。EmueraEM+EEはさらに機能拡張版）

■ ERBでの呼び出し例（1824以降）
  GCREATEFROMFILE 0, "resources/face_01.png", 1
  GDISP 0, 0, 0, 100, 100

■ Emuera1820.exe はバックアップとして保持してあります
  新エンジンで動作確認できたら削除してください。

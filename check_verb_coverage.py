import json
import os

# JSONファイルから設定済みの画像ファイルを取得
def get_configured_images():
    try:
        with open('image_meta_tags.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [item['image_file'] for item in data]
    except:
        return []

# 動詞と考えられるファイル名のリスト（手動で選別）
verb_files = [
    "analyze.png",
    "appear.png", 
    "ask.png",
    "avoid.png",
    "become.png",
    "begin.png",
    "believe.png",
    "belong.png",
    "catch.png",
    "catch up.png",
    "caught.png",
    "change.png",
    "charge.png",
    "choose.png",  # chosen.png -> choose
    "clear.png",
    "close.png",
    "complete.png",
    "consider.png",
    "control.png",
    "decide.png",
    "deliver.png",
    "discuss.png",
    "end.png",
    "enjoy.png",
    "escape.png",
    "explain.png",
    "explaining.png",
    "face.png",
    "figure out.png",
    "find.png",
    "get.png",
    "give.png",
    "happen.png",
    "help.png",
    "include.png",
    "increase.png",
    "intend.png",
    "joined.png",  # join
    "keep.png",
    "know.png",
    "like.png",
    "lingered.png",  # linger
    "make.png",
    "missed.png",   # miss
    "notice.png",
    "offer.png",
    "plan.png",
    "push.png",
    "refuse.png",
    "request.png",
    "return.png",
    "take.png",
    "want.png",
    "wish.png",
    "would_rather.png"
]

# 設定済みの画像ファイルを取得
configured = get_configured_images()

print("=== 動詞PNG画像の設定状況 ===")
print(f"総動詞画像数: {len(verb_files)}")
print(f"設定済み動詞数: {len([f for f in verb_files if f in configured])}")
print()

print("✅ 設定済みの動詞:")
for verb in verb_files:
    if verb in configured:
        print(f"  {verb}")

print()
print("❌ 未設定の動詞:")
missing = []
for verb in verb_files:
    if verb not in configured:
        missing.append(verb)
        print(f"  {verb}")

print()
print(f"未設定の動詞数: {len(missing)}")

# 未設定の動詞をリストとして出力
if missing:
    print()
    print("未設定動詞のリスト:")
    print(missing)


// renderer_core.js（subslotも含む描画統合版 + export + テキスト描画修正）
export function renderAllSlots() {
  const slotIds = [
    // 上位スロット
    "slot-m1", "slot-s", "slot-aux", "slot-m2", "slot-v",
    "slot-c", "slot-o1", "slot-o2", "slot-c2", "slot-m3",

    // subslot - O1
    "slot-o1-sub-m1", "slot-o1-sub-s", "slot-o1-sub-aux", "slot-o1-sub-m2",
    "slot-o1-sub-v", "slot-o1-sub-c", "slot-o1-sub-o1", "slot-o1-sub-o2",
    "slot-o1-sub-c2", "slot-o1-sub-m3",

    // subslot - C
    "slot-c-sub-m1", "slot-c-sub-s", "slot-c-sub-aux", "slot-c-sub-m2",
    "slot-c-sub-v", "slot-c-sub-c", "slot-c-sub-o1", "slot-c-sub-o2",
    "slot-c-sub-c2", "slot-c-sub-m3",

    // subslot - O2
    "slot-o2-sub-m1", "slot-o2-sub-s", "slot-o2-sub-aux", "slot-o2-sub-m2",
    "slot-o2-sub-v", "slot-o2-sub-c", "slot-o2-sub-o1", "slot-o2-sub-o2",
    "slot-o2-sub-c2", "slot-o2-sub-m3"
  ,
  "slot-m1-sub-m1",
  "slot-m1-sub-s",
  "slot-m1-sub-aux",
  "slot-m1-sub-m2",
  "slot-m1-sub-v",
  "slot-m1-sub-c",
  "slot-m1-sub-o1",
  "slot-m1-sub-o2",
  "slot-m1-sub-c2",
  "slot-m1-sub-m3"  "slot-s-sub-m1",
  "slot-s-sub-s",
  "slot-s-sub-aux",
  "slot-s-sub-m2",
  "slot-s-sub-v",
  "slot-s-sub-c",
  "slot-s-sub-o1",
  "slot-s-sub-o2",
  "slot-s-sub-c2",
  "slot-s-sub-m3",
];

  slotIds.forEach(slotId => {
    const img = document.querySelector(`#${slotId} img`);
    if (img) {
      img.src = "slot_images/common/placeholder.png";
      img.alt = `Placeholder for ${slotId}`;
      console.log(`描画中: ${slotId} → ${img.src}`);
    }

    const text = document.querySelector(`#${slotId} .slot-text`);
    if (text) {
      // スロットID末尾の名称だけを抽出して使用
      const slotKey = slotId.split("-").slice(-1)[0].toUpperCase();
      text.textContent = `【${slotKey}】の文法ガイド`;
      console.log(`テキスト描画: ${slotId} → ${text.textContent}`);
    }
  });
}

// 自動実行：必要ならコメントアウト可
window.addEventListener("DOMContentLoaded", renderAllSlots);


export function renderAllTexts(slotTextMap) {
  console.log("✅ renderAllTexts called");

  Object.entries(slotTextMap).forEach(([slotId, text]) => {
    const textElement = document.querySelector(`#${slotId} .slot-text`);
    if (textElement) {
      textElement.textContent = text;
      console.log(`テキスト設定: ${slotId} → ${text}`);
    }
  });
}


export function updateSubslotLabel(slotId) {
  const label = document.getElementById("subslot-label");
  if (label) {
    label.textContent = `【${slotId.toUpperCase()}】の展開中サブスロット`;
  }
}

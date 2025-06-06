
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
  "slot-m1-sub-m3"];

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
  const text_slot-s-sub-m1 = document.querySelector("#slot-s-sub-m1 .slot-text");
  if (text_slot-s-sub-m1) {
    text_slot-s-sub-m1.textContent = "【M1】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-m1 →", text_slot-s-sub-m1.textContent);
  }
  const text_slot-s-sub-s = document.querySelector("#slot-s-sub-s .slot-text");
  if (text_slot-s-sub-s) {
    text_slot-s-sub-s.textContent = "【S】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-s →", text_slot-s-sub-s.textContent);
  }
  const text_slot-s-sub-aux = document.querySelector("#slot-s-sub-aux .slot-text");
  if (text_slot-s-sub-aux) {
    text_slot-s-sub-aux.textContent = "【AUX】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-aux →", text_slot-s-sub-aux.textContent);
  }
  const text_slot-s-sub-m2 = document.querySelector("#slot-s-sub-m2 .slot-text");
  if (text_slot-s-sub-m2) {
    text_slot-s-sub-m2.textContent = "【M2】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-m2 →", text_slot-s-sub-m2.textContent);
  }
  const text_slot-s-sub-v = document.querySelector("#slot-s-sub-v .slot-text");
  if (text_slot-s-sub-v) {
    text_slot-s-sub-v.textContent = "【V】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-v →", text_slot-s-sub-v.textContent);
  }
  const text_slot-s-sub-c = document.querySelector("#slot-s-sub-c .slot-text");
  if (text_slot-s-sub-c) {
    text_slot-s-sub-c.textContent = "【C】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-c →", text_slot-s-sub-c.textContent);
  }
  const text_slot-s-sub-o1 = document.querySelector("#slot-s-sub-o1 .slot-text");
  if (text_slot-s-sub-o1) {
    text_slot-s-sub-o1.textContent = "【O1】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-o1 →", text_slot-s-sub-o1.textContent);
  }
  const text_slot-s-sub-o2 = document.querySelector("#slot-s-sub-o2 .slot-text");
  if (text_slot-s-sub-o2) {
    text_slot-s-sub-o2.textContent = "【O2】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-o2 →", text_slot-s-sub-o2.textContent);
  }
  const text_slot-s-sub-c2 = document.querySelector("#slot-s-sub-c2 .slot-text");
  if (text_slot-s-sub-c2) {
    text_slot-s-sub-c2.textContent = "【C2】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-c2 →", text_slot-s-sub-c2.textContent);
  }
  const text_slot-s-sub-m3 = document.querySelector("#slot-s-sub-m3 .slot-text");
  if (text_slot-s-sub-m3) {
    text_slot-s-sub-m3.textContent = "【M3】の文法ガイド";
    console.log("テキスト描画: slot-s-sub-m3 →", text_slot-s-sub-m3.textContent);
  }
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
// renderer_core.js（subslotも含む描画統合版 + export + テキスト描画修正 + ログ強化）
export function renderAllSlots(slotData) {
  const slotIds = [
    // 上位スロット
    "slot-m1", "slot-s", "slot-aux", "slot-m2", "slot-v",
    "slot-c", "slot-o1", "slot-o2", "slot-c2", "slot-m3",

    // subslot - O1
    "slot-o1-sub-m1", "slot-o1-sub-s", "slot-o1-sub-aux", "slot-o1-sub-m2",
    "slot-o1-sub-v", "slot-o1-sub-c", "slot-o1-sub-o1", "slot-o1-sub-o2",
    "slot-o1-sub-c2", "slot-o1-sub-m3",

    // subslot - M2
    "slot-m2-sub-m1", "slot-m2-sub-s", "slot-m2-sub-aux", "slot-m2-sub-m2",
    "slot-m2-sub-v", "slot-m2-sub-c", "slot-m2-sub-o1", "slot-m2-sub-o2",
    "slot-m2-sub-c2", "slot-m2-sub-m3",

    // subslot - C
    "slot-c-sub-m1", "slot-c-sub-s", "slot-c-sub-aux", "slot-c-sub-m2",
    "slot-c-sub-v", "slot-c-sub-c", "slot-c-sub-o1", "slot-c-sub-o2",
    "slot-c-sub-c2", "slot-c-sub-m3",

    // subslot - O2
    "slot-o2-sub-m1", "slot-o2-sub-s", "slot-o2-sub-aux", "slot-o2-sub-m2",
    "slot-o2-sub-v", "slot-o2-sub-c", "slot-o2-sub-o1", "slot-o2-sub-o2",
    "slot-o2-sub-c2", "slot-o2-sub-m3",

    // subslot - M1
    "slot-m1-sub-m1", "slot-m1-sub-s", "slot-m1-sub-aux", "slot-m1-sub-m2",
    "slot-m1-sub-v", "slot-m1-sub-c", "slot-m1-sub-o1", "slot-m1-sub-o2",
    "slot-m1-sub-c2", "slot-m1-sub-m3",

    // subslot - S（検証対象）
    "slot-s-sub-m1", "slot-s-sub-s", "slot-s-sub-aux", "slot-s-sub-m2",
    "slot-s-sub-v", "slot-s-sub-c", "slot-s-sub-o1", "slot-s-sub-o2",
    "slot-s-sub-c2", "slot-s-sub-m3"
  ];

  slotIds.forEach(slotId => {
    const container = document.getElementById(slotId);
    if (container) {
      const slotTextCheck = container.querySelector(".slot-text");
    }

    const img = document.querySelector(`#${slotId} img`);
    if (img) {
      img.src = "slot_images/common/placeholder.png";
      img.alt = `Placeholder for ${slotId}`;
    }

    const text = document.querySelector(`#${slotId} .slot-text`);
    if (text) {
      const slotKey = slotId.split("-").slice(-1)[0].toUpperCase();
      text.textContent = slotData[slotId] || `【${slotKey}】の文法ガイド`;
    }
  });
}

// 自動実行：コメントアウト済
// window.addEventListener("DOMContentLoaded", renderAllSlots);

export function renderAllTexts(slotTextMap) {
  Object.entries(slotTextMap).forEach(([slotId, text]) => {
    const textElement = document.querySelector(`#${slotId} .slot-text`);
    if (textElement) {
      if (text === undefined || text === null) return;
      textElement.textContent = text;
    }
  });
}

export function updateSubslotLabel(slotId) {
  const label = document.getElementById("subslot-label");
  if (label) {
    label.textContent = `【${slotId.toUpperCase()}】の展開中サブスロット`;
  }
}

export function injectSlotText(slotId) {
  const text = document.querySelector(`#${slotId} .slot-text`);
  if (text) {
    const slotKey = slotId.split("-").slice(-1)[0].toUpperCase();
    text.textContent = slotData[slotId] || `【${slotKey}】の文法ガイド`;
  }
}
window.injectSlotText = injectSlotText;

export function injectAllSubslotTexts(containerId) {
  const subslots = document.querySelectorAll(`#${containerId} .subslot`);
  subslots.forEach(subslot => {
  }

  let chosenId, targetRows = [];
  const json = XLSX.utils.sheet_to_json(sheet);

  const availableIds = [...new Set(
    json.map(row => String(parseInt(row['文法項目番号'])))
        .filter(id => id && id !== "NaN")
  )];

  while (targetRows.length === 0 && availableIds.length > 0) {
    const index = Math.floor(Math.random() * availableIds.length);
    chosenId = availableIds.splice(index, 1)[0];

    targetRows = json.filter(row => {
      const idMatch = String(parseInt(row['文法項目番号'])) === chosenId;
      const hasSlot = !!(row['Slot'] || '').trim();
      return idMatch && hasSlot;
    });
  }

  const slotData = {};

  for (const row of targetRows) {
    const rawSlot = (row['Slot'] || '').trim().toLowerCase();
    const internalSub = (row['内部スロット'] || '').trim();
    const value = (row['Phrase'] || '').trim();
    const verb = (row['A_group_V'] || '').trim();

    if (verb && !slotData['slot-v']) slotData['slot-v'] = verb;
    if (!value || internalSub.startsWith('sub-')) continue;
    slotData[`slot-${rawSlot}`] = value;
  }

  for (const row of targetRows) {
    const rawSlot = (row['Slot'] || '').trim().toLowerCase();
    const internalSub = (row['内部スロット'] || '').trim().toLowerCase();
    const value = (row['Phrase'] || '').trim();
    if (!value || !internalSub.startsWith('sub-')) continue;
    slotData[`slot-${rawSlot}-sub-${internalSub.replace('sub-', '')}`] = value;
  }

  console.log("🧪 再抽選 chosenId:", chosenId);
  console.log("📘 slotData (再抽選):", slotData);
  return slotData;
}

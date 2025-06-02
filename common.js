// 共通ユーティリティ関数群

// null/undefined安全に処理
export function safe(value) {
  return value ?? '';
}

// スロットにテキストを更新（例：slot-v）
export function updateSlotDisplay(slotId, text) {
  const el = document.getElementById(slotId);
  if (el) el.textContent = text;
}

// スロット名（V, S, O1など）から要素を更新（例：V -> slot-V）
export function updateSlot(slot, word) {
  const el = document.getElementById("slot-" + slot);
  if (el) el.textContent = word;
}
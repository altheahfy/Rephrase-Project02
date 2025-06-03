/**
 * slotKey に対応する subslot を表示／非表示トグル
 * DOM構造は一切変更せず、display の切り替えのみ行う
 */
export function toggleSubslot(slotKey) {
  const subslotId = `slot-${slotKey}-sub`;
  const container = document.getElementById(subslotId);
  if (!container) return;

  const isHidden = container.style.display === "none";
  container.style.display = isHidden ? "block" : "none";
}
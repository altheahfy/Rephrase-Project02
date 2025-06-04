export function toggleSubslot(slotKey) {
  const subslotId = `slot-${slotKey}-sub`;
  const container = document.getElementById(subslotId);
  if (!container) return;

  // getComputedStyle を使って正確に状態を判定
  const isHidden = window.getComputedStyle(container).display === "none";
  container.style.display = isHidden ? "block" : "none";
}

function toggleSubslot(slotKey) {
  const subslotId = `slot-${slotKey}-sub`;
  const container = document.getElementById(subslotId);
  if (!container) return;

  const isHidden = window.getComputedStyle(container).display === "none";
  container.style.display = isHidden ? "block" : "none";
}

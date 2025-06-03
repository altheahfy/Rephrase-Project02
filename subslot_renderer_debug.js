/**
 * サブスロットを一度だけ描画（展開ボタンで展開される領域）
 * - containerId: "slot-o1-sub" など
 */
export function renderSubSlotsOnce(embeddedStructure, containerId) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`❌ container が見つかりません: ${containerId}`);
    return;
  }

  if (container.dataset.rendered === "true") {
    console.log(`⏭️ subslotRenderer: すでに描画済み - ${containerId}`);
    return;
  }

  console.log(`🛠️ subslotRenderer: 描画開始 - ${containerId}`);

  const slotKeys = [
    "m1", "s", "aux", "m2", "v", "c1", "o1", "o2", "c2", "m3"
  ];

  slotKeys.forEach((key) => {
    const wrapper = document.createElement("div");
    wrapper.className = "subslot-wrapper";

    const btn = document.createElement("button");
    btn.textContent = "▼";
    btn.className = "subslot-toggle";
    btn.id = `toggle-${key}`;
    btn.onclick = () => {
      const subId = `slot-o1-${key}-sub`;
      const target = document.getElementById(subId);
      if (!target) {
        console.warn(`❌ toggle対象なし: ${subId}`);
        return;
      }
      const isHidden = target.style.display === "none";
      target.style.display = isHidden ? "block" : "none";
      console.log(`🔀 toggle ${subId}: ${isHidden ? "表示" : "非表示"}`);
    };

    const slotDiv = document.createElement("div");
    slotDiv.id = `slot-o1-${key}-sub`;
    slotDiv.className = "subslot";
    slotDiv.style.display = "none";  // 初期状態で非表示

    wrapper.appendChild(btn);
    wrapper.appendChild(slotDiv);
    container.appendChild(wrapper);
  });

  container.dataset.rendered = "true";
  console.log(`✅ subslotRenderer: 描画完了 - ${containerId}`);
}
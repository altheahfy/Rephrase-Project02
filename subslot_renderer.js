// subslot_renderer_v2.js

const slotOrder = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];

/**
 * subslot描画フラグ管理
 * 各slotKeyごとにrender済みかどうかを記録
 */
const renderedSubslotMap = {};

/**
 * 指定したスロットのサブスロットを描画（初回のみ）
 */
export function renderSubSlots(embeddedStructure, targetElementId) {
    clearSubSlots(targetElementId);

    slotOrder.forEach(slotKey => {
        const slotData = embeddedStructure[slotKey] || {};
        const slotElement = generateSlotHtmlV2(slotKey, slotData);
        appendSlotToTarget(targetElementId, slotElement);
    });
}

function generateSlotHtmlV2(slotKey, slotData) {
    const randomizableSlots = ["m1", "s", "m2", "c", "o1", "o2", "c2", "m3"];
    const collapsibleSlots = ["m1", "s", "m2", "c", "o1", "o2", "c2", "m3"];

    const wrapper = document.createElement("div");
    wrapper.className = `slot slot-${slotKey}-sub`;

    const label = document.createElement("div");
    label.className = "slot-label";
    label.innerText = slotKey;
    wrapper.insertBefore(label, wrapper.firstChild);

    // テキスト or 画像表示
    if (slotKey === "aux" && slotData.text) {
        const textEl = document.createElement("div");
        textEl.className = "slot-text";
        textEl.innerText = slotData.text;
        wrapper.appendChild(textEl);
    } else if (slotData.imagePath) {
        const imgEl = document.createElement("img");
        imgEl.src = slotData.imagePath;
        imgEl.alt = slotKey;
        imgEl.onerror = () => imgEl.style.display = "none";
        wrapper.appendChild(imgEl);
    }

    // 🎲 個別ランダマイズ
    if (randomizableSlots.includes(slotKey)) {
        const button = document.createElement("button");
        button.className = "subslot-randomize-btn";
        button.innerText = "🎲";
        button.onclick = () => randomizeSubSlot(slotKey);
        wrapper.appendChild(button);
    }

    // ▼ 折り畳み構造（常設）
    if (collapsibleSlots.includes(slotKey)) {
        const toggleButton = document.createElement("button");
        toggleButton.className = "subslot-toggle-btn";
        toggleButton.innerText = "▼";

        toggleButton.onclick = () => {
            const subslotId = `slot-${slotKey}-sub`;
            const subslotContainer = document.getElementById(subslotId);

            if (!renderedSubslotMap[subslotId]) {
                renderSubSlotsV2(slotData.subslots ?? generateEmptyStructure(), subslotId);
                renderedSubslotMap[subslotId] = true;
            }

            const isHidden = subslotContainer.style.display === "none";
            subslotContainer.style.display = isHidden ? "block" : "none";
        };

        wrapper.appendChild(toggleButton);

        const subslotContainer = document.createElement("div");
        subslotContainer.id = `slot-${slotKey}-sub`;
        subslotContainer.className = "subslot-container";
        subslotContainer.style.display = "none";

        wrapper.appendChild(subslotContainer);
    }

    return wrapper;
}

function clearSubSlots(targetElementId) {
    const container = document.getElementById(targetElementId);
    if (container) container.innerHTML = "";
}

function appendSlotToTarget(targetElementId, slotElement) {
    const container = document.getElementById(targetElementId);
    if (container && slotElement) container.appendChild(slotElement);
}

function generateEmptyStructure() {
    const empty = {};
    slotOrder.forEach(key => {
        empty[key] = {};
    });
    return empty;
}

function randomizeSubSlot(slotKey) {
    console.log(`Randomize requested for: ${slotKey}`);
}


// グローバルスコープに登録
window.renderSubSlots = renderSubSlots;

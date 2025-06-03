
const slotOrder = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];

/**
 * 元のrenderSubSlots（全体一括描画）はそのまま残す
 */
function renderSubSlots(embeddedStructure, targetElementId) {
    clearSubSlots(targetElementId);
    slotOrder.forEach(slotKey => {
        const slotData = embeddedStructure[slotKey] || {};
        const slotElement = generateSlotHtml(slotKey, slotData);
        appendSlotToTarget(targetElementId, slotElement);
    });
}

/**
 * 新規追加: slotKey単位での描画・トグル
 */
function renderSubSlot(embeddedStructure, slotKey, targetElementId) {
    // 対象サブスロット領域のみクリア＆描画
    const container = document.getElementById(targetElementId);
    if (container) {
        container.innerHTML = "";
        const slotData = embeddedStructure[slotKey] || {};
        const slotElement = generateSlotHtml(slotKey, slotData);
        container.appendChild(slotElement);

        // トグル制御
        const isHidden = container.style.display === "none";
        container.style.display = isHidden ? "block" : "none";
    }
}

/**
 * スロット要素生成（toggleボタンのみ renderSubSlot を呼ぶよう差分追加）
 */
function generateSlotHtml(slotKey, slotData) {
    const randomizableSlots = ["m1", "s", "m2", "c", "o1", "o2", "c2", "m3"];
    const collapsibleSlots = ["m1", "s", "m2", "c", "o1", "o2", "c2", "m3"];

    const wrapper = document.createElement("div");
    wrapper.className = `slot slot-${slotKey}-sub`;

    const label = document.createElement("div");
    label.className = "slot-label";
    label.innerText = slotKey;
    wrapper.insertBefore(label, wrapper.firstChild);

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

    if (randomizableSlots.includes(slotKey)) {
        const button = document.createElement("button");
        button.className = "subslot-randomize-btn";
        button.innerText = "🎲";
        button.onclick = () => randomizeSubSlot(slotKey);
        wrapper.appendChild(button);
    }

    if (collapsibleSlots.includes(slotKey)) {
        const toggleButton = document.createElement("button");
        toggleButton.className = "subslot-toggle-btn";
        toggleButton.innerText = "▼";
        toggleButton.onclick = () => {
            const subslotId = `slot-${slotKey}-sub`;
            renderSubSlot(slotData.subslots ?? generateEmptyStructure(), slotKey, subslotId);
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

function appendSlotToTarget(targetId, element) {
    const target = document.getElementById(targetId);
    if (target) {
        target.appendChild(element);
    }
}

function clearSubSlots(targetElementId) {
    const container = document.getElementById(targetElementId);
    if (container) container.innerHTML = "";
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

// グローバル登録
window.renderSubSlot = renderSubSlot;
window.renderSubSlots = renderSubSlots;

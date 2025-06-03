// subslot_renderer.js

const slotOrder = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];

/**
 * 初回のみ全subslot要素を描画（MSAuxMVCOOCM構造を保持）
 */
export function renderSubSlotsOnce(embeddedStructure, targetElementId) {
    const target = document.getElementById(targetElementId);
    if (!target || target.dataset.initialized === "true") return;

    slotOrder.forEach(slotKey => {
        const slotData = embeddedStructure[slotKey] || {};
        const slotElement = generateSlotHtml(slotKey, slotData);
        target.appendChild(slotElement);
    });

    target.dataset.initialized = "true"; // ✅ 二度描画防止
}

/**
 * スロット要素の生成
 */
function generateSlotHtml(slotKey, slotData) {
    const randomizableSlots = ["m1", "s", "m2", "c", "o1", "o2", "c2", "m3"];
    const collapsibleSlots = ["m1", "s", "m2", "c", "o1", "o2", "c2", "m3"];

    const wrapper = document.createElement("div");
    const label = document.createElement("div");
    label.className = "slot-label";
    label.innerText = slotKey;
    wrapper.insertBefore(label, wrapper.firstChild);
    wrapper.className = `slot slot-${slotKey}-sub`;

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
            const subslotContainer = document.getElementById(subslotId);

            if (!subslotContainer.dataset.rendered) {
                renderSubSlotsOnce(slotData.subslots ?? generateEmptyStructure(), subslotId);
                subslotContainer.dataset.rendered = "true";
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

/**
 * 空のsubslot構造（10スロット）を返す
 */
function generateEmptyStructure() {
    return {
        m1: {}, s: {}, aux: {}, m2: {}, v: {}, c: {},
        o1: {}, o2: {}, c2: {}, m3: {}
    };
}

/**
 * ランダマイズ関数（仮）
 */
function randomizeSubSlot(slotKey) {
    console.log(`Randomize requested for ${slotKey}`);
}
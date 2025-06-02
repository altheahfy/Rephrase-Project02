// subslot_renderer.js

const slotOrder = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];

/**
 * サブスロット描画（例：slot-o1-sub）に対し、embedded_structure に基づいて描画
 * @param {Object} embeddedStructure - grammar_dataの構造情報
 * @param {string} targetElementId - 描画対象のDOM ID（例："slot-o1-sub"）
 */
export function renderSubSlots(embeddedStructure, targetElementId) {
    clearSubSlots(targetElementId);

    slotOrder.forEach(slotKey => {
        const slotData = embeddedStructure[slotKey] || {};
        const slotElement = generateSlotHtml(slotKey, slotData);
        appendSlotToTarget(targetElementId, slotElement);
    });
}

/**
 * スロット要素の生成（slot-auxは文字列、それ以外は画像表示）
 */
function generateSlotHtml(slotKey, slotData) {
    const wrapper = document.createElement("div");
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

    return wrapper;
}

/**
 * 対象DOMにスロット要素を追加
 */
function appendSlotToTarget(targetId, element) {
    const target = document.getElementById(targetId);
    if (target) {
        target.appendChild(element);
    }
}

/**
 * 対象DOMの内容をクリア
 */
function clearSubSlots(targetId) {
    const target = document.getElementById(targetId);
    if (target) {
        target.innerHTML = '';
    }
} 
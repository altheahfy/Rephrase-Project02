// subslot_renderer.js

// MSauxMVCOOCM順の10スロット
const slotOrder = ["m1", "s", "aux", "m2", "v", "c", "o1", "o2", "c2", "m3"];

/**
 * サブスロット（slot-o1-sub）に対し、embedded_structure に基づき描画する
 * @param {Object} embeddedStructure - grammar_dataからの構造情報
 * @param {string} targetElementId - 描画対象（通常 "slot-o1-sub"）
 */
export function renderSubSlots(embeddedStructure, targetElementId) {
    clearSubSlots(targetElementId);

    slotOrder.forEach(slotKey => {
        const slotData = embeddedStructure[slotKey] || {};
        const slotHtml = generateSlotHtml(slotKey, slotData);
        appendSlotToTarget(targetElementId, slotHtml);
    });
}

/**
 * 各スロットごとのHTML要素を生成
 * slot-auxは文字列、その他は画像表示
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
 * 指定DOMにスロット要素を追加
 */
function appendSlotToTarget(targetId, element) {
    const target = document.getElementById(targetId);
    if (target) {
        target.appendChild(element);
    }
}

/**
 * 既存スロット内容をクリア
 */
function clearSubSlots(targetId) {
    const target = document.getElementById(targetId);
    if (target) {
        target.innerHTML = '';
    }
}
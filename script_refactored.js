/*******************************************************
 🔒 この script.js はモジュール分割前の旧バージョンです。
 現在は参照専用であり、直接使用・実行されるべきではありません。
*******************************************************/

/*******************************************************
 ✅ generateSlotO1Details は subslot_renderer.js に責務移管済
 今後は本関数を直接使用しないでください。
*******************************************************

function generateSlotO1Details(data) {
    const slotO1 = document.getElementById("slot-o1");
    if (!slotO1 || document.getElementById("slot-o1-sub-m1")) return;

    const details = document.createElement("details");
    const summary = document.createElement("summary");
    summary.textContent = "構文要素を表示";
    details.appendChild(summary);

    const slotKeys = data.slot_o1_internal_keys || ["m1", "s", "aux", "m2", "v", "c1", "o1", "o2", "c2", "m3"];

    slotKeys.forEach((key) => {
        const div = document.createElement("div");
        div.id = `slot-o1-sub-${key}`;
        div.className = "sub-slot";

        let chunk = "";
        let image = "";

        if (key === "v") {
            chunk = data["chunk_o_v"] || "";
            image = data["image_o_v"] || "";
        } else if (key === "o1") {
            const full = data["chunk_o1"] || "";
            const part = data["chunk_o_v"] || "";
            chunk = full.replace(part, "").trim();
            image = data["image_o1_sub"] || "";
        } else {
            chunk = data[`chunk_${key}`] || "";
            image = data[`image_${key}`] || "";
        }

        if (chunk) {
            const text = document.createElement("div");
            text.textContent = chunk;
            div.appendChild(text);
        }

        if (image) {
            const img = document.createElement("img");
            img.src = "slot_images/common/" + image;
            img.alt = key;
            img.style.maxHeight = "80px"; img.style.maxWidth = "120px"; img.style.height = "auto";
            div.appendChild(img);
        }

        details.appendChild(div);
    });

    slotO1.appendChild(details);
}
*/

/* 旧版の randomizeAll も退避済（→ randomizer_all.js へ移管済） */

/* randomizeSlot などの個別関数は randomizer_individual.js に移動済 */
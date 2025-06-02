
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



function getStructureId() {
  const input = document.getElementById("structureId");
  return input ? input.value : "INF-N-OBJ-010";
}

async function loadStructureData(structureId) {
  const dir = structureId.slice(-3);
  try {
    const response = await fetch(`slot_assignments/${dir}/slot_assignment.json`);
    const json = await response.json();
    return json[structureId];
  } catch (error) {
    console.error(`❌ 構文データの読み込みに失敗: ${structureId}`, error);
    return null;
  }
}

function updateSlotDisplay(slotId, text) {
  const element = document.getElementById(slotId);
  if (!element) return;
  const span = element.querySelector(".chunk-content");
  if (span) span.textContent = text;
}

function updateSlotImage(slotId, imageFile) {
  console.log(`🔧 updateSlotImage called: ${slotId}, imageFile: ${imageFile}`);
  const element = document.getElementById(slotId);
  if (!element) {
    console.warn(`❌ slot not found: ${slotId}`);
    return;
  }
  const img = element.querySelector("img");
  if (!img) {
    console.warn(`❌ <img> タグが見つかりません: ${slotId}`);
    return;
  }
  const path = `slot_images/common/${imageFile}`;
  const placeholder = `slot_images/common/placeholder.png`;

  img.onerror = () => {
    console.warn(`⚠️ image load failed for ${slotId}, fallback`);
    img.src = placeholder;
  };

  img.onload = () => {
    console.log(`✅ image loaded: ${slotId}, src: ${img.src}, height: ${img.offsetHeight}px`);
  };

  img.src = path;
  img.style.maxHeight = "80px";
  img.style.maxWidth = "120px";
  img.style.height = "auto";
}

function safe(value, fallback = "") {
  return value === null || value === undefined ? fallback : value;
}

async function randomizeAll() {
  const structureId = getStructureId();
  const data = await loadStructureData(structureId);
  if (!data) return;

  const slotMap = {
    "slot-s": safe(data.subject),
    "slot-aux": safe(data.auxiliary),
    "slot-v": safe(data.verb),
    "slot-o1": safe(data.object),
    "slot-o_v": safe(data.object_verb),
    "slot-c1": safe(data.complement),
    "slot-o2": safe(data.object2),
    "slot-c2": safe(data.complement2),
    "slot-m1": safe(data.adverbial),
    "slot-m2": safe(data.adverbial2),
    "slot-m3": safe(data.adverbial3),

    // 🔽 sub-slot (slot-o1配下など)
    "slot-o1-m1": safe(data.sub_m1),
    "slot-o1-s": safe(data.sub_s),
    "slot-o1-aux": safe(data.sub_aux),
    "slot-o1-m2": safe(data.sub_m2),
    "slot-o1-v": safe(data.sub_v),
    "slot-o1-c1": safe(data.sub_c1),
    "slot-o1-o1": safe(data.sub_o1),
    "slot-o1-o2": safe(data.sub_o2),
    "slot-o1-c2": safe(data.sub_c2),
    "slot-o1-m3": safe(data.sub_m3)
  };

  for (const [slotId, text] of Object.entries(slotMap)) {
    updateSlotDisplay(slotId, text);
  }

  const imageMap = {
    "slot-s": data.image_s,
    "slot-aux": data.image_aux,
    "slot-v": data.image_v,
    "slot-o1": data.image_o1,
    "slot-o_v": data.image_o_v,
    "slot-c1": data.image_c1,
    "slot-o2": data.image_o2,
    "slot-c2": data.image_c2,
    "slot-m1": data.image_m1,
    "slot-m2": data.image_m2,
    "slot-m3": data.image_m3,

    // 🔽 sub-slot images
    "slot-o1-m1": data.image_sub_m1,
    "slot-o1-s": data.image_sub_s,
    "slot-o1-aux": data.image_sub_aux,
    "slot-o1-m2": data.image_sub_m2,
    "slot-o1-v": data.image_sub_v,
    "slot-o1-c1": data.image_sub_c1,
    "slot-o1-o1": data.image_sub_o1,
    "slot-o1-o2": data.image_sub_o2,
    "slot-o1-c2": data.image_sub_c2,
    "slot-o1-m3": data.image_sub_m3
  };

  for (const [slotId, imgFile] of Object.entries(imageMap)) {
    if (!imgFile) continue;
    updateSlotImage(slotId, imgFile);
  }
}

function randomizeSlot(data, key) {
  const contentMap = {
    s: data.subject,
    aux: data.auxiliary,
    v: data.verb,
    o1: data.object,
    o_v: data.object_verb,
    c1: data.complement,
    o2: data.object2,
    c2: data.complement2,
    m1: data.adverbial,
    m2: data.adverbial2,
    m3: data.adverbial3,

    // sub-slot
    "o1-m1": data.sub_m1,
    "o1-s": data.sub_s,
    "o1-aux": data.sub_aux,
    "o1-m2": data.sub_m2,
    "o1-v": data.sub_v,
    "o1-c1": data.sub_c1,
    "o1-o1": data.sub_o1,
    "o1-o2": data.sub_o2,
    "o1-c2": data.sub_c2,
    "o1-m3": data.sub_m3
  };

  updateSlotDisplay(`slot-${key}`, safe(contentMap[key]));
}

document.addEventListener("DOMContentLoaded", async () => {
  const structureId = getStructureId();
  const data = await loadStructureData(structureId);
  if (!data) return;
  randomizeAll();

  window.latestStructureData = data;
  generateSlotO1Details(data);


  const allBtn = document.getElementById("randomize-all");
  if (allBtn) allBtn.addEventListener("click", () => randomizeAll());

  
  // slot-o1 配下に <details><summary>構造詳細文要素</summary> を生成し sub-slot を内包
  


  document.querySelectorAll(".randomize-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const key = btn.dataset.slot;
      randomizeSlot(data, key);
    });
  });
});




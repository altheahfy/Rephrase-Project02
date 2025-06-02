// slot画像の表示関数
export function updateSlotImage(slotId, imgFile) {
  const element = document.getElementById(slotId);
  if (!element) return;

  // 一度既存のimgを消す
  const existing = element.querySelector("img");
  if (existing) element.removeChild(existing);

  // 新しいimgを挿入
  const img = document.createElement("img");
  img.src = `slot_images/common/${imgFile}`;
  img.alt = slotId;
  img.style.maxHeight = "80px";
  img.style.maxWidth = "120px";
  img.style.height = "auto";

  element.appendChild(img);
}

// slot画像をまとめて適用
export function applyImages(data) {
  const imageMap = {
    "slot-s": data.image_s,
    "slot-aux": data.image_aux,
    "slot-v": data.image_v,
    "slot-c1": data.image_c1,
    "slot-o1": data.image_o1,
    "slot-o2": data.image_o2,
    "slot-c2": data.image_c2,
    "slot-m1": data.image_m1,
    "slot-m2": data.image_m2,
    "slot-m3": data.image_m3,

    // sub-slot images
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
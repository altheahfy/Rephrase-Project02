import { updateSlotDisplay, safe } from './common.js';

// 主要10スロットにテキストを適用する
export function applySlotText(data) {
  const textMap = {
    "slot-s": data.chunk_s,
    "slot-aux": data.chunk_aux,
    "slot-v": data.chunk_v,
    "slot-c1": data.chunk_c1,
    "slot-o1": data.chunk_o1,
    "slot-o2": data.chunk_o2,
    "slot-c2": data.chunk_c2,
    "slot-m1": data.chunk_m1,
    "slot-m2": data.chunk_m2,
    "slot-m3": data.chunk_m3
  };

  for (const [slotId, text] of Object.entries(textMap)) {
    updateSlotDisplay(slotId, safe(text));
  }
}

// sub-slot配下の10スロットにもテキストを適用する
export function applySubSlotText(data) {
  const subTextMap = {
    "slot-o1-m1": data.chunk_sub_m1,
    "slot-o1-s": data.chunk_sub_s,
    "slot-o1-aux": data.chunk_sub_aux,
    "slot-o1-m2": data.chunk_sub_m2,
    "slot-o1-v": data.chunk_sub_v,
    "slot-o1-c1": data.chunk_sub_c1,
    "slot-o1-o1": data.chunk_sub_o1,
    "slot-o1-o2": data.chunk_sub_o2,
    "slot-o1-c2": data.chunk_sub_c2,
    "slot-o1-m3": data.chunk_sub_m3
  };

  for (const [slotId, text] of Object.entries(subTextMap)) {
    updateSlotDisplay(slotId, safe(text));
  }
}
import { updateSlotDisplay, updateSlotImage } from './image_handler.js';

/**
 * 全slot（上位 + slot-o1配下）に対して、テキストと画像を一括で反映
 */
export function randomizeAll(data) {
  const slotMap = {
    "slot-s": data.subject,
    "slot-aux": data.auxiliary,
    "slot-v": data.verb,
    "slot-o1": data.object,
    "slot-o_v": data.object_verb,
    "slot-c1": data.complement,
    "slot-o2": data.object2,
    "slot-c2": data.complement2,
    "slot-m1": data.adverbial,
    "slot-m2": data.adverbial2,
    "slot-m3": data.adverbial3,
    "slot-o1-m1": data.sub_m1,
    "slot-o1-s": data.sub_s,
    "slot-o1-aux": data.sub_aux,
    "slot-o1-m2": data.sub_m2,
    "slot-o1-v": data.sub_v,
    "slot-o1-c1": data.sub_c1,
    "slot-o1-o1": data.sub_o1,
    "slot-o1-o2": data.sub_o2,
    "slot-o1-c2": data.sub_c2,
    "slot-o1-m3": data.sub_m3
  };

  for (const [slotId, text] of Object.entries(slotMap)) {
    if (text) updateSlotDisplay(slotId, text);
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
    if (imgFile) updateSlotImage(slotId, imgFile);
  }
}
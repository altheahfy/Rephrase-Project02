// test_controller.js
import { renderAllSlots } from './renderer_core.js';

// テスト用の仮画像マップ（全スロットに共通プレースホルダー画像を割り当て）
const testSlotImageMap = {
  "slot-o1-sub-m1": "slot_images/common/placeholder.png",
  "slot-o1-sub-s": "slot_images/common/placeholder.png",
  "slot-o1-sub-aux": "slot_images/common/placeholder.png",
  "slot-o1-sub-m2": "slot_images/common/placeholder.png",
  "slot-o1-sub-v": "slot_images/common/placeholder.png",
  "slot-o1-sub-c": "slot_images/common/placeholder.png",
  "slot-o1-sub-o1": "slot_images/common/placeholder.png",
  "slot-o1-sub-o2": "slot_images/common/placeholder.png",
  "slot-o1-sub-c2": "slot_images/common/placeholder.png",
  "slot-o1-sub-m3": "slot_images/common/placeholder.png"
};

// DOMがロードされたら描画実行
window.addEventListener("DOMContentLoaded", () => {
  renderAllSlots(testSlotImageMap);
});
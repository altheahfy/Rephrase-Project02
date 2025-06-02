import { updateSlotDisplay, safe } from './common.js';
import { applyImages } from './image_handler.js';
import { applySlotText, applySubSlotText } from './structure_analyzer.js';

// 全体ランダマイズ処理：全slotにランダム表示を適用
export function randomizeAll(data) {
  // 画像表示
  applyImages(data);

  // テキスト表示（主スロット＋subスロット）
  applySlotText(data);
  applySubSlotText(data);
}
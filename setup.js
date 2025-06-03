import { grammarData } from './grammar_data.js';
import { renderSubSlotsOnce } from './subslot_renderer.js';
import { randomizeAll } from './randomizer_all.js';
import { randomizeSlot } from './randomizer_individual.js';

/**
 * ページ初期化：構文読み込み・描画・ランダマイズ・イベントバインド
 */
export async function setup(structureId = "010") {
  const data = grammarData[structureId];
  if (!data || !data.embedded_structure) {
    console.error(`構文データが見つかりません: ${structureId}`);
    return;
  }

  renderSubSlotsOnce(data.embedded_structure, "slot-o1-sub");
  randomizeAll(data);

  // グローバルにも保持（他イベントで再利用）
  window.latestStructureData = data;

  // ボタンイベント登録
  document.querySelectorAll(".randomize-btn").forEach((btn) => {
    const key = btn.dataset.slot;
    btn.addEventListener("click", () => {
      randomizeSlot(data, key);
    });
  });
}
import { loadXlsxSheet } from './utils/xlsx_loader.js';

document.addEventListener('DOMContentLoaded', () => {
  const randomizeButton = document.getElementById('randomize-all');
  if (randomizeButton) {
    randomizeButton.addEventListener('click', async () => {
      const json = await loadXlsxSheet('data/grammar_data0001.xlsx', '増殖①');

      // 文法項目番号の一覧を取得（重複排除）
      const allIds = [...new Set(json.map(row => String(row['文法項目番号']).trim()))];

      // ランダムに1つ選ぶ
      const chosenId = allIds[Math.floor(Math.random() * allIds.length)];

      // 対象行を抽出
      const targetRows = json.filter(row => String(row['文法項目番号']).trim() === chosenId);
      if (targetRows.length === 0) {
        console.error("❌ 対象文法項目が見つかりませんでした:", chosenId);
        return;
      }

      const slotData = {};

      for (const row of targetRows) {
        const internal = row['構文要素ID']; // sub_s など
        const value = row['表示テキスト'];  // 表示内容

        if (!internal || !value) continue;

        let slotId = '';
        if (internal.startsWith('sub_')) {
          // サブスロットの場合
          const slotSuffix = internal.replace('sub_', '');
          slotId = `slot-o1-sub-${slotSuffix}`;
        } else {
          // 上位スロットの場合
          slotId = `slot-${internal}`;
        }

        slotData[slotId] = value;
      }

      console.log("📘 構文スロットデータ:", slotData);

      for (const [slotId, value] of Object.entries(slotData)) {
        const textEl = document.querySelector(`#${slotId} .slot-text`);
        if (textEl) {
          textEl.textContent = value;
        } else {
          console.warn(`⚠️ テキスト要素が見つかりませんでした: ${slotId}`);
        }
      }
    });
  }
});
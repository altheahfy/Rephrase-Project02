// randomizer_controller.js（PH-35-R-FIX-2 完全対応版）
import { randomizeAll } from './randomizer_all.js';
import { renderAllSlots } from './renderer_core.js';

export function handleExcelFileUpload(file) {
  const reader = new FileReader();
  reader.onload = function (e) {
    let slotData = {};
    let parentSlot = null;
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const sheet = workbook.Sheets['増殖①'];
    if (!sheet) {
      alert('シート「増殖①」が見つかりません');
      return;
    }
    let chosenId, targetRows = [];
    const json = XLSX.utils.sheet_to_json(sheet);

    // 🔧 修正: NaN除外 + 空白除外
    const availableIds = [...new Set(
      json
        .map(row => String(parseInt(row['文法項目番号'])))
        .filter(id => id && id !== "NaN")
    )];

    while (targetRows.length === 0 && availableIds.length > 0) {
      const index = Math.floor(Math.random() * availableIds.length);
      chosenId = availableIds.splice(index, 1)[0];

      // 🔧 修正: Slotが空の行を除外して targetRows 抽出
      targetRows = json.filter(row => {
        const idMatch = String(parseInt(row['文法項目番号'])) === chosenId;
        const hasSlot = !!(row['Slot'] || '').trim();
        return idMatch && hasSlot;
      });
    }

    console.log("🧪 選出構文ID:", chosenId);
    console.log("📑 targetRows:", targetRows);

    // PH-36-R-BUILD-2: 親スロット先処理
    for (const row of targetRows) {
      const rawSlot = (row['Slot'] || '').trim().toLowerCase();
      const internalSub = (row['内部スロット'] || '').trim();
      const value = (row['Phrase'] || '').trim();
      if (!value || internalSub.startsWith('sub-')) continue;
      const slotId = `slot-${rawSlot}`;
      slotData[slotId] = value;
    }

    // subslot 後処理（parentSlot 使用）
    for (const row of targetRows) {
      const rawSlot = (row['Slot'] || '').trim().toLowerCase();
      const internalSub = (row['内部スロット'] || '').trim().toLowerCase();
      const value = (row['Phrase'] || '').trim();
      if (!value || !internalSub.startsWith('sub-')) continue;
      const slotId = `slot-${rawSlot}-sub-${internalSub.replace('sub-', '')}`;
      slotData[slotId] = value;
    }

    console.log('📘 構文スロットデータ:', slotData);
    window.lastSlotData = slotData;
    randomizeAll(slotData);
    console.log("🔍 slotData 内容:", slotData);
    renderAllSlots(slotData);
  }; // ← 正しく閉じる

  reader.readAsArrayBuffer(file); // ← 関数外に移動
}

// グローバル登録
window.handleExcelFileUpload = handleExcelFileUpload;
window.randomizeAll = randomizeAll;


// randomizer_controller.js（PH-35-R-FIX-2 完全対応版）
import { randomizeAll } from './randomizer_all.js';

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
    const json = XLSX.utils.sheet_to_json(sheet);

    let chosenId, targetRows = [];
    const availableIds = [...new Set(json.map(row => String(row['文法項目番号']).trim()))];

    while (targetRows.length === 0 && availableIds.length > 0) {
      const index = Math.floor(Math.random() * availableIds.length);
      chosenId = availableIds.splice(index, 1)[0]; // 選んだIDは一度使ったら除外
      targetRows = json.filter(row => String(row['文法項目番号']).trim() === chosenId);
    }

    
    console.log("🧪 選出構文ID:", chosenId);
    console.log("📑 targetRows:", targetRows);
    for (const row of targetRows) {
  const rawSlot = (row['Slot'] || '').trim();
  const internalSub = (row['内部スロット'] || '').trim();
  const value = (row['Phrase'] || '').trim();
  if (!value) continue;

  let slotId = '';

  if (internalSub.startsWith('sub-')) {
    if (!parentSlot) {
      console.warn(`⚠️ 親スロット未設定で subslot 検出: ${internalSub}`);
      continue;
    }
    const child = internalSub.replace('sub-', '');
    slotId = `slot-${parentSlot}-sub-${child}`;
  } else if (rawSlot) {
    slotId = `slot-${rawSlot}`;
    parentSlot = rawSlot; // 親スロット更新
  } else {
    console.warn('⚠️ Slot情報が欠落しています（valueは存在）:', value);
    continue;
  }

  slotData[slotId] = value;
}

    console.log('📘 構文スロットデータ:', slotData);
    window.lastSlotData = slotData;
    randomizeAll(slotData);
  };
  reader.readAsArrayBuffer(file);
}

// グローバル登録
window.handleExcelFileUpload = handleExcelFileUpload;
window.randomizeAll = randomizeAll;

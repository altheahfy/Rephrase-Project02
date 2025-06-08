
// randomizer_controller.js（PH-35-R-FIX-2 対応版）
import { randomizeAll } from './randomizer_all.js';

export function handleExcelFileUpload(file) {
  const reader = new FileReader();
  reader.onload = function (e) {
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const sheet = workbook.Sheets['増殖①'];
    if (!sheet) {
      alert('シート「増殖①」が見つかりません');
      return;
    }
    const json = XLSX.utils.sheet_to_json(sheet);

    const allIds = [...new Set(json.map(row => String(row['文法項目番号']).trim()))];
    const chosenId = allIds[Math.floor(Math.random() * allIds.length)];
    const targetRows = json.filter(row => String(row['文法項目番号']).trim() === chosenId);
    if (targetRows.length === 0) {
      console.warn('⚠️ 対象文法項目が見つかりません:', chosenId);
      return;
    }

    const slotData = {};
    let parentSlot = null;

    for (const row of targetRows) {
      const internal = row['Slot'];
      if (internal && !internal.startsWith('sub_')) {
        parentSlot = internal;
      }
    }

    for (const row of targetRows) {
      const rawSlot = row['Slot'];
      const internalSub = row['内部スロット'];
      const value = row['Phrase'];
      if (!value) continue;

      let slotId = '';

      if (internalSub && internalSub.startsWith('sub-')) {
        if (!parentSlot) {
          console.warn('⚠️ 親スロット未設定で subslot 検出:', internalSub);
          continue;
        }
        const child = internalSub.replace('sub-', '');
        slotId = `slot-${parentSlot}-sub-${child}`;
      } else if (rawSlot) {
        slotId = `slot-${rawSlot}`;
        parentSlot = rawSlot; // 更新
      } else {
        continue; // Slot も subslot も無ければ無視
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

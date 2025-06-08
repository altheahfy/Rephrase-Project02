
// randomizer_controller.js（グローバル関数対応）
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
      if (!internal || !internal.trim()) continue;
      if (!internal.startsWith('sub_')) {
        parentSlot = internal;
      }
    }

    for (const row of targetRows) {
      const internal = row['Slot'];
      const value = row['Phrase'];
      if (!internal || !value) continue;

      let slotId = '';
      if (internal.startsWith('sub_')) {
        if (!parentSlot) {
          console.warn('⚠️ 親スロットが未定義のまま sub_ スロットが検出されました:', internal);
          continue;
        }
        const child = internal.replace('sub_', '');
        slotId = `slot-${parentSlot}-sub-${child}`;
      } else {
        slotId = `slot-${internal}`;
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

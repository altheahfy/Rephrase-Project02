// randomizer_controller.js（修正版：構文スロットUI完全対応）
// 必要ライブラリ: SheetJS (XLSX)
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

    // 文法項目番号のランダム抽出
    const allIds = [...new Set(json.map(row => row['文法項目番号']))];
    const chosenId = allIds[Math.floor(Math.random() * allIds.length)];

    // 対象行を抽出
    const targetRows = json.filter(row => row['文法項目番号'] === chosenId);

    // slotId生成マッピング関数
    function determineSlotId(row) {
      const slot = row['Slot'];
      const internal = row['内部スロット'];
      if (internal) {
        return {
          sub_s: 'slot-o1-s', sub_aux: 'slot-o1-aux', sub_v: 'slot-o1-v',
          sub_o1: 'slot-o1-o1', sub_o2: 'slot-o1-o2', sub_c1: 'slot-o1-c1',
          sub_c2: 'slot-o1-c2', sub_m1: 'slot-o1-m1', sub_m2: 'slot-o1-m2', sub_m3: 'slot-o1-m3'
        }[internal] || null;
      } else if (slot) {
        return {
          S: 'slot-s', V: 'slot-v', AUX: 'slot-aux', C: 'slot-c', 'O-V': 'slot-o_v',
          O1: 'slot-o1', O2: 'slot-o2', C1: 'slot-c1', C2: 'slot-c2',
          M1: 'slot-m1', M2: 'slot-m2', M3: 'slot-m3'
        }[slot] || null;
      }
      return null;
    }

    const slotData = {};
    for (const row of targetRows) {
      const slotId = determineSlotId(row);
      if (!slotId) continue;
      const value = row['Phrase'] || row['内部要素'];
      if (value) slotData[slotId] = value;
    }

    console.log("📘 構文スロットデータ:", slotData);
    randomizeAll(slotData);
  };
  reader.readAsArrayBuffer(file);
}

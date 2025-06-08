// randomizer_controller.js（構文修復済み + subslot描画対応）
import { randomizeAll } from './randomizer_all.js';
import { renderAllSlots, renderAllSubslots } from './renderer_core.js';

export function handleExcelFileUpload(file) {
  const reader = new FileReader();
  reader.onload = function (e) {
    let slotData = {};
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const sheet = workbook.Sheets['増殖①'];
    if (!sheet) {
      alert('シート「増殖①」が見つかりません');
      return;
    }

    let chosenId, targetRows = [];
    const json = XLSX.utils.sheet_to_json(sheet);

    const availableIds = [...new Set(
      json.map(row => String(parseInt(row['文法項目番号'])))
          .filter(id => id && id !== "NaN")
    )];

    while (targetRows.length === 0 && availableIds.length > 0) {
      const index = Math.floor(Math.random() * availableIds.length);
      chosenId = availableIds.splice(index, 1)[0];

      targetRows = json.filter(row => {
        const idMatch = String(parseInt(row['文法項目番号'])) === chosenId;
        const hasSlot = !!(row['Slot'] || '').trim();
        return idMatch && hasSlot;
      });
    }

    for (const row of targetRows) {
      const rawSlot = (row['Slot'] || '').trim().toLowerCase();
      const internalSub = (row['内部スロット'] || '').trim();
      const value = (row['Phrase'] || '').trim();
      const verb = (row['A_group_V'] || '').trim();

      if (verb && !slotData['slot-v']) slotData['slot-v'] = verb;
      if (!value || internalSub.startsWith('sub-')) continue;
      slotData[`slot-${rawSlot}`] = value;
    }

    for (const row of targetRows) {
      const rawSlot = (row['Slot'] || '').trim().toLowerCase();
      const internalSub = (row['内部スロット'] || '').trim().toLowerCase();
      const value = (row['Phrase'] || '').trim();
      if (!value || !internalSub.startsWith('sub-')) continue;
      slotData[`slot-${rawSlot}-sub-${internalSub.replace('sub-', '')}`] = value;
    }

    console.log("🧪 選出構文ID:", chosenId);
    console.log("📘 slotData:", slotData);

    window.lastSlotData = slotData;
    randomizeAll(slotData);
    renderAllSlots(slotData);
    renderAllSubslots(slotData);
  };

  reader.readAsArrayBuffer(file);
}

export function extractSlotDataFromWorkbook(workbook) {
  const sheet = workbook.Sheets['増殖①'];
  if (!sheet) {
    alert('シート「増殖①」が見つかりません');
    return null;
  }

  let chosenId, targetRows = [];
  const json = XLSX.utils.sheet_to_json(sheet);

  const availableIds = [...new Set(
    json.map(row => String(parseInt(row['文法項目番号'])))
        .filter(id => id && id !== "NaN")
  )];

  while (targetRows.length === 0 && availableIds.length > 0) {
    const index = Math.floor(Math.random() * availableIds.length);
    chosenId = availableIds.splice(index, 1)[0];

    targetRows = json.filter(row => {
      const idMatch = String(parseInt(row['文法項目番号'])) === chosenId;
      const hasSlot = !!(row['Slot'] || '').trim();
      return idMatch && hasSlot;
    });
  }

  const slotData = {};

  for (const row of targetRows) {
    const rawSlot = (row['Slot'] || '').trim().toLowerCase();
    const internalSub = (row['内部スロット'] || '').trim();
    const value = (row['Phrase'] || '').trim();
    const verb = (row['A_group_V'] || '').trim();

    if (verb && !slotData['slot-v']) slotData['slot-v'] = verb;
    if (!value || internalSub.startsWith('sub-')) continue;
    slotData[`slot-${rawSlot}`] = value;
  }

  for (const row of targetRows) {
    const rawSlot = (row['Slot'] || '').trim().toLowerCase();
    const internalSub = (row['内部スロット'] || '').trim().toLowerCase();
    const value = (row['Phrase'] || '').trim();
    if (!value || !internalSub.startsWith('sub-')) continue;
    slotData[`slot-${rawSlot}-sub-${internalSub.replace('sub-', '')}`] = value;
  }

  console.log("🧪 再抽選 chosenId:", chosenId);
  console.log("📘 slotData (再抽選):", slotData);
  return slotData;
}

// ✅ 正常定義化
export function injectAllSubslotTexts(containerId) {
  const subslots = document.querySelectorAll(`#${containerId} .subslot`);
  subslots.forEach(subslot => {
    const slotId = subslot.id;
    const text = subslot.querySelector(".slot-text");
    if (text) {
      const key = slotId.split("-").pop().toUpperCase();
      text.textContent = `【${key}】の文法ガイド`;
    }
  });
}

window.handleExcelFileUpload = handleExcelFileUpload;
window.randomizeAll = randomizeAll;


export function flowIntoO1StaticSlot(data) {
  const o1Data = data.find(slot => slot.Slot === 'O1');
  if (!o1Data) {
    console.warn('⚠ O1 データが見つかりません');
    return;
  }

  // 上位O1スロットの流し込み
  const o1TextContainer = document.querySelector('#slot-o1 .slot-text');
  if (o1TextContainer) {
    o1TextContainer.textContent = o1Data.SlotPhrase || '';
    console.log(`✅ O1 スロットに流し込み: ${o1Data.SlotPhrase || ''}`);
  } else {
    console.warn('⚠ O1 スロットの .slot-text DOM が見つかりません');
  }

  // サブスロットの流し込み
  if (o1Data.Subslots && Array.isArray(o1Data.Subslots)) {
    o1Data.Subslots.forEach(sub => {
      const subId = sub.SubslotID.toLowerCase();
      const subContainer = document.querySelector(`#slot-o1-sub-${subId} .slot-text`);
      if (subContainer) {
        subContainer.textContent = sub.SubslotElement || '';
        console.log(`✅ O1 サブスロット slot-o1-sub-${subId} に流し込み: ${sub.SubslotElement || ''}`);
      } else {
        console.warn(`⚠ サブスロット DOM 見つからず: slot-o1-sub-${subId}`);
      }

      const subImg = document.querySelector(`#slot-o1-sub-${subId} .slot-image`);
      if (subImg && sub.imagePath) {
        subImg.src = sub.imagePath;
        console.log(`✅ O1 サブスロット slot-o1-sub-${subId} に画像流し込み: ${sub.imagePath}`);
      }
    });
  }
}

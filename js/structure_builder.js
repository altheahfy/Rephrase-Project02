
// 差分案: O1 の場合は PhraseType にかかわらず SlotPhrase を表示する処理を追加

if (item.Slot === 'O1' || item.PhraseType === 'word') {
  // O1 または word の場合は SlotPhrase と SlotText を表示
  const slotPhraseElement = document.createElement('div');
  slotPhraseElement.className = 'slot-phrase';
  slotPhraseElement.textContent = item.SlotPhrase;
  wrapper.appendChild(slotPhraseElement);

  const slotTextElement = document.createElement('div');
  slotTextElement.className = 'slot-text';
  slotTextElement.textContent = item.SlotText;
  wrapper.appendChild(slotTextElement);
} else {
  // その他の場合は slot-mark のみ表示
  const markElement = document.createElement('div');
  markElement.className = 'slot-mark';
  markElement.textContent = '▶';
  wrapper.appendChild(markElement);
}

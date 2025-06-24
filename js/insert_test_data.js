
window.onload = function() {
    const testData = [ /* 現在の testData と同じ内容をここに配置 */ ];

    testData.forEach(data => {
        const slotElement = document.getElementById(data.Slot);
        if (slotElement) {
            // SlotPhrase の要素を作成 or 更新
            let phraseElement = slotElement.querySelector('.slot-phrase');
            if (!phraseElement) {
                phraseElement = document.createElement('div');
                phraseElement.className = 'slot-phrase';
                slotElement.appendChild(phraseElement);
            }
            phraseElement.textContent = data.SlotPhrase;

            // SlotText の要素を作成 or 更新
            let textElement = slotElement.querySelector('.slot-text');
            if (!textElement) {
                textElement = document.createElement('div');
                textElement.className = 'slot-text';
                slotElement.appendChild(textElement);
            }
            textElement.textContent = data.SlotText;

            console.log(`✅ 書き込み成功: ${data.Slot}`);
        } else {
            console.warn(`⚠ スロットが見つからない: ${data.Slot}`);
        }
    });
};

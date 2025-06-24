
window.onload = function() {
    const testData = [
        { Slot: "M1", SlotPhrase: "That afternoon at the crucial point in the presentation", SlotText: "あの、～の時点・地点で、～の中に、～の中で", PhraseType: "word" },
        { Slot: "S", SlotPhrase: "the manager who had recently taken charge of the project", SlotText: "最近", PhraseType: "clause" },
        { Slot: "Aux", SlotPhrase: "had to", SlotText: "～しなければならなかった", PhraseType: "word" },
        { Slot: "V", SlotPhrase: "make", SlotText: "", PhraseType: "word" }
    ];

    testData.forEach(data => {
        const slotId = 'slot-' + data.Slot.toLowerCase();
        const slotElement = document.getElementById(slotId);
        console.log(`探している: ${slotId}`, slotElement);
        if (slotElement) {
            const slotTextElement = slotElement.querySelector('.slot-text');
            if (slotTextElement) {
                slotTextElement.textContent = data.SlotPhrase + " " + data.SlotText;
                console.log(`✅ ${slotId} に挿入成功: ${slotTextElement.textContent}`);
            } else {
                console.warn(`⚠ slot-text が見つからない: ${slotId}`);
            }
        } else {
            console.warn(`⚠ スロットが見つからない: ${slotId}`);
        }
    });
};

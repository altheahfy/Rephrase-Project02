
window.onload = function() {
    const testData = [
        { Slot: "slot-m1", SlotPhrase: "TEST_SLOT-M1", SlotText: "テストデータ" },
        { Slot: "slot-s", SlotPhrase: "TEST_SLOT-S", SlotText: "テストデータ" },
        { Slot: "slot-aux", SlotPhrase: "TEST_SLOT-AUX", SlotText: "テストデータ" },
        { Slot: "slot-m2", SlotPhrase: "TEST_SLOT-M2", SlotText: "テストデータ" },
        { Slot: "slot-v", SlotPhrase: "TEST_SLOT-V", SlotText: "テストデータ" },
        { Slot: "slot-c1", SlotPhrase: "TEST_SLOT-C1", SlotText: "テストデータ" },
        { Slot: "slot-o1", SlotPhrase: "TEST_SLOT-O1", SlotText: "テストデータ" },
        { Slot: "slot-o2", SlotPhrase: "TEST_SLOT-O2", SlotText: "テストデータ" },
        { Slot: "slot-c2", SlotPhrase: "TEST_SLOT-C2", SlotText: "テストデータ" },
        { Slot: "slot-m3", SlotPhrase: "TEST_SLOT-M3", SlotText: "テストデータ" }
    ];

    testData.forEach(data => {
        const slotElement = document.getElementById(data.Slot);
        if (slotElement) {
            const phraseElement = slotElement.querySelector('.slot-phrase');
            if (phraseElement) {
                phraseElement.textContent = data.SlotPhrase;
                console.log(`✅ phrase書き込み成功: ${data.Slot}`);
            } else {
                console.warn(`⚠ slot-phrase が見つからない: ${data.Slot}`);
            }

            const textElement = slotElement.querySelector('.slot-text');
            if (textElement) {
                textElement.textContent = data.SlotText;
                console.log(`✅ text書き込み成功: ${data.Slot}`);
            } else {
                console.warn(`⚠ slot-text が見つからない: ${data.Slot}`);
            }
        } else {
            console.warn(`⚠ スロットが見つからない: ${data.Slot}`);
        }
    });
};

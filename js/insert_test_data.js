
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
        { Slot: "slot-m3", SlotPhrase: "TEST_SLOT-M3", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-m1", SlotPhrase: "TEST_SLOT-O1-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-s", SlotPhrase: "TEST_SLOT-O1-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-aux", SlotPhrase: "TEST_SLOT-O1-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-m2", SlotPhrase: "TEST_SLOT-O1-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-v", SlotPhrase: "TEST_SLOT-O1-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-c1", SlotPhrase: "TEST_SLOT-O1-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-o1", SlotPhrase: "TEST_SLOT-O1-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-o2", SlotPhrase: "TEST_SLOT-O1-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-c2", SlotPhrase: "TEST_SLOT-O1-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-o1-sub-m3", SlotPhrase: "TEST_SLOT-O1-SUB-M3", SlotText: "テストデータ" }
    ];

    testData.forEach(data => {
        const slotElement = document.getElementById(data.Slot);
        console.log(`探している: ${data.Slot}`, slotElement);
        if (slotElement) {
            const slotTextElement = slotElement.querySelector('.slot-text');
            if (slotTextElement) {
                slotTextElement.textContent = data.SlotPhrase + " " + data.SlotText;
                console.log(`✅ ${data.Slot} に挿入成功: ${slotTextElement.textContent}`);
            } else {
                console.warn(`⚠ slot-text が見つからない: ${data.Slot}`);
            }
        } else {
            console.warn(`⚠ スロットが見つからない: ${data.Slot}`);
        }
    });
};

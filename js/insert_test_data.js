
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
        { Slot: "slot-o1-sub-m3", SlotPhrase: "TEST_SLOT-O1-SUB-M3", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-m1", SlotPhrase: "TEST_SLOT-M1-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-s", SlotPhrase: "TEST_SLOT-M1-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-aux", SlotPhrase: "TEST_SLOT-M1-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-m2", SlotPhrase: "TEST_SLOT-M1-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-v", SlotPhrase: "TEST_SLOT-M1-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-c1", SlotPhrase: "TEST_SLOT-M1-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-o1", SlotPhrase: "TEST_SLOT-M1-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-o2", SlotPhrase: "TEST_SLOT-M1-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-c2", SlotPhrase: "TEST_SLOT-M1-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-m1-sub-m3", SlotPhrase: "TEST_SLOT-M1-SUB-M3", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-m1", SlotPhrase: "TEST_SLOT-O2-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-s", SlotPhrase: "TEST_SLOT-O2-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-aux", SlotPhrase: "TEST_SLOT-O2-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-m2", SlotPhrase: "TEST_SLOT-O2-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-v", SlotPhrase: "TEST_SLOT-O2-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-c1", SlotPhrase: "TEST_SLOT-O2-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-o1", SlotPhrase: "TEST_SLOT-O2-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-o2", SlotPhrase: "TEST_SLOT-O2-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-c2", SlotPhrase: "TEST_SLOT-O2-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-o2-sub-m3", SlotPhrase: "TEST_SLOT-O2-SUB-M3", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-m1", SlotPhrase: "TEST_SLOT-M2-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-s", SlotPhrase: "TEST_SLOT-M2-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-aux", SlotPhrase: "TEST_SLOT-M2-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-m2", SlotPhrase: "TEST_SLOT-M2-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-v", SlotPhrase: "TEST_SLOT-M2-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-c1", SlotPhrase: "TEST_SLOT-M2-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-o1", SlotPhrase: "TEST_SLOT-M2-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-o2", SlotPhrase: "TEST_SLOT-M2-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-c2", SlotPhrase: "TEST_SLOT-M2-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-m2-sub-m3", SlotPhrase: "TEST_SLOT-M2-SUB-M3", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-m1", SlotPhrase: "TEST_SLOT-C2-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-s", SlotPhrase: "TEST_SLOT-C2-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-aux", SlotPhrase: "TEST_SLOT-C2-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-m2", SlotPhrase: "TEST_SLOT-C2-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-v", SlotPhrase: "TEST_SLOT-C2-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-c1", SlotPhrase: "TEST_SLOT-C2-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-o1", SlotPhrase: "TEST_SLOT-C2-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-o2", SlotPhrase: "TEST_SLOT-C2-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-c2", SlotPhrase: "TEST_SLOT-C2-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-c2-sub-m3", SlotPhrase: "TEST_SLOT-C2-SUB-M3", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-m1", SlotPhrase: "TEST_SLOT-M3-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-s", SlotPhrase: "TEST_SLOT-M3-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-aux", SlotPhrase: "TEST_SLOT-M3-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-m2", SlotPhrase: "TEST_SLOT-M3-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-v", SlotPhrase: "TEST_SLOT-M3-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-c1", SlotPhrase: "TEST_SLOT-M3-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-o1", SlotPhrase: "TEST_SLOT-M3-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-o2", SlotPhrase: "TEST_SLOT-M3-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-c2", SlotPhrase: "TEST_SLOT-M3-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-m3-sub-m3", SlotPhrase: "TEST_SLOT-M3-SUB-M3", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-m1", SlotPhrase: "TEST_SLOT-S-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-s", SlotPhrase: "TEST_SLOT-S-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-aux", SlotPhrase: "TEST_SLOT-S-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-m2", SlotPhrase: "TEST_SLOT-S-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-v", SlotPhrase: "TEST_SLOT-S-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-c1", SlotPhrase: "TEST_SLOT-S-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-o1", SlotPhrase: "TEST_SLOT-S-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-o2", SlotPhrase: "TEST_SLOT-S-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-c2", SlotPhrase: "TEST_SLOT-S-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-s-sub-m3", SlotPhrase: "TEST_SLOT-S-SUB-M3", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-m1", SlotPhrase: "TEST_SLOT-C-SUB-M1", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-s", SlotPhrase: "TEST_SLOT-C-SUB-S", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-aux", SlotPhrase: "TEST_SLOT-C-SUB-AUX", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-m2", SlotPhrase: "TEST_SLOT-C-SUB-M2", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-v", SlotPhrase: "TEST_SLOT-C-SUB-V", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-c1", SlotPhrase: "TEST_SLOT-C-SUB-C1", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-o1", SlotPhrase: "TEST_SLOT-C-SUB-O1", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-o2", SlotPhrase: "TEST_SLOT-C-SUB-O2", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-c2", SlotPhrase: "TEST_SLOT-C-SUB-C2", SlotText: "テストデータ" },
        { Slot: "slot-c-sub-m3", SlotPhrase: "TEST_SLOT-C-SUB-M3", SlotText: "テストデータ" }
    ];

    testData.forEach(data => {
        const slotElement = document.getElementById(data.Slot);
        if (slotElement) {
            const slotTextElement = slotElement.querySelector('.slot-text');
            if (slotTextElement) {
                
                const phraseElement = slotElement.querySelector('.slot-phrase');
                if (phraseElement) {
                    phraseElement.textContent = data.SlotPhrase;
                    console.log(`✅ phrase書き込み成功: ${data.Slot}`);
                }
                slotTextElement.textContent = data.SlotText;
                console.log(`✅ text書き込み成功: ${data.Slot}`);
    
                console.log(`✅ 書き込み成功: ${data.Slot} → ${slotTextElement.textContent}`);
            } else {
                console.warn(`⚠ slot-text が見つからない: ${data.Slot}`);
            }
        } else {
            console.warn(`⚠ スロットが見つからない: ${data.Slot}`);
        }
    });
};

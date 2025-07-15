// 🔍 現在の選択データ詳細調査スクリプト

function analyzeCurrentSelection() {
    console.log("🔍=== 現在選択データの詳細分析 ===");
    
    // 1. randomizer_all.jsの実行結果を確認
    if (window.selectedSlots) {
        console.log("🎯 selectedSlots全体:", window.selectedSlots);
        
        // O1スロットの詳細分析
        const o1Slots = window.selectedSlots.filter(s => s.Slot === "O1");
        console.log("🔍 O1スロット数:", o1Slots.length);
        
        // 🔍 修正効果確認：同一例文内複数O1か異なる例文混在か
        if (o1Slots.length > 1) {
            const uniqueExampleIds = [...new Set(o1Slots.map(s => s.例文ID))];
            if (uniqueExampleIds.length === 1) {
                console.log("✅ 同一例文内の複数O1 (分離疑問詞構文)");
            } else {
                console.warn("⚠️ 異なる例文由来のO1混在 (修正が必要)");
            }
        }
        
        o1Slots.forEach((slot, index) => {
            console.log(`  O1[${index}]:`, {
                例文ID: slot.例文ID,
                V_group_key: slot.V_group_key,
                Slot_display_order: slot.Slot_display_order,
                PhraseType: slot.PhraseType,
                SlotPhrase: slot.SlotPhrase,
                SubslotID: slot.SubslotID
            });
        });
        
        // M1とSの順序確認
        const m1Slots = window.selectedSlots.filter(s => s.Slot === "M1");
        const sSlots = window.selectedSlots.filter(s => s.Slot === "S");
        
        console.log("🔍 M1スロット:", m1Slots.map(s => ({
            V_group_key: s.V_group_key,
            Slot_display_order: s.Slot_display_order,
            SlotPhrase: s.SlotPhrase
        })));
        
        console.log("🔍 Sスロット:", sSlots.map(s => ({
            V_group_key: s.V_group_key,
            Slot_display_order: s.Slot_display_order,
            SlotPhrase: s.SlotPhrase
        })));
        
        // V_group_key混在確認
        const uniqueVGroups = [...new Set(window.selectedSlots.map(s => s.V_group_key))];
        console.log("🔍 選択されたV_group_key:", uniqueVGroups);
        if (uniqueVGroups.length > 1) {
            console.warn("⚠️ 複数のV_group_keyが混在しています！");
            uniqueVGroups.forEach(vgk => {
                const slotsInGroup = window.selectedSlots.filter(s => s.V_group_key === vgk);
                console.log(`  V_group_key=${vgk}:`, slotsInGroup.map(s => `${s.Slot}(${s.Slot_display_order})`));
            });
        }
    }
    
    // 2. DOMの実際の表示順序確認
    console.log("🔍=== DOM表示順序確認 ===");
    const dynamicArea = document.getElementById('dynamic-slot-area');
    if (dynamicArea) {
        const allElements = dynamicArea.children;
        console.log(`🔍 動的エリア要素数: ${allElements.length}`);
        Array.from(allElements).forEach((el, index) => {
            const displayOrder = el.dataset.displayOrder;
            const slotType = el.className.includes('subslot') ? 'subslot' : 'slot';
            const content = el.textContent.trim();
            console.log(`  [${index}] ${slotType} order=${displayOrder}: "${content}"`);
        });
    }
    
    // 3. 上位スロットの表示確認
    console.log("🔍=== 上位スロット表示確認 ===");
    const slotContainers = document.querySelectorAll('.slot-container');
    slotContainers.forEach(container => {
        const slotId = container.id;
        const phraseEl = container.querySelector('.slot-phrase');
        const phrase = phraseEl ? phraseEl.textContent.trim() : '';
        if (phrase) {
            console.log(`  ${slotId}: "${phrase}"`);
        }
    });
}

// 実行
analyzeCurrentSelection();

// insert_test_data_cleaned.js

window.onload = function () {
  if (!window.loadedJsonData) {
    console.warn("loadedJsonData is not set.");
    return;
  }

  clearUpperSlots();
  clearSubslots();
  syncUpperSlotsFromJson(window.loadedJsonData);
  syncSubslotsFromJson(window.loadedJsonData);
};

// 上位スロットの初期化（slot-s, slot-v など）
function clearUpperSlots() {
  const slotIds = [
    "slot-m1", "slot-s", "slot-aux", "slot-v",
    "slot-o1", "slot-o2", "slot-c1", "slot-c2",
    "slot-m2", "slot-m3"
  ];
  slotIds.forEach(id => {
    const container = document.getElementById(id);
    if (!container) return;
    const phrase = container.querySelector(".slot-phrase");
    const text = container.querySelector(".slot-text");
    if (phrase) phrase.textContent = "";
    if (text) text.textContent = "";
  });
}

// サブスロットの初期化（slot-s-sub-001 など）
function clearSubslots() {
  const subslotElements = document.querySelectorAll('[id*="-sub-"]');
  subslotElements.forEach(slot => {
    const phrase = slot.querySelector(".slot-phrase");
    const text = slot.querySelector(".slot-text");
    if (phrase) phrase.textContent = "";
    if (text) text.textContent = "";
  });
}

// 上位スロットの同期処理
function syncUpperSlotsFromJson(data) {
  data.forEach(item => {
    if (item.SubslotID === "" && item.PhraseType === "word") {
      const slotId = "slot-" + item.Slot.toLowerCase();
      const container = document.getElementById(slotId);
      if (!container) return;
      const phrase = container.querySelector(".slot-phrase");
      const text = container.querySelector(".slot-text");
      if (phrase && item.SlotPhrase) phrase.textContent = item.SlotPhrase;
      if (text && item.SlotText) text.textContent = item.SlotText;
    }
  });
}

// サブスロットの同期処理
function syncSubslotsFromJson(data) {
  data.forEach(item => {
    if (item.SubslotID !== "") {
      const slotId = "slot-" + item.Slot.toLowerCase() + "-sub-" + item.SubslotID;
      const container = document.getElementById(slotId);
      if (!container) return;
      const phrase = container.querySelector(".slot-phrase");
      const text = container.querySelector(".slot-text");
      if (phrase && item.SlotPhrase) phrase.textContent = item.SlotPhrase;
      if (text && item.SlotText) text.textContent = item.SlotText;
    }
  });
}
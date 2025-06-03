window.grammarData = {
  "010": {
    A: ["want", "hope", "plan"],
    B: { /* ...省略（前回同様）... */ },
    embedded_structure: {
      m1: {
        imagePath: "slot_images/common/soon.png",
        subslots: generateAllSubslots()
      },
      s: {
        imagePath: "slot_images/common/you.png",
        subslots: generateAllSubslots()
      },
      aux: {
        text: "するつもりだった",
        subslots: generateAllSubslots()
      },
      m2: {
        subslots: generateAllSubslots()
      },
      v: {
        imagePath: "slot_images/common/want.png",
        subslots: generateAllSubslots()
      },
      c: {
        subslots: generateAllSubslots()
      },
      o1: {
        imagePath: "slot_images/common/to_go.png",
        subslots: generateAllSubslots()
      },
      o2: {
        subslots: generateAllSubslots()
      },
      c2: {
        subslots: generateAllSubslots()
      },
      m3: {
        imagePath: "slot_images/common/quickly.png",
        subslots: generateAllSubslots()
      }
    }
  }
};

// ---- サンプル：全slotの空subslotを一括生成する関数 ----
function generateAllSubslots() {
  return {
    m1: {},
    s: {},
    aux: {},
    m2: {},
    v: {},
    c: {},
    o1: {},
    o2: {},
    c2: {},
    m3: {}
  };
}
window.grammarData = {
  "010": {
    A: ["want", "hope", "plan"],
    B: {
      "want": {
        subject: ["I", "You", "They"],
        object1: ["to go", "to eat", "to sleep", "a coffee"],
        object2: [],
        complement: [],
        m1: ["tomorrow", "soon", "now"],
        m2: [],
        m3: [],
        aux: ["would", "might", "can"],
        "slot-o1-v": ["eat", "go", "sleep"],
        "slot-o1-o1": ["lunch", "home", "well"],
        "slot-o1-m3": ["quickly", "happily", "early"]
      },
      "hope": {
        subject: ["She", "We"],
        object1: ["to win", "to find it"],
        object2: [],
        complement: [],
        m1: ["next time", "by Friday"],
        m2: [],
        m3: [],
        aux: ["can", "will"],
        "slot-o1-v": ["find", "win"],
        "slot-o1-o1": ["the prize", "the answer"],
        "slot-o1-m3": ["immediately", "eventually"]
      },
      "plan": {
        subject: ["They", "My team"],
        object1: ["to start", "to leave early"],
        object2: [],
        complement: [],
        m1: ["this week", "soon"],
        m2: [],
        m3: [],
        aux: ["must", "may"],
        "slot-o1-v": ["leave", "start"],
        "slot-o1-o1": ["the project", "the meeting"],
        "slot-o1-m3": ["promptly", "together"]
      }
    },
    embedded_structure: {
      m1: { imagePath: "slot_images/common/soon.png" },
      s: { imagePath: "slot_images/common/you.png" },
      aux: { text: "するつもりだった" },
      m2: {},
      v: { imagePath: "slot_images/common/want.png" },
      c: {},
      o1: { imagePath: "slot_images/common/to_go.png" },
      o2: {},
      c2: {},
      m3: { imagePath: "slot_images/common/quickly.png" }
    }
  }
};
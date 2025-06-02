export const grammarData = {
  "010": {
    "A": ["want", "hope", "plan"],
    "B": {
      "want": {
        subject: ["I", "You", "They"],
        object1: ["to go", "to eat", "to sleep"],
        object2: [],
        complement: [],
        m1: ["tomorrow", "soon", "now"],
        m2: [],
        m3: [],
        aux: ["would", "might", "can"],
        // sub-slot（折り畳み）用
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
    }
  }
};
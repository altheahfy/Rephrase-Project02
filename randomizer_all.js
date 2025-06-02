
// 構文スロット型ランダマイズ（3段階制御）対応版

import { grammarData } from './data/grammar_data.js';
import { updateSlot } from './common.js';

// 全体ランダマイズ実行関数
export function performGlobalRandomization() {
  // 第1段階：構文IDのランダム選定
  const grammarIDs = Object.keys(grammarData);
  const randomGrammarID = grammarIDs[Math.floor(Math.random() * grammarIDs.length)];
  const grammar = grammarData[randomGrammarID];

  // 第2段階：A群（動詞）のランダム選定
  const verbList = grammar.A;
  const randomVerb = verbList[Math.floor(Math.random() * verbList.length)];

  // 第3段階：B群（スロットごとの語句）のランダム選定
  const slotWords = grammar.B[randomVerb];

  const result = {
    V: randomVerb,
    S: getRandomFromList(slotWords.subject),
    O1: getRandomFromList(slotWords.object1),
    O2: getRandomFromList(slotWords.object2),
    C: getRandomFromList(slotWords.complement),
    M1: getRandomFromList(slotWords.m1),
    M2: getRandomFromList(slotWords.m2),
    M3: getRandomFromList(slotWords.m3),
    Aux: getRandomFromList(slotWords.aux)
  };

  // 表示更新
  for (const [slot, word] of Object.entries(result)) {
    updateSlot(slot, word);
  }

  console.log(`[構文ID: ${randomGrammarID}] A群: ${randomVerb}`, result);
}

// ヘルパー関数
function getRandomFromList(list) {
  if (!Array.isArray(list) || list.length === 0) return '';
  return list[Math.floor(Math.random() * list.length)];
}

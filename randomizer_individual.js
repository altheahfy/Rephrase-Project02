// randomizer_individual.js（slot名マッピング対応）
import { updateSlot } from './common.js';
import { grammarData } from './grammar_data.js';

export function initIndividualRandomizer(structureId, currentVerb) {
  const slotMap = {
    "S": "subject",
    "V": "verb",
    "O1": "object1",
    "O2": "object2",
    "C": "complement",
    "M1": "m1",
    "M2": "m2",
    "M3": "m3",
    "Aux": "aux"
  };

  Object.keys(slotMap).forEach(slot => {
    const button = document.getElementById(`btn-${slot}`);
    if (button) {
      button.addEventListener("click", () => {
        const mappedKey = slotMap[slot];
        const options = grammarData[structureId].B[currentVerb][mappedKey];
        if (!options || options.length === 0) return;
        const selected = options[Math.floor(Math.random() * options.length)];
        updateSlot(slot, selected);
        console.log(`[${slot}] →`, selected);
      });
    }
  });
}
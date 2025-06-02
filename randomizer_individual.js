// randomizer_individual.js
import { updateSlot } from './common.js';
import { grammarData } from './grammar_data.js';

export function initIndividualRandomizer(structureId, currentVerb) {
  const slots = Object.keys(grammarData[structureId].B[currentVerb]);

  slots.forEach(slot => {
    const button = document.getElementById(`btn-${slot}`);
    if (button) {
      button.addEventListener("click", () => {
        const options = grammarData[structureId].B[currentVerb][slot];
        const selected = options[Math.floor(Math.random() * options.length)];
        updateSlot(slot, selected);
      });
    }
  });
}
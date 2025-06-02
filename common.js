function getStructureId() {
  const input = document.getElementById("structureId");
  return input ? input.value : "INF-N-OBJ-010";
}

async function loadStructureData(structureId) {
  const dir = structureId.slice(-3);
  try {
    const response = await fetch(`slot_assignments/${dir}/slot_assignment.json`);
    const json = await response.json();
    return json[structureId];
  } catch (error) {
    console.error(`❌ 構文データの読み込みに失敗: ${structureId}`, error);
    return null;
  }
}


function safe(value) {
  return value == null ? "" : value;
}



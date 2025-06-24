
let testData = [
    {
        "Slot": "M1",
        "SlotPhrase": "That afternoon at the crucial point in the presentation",
        "SlotText": "あの、～の時点・地点で、～の中に、～の中で",
        "PhraseType": "word"
    },
    {
        "Slot": "S",
        "SlotPhrase": "the manager who had recently taken charge of the project",
        "SlotText": "最近",
        "PhraseType": "clause"
    },
    {
        "Slot": "Aux",
        "SlotPhrase": "had to",
        "SlotText": "～しなければならなかった",
        "PhraseType": "word"
    },
    {
        "Slot": "V",
        "SlotPhrase": "make",
        "SlotText": "",
        "PhraseType": "word"
    }
];

// Inserting the test data into the corresponding slots in the HTML
testData.forEach(data => {
    const slotElement = document.getElementById('slot-' + data.Slot.toLowerCase());
    if (slotElement) {
        // Insert SlotPhrase and SlotText into the slot's text container
        const slotTextElement = slotElement.querySelector('.slot-text');
        if (slotTextElement) {
            slotTextElement.textContent = data.SlotPhrase + " " + data.SlotText;
        }
    }
});

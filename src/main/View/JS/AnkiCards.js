document.addEventListener('DOMContentLoaded', () => {
    fetch('Navigation.html')
    .then(response => response.text())
    .then(html => {
        document.getElementById('Navigation').innerHTML = html;
    })
    .catch(error => console.error('Error loading navigation:', error));
});

const chooseWindow = document.querySelector('.module-card-area');
const currentCard = document.querySelector('.current-card-area');
const answerButton = document.querySelector('.answer-button-area');
const answer = document.querySelector('.current-card-answer');
const question = document.querySelector('.current-card-question');
let currentDeckId = null;
let currentCards = [];
let currentCardIndex = 0;

// Fetch decks and cards count from the API
async function fetchDecks() {
    try {
        const response = await fetch('http://127.0.0.1:8000/decks', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer Token'
            }
        });
        const decks = await response.json();
        return decks;
    } catch (error) {
        console.error('Error fetching decks:', error);
        return [];
    }
}

// Show modify deck form
async function showModifyDeckForm(deckId) {
    currentDeckId = deckId;
    // Populate the form with the current deck details
    const decks = await fetchDecks();
    const deck = decks.find(deck => deck.id === deckId);
    document.getElementById('moduleName').value = deck.name;
    document.getElementById('moduleDescription').value = deck.description;
    document.querySelector('.create-module-form').style.display = 'block';

    // Change form title to "Modify Deck"
    document.querySelector('.create-module-form h2').textContent = 'Modify Deck';

    // Change form submission to modify deck
    const form = document.querySelector('.create-module-form');
    form.onsubmit = async (event) => {
        event.preventDefault();
        await modifyDeck(deckId);
    };
}

async function modifyDeck(deckId) {
    const moduleName = document.getElementById('moduleName').value;
    const moduleDescription = document.getElementById('moduleDescription').value;

    if (!moduleName) {
        console.log('Module name is required');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/decks/${deckId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer Token'
            },
            body: JSON.stringify({
                name: moduleName,
                description: moduleDescription
            })
        });

        if (response.ok) {
            console.log('Deck modified successfully');
            hideCreateModuleForm();
            displayDecks();
        } else {
            const result = await response.json();
            console.log('Error modifying deck: ' + result.error);
        }
    } catch (error) {
        console.error('Error modifying deck:', error);
    }
}

// Delete deck
async function deleteDeck(deckId) {
    if (confirm('Are you sure you want to delete this deck?')) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/decks/${deckId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer Token'
                }
            });

            if (response.ok) {
                console.log('Deck deleted successfully');
                displayDecks();
            } else {
                console.log('Error deleting deck');
            }
        } catch (error) {
            console.error('Error deleting deck:', error);
        }
    }
}

// Display decks and cards count
async function displayDecks() {
    const decks = await fetchDecks();
    const moduleCardArea = document.querySelector('.module-card-area');
    moduleCardArea.innerHTML = ''; // Clear existing content

    decks.forEach(deck => {
        const moduleContainer = document.createElement('div');
        moduleContainer.className = 'module-card-container';

        const moduleHeader = document.createElement('h2');
        moduleHeader.className = 'module-card-header';
        moduleHeader.textContent = deck.name;

        const moduleList = document.createElement('div');
        moduleList.className = 'module-card-list';
        moduleList.style.maxHeight = '200px'; // Set max height for scrollable area
        moduleList.style.overflowY = 'auto'; // Enable vertical scrolling

        const ul = document.createElement('ul');
        deck.cards.forEach(card => {
            const li = document.createElement('li');
            li.textContent = card.front;
            li.setAttribute('data-deck-id', deck.id);
            ul.appendChild(li);
        });

        moduleList.appendChild(ul);
        moduleContainer.appendChild(moduleHeader);
        moduleContainer.appendChild(moduleList);
        moduleCardArea.appendChild(moduleContainer);

        // Add create card button
        const createCardButton = document.createElement('button');
        createCardButton.className = 'create-card-button';
        createCardButton.innerHTML = '<i class="fas fa-plus"></i>';
        createCardButton.onclick = () => showCreateCardForm(deck.id);
        moduleContainer.appendChild(createCardButton);

        // Add auto generate cards button
        const autoGenerateCardsButton = document.createElement('button');
        autoGenerateCardsButton.className = 'auto-generate-cards-button';
        autoGenerateCardsButton.textContent = 'Auto Generate Cards';
        autoGenerateCardsButton.onclick = () => showAutoGenerateCardsForm(deck.id);
        moduleContainer.appendChild(autoGenerateCardsButton);

        // Add start learning button
        const startLearningButton = document.createElement('button');
        startLearningButton.className = 'start-learning-button';
        startLearningButton.textContent = 'Start Learning';
        startLearningButton.onclick = () => startLearningSession(deck.id);
        moduleContainer.appendChild(startLearningButton);

        // Add modify deck button
        const modifyDeckButton = document.createElement('button');
        modifyDeckButton.className = 'modify-deck-button';
        modifyDeckButton.textContent = 'Modify Deck';
        modifyDeckButton.onclick = () => showModifyDeckForm(deck.id);
        moduleContainer.appendChild(modifyDeckButton);

        // Add delete deck button
        const deleteDeckButton = document.createElement('button');
        deleteDeckButton.className = 'delete-deck-button';
        deleteDeckButton.textContent = 'Delete Deck';
        deleteDeckButton.onclick = () => deleteDeck(deck.id);
        moduleContainer.appendChild(deleteDeckButton);
    });

    // Add event listeners to the new list items
    const moduleCardListItems = document.querySelectorAll(".module-card-list li");
    moduleCardListItems.forEach((item) => {
        item.addEventListener("click", () => {
            const deckId = item.getAttribute('data-deck-id');
            startLearningSession(deckId);
        });
    });
}

// Fetch cards from the API
async function fetchCards(deckId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/decks/${deckId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer Token'
            }
        });
        const deck = await response.json();
        return deck.cards;
    } catch (error) {
        console.error('Error fetching cards:', error);
        return [];
    }
}

// Start learning session
async function startLearningSession(deckId) {
    currentCards = await fetchCards(deckId);
    currentCardIndex = 0;
    if (currentCards.length > 0) {
        currentCard.style.display = "flex";
        chooseWindow.style.display = "none";
        displayCard(currentCards[currentCardIndex]);
    } else {
        console.log('No cards available in this deck');
    }
}

// Display card
function displayCard(card) {
    question.textContent = card.front;
    answer.textContent = card.back;
    answer.style.display = 'none';
    answerButton.style.display = 'none';
}

// Clickable card
function toggleAnswer() {
    answer.style.display = answer.style.display === 'none' || answer.style.display === '' ? 'block' : 'none';
    answerButton.style.display = "flex";
}

// Switch back
function quitLearningSession() {
    currentCard.style.display = "none";
    chooseWindow.style.display = "flex";
    answer.style.display = "none";
    answerButton.style.display = "none";
}

// Answer button functions
async function submitAnswer(button) {
    const card = currentCards[currentCardIndex];
    try {
        const response = await fetch(`http://127.0.0.1:8000/cards/${card.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer Token'
            },
            body: JSON.stringify({ button: button })
        });

        if (response.ok) {
            console.log('Answer submitted successfully');
            currentCardIndex++;
            if (currentCardIndex < currentCards.length) {
                displayCard(currentCards[currentCardIndex]);
            } else {
                quitLearningSession();
            }
        } else {
            console.log('Error submitting answer');
        }
    } catch (error) {
        console.error('Error submitting answer:', error);
    }
}

function verHard() {
    submitAnswer('Again');
}

function okay() {
    submitAnswer('Hard');
}

function easy() {
    submitAnswer('Good');
}

function veryEasy() {
    submitAnswer('Easy');
}

// Show create module form
function showCreateModuleForm() {
    document.querySelector('.create-module-form').style.display = 'block';
}

// Hide create module form
function hideCreateModuleForm() {
    document.querySelector('.create-module-form').style.display = 'none';
    // Reset form title to "Create New Module"
    document.querySelector('.create-module-form h2').textContent = 'Create New Module';
    // Reset form submission to create module
    const form = document.querySelector('.create-module-form');
    form.onsubmit = async (event) => {
        event.preventDefault();
        await createModule();
    };
}

// Create new module
async function createModule() {
    const moduleName = document.getElementById('moduleName').value;
    const moduleDescription = document.getElementById('moduleDescription').value;

    if (!moduleName) {
        console.log('Module name is required');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/decks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: moduleName,
                description: moduleDescription
            })
        });

        if (response.ok) {
            console.log('Module created successfully');
            hideCreateModuleForm();
            displayDecks();
        } else {
            const result = await response.json();
            console.log('Error creating module: ' + result.error);
        }
    } catch (error) {
        console.error('Error creating module:', error);
    }
}

// Show create card form
function showCreateCardForm(deckId) {
    currentDeckId = deckId;
    document.querySelector('.create-card-form').style.display = 'block';
}

// Hide create card form
function hideCreateCardForm() {
    document.querySelector('.create-card-form').style.display = 'none';
}

// Create new card
async function createCard() {
    const cardFront = document.getElementById('cardFront').value;
    const cardBack = document.getElementById('cardBack').value;

    if (!cardFront || !cardBack) {
        console.log('Both front and back of the card are required');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/cards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Bearer Token',
            },
            body: JSON.stringify({
                front: cardFront,
                back: cardBack,
                deck_id: currentDeckId
            })
        });

        const result = await response.json();
        if (response.ok) {
            console.log('Card created successfully');
            hideCreateCardForm();
            displayDecks();
        } else {
            console.log('Error creating card: ' + result.error);
        }
    } catch (error) {
        console.error('Error creating card:', error);
    }
}

// Show auto generate cards form
async function showAutoGenerateCardsForm(deckId) {
    currentDeckId = deckId;
    await fetchModules();
    document.querySelector('.auto-generate-cards-form').style.display = 'block';
}

// Hide auto generate cards form
function hideAutoGenerateCardsForm() {
    document.querySelector('.auto-generate-cards-form').style.display = 'none';
}

// Auto generate cards
async function autoGenerateCards() {
    const content = document.getElementById('content').value;
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const existingFile = document.getElementById('existingFiles').value;

    if (!content && !file && !existingFile) {
        console.log('Either content, a PDF file, or an existing file is required for auto generation');
        return;
    }

    const formData = new FormData();
    if (file) {
        formData.append('file', file);
    } else if (existingFile) {
        formData.append('existing_file', existingFile);
    }
    formData.append('deck_id', currentDeckId);
    formData.append('content', content);

    try {
        const response = await fetch('http://127.0.0.1:8000/auto-generate-cards', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': 'Bearer Token'
            }
        });

        const result = await response.json();
        if (response.ok) {
            console.log('Cards auto generated successfully');
            hideAutoGenerateCardsForm();
            displayDecks();
        } else {
            console.log('Error auto generating cards: ' + result.error);
        }
    } catch (error) {
        console.error('Error auto generating cards:', error);
    }
}

// Fetch files from the API
async function fetchFiles(moduleName, topicName) {
    try {
        const response = await fetch(`http://127.0.0.1:5002/files/${moduleName}/${topicName}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const files = await response.json();
        return files;
    } catch (error) {
        console.error('Error fetching files:', error);
        return [];
    }
}

// Populate file selection dropdown
async function populateFileSelection(moduleName, topicName) {
    const files = await fetchFiles(moduleName, topicName);
    const fileSelection = document.getElementById('existingFiles');
    if (!fileSelection) {
        console.error('File selection element not found');
        return;
    }
    fileSelection.innerHTML = ''; // Clear existing options

    files.forEach(file => {
        const option = document.createElement('option');
        option.value = file.id;
        option.textContent = file.name;
        fileSelection.appendChild(option);
    });
}

// Fetch modules from the API
async function fetchModules() {
    try {
        const response = await fetch('http://127.0.0.1:5002/modules', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const modules = await response.json();
        populateModulesDropdown(modules);
    } catch (error) {
        console.error('Error fetching modules:', error);
    }
}

// Populate modules dropdown
function populateModulesDropdown(modules) {
    const modulesDropdown = document.getElementById('modulesDropdown');
    modulesDropdown.innerHTML = ''; // Clear existing options

    modules.forEach(module => {
        const option = document.createElement('option');
        option.value = module.id;
        option.textContent = module.name;
        modulesDropdown.appendChild(option);
    });
}

// Fetch topics based on selected module
async function fetchTopics() {
    const moduleId = document.getElementById('modulesDropdown').value;
    try {
        const response = await fetch(`http://127.0.0.1:5002/modules/${moduleId}/topics`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const topics = await response.json();
        populateTopicsDropdown(topics);
    } catch (error) {
        console.error('Error fetching topics:', error);
    }
}

// Populate topics dropdown
function populateTopicsDropdown(topics) {
    const topicsDropdown = document.getElementById('topicsDropdown');
    topicsDropdown.innerHTML = ''; // Clear existing options

    topics.forEach(topic => {
        const option = document.createElement('option');
        option.value = topic.id;
        option.textContent = topic.name;
        topicsDropdown.appendChild(option);
    });
}

// Fetch files based on selected topic
async function fetchFiles() {
    const moduleId = document.getElementById('modulesDropdown').value;
    const topicId = document.getElementById('topicsDropdown').value;
    try {
        const response = await fetch(`http://127.0.0.1:5002/modules/${moduleId}/topics/${topicId}/files`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const files = await response.json();
        populateFilesDropdown(files);
    } catch (error) {
        console.error('Error fetching files:', error);
    }
}

// Populate files dropdown
function populateFilesDropdown(files) {
    const filesDropdown = document.getElementById('existingFiles');
    filesDropdown.innerHTML = ''; // Clear existing options

    files.forEach(file => {
        const option = document.createElement('option');
        option.value = file.id;
        option.textContent = file.name;
        filesDropdown.appendChild(option);
    });
}

// Initialize decks display on page load
document.addEventListener("DOMContentLoaded", () => {
    displayDecks();
});

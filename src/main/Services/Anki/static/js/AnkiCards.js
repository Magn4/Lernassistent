async function createModule() {
    const moduleName = document.getElementById('moduleName').value;
    const topicName = document.getElementById('topicName').value;

    const data = {
        module_name: moduleName,
        topic_name: topicName
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/decks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Module created successfully:', result);
    } catch (error) {
        console.error('Error creating module:', error);
    }
}

document.getElementById('predictBtn').addEventListener('click', async () => {
    const inputText = document.getElementById('inputText').value.trim();
    
    if (inputText === '') {
        alert('Please enter some text!');
        return;
    }
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText }),
        });
        
        const data = await response.json();
        
        // Display results
        document.getElementById('inputTextDisplay').textContent = data.input_text;
        
        const predictionsDiv = document.getElementById('predictions');
        predictionsDiv.innerHTML = '';
        
        data.predictions.forEach(word => {
            const wordElem = document.createElement('span');
            wordElem.className = 'prediction-word';
            wordElem.textContent = word;
            wordElem.addEventListener('click', () => {
                document.getElementById('inputText').value = inputText + ' ' + word;
            });
            predictionsDiv.appendChild(wordElem);
        });
        
        document.getElementById('result').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while making the prediction!');
    }
});
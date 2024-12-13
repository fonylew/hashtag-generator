const form = document.getElementById('contact-form');
const successModal = document.getElementById('success-modal');
const closeModalButton = document.getElementById('close-modal');
const action = form.getAttribute('action');

function hideModal() {
    successModal.style.display = 'none';
}

async function showModal(responseData) {
    const responseText = document.getElementById('response-text');
    // Transform comma-separated string to hashtag format
    const hashtags = responseData.split(',').map(tag => tag.trim());
    const formattedResponse = '#' + hashtags.join(' #');
    responseText.textContent = formattedResponse;
    successModal.style.display = 'block';
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const name = document.getElementById('name').value || 'anonymous';
    const message = document.getElementById('message').value;

    if (!message) {
        alert('Please enter a message');
        return;
    }

    try {
        const response = await fetch(action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, message })
        });

        if (response.ok) {
            const data = await response.json();
            showModal(data.response);
            form.reset();
        } else {
            alert('Error submitting form. Please try again.');
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        alert('Error submitting form. Please try again.');
        console.error('Error:', error);
    }
});

closeModalButton.addEventListener('click', hideModal);
// Close modal when clicking outside
window.addEventListener('click', (event) => {
if (event.target === successModal) {
    hideModal();
}
});

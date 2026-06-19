function handleContactForm(event) {
    // 1. CRITICAL: This stops the browser from reloading to the white screen
    event.preventDefault(); 

    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerText;

    // 2. Change button text to show it's working
    submitButton.innerText = "Sending...";
    submitButton.disabled = true;

    // 3. Package up all the form data
    const formData = new FormData(form);

    // 4. Send the data to your Flask backend silently
    fetch('/submit-quote', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Expect JSON back from Python
    .then(data => {
        if(data.status === 'success') {
            // Show a success message to the user
            alert("Thank you! We will contact you on WhatsApp shortly.");
            form.reset(); // Clear the form fields
        } else {
            alert("Oops! Something went wrong.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Server error. Please try again later.");
    })
    .finally(() => {
        // Reset the button back to normal
        submitButton.innerText = originalButtonText;
        submitButton.disabled = false;
    });
}
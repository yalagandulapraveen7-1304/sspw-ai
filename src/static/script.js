function handleContactForm(event) {
    // 1. CRITICAL: This stops the browser from reloading to the white screen
    event.preventDefault();

    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerText;

    // 2. Change button text to show it's working
    submitButton.innerText = "SENDING...";
    submitButton.disabled = true;

    // 3. Package up all the form data
    const formData = new FormData(form);

    // 4. Send the data to your Render backend silently
    fetch('https://sspw-ai-1.onrender.com/submit-quote', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) 
    .then(data => {
        // 5. Check for the exact "success" variable Python sends back
        if (data.success === true) {
            // Show a nice popup alert
            alert("Success! Your quote request has been sent to SSPW.");
            // Clear the form fields so it's fresh
            form.reset(); 
        } else {
            alert("Oops! Something went wrong: " + (data.error || "Please try again."));
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        alert("Network error. Please make sure you are connected to the internet.");
    })
    .finally(() => {
        // 6. Always turn the button back on, whether it succeeded or failed
        submitButton.innerText = originalButtonText;
        submitButton.disabled = false;
    });
}
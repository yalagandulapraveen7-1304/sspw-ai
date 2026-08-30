function handleContactForm(event) {
    event.preventDefault();

    const form = event.target;
    const name = form.querySelector('[name="name"]')?.value?.trim() || 'Customer';
    const phone = form.querySelector('[name="phone"]')?.value?.trim() || 'Not provided';
    const service = form.querySelector('[name="service"]')?.value?.trim() || 'General Inquiry';
    const vehicle = form.querySelector('[name="vehicle"]')?.value?.trim() || 'Not specified';
    const message = form.querySelector('[name="message"]')?.value?.trim() || 'Please provide an estimate.';

    // Construct professional WhatsApp message
    const waMessage = 
`*🚗 NEW QUOTE REQUEST — SRI SAI PAINT WORKS (SSPW)*

👤 *Customer Name:* ${name}
📞 *Phone Number:* ${phone}
🎨 *Service Needed:* ${service}
🚙 *Vehicle Model:* ${vehicle}
💬 *Details/Message:* ${message}

📍 *Location:* Kothagudem, Bhadradri Kothagudem`;

    const encodedText = encodeURIComponent(waMessage);
    const waUrl = `https://wa.me/918179727255?text=${encodedText}`;

    // Background attempt to log quote if backend exists
    try {
        const formData = new FormData(form);
        fetch('/submit-quote', { method: 'POST', body: formData }).catch(function() {});
    } catch(e) {}

    // Clear the form
    form.reset();

    // Redirect to WhatsApp directly
    window.open(waUrl, '_blank');
}

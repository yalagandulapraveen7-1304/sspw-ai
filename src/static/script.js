function handleContactForm(event) {
    if (event) event.preventDefault();
    const form = event ? event.target : document.getElementById('quoteForm');
    
    const name = form.querySelector('[name="name"]')?.value?.trim() || 'Customer';
    const phone = form.querySelector('[name="phone"]')?.value?.trim() || 'Not provided';
    const service = form.querySelector('[name="service"]')?.value?.trim() || 'General Inquiry';
    const vehicle = form.querySelector('[name="vehicle"]')?.value?.trim() || 'Not specified';
    const message = form.querySelector('[name="message"]')?.value?.trim() || 'Please provide an estimate.';

    const waText = 
`*🚗 NEW QUOTE REQUEST — SRI SAI PAINT WORKS (SSPW)*

👤 *Customer Name:* ${name}
📞 *Phone Number:* ${phone}
🎨 *Service Needed:* ${service}
🚙 *Vehicle Model:* ${vehicle}
💬 *Message/Notes:* ${message}

📍 *Location:* SSPW Workshop, Kothagudem`;

    const encoded = encodeURIComponent(waText);
    const waUrl = "https://wa.me/918179727255?text=" + encoded;

    if (form) form.reset();

    window.open(waUrl, "_blank") || (window.location.href = waUrl);
    return false;
}

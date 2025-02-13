let highlightedElement = null;  // This will hold the currently highlighted element

// Listen for mouseover events on the document
document.addEventListener('mouseover', (event) => {
    const element = event.target;

    // Add the 'highlight' class to the hovered element
    element.classList.add('highlight');

    // Remove the 'highlight' class when the mouse leaves the element
    element.addEventListener('mouseout', () => {
        element.classList.remove('highlight');
    });

    // Store the element being hovered on for later capture
    highlightedElement = element;
});

// Listen for click event to capture the HTML and CSS of the highlighted element
document.addEventListener('click', () => {
    if (highlightedElement) {
        const html = highlightedElement.outerHTML;  // Capture the outer HTML of the highlighted element
        const computedStyle = window.getComputedStyle(highlightedElement);  // Get the computed styles of the element

        // Prepare the CSS object to send
        const styles = {};
        const properties = [
            'backgroundColor', 'color', 'border', 'width', 'height', 'fontSize',
            'margin', 'padding', 'borderRadius', 'fontFamily', 'fontWeight'
        ];

        properties.forEach(property => {
            styles[property] = computedStyle[property];
        });

        chrome.runtime.sendMessage({ action: 'captureComponent', html: html, styles: styles });
    }
});

// Function to capture a screenshot of the highlighted element
function captureScreenshot(element) {
    const rect = element.getBoundingClientRect(); // Get the position of the element
    console.log(html2canvas);


    // Use html2canvas to capture the highlighted area
    html2canvas(element, {
        x: rect.left,  // Set the x offset to the element's position
        y: rect.top,   // Set the y offset to the element's position
        width: rect.width,  // Set the width to the element's width
        height: rect.height, // Set the height to the element's height
        scrollX: 0, // Disable page scrolling during capture
        scrollY: 0  // Disable page scrolling during capture
    }).then(canvas => {
        const imgURL = canvas.toDataURL("image/png"); // Convert to PNG
        console.log("Generated Screenshot URL:", imgURL);  // Log the screenshot URL for debugging
        chrome.runtime.sendMessage({ action: "downloadScreenshot", image: imgURL });
    }).catch(error => {
        console.error("Error in screenshot capture:", error); // Handle any errors
    });
}


// Listen for click events to capture the element and take a screenshot
document.addEventListener('click', (event) => {
    if (highlightedElement) {
        captureScreenshot(highlightedElement);
    }
});

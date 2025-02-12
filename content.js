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

// Listen for click event to capture the HTML of the highlighted element
document.addEventListener('click', () => {
    if (highlightedElement) {
        const html = highlightedElement.outerHTML;  // Capture the outer HTML of the highlighted element
        chrome.runtime.sendMessage({ action: 'captureComponent', html: html });
    }
});

// Listen for mouseover events on the document
document.addEventListener('mouseover', (event) => {
    const element = event.target;

    // Add the 'highlight' class to the hovered element
    element.classList.add('highlight');

    // Remove the 'highlight' class when the mouse leaves the element
    element.addEventListener('mouseout', () => {
        element.classList.remove('highlight');
    });
});

document.getElementById("toggle-highlight").addEventListener("click", () => {
    console.log("Button clicked"); // Check if this logs when the button is clicked

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const tabId = tabs[0].id;

        // Toggle highlighting by executing content script
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            func: toggleHighlighting
        });
    });
});

function toggleHighlighting() {
    const body = document.body;

    // Check if there's already a highlight class on body
    if (!body.classList.contains('highlighting-active')) {
        body.classList.add('highlighting-active');
        console.log("Highlighting enabled");
    } else {
        body.classList.remove('highlighting-active');
        console.log("Highlighting disabled");
    }
}

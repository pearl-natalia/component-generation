console.log("html2canvas is loaded:", typeof html2canvas !== "undefined");

let highlightedElement = null; // This will hold the currently highlighted element
let isCapturing = false; // Flag to track if the capture process is ongoing

// Listen for mouseover events on the document
document.addEventListener("mouseover", (event) => {
    const element = event.target;

    // Remove highlight from previous element
    if (highlightedElement && highlightedElement !== element) {
        highlightedElement.classList.remove("highlighted");
    }

    // Add the 'highlight' class to the hovered element
    element.classList.add("highlighted");
    highlightedElement = element;
});

// Listen for mouseout event on document
document.addEventListener("mouseout", (event) => {
    if (highlightedElement) {
        highlightedElement.classList.remove("highlighted");
        highlightedElement = null;
    }
});

// Function to capture screenshot
const captureScreenshot = () => {
    if (isCapturing) {
        console.log("Capture in progress, ignoring new click");
        return; // Skip if the capture process is ongoing
    }

    if (highlightedElement) {
        const html = highlightedElement.outerHTML; // Capture the outer HTML of the highlighted element
        const computedStyle = window.getComputedStyle(highlightedElement); // Get computed styles

        // Prepare the CSS object to send
        const styles = {};
        const properties = [
            "backgroundColor", "color", "border", "width", "height", "fontSize",
            "margin", "padding", "borderRadius", "fontFamily", "fontWeight"
        ];

        properties.forEach((property) => {
            styles[property] = computedStyle[property];
        });

        chrome.runtime.sendMessage({
            action: "captureComponent",
            html: html,
            styles: styles,
        });
    }

    if (typeof html2canvas !== "undefined") {
        isCapturing = true; // Set flag to indicate that capture is in progress

        html2canvas(document.querySelector(".highlighted"), {
            useCORS: true, // Allows capturing images from external sources (if CORS is enabled)
            logging: false, // Disable console logs from html2canvas
            scale: window.devicePixelRatio // Higher quality screenshot
        }).then((canvas) => {
            const imageData = canvas.toDataURL("image/png"); // Convert to base64 image

            // Send captured image data to background script
            chrome.runtime.sendMessage({
                action: "captureScreen",
                screenshot: imageData
            });

            isCapturing = false; // Reset flag once capture is done
        }).catch((error) => {
            console.error("Screenshot capture failed:", error);
            isCapturing = false; // Reset flag in case of error
        });
    } else {
        console.error("html2canvas is not loaded.");
    }
}

// Debounce function with the additional capturing flag check
function debounce(func, delay) {
    let lastExecutionTime = 0;
    return function (...args) {
        const now = Date.now();
        if (now - lastExecutionTime >= delay) {
            lastExecutionTime = now;
            func.apply(this, args);
        }
    };
}

// Apply debounce to the captureScreenshot function
document.addEventListener("click", debounce(captureScreenshot, 5000));

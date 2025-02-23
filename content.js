console.log("html2canvas is loaded:", typeof html2canvas !== "undefined");

let highlightedElement = null; // This will hold the currently highlighted element

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

// Listen for click event to capture the HTML and CSS of the highlighted element
document.addEventListener("click", (event) => {
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
        console.log("html2canvas:", window.html2canvas);

        const element = document.querySelector(".highlighted");


        html2canvas(document.querySelector(".highlighted"), {
            useCORS: true,
            logging: false,
            scale: window.devicePixelRatio,
            backgroundColor: null
        }).then((canvas) => {
            // Convert canvas to data URL
            const imageData = canvas.toDataURL("image/png");

            // Create a download link without appending anything to the DOM
            const link = document.createElement("a");
            link.href = imageData;
            link.download = "screenshot.png";
            link.click(); // Directly trigger the download

            // Send captured image data to background script (optional)
            chrome.runtime.sendMessage({
                action: "captureScreen",
                screenshot: imageData
            });
        }).catch((error) => {
            console.error("Screenshot capture failed:", error);
        });



    } else {
        console.error("html2canvas is not loaded.");
    }
});




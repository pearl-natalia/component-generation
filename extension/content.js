console.log("html2canvas is loaded:", typeof html2canvas !== "undefined");

let highlightedElement = null;

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

document.addEventListener("mouseout", (event) => {
    if (highlightedElement) {
        highlightedElement.classList.remove("highlighted");
        highlightedElement = null;
    }
});

// Capture HTML & CSS of the clicked element
document.addEventListener("click", (event) => {
    if (highlightedElement) {
        const html = highlightedElement.outerHTML;  // Capture HTML
        const computedStyle = window.getComputedStyle(highlightedElement); // Capture CSS

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
            const imageData = canvas.toDataURL("image/png");

            // Send image to flask
            fetch("http://localhost:5000/process-image", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ image: imageData })
            })
                .then(response => response.json())
                .then(data => {
                    console.log("Image processed:", data);
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        }).catch((error) => {
            console.error("Screenshot capture failed:", error);
        });

    } else {
        console.error("html2canvas is not loaded.");
    }
});




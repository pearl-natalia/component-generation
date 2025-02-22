chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "captureComponent") {
        console.log("Captured HTML:", message.html);
        console.log("Captured CSS:", message.styles);

        // Optionally, you can store this HTML & CSS in Chrome storage
        chrome.storage.local.set({ capturedHtml: message.html, capturedStyles: message.styles }, () => {
            console.log("Captured HTML and CSS saved to local storage");
        });

        // send to backend
        if (message.action === "captureComponent") {
            const html = document.body.innerHTML; // Capture full page HTML
            const styles = [...document.styleSheets].map((sheet) => {
                try {
                    return [...sheet.cssRules].map(rule => rule.cssText).join("\n");
                } catch (e) {
                    return ""; // Skip inaccessible stylesheets
                }
            }).join("\n");

            fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ html, styles })
            })
                .then(response => response.json())
                .then(data => console.log("Response from backend:", data))
                .catch(error => console.error("Error:", error));
        }
    }

    let lastExecutionTime = 0; // Time of the last executed action
    let isDebounced = false; // Flag to prevent multiple executions

    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === "captureComponent") {
            console.log("Captured HTML:", message.html);
            console.log("Captured CSS:", message.styles);

            // Optionally, you can store this HTML & CSS in Chrome storage
            chrome.storage.local.set({ capturedHtml: message.html, capturedStyles: message.styles }, () => {
                console.log("Captured HTML and CSS saved to local storage");
            });
        }

        if (message.action === "captureScreen" && !isDebounced) {
            const now = Date.now();

            // Check if 5 seconds have passed since the last execution
            if (now - lastExecutionTime >= 5000) {
                const url = message.screenshot; // Get the screenshot URL
                console.log("Here is the URL: ", url);

                // Send the screenshot URL to the content script or popup
                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    chrome.tabs.sendMessage(tabs[0].id, { action: "displayScreenshot", url: url });
                });

                // Update the last execution time and set the debounce flag
                lastExecutionTime = now;
                isDebounced = true;

                // Reset the debounce flag after 5 seconds
                setTimeout(() => {
                    isDebounced = false;
                }, 5000);
            } else {
                // If it's been less than 5 seconds, discard the request
                console.log("Request discarded. Too soon.");
            }
        }
    });



});


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "captureComponent") {
        console.log("Captured HTML:", message.html);
        console.log("Captured CSS:", message.styles);

        // Optionally, you can store this HTML & CSS in Chrome storage
        chrome.storage.local.set({ capturedHtml: message.html, capturedStyles: message.styles }, () => {
            console.log("Captured HTML and CSS saved to local storage");
        });
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


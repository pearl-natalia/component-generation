chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "captureComponent") {
        console.log("Captured HTML:", message.html);
        console.log("Captured CSS:", message.styles);

        chrome.storage.local.set({ capturedHtml: message.html, capturedStyles: message.styles }, () => {
            console.log("Captured HTML and CSS saved to local storage");
        });

        // Send to backend
        if (message.action === "captureComponent") {
            const html = document.body.innerHTML;
            const styles = [...document.styleSheets].map((sheet) => {
                try {
                    return [...sheet.cssRules].map(rule => rule.cssText).join("\n");
                } catch (e) {
                    return "";
                }
            }).join("\n");

            fetch("http://127.0.0.1:5000/fetch-html", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ html, styles })
            })
                .then(response => response.json())
                .then(data => console.log("Response from backend:", data))
                .catch(error => console.error("Error:", error));
        }
    }

    let lastExecutionTime = 0;
    let isDebounced = false;

    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message.action === "captureComponent") {
            console.log("Captured HTML:", message.html);
            console.log("Captured CSS:", message.styles);

            chrome.storage.local.set({ capturedHtml: message.html, capturedStyles: message.styles }, () => {
                console.log("Captured HTML and CSS saved to local storage");
            });
        }

        if (message.action === "captureScreen" && !isDebounced) {
            const now = Date.now();

            if (now - lastExecutionTime >= 5000) {
                const url = message.screenshot;
                console.log("Here is the URL: ", url);

                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    chrome.tabs.sendMessage(tabs[0].id, { action: "displayScreenshot", url: url });
                });

                lastExecutionTime = now;
                isDebounced = true;

                setTimeout(() => {
                    isDebounced = false;
                }, 5000);
            } else {
                console.log("Request discarded. Too soon.");
            }
        }
    });



});


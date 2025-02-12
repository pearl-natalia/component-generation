chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "captureComponent") {
        console.log("Captured HTML:", message.html);
        // Optionally, you can store this HTML in Chrome storage or process it further
        chrome.storage.local.set({ capturedHtml: message.html }, () => {
            console.log("Captured HTML saved to local storage");
        });
    }
});

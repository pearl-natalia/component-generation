chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "captureComponent") {
        console.log("Captured HTML:", message.html);
        console.log("Captured CSS:", message.styles);

        // Optionally, you can store this HTML & CSS in Chrome storage
        chrome.storage.local.set({ capturedHtml: message.html, capturedStyles: message.styles }, () => {
            console.log("Captured HTML and CSS saved to local storage");
        });
    }

    if (message.action === "downloadScreenshot") {
        const url = message.image;

        chrome.downloads.download({
            url: url,
            filename: "element_screenshot.png",
            saveAs: true  // Prompts user to save the file
        });
    }
});
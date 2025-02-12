document.addEventListener("DOMContentLoaded", () => {
    // Add listener to the "Show HTML" button
    document.getElementById("show-html").addEventListener("click", () => {
        chrome.storage.local.get("capturedHtml", (data) => {
            const htmlOutput = document.getElementById("html-output");
            if (data.capturedHtml) {
                htmlOutput.value = data.capturedHtml;  // Display the captured HTML in the textarea
            } else {
                htmlOutput.value = "No HTML captured yet.";
            }
        });
    });
});

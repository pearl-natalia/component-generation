document.addEventListener("DOMContentLoaded", () => {
    // Add listener to the "Show HTML & CSS" button
    document.getElementById("show-html").addEventListener("click", () => {
        chrome.storage.local.get(["capturedHtml", "capturedStyles"], (data) => {
            const htmlOutput = document.getElementById("html-output");
            const cssOutput = document.getElementById("css-output");

            if (data.capturedHtml) {
                htmlOutput.value = data.capturedHtml;  // Display the captured HTML in the textarea
            } else {
                htmlOutput.value = "No HTML captured yet.";
            }

            if (data.capturedStyles) {
                // Format the styles as a JSON string for better readability
                cssOutput.value = JSON.stringify(data.capturedStyles, null, 2);  
            } else {
                cssOutput.value = "No CSS captured yet.";
            }
        });
    });
});

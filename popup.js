document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("generate").addEventListener("click", () => {
        chrome.storage.local.get(["capturedHtml", "capturedStyles"], (data) => {
            if (!data.capturedHtml || !data.capturedStyles) {
                console.log("No HTML or CSS captured yet.");
                return;
            }

            // Send data to Flask backend
            fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ html: data.capturedHtml, styles: data.capturedStyles })
            })
                .then(response => response.json())
                .then(data => console.log("Response from backend:", data))
                .catch(error => console.error("Error:", error));
        });
    });
});

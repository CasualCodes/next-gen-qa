/* MAIN SCRIPT
* - Use for templates after making the decision of dynamic or static results page
*/

// LOADING PAGE //
if (window.location.pathname.includes("/loading")) {
    function processData() {
        fetch('/process_data')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'completed') {
                    window.location.href = '/results';
                }
            });
    }

    window.onload = function() {
        processData();
    };
}

// RESULTS PAGE
if (window.location.pathname.includes("/results")) {
    // click download button
    document.getElementById("download-btn").addEventListener("click", () => {
        window.location.href = "/download";
    });

    // click download pdf button
    document.getElementById("download-pdf-btn").addEventListener("click", () => {
        window.location.href = "/download_pdf";
    });

    // click regenerate button
    document.getElementById("regenerate-btn").addEventListener("click", () => {
        window.location.href = "/loading";
    });

    // click new url button
    document.getElementById("new-url-btn").addEventListener("click", () => {
        window.location.href = "/";
    });
}
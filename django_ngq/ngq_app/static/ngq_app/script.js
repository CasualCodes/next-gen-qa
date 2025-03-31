/* MAIN SCRIPT
* - Use for templates after making the decision of dynamic or static results page
*/

// LOADING PAGE [UNUSED] [LEGACY] //
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

// RESULTS PAGE - DYNAMIC// 
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

    //// FETCH / ASYNC FUNCTIONS ////
        // Scraping
        async function processData() {
            try {
                console.log("Scraping Begins");
                const response = await fetch('/process_data', {
                    signal: stop_fetch.signal,
                    });

                const data = await response.json();
                if (data.status === 'completed') {
                    processResults();
                    // window.location.href = '/loading_results';
                }
            } catch (error) {
                console.log("Closing page and its functions");
                const response = await fetch('/cancel_scraping');

                const data = await response.json();
                if (data.status === 'completed') {
                    console.log("Scraping Cancelled");
                }
            }
        }
        // Generation : Dynamic Results
        const socket = new WebSocket('ws://'+ window.location.host +'/ws/updates/');
            socket.onopen = () => {
                console.log("Connection Opened");
            }
            socket.onmessage = function(event) {
                // Parse the incoming JSON data
                const context = JSON.parse(event.data);

                // Dynamically update statistics
                document.getElementById('test-url').innerText = context.url;
                document.getElementById('total-elements').innerText = context.accurate_elements_count;
                document.getElementById('buttons-count').innerText = context.buttons_count;
                document.getElementById('links-count').innerText = context.links_count;
                document.getElementById('headers-count').innerText = context.headers_count;
                document.getElementById('paragraphs-count').innerText = context.paragraphs_count;
                document.getElementById('submit-fields-count').innerText = context.submit_fields_count;
                document.getElementById('input-fields-count').innerText = context.input_fields_count;
                document.getElementById('test-case-total').innerText = context.elements_count;
                document.getElementById('test-case-progress').innerText = context.test_case_count;

                // Dynamically update Table
                document.getElementById('table-container').innerHTML = context.test_cases_dynamic;
            };
        async function processResults() {
            try {
                console.log("Generation Begins");
                document.getElementById('generation-status').innerText = "generating test cases..."
                const response = await fetch('/process_results',{
                    signal: stop_fetch.signal,
                });
                const data = await response.json();
                if (data.status === 'completed') {
                    document.getElementById('generation-status').innerText = "generation completed!"
                    console.log("Generation Finished!")
                    window.location.href = '/static_results';
                }
            } catch (error) {
                // socket.close();
                console.log("Closing page and its functions");
                const response = await fetch('/cancel_generation');
                
                const data = await response.json();
                if (data.status === 'completed') {
                    console.log("Generation Cancelled");
                }
            }
        }

        //// STOP FUNCTIONS ////
        // Stop Scraping
        const stop_fetch = new AbortController();
        
        //// ON LOAD | ON UNLOAD ////
        window.onload = function() {
            // Start Scraping
            // document.getElementById('generation-status').innerText = "scraping website..."
            processData();
        };
        window.onbeforeunload = function() {
            // Trigger All Stop Signals
            stop_fetch.abort();

            // // Socket Closing
            // try {
            //     console.log("Connection Closed");
            // } catch (error) {
            //     // Do Nothing
            // }
        }

        // //// TAB IDENTIFICATION ////
        // function generateUUID() {
        //     return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        //         const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        //         return v.toString(16);
        //     });
        // }
        // const tabID = generateUUID();
}

// RESULTS PAGE - STATIC // 
if (window.location.pathname.includes("/static_results")) {
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
////////// click generate button
if (window.location.pathname.includes("home.html")) {
    const form = document.querySelector(".input-container");
    const inputField = form.querySelector("input[type='url']");
    const generateButton = form.querySelector("button");
  
    generateButton.addEventListener("click", (event) => {
        event.preventDefault();
      
        const websiteURL = inputField.value.trim();
        if (!websiteURL) {
            alert("Please enter a valid URL.");
            return;
        }
        
        // store URL in sessionStorage to access it on results page
        sessionStorage.setItem("websiteURL", websiteURL);
      
        // simulate loading by redirecting to loading screen
        window.location.href = "results.html";
    });
}
  

////////// results page
document.addEventListener("DOMContentLoaded", () => {
    const resultsContainer = document.querySelector(".table-container");
    const progressTracker = document.getElementById("test-case-progress");
    const totalTracker = document.getElementById("test-case-total");
    const totalElementsDisplay = document.getElementById("total-elements");
    const testUrlDisplay = document.getElementById("test-url");
    const breakdownList = document.getElementById("breakdown-list");

    // retrieve URL 
    const testUrl = sessionStorage.getItem("websiteURL") || "https://example.com";
    testUrlDisplay.textContent = testUrl;

    // simulated elements
    const elements = {
        buttons: 3,
        links: 4,
        inputFields: 2,
        paragraphs: 5
    };

    // display breakdown dynamically
    function updateBreakdownList() {
        document.getElementById("buttons-count").textContent = elements.buttons;
        document.getElementById("links-count").textContent = elements.links;
        document.getElementById("input-fields-count").textContent = elements.inputFields;
        document.getElementById("paragraphs-count").textContent = elements.paragraphs;

        
    }
    updateBreakdownList();

    let testCases = {};
    let generatedTestCases = 0;
    const totalTestCases = Object.values(elements).reduce((sum, count) => sum + count, 0);

    totalElementsDisplay.textContent = totalTestCases;
    totalTracker.textContent = totalTestCases;

    // create a table for each element type
    function createTableForElementType(type) {
        if (!testCases[type] && !document.getElementById(`table-${type}`)) {
            testCases[type] = [];

            const tableWrapper = document.createElement("div");
            tableWrapper.classList.add("table-section");
            tableWrapper.style.display = "none";

            const title = document.createElement("h2");
            const displayType = type === 'inputFields' ? 'Input Fields' : type.charAt(0).toUpperCase() + type.slice(1);
            title.textContent = `${displayType}: ${elements[type]}`;
            
            const table = document.createElement("table");
            table.id = `table-${type}`;
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Test ID</th>
                        <th>Objective</th>
                        <th>Preconditions</th>
                        <th>Test Steps</th>
                        <th>Expected Result</th>
                        <th>Actual Result</th>
                    </tr>
                </thead>
                <tbody></tbody>
            `;

            tableWrapper.appendChild(title);
            tableWrapper.appendChild(table);
            resultsContainer.appendChild(tableWrapper);
        }
    }

    // add test case to correct table
    function addTestCaseToTable(type, testCase) {
        const tableBody = document.querySelector(`#table-${type} tbody`);
        
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${testCase.id}</td>
            <td>${testCase.objective}</td>
            <td>${testCase.precondition}</td>
            <td>${testCase.steps}</td>
            <td>${testCase.expected}</td>
            <td>${testCase.actual}</td>
        `;
        tableBody.appendChild(row);
    
        document.getElementById(`table-${type}`).parentElement.style.display = "block"; // Show table
    }

    // dummy test case
    function createTestCase(type, testId) {
        return {
            id: testId,
            objective: `Verify ${type} functionality`,
            precondition: `Ensure ${type} exists`,
            steps: `Click/Interact with ${type}`,
            expected: `Expected behavior of ${type}`,
            actual: `Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observe Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed Actual behavior observed`
        };
    }

    
    document.getElementById("generation-status").textContent = "waiting to generate test cases...";
    progressTracker.textContent = "0"; 
    if (generatedTestCases === 0) {
        resultsContainer.innerHTML = ""; 
    }
    
    // show 0/14 3 seconds before starting test generation bc long
    setTimeout(() => {
        document.getElementById("generation-status").textContent = "starting test case generation...";
        
        // after 3 seconds, begin generating test cases
        setTimeout(() => {
            generateTestCases();
        }, 3000);
    }, 100);


    let testIdCounter = 1;
    function generateTestCases() {
        if (generatedTestCases >= totalTestCases) return;
    
        if (generatedTestCases === 0) {
            resultsContainer.innerHTML = ""; 
        }
    
        let batchCount = 0;
    
        Object.entries(elements).forEach(([type, count]) => {
            createTableForElementType(type);
    
            while (testCases[type].length < count && batchCount < 3) {
                const testId = `TC-${testIdCounter}`;
                const testCase = createTestCase(type, testId);
                testCases[type].push(testCase);
                addTestCaseToTable(type, testCase);
                generatedTestCases++;
                testIdCounter++;
                batchCount++;
            }
        });
    
        updateProgress();
    
        if (generatedTestCases < totalTestCases) {
            setTimeout(generateTestCases, 2000);
        }
    }

    // update progress
    function updateProgress() {
        progressTracker.textContent = generatedTestCases;
        document.getElementById("generation-status").textContent = 
            generatedTestCases < totalTestCases ? "generating test cases..." : "test cases generated";
    }


    // event listeners
    document.getElementById("print-btn").addEventListener("click", () => window.print());

    document.getElementById("download-btn").addEventListener("click", () => {
        const csvContent = "Test ID,Objective,Preconditions,Test Steps,Expected Result,Actual Result\n" +
            Object.values(testCases)
                .flat()
                .map(tc => `${tc.id},${tc.objective},${tc.precondition},${tc.steps},${tc.expected},${tc.actual}`)
                .join("\n");

        const blob = new Blob([csvContent], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "test_cases.csv";
        link.click();
    });

    document.getElementById("regenerate-btn").addEventListener("click", () => {
        testCases = {};
        generatedTestCases = 0;
        testIdCounter = 1;
        
        resultsContainer.innerHTML = "";
    
        progressTracker.textContent = "0";
        document.getElementById("generation-status").textContent = "waiting to generate test cases...";
    
        generateTestCases();
    });

    document.getElementById("new-url-btn").addEventListener("click", () => {
        window.location.href = "home.html"; 
    });
});

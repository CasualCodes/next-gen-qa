// ////////// click generate button
// if (window.location.pathname.includes("home.html")) {
//     const form = document.querySelector(".input-container");
//     const inputField = form.querySelector("input[type='url']");
//     const generateButton = form.querySelector("button");
  
//     generateButton.addEventListener("click", (event) => {
//         event.preventDefault();
      
//         const websiteURL = inputField.value.trim();
//         if (!websiteURL) {
//             alert("Please enter a valid URL.");
//             return;
//         }
        
//         // store URL in sessionStorage to access it on results page
//         sessionStorage.setItem("websiteURL", websiteURL);
      
//         // simulate loading by redirecting to loading screen
//         window.location.href = "loading.html";
//     });
// }
  

// ////////// loading screen to results
// if (window.location.pathname.includes("loading.html")) {
//     // simulate a delay for loading (e.g., 2 seconds)
//     setTimeout(() => {
//         window.location.href = "results.html";
//     }, 2000); // adjust delay as needed
// }
  

// ////////// results page
// document.addEventListener("DOMContentLoaded", () => {
//     const testCaseCount = Math.floor(Math.random() * 10) + 1; // simulate number of test cases (1-10)
//     const websiteUrl = localStorage.getItem("userUrl") || "example.com";
//     const timestamp = new Date().toLocaleString();

//     // update page content dynamically
//     document.getElementById("website-url").textContent = websiteUrl;
//     document.getElementById("timestamp").textContent = timestamp;
//     document.getElementById("test-case-count").textContent = testCaseCount;

//     // simulate test case data
//     const resultsTable = document.getElementById("results-table").querySelector("tbody");
//     for (let i = 1; i <= testCaseCount; i++) {
//         const row = document.createElement("tr");
//         row.innerHTML = `
//         <td>${i}</td>
//         <td>Objective for test case ${i}</td>
//         <td>Precondition ${i}</td>
//         <td>Step 1: Action ${i}, Step 2: Action ${i}</td>
//         <td>Expected result ${i}</td>
//         <td>Actual result ${i}</td>
//         `;
//         resultsTable.appendChild(row);
//     }

//     // click download button
//     document.getElementById("download-btn").addEventListener("click", () => {
//         const rows = [...resultsTable.children];
//         const csvData = rows.map(row =>
//             [...row.children].map(cell => `"${cell.textContent}"`).join(",")
//         );
//         const csvContent = `data:text/csv;charset=utf-8,Test ID,Objective,Preconditions,Test Steps,Expected Result,Actual Result\n${csvData.join("\n")}`;
//         const link = document.createElement("a");
//         link.setAttribute("href", encodeURI(csvContent));
//         link.setAttribute("download", "test_cases.csv");
//         document.body.appendChild(link);
//         link.click();
//         link.remove();
//     });

//     // click regenerate button
//     document.getElementById("regenerate-btn").addEventListener("click", () => {
//         window.location.href = "home.html";
//     });
// });

// document.querySelector("form").addEventListener("submit", function(event) {
//     // Stop the page from refreshing
//     event.preventDefault();

//     // Get data from the HTML form
//     let data = {
//         role: document.getElementById("role").value,
//         aadhar: document.getElementById("aadhar").value,
//         name: document.getElementById("name").value,
//         validate: document.getElementById("validate").value,
//         gender: document.getElementById("gender").value,
//         contact: document.getElementById("contact").value,
//         address: document.getElementById("address").value,
//         dob: document.getElementById("dob").value
//     };

//     // Send data to the backend
//     fetch("http://localhost:8096/api/register", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => {
//         if (response.ok) {
//             alert("Registration successful!");
//         } else {
//             alert("Registration failed!");
//         }
//     })
//     .catch(error => {
//         console.log(error);
//         alert("Backend connection failed!");
//     });
// });



document.querySelector("form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = {
        role: document.getElementById("role").value,
        aadhar: document.getElementById("aadhar").value,
        name: document.getElementById("name").value,
        validate: document.getElementById("validate").value,
        gender: document.getElementById("gender").value,
        contact: document.getElementById("contact").value,
        address: document.getElementById("address").value,
        dob: document.getElementById("dob").value
    };

    try {
        const response = await fetch("http://127.0.0.1:8096/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            console.error("Backend error:", response.status, result);
            alert(`Registration failed (${response.status}): ${
                result.error || "Unknown error"
            }`);
            return;
        }

        alert(result.message);

    } catch (error) {
        console.error("Request failed:", error);
        alert(
            "Could not reach the backend. Check the Python terminal " +
            "and browser Console/Network tabs."
        );
    }
});

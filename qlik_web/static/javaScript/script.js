document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    // Get the username and password entered by the user
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // You can add your authentication logic here
    // For demonstration purposes, let's check if the username is "admin" and password is "password"
    if (username === "admin" && password === "password") {
        alert("Login successful!"); // Display a success message
        // Redirect to the connected page or unlock content here
        // Example: window.location.href = "connected-page.html";
    } else {
        alert("Invalid username or password. Please try again."); // Display an error message
    }
});

// Listen for the form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    // Prevent the default behavior (which is refreshing the page)
    event.preventDefault();

    // Grab the values the user typed in
    const usernameInput = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;
    const messageArea = document.getElementById('messageArea');

    // Set our "fake database" credentials for testing
    const validUsername = 'admin';
    const validPassword = 'password123';

    // Check if what they typed matches our test credentials
    if (usernameInput === validUsername && passwordInput === validPassword) {
        messageArea.style.color = 'green';
        messageArea.textContent = 'Login successful! Logging you in...';
        // In a real app, we would redirect them to a dashboard here
    } else {
        messageArea.style.color = 'red';
        messageArea.textContent = 'Invalid username or password.';
    }
});
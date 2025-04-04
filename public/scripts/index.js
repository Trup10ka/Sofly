
loginButton = document.getElementById("login-button")

loginButton.addEventListener("click", async function (event)
    {
        event.preventDefault()
        login()
    }
)

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                username: username,
                password: password
            }
        )
    });

    if (response.ok) {
        window.location.href = '/dashboard';
    } else {
        alert('Login failed');
    }
}
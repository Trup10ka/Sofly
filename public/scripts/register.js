
registerButton = document.getElementById("register-button")

registerButton.addEventListener("click", async function (event)
    {
        event.preventDefault()
        register()
    }
)

async function register() {
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value
    const email = document.getElementById("email").value

    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {
                username: username,
                password: password,
                email: email
            }
        )
    });

    if (response.ok)
    {
        window.location.href = '/dashboard'
    }
    else
    {
        const error = await response.json()
        alert(error.error_message)
    }
}
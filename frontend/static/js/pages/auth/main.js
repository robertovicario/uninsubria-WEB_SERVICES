/////////////////////////
/**
 * Authentication :: Pages
 */
/////////////////////////

document.querySelector('form').addEventListener('submit', async function (e) {

    // Preventing default form submission
    e.preventDefault();

    // -------------------------

    // Getting form data
    const input_email = document.getElementById('input-email').value;
    const input_password = document.getElementById('input-password').value;
    const alert_msg = document.getElementById('alert-msg');
    const btn_submit = document.getElementById('btn-submit');

    // Resetting alert and disabling submit button
    alert_msg.classList.add('d-none');
    btn_submit.disabled = true;

    try {

        // Sending POST request
        const response = await fetch(
            `/auth/api/login`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    email: input_email,
                    password: input_password
                })
            }
        );

        // -------------------------

        // Handling response
        const data = await response.json();
        if (response.ok && data.success) {
            window.location.href = '/dashboard';
        } else {
            alert_msg.textContent = 'Invalid email or password. Please try again.';
            alert_msg.classList.remove('d-none');
        }
    } catch (err) {

        // Handling errors
        console.error(err);
        alert_msg.textContent = 'An error occurred while processing your request. Please try again later.';
        alert_msg.classList.remove('d-none');
    } finally {
        btn_submit.disabled = false;
    }
});

/////////////////////////

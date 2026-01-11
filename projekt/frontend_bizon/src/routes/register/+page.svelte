<script>
    let username = '';
    let password = '';
    let password_confirm = '';
    let email = '';
    let message = '';

    async function handleRegister() {
        const res = await fetch('http://127.0.0.1:8000/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, password_confirm, email })
        });

        if (res.ok) {
            message = "Konto utworzone! Możesz się zalogować.";
        } else {
            const data = await res.json();
            message = "Błąd: " + JSON.stringify(data);
        }
    }
</script>

<form on:submit|preventDefault={handleRegister}>
    <input type="text" bind:value={username} placeholder="Username" required />
    <input type="email" bind:value={email} placeholder="Email" required />
    <input type="password" bind:value={password} placeholder="Password" required />
    <input type="password" bind:value={password_confirm} placeholder="powtorz" required />
    <button type="submit">Zarejestruj</button>
</form>
<p>{message}</p>
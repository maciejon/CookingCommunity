<script lang="ts">
    import { fly } from 'svelte/transition';
    import { goto } from '$app/navigation';
    import { isAuthenticated } from '../../lib/authStore';

    let username = '';
    let email = '';
    let password = '';
    let password_confirm = '';
    
    let message = '';
    let errorExists = false;
    let errors: Record<string, string[]> = {}; 

    let showPassword = false;
    let showConfirmPassword = false;

    function toggleShow() { showPassword = !showPassword; }
    function toggleShowConfirm() { showConfirmPassword = !showConfirmPassword; }

    async function handleRegister() {
        message = "";
        errorExists = false;
        errors = {};

        if (password !== password_confirm) {
            message = "Hasła nie są identyczne";
            errorExists = true;
            return;
        }

        try {
            const res = await fetch('http://127.0.0.1:8000/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, password_confirm, email }),
                credentials: 'include'
            });

            const contentType = res.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const data = await res.json();

                if (res.ok) {
                    message = "Konto utworzone! Logowanie...";
                    isAuthenticated.set(true);
                    
                    setTimeout(() => goto("/"), 1000);
                } else {
                    errorExists = true;
                    errors = data;
                    if (data.detail) message = data.detail;
                }
            } else {
                const text = await res.text();
                console.error("Błąd serwera (HTML):", text);
                message = "Błąd serwera. Sprawdź konsolę backendu.";
                errorExists = true;
            }
        } catch (err) {
            errorExists = true;
            message = "Błąd połączenia z API.";
            console.error(err);
        }
    }
</script>

<div class="page-container">
    <div class="panel" in:fly={{ y: 200, duration: 600 }}>
        <div class="header">ZAREJESTRUJ SIĘ</div>
        
        <form on:submit|preventDefault={handleRegister}>
            <input type="text" class="input-text-box" bind:value={username} placeholder="Login" required />
            <input type="email" class="input-text-box" bind:value={email} placeholder="Email" required />
            <!-- hasło 1 -->
            <div class="input-wrapper">
                <input type={showPassword ? "text" : "password"} class="input-text-box" bind:value={password} placeholder="Hasło" required />
                <button type="button" class="show-password-button" on:click={toggleShow}>
                    {#if showPassword}
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="eye-icon">
                            <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
                            <path fill-rule="evenodd" d="M1.323 11.447C2.811 6.976 7.028 3.75 12.001 3.75c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113-1.487 4.471-5.705 7.697-10.677 7.697-4.97 0-9.186-3.223-10.675-7.69a1.762 1.762 0 0 1 0-1.113ZM17.25 12a5.25 5.25 0 1 1-10.5 0 5.25 5.25 0 0 1 10.5 0Z" clip-rule="evenodd" />
                        </svg>
                    {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="eye-icon">
                            <path d="M3.53 2.47a.75.75 0 0 0-1.06 1.06l18 18a.75.75 0 1 0 1.06-1.06l-18-18ZM22.676 12.553a11.249 11.249 0 0 1-2.631 4.31l-3.099-3.099a5.25 5.25 0 0 0-6.71-6.71L7.759 4.577a11.217 11.217 0 0 1 4.242-.827c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113Z" />
                            <path d="M15.75 12c0 .18-.013.357-.037.53l-4.244-4.243A3.75 3.75 0 0 1 15.75 12ZM12.53 15.713l-4.243-4.244a3.75 3.75 0 0 0 4.244 4.243Z" />
                            <path d="M6.75 12c0-.619.107-1.213.304-1.764l-3.1-3.1a11.25 11.25 0 0 0-2.63 4.31c-.12.362-.12.752 0 1.114 1.489 4.467 5.704 7.69 10.675 7.69 1.5 0 2.933-.294 4.242-.827l-2.477-2.477A5.25 5.25 0 0 1 6.75 12Z" />
                        </svg>
                    {/if}
                </button>
            </div>

            <!-- hsło 2 -->
            <div class="input-wrapper">
                <input type={showConfirmPassword ? "text" : "password"} class="input-text-box" bind:value={password_confirm} placeholder="Powtórz hasło" required />
                <button type="button" class="show-password-button" on:click={toggleShowConfirm}>
                    {#if showConfirmPassword}
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="eye-icon"><path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" /><path fill-rule="evenodd" d="M1.323 11.447C2.811 6.976 7.028 3.75 12.001 3.75c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113-1.487 4.471-5.705 7.697-10.677 7.697-4.97 0-9.186-3.223-10.675-7.69a1.762 1.762 0 0 1 0-1.113ZM17.25 12a5.25 5.25 0 1 1-10.5 0 5.25 5.25 0 0 1 10.5 0Z" clip-rule="evenodd" /></svg>
                    {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="eye-icon"><path d="M3.53 2.47a.75.75 0 0 0-1.06 1.06l18 18a.75.75 0 1 0 1.06-1.06l-18-18ZM22.676 12.553a11.249 11.249 0 0 1-2.631 4.31l-3.099-3.099a5.25 5.25 0 0 0-6.71-6.71L7.759 4.577a11.217 11.217 0 0 1 4.242-.827c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113Z" /><path d="M15.75 12c0 .18-.013.357-.037.53l-4.244-4.243A3.75 3.75 0 0 1 15.75 12ZM12.53 15.713l-4.243-4.244a3.75 3.75 0 0 0 4.244 4.243Z" /><path d="M6.75 12c0-.619.107-1.213.304-1.764l-3.1-3.1a11.25 11.25 0 0 0-2.63 4.31c-.12.362-.12.752 0 1.114 1.489 4.467 5.704 7.69 10.675 7.69 1.5 0 2.933-.294 4.242-.827l-2.477-2.477A5.25 5.25 0 0 1 6.75 12Z" /></svg>
                    {/if}
                </button>
            </div>

            {#if message}
                <p class="status-message" class:error-text={errorExists}>{message}</p>
            {/if}

            {#if errorExists}
                <div class="error-box">
                    {#each Object.values(errors) as errGroup}
                        {#each Array.isArray(errGroup) ? errGroup : [errGroup] as error}
                            <p class="error-item">• {error}</p>
                        {/each}
                    {/each}
                </div>
            {/if}

            <button type="submit" class="submit-button" style="width: 150px; margin-top: 15px;">Zarejestruj</button>
        </form>

        <a href="/" class="submit-button link-button"> Masz już konto? Zaloguj się.</a>
    </div>
</div>

<style>
    .page-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        background-image: url('mesh-679.png');
        /* background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='18' viewBox='0 0 100 18'%3E%3Cpath fill='%23bababa' fill-opacity='0.49' d='M61.82 18c3.47-1.45 6.86-3.78 11.3-7.34C78 6.76 80.34 5.1 83.87 3.42 88.56 1.16 93.75 0 100 0v6.16C98.76 6.05 97.43 6 96 6c-9.59 0-14.23 2.23-23.13 9.34-1.28 1.03-2.39 1.9-3.4 2.66h-7.65zm-23.64 0H22.52c-1-.76-2.1-1.63-3.4-2.66C11.57 9.3 7.08 6.78 0 6.16V0c6.25 0 11.44 1.16 16.14 3.42 3.53 1.7 5.87 3.35 10.73 7.24 4.45 3.56 7.84 5.9 11.31 7.34zM61.82 0h7.66a39.57 39.57 0 0 1-7.34 4.58C57.44 6.84 52.25 8 46 8S34.56 6.84 29.86 4.58A39.57 39.57 0 0 1 22.52 0h15.66C41.65 1.44 45.21 2 50 2c4.8 0 8.35-.56 11.82-2z'%3E%3C/path%3E%3C/svg%3E"); */
    }

    .panel {
        width: 100%;
        max-width: 400px;
        padding: 20px;
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.4);
        border: 2px solid rgba(184, 184, 184, 0.164);
        backdrop-filter: blur(3px);
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
        position: relative;
    }

    .header {
        text-align: center;
        margin: 8px 0 20px 0;
        font-size: 18px;
        font-weight: bold;
    }

    .input-wrapper {
        position: relative;
        width: 100%;
    }

    .input-text-box {
        margin-bottom: 10px;
        padding: 8px 12px;
        width: 100%;
        box-sizing: border-box;
        font-size: 16px;
        border: 1px solid rgb(68, 68, 68);
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.8);
    }

    .show-password-button {
        position: absolute;
        right: 10px;
        top: 6px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
    }

    .eye-icon {
        height: 28px;
        color: #333;
    }

    .submit-button {
        display: block;
        margin: 10px auto;
        font-size: 16px;
        border-radius: 10px;
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
        border: 1px solid rgb(68, 68, 68);
        background-color: rgba(255, 255, 255, 0.507);
        cursor: pointer;
        padding: 8px 15px;
        backdrop-filter: blur(10px);
        text-align: center;
        transition: transform 0.3s ease-in-out;
    }

    .submit-button:hover {
        transform: scale(1.05);
    }

    .link-button {
        width: 90%;
        font-size: 14px;
        text-decoration: none;
        color: inherit;
    }

    .status-message {
        text-align: center;
        font-size: 14px;
        margin: 10px 0;
        color: green;
    }

    .error-text {
        color: #D60036;
    }
    .error-box {
        margin-bottom: 10px;
        text-align: left;
        padding: 0 15px;
    }

    .error-item {
        color: #D60036;
        font-size: 13px;
        margin: 2px 0;
        font-weight: 500;
    }
</style>
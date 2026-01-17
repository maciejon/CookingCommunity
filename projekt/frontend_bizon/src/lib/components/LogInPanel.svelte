<script>    
    import { auth, logout } from '../authStore.ts';
    import { scale, fade, fly } from 'svelte/transition';
    let isActive=false;
    function toggle(){
        isActive = !isActive;
    }
    let showPassword = false;
    function toggleShow(){
        showPassword = !showPassword;
    }

    let username = '';
    let password = '';
    let error = '';

    async function handleLogin() {
        const res = await fetch('http://127.0.0.1:8000/token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);
            auth.set({ 
                isLoggedIn: true, 
                accessToken: data.access, 
                refreshToken: data.refresh 
            });
        } else {
            error = "Błędny login lub hasło";
        }
    }
</script>

<main>
    <!-- coś klikalnego po czym wyskoczy panel -->
     <slot {isActive} {toggle}></slot>
    <!-- panel logowania -->
    {#if isActive}
    <div class="panel" in:fly={{ x: 300, duration: 500 }} out:fade={{ duration: 100 }}>
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <svg on:click={() => isActive = false} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"stroke-width="1" stroke="#333333" fill="currentColor" class="X-button">
            <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-1.72 6.97a.75.75 0 1 0-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 1 0 1.06 1.06L12 13.06l1.72 1.72a.75.75 0 1 0 1.06-1.06L13.06 12l1.72-1.72a.75.75 0 1 0-1.06-1.06L12 10.94l-1.72-1.72Z" clip-rule="evenodd" />
        </svg>
        <div style="text-align:center;margin:8px;font-size:18px;">{!$auth.isLoggedIn ? "ZALOGUJ SIĘ" : "SUKCES"}</div>
        {#if !$auth.isLoggedIn}
        <form on:submit|preventDefault={handleLogin}>
            <input type="text" class="input-text-box" bind:value={username} placeholder="Login" required />
            <input type={showPassword ? "text" : "password"}  class="input-text-box" bind:value={password} placeholder="Hasło" required />
            <button type="button" class="show-password-button" on:click={toggleShow}>
                {#if showPassword}
                    <span><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="eye-icon">
                    <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
                    <path fill-rule="evenodd" d="M1.323 11.447C2.811 6.976 7.028 3.75 12.001 3.75c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113-1.487 4.471-5.705 7.697-10.677 7.697-4.97 0-9.186-3.223-10.675-7.69a1.762 1.762 0 0 1 0-1.113ZM17.25 12a5.25 5.25 0 1 1-10.5 0 5.25 5.25 0 0 1 10.5 0Z" clip-rule="evenodd" />
                    </svg>
                    </span>
                {:else}
                    <span><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="eye-icon">
                    <path d="M3.53 2.47a.75.75 0 0 0-1.06 1.06l18 18a.75.75 0 1 0 1.06-1.06l-18-18ZM22.676 12.553a11.249 11.249 0 0 1-2.631 4.31l-3.099-3.099a5.25 5.25 0 0 0-6.71-6.71L7.759 4.577a11.217 11.217 0 0 1 4.242-.827c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113Z" />
                    <path d="M15.75 12c0 .18-.013.357-.037.53l-4.244-4.243A3.75 3.75 0 0 1 15.75 12ZM12.53 15.713l-4.243-4.244a3.75 3.75 0 0 0 4.244 4.243Z" />
                    <path d="M6.75 12c0-.619.107-1.213.304-1.764l-3.1-3.1a11.25 11.25 0 0 0-2.63 4.31c-.12.362-.12.752 0 1.114 1.489 4.467 5.704 7.69 10.675 7.69 1.5 0 2.933-.294 4.242-.827l-2.477-2.477A5.25 5.25 0 0 1 6.75 12Z" />
                    </svg>
                    </span>
                {/if}</button>
        {#if error}<p style="text-align:center;color:red">{error}</p>{/if}
            <button type="submit" class="submit-button" style="width: 100px;">Zaloguj</button>
        </form>
        <a href="/register" class="submit-button" style="width: 90%;" on:click={toggle}> Nie masz konta? Przejdź do rejestracji.</a>
        {:else}
        <div class="success-container" in:scale>
            Zalogowano. Witaj, {username}
            <button class="submit-button" style="width: 90%;" on:click={logout}>Wyloguj</button>
        </div>
    {/if}
        </div>
    {/if}
</main>

<style>
    main{
        position: absolute;
        display: contents;
    }
    .panel{
        position:fixed;
        top:100px;
        right:10px;
        width:25%;
        /* height:200px; */
        border-radius: 20px;
        background-color: rgb(255, 255, 255, 0.4);
        border: 2px solid rgba(184, 184, 184, 0.164);
        backdrop-filter: blur(10px);
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
    }
    .X-button{
        width:30px;
        height:30px;
        top:5px;
        right:5px;
        position:absolute;
        transition: transform 0.1s ease-in-out;
    }
    .X-button:hover{
        color:#D60036;
    }
    .X-button:active{
        transform: scale(1.1);
    }
    .input-text-box{
        margin-left: 3%;
        margin-bottom:1%;
        padding:6px;
        width:94%;
        font-size:16px;
        border: 1px solid rgb(68, 68, 68);
        border-radius: 10px;
    }
    .show-password-button{
        position: absolute;
        right: 4%;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        font-size: 1.2rem;
    }
    .eye-icon{
        padding:4px;
        height:32px;
    }
    .submit-button{
        display: block;
        margin: 3px auto;
        font-size:16px;
        border-radius: 10px;
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));
        border: 1px solid rgb(68, 68, 68);
        background-color: rgba(255, 255, 255, 0.507);
        cursor: pointer;
        padding:3px;
        backdrop-filter: blur(10px);
    }
    .submit-button:hover{
    transition: transform 0.3s ease-in-out;
    transform: scale(1.05);
    }
    .success-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        font-weight: bold;
    }
    a{color: inherit;
    text-decoration: none;
    }
</style>
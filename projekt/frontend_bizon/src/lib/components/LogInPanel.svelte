<script>
    let isActive=false;
    function toggle(){
        isActive = !isActive;
    }
</script>

<main>
    <!-- coś klikalnego po czym wyskoczy panel -->
     <slot {isActive} {toggle}></slot>
    <!-- panel logowania -->
    <div class:inActive={!isActive} class="panel">
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <svg on:click={() => isActive = false} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"stroke-width="1" stroke="#333333" fill="currentColor" class="X-button">
        <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-1.72 6.97a.75.75 0 1 0-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 1 0 1.06 1.06L12 13.06l1.72 1.72a.75.75 0 1 0 1.06-1.06L13.06 12l1.72-1.72a.75.75 0 1 0-1.06-1.06L12 10.94l-1.72-1.72Z" clip-rule="evenodd" />
        </svg>
        <div style="text-align:center;margin:2px;">LOGOWANIE</div>
        Nie masz konta? przejdź do rejestracji
    </div>
</main>

<style>
    main{
        display: contents;
        z-index:10;
    }
    .inActive{
        display:none;
    }
    .panel{
        position:fixed;
        top:100px;
        right:10px;
        width:25%;
        height:200px;
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
</style>
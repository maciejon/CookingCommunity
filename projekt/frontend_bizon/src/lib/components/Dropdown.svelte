<!-- /** title - tytuł dropdownu
* content - tablica opcji dropdownu. etykieta jest wyświetlana a wartość moze być uzywana do czegos innego np. url
*/ -->
<script>
    export let title;
    /*@type {boolean} */
    export let is_child = false;
    // np. w panelu navbar wartosc to bedzie url
    /* @type {{etykieta: string, wartosc?: string, children?: any[]}[]}  */ 
    export let content = [];
</script>

<div class="dropdown" class:is-child={is_child} >
  {#if content && content.length > 0}
    {title}
    <div class="dropdown-content">
        {#each content as dropdown_option}
        <div class="dropdown-option">
             {#if dropdown_option.children}
             <div class="dropdown-child">
             <svelte:self title={dropdown_option.etykieta} content={dropdown_option.children} is_child={true} />
             </div>
             {:else}
             <div class="no_children">
            {dropdown_option.etykieta}
            </div>
            {/if}  
          </div>
        {/each}
    </div>
    {/if}
</div>

<style>
.dropdown{
  position: relative;
  padding: 5px;
}

.no_children{
  padding:5px;
}

.dropdown-content {
  display: none;
  position: absolute;
  /* border: 1px solid rgb(224,224,224); */
    border: 1px solid rgb(0,0,0);
}

.dropdown:hover > .dropdown-content { /* strzałka > sprawia że działa to tylko na dziecko 1 rzędu*/
  display:block;
}

.dropdown-option {
  color: black;
  /* padding: 5px; */

}

.dropdown-option:hover{
  color: white;
  background-color: black;
}

.dropdown.is-child > .dropdown-content {
  left: 100%; 
  top: 0; 
}
</style>
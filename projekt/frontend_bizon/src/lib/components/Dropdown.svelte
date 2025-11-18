<!-- /** title - tytuł dropdownu
* content - tablica opcji dropdownu. etykieta jest wyświetlana a wartość moze być uzywana do czegos innego np. url
*/ -->
<script>
    export let title;
    export let wartosc ='';
    /*@type {boolean} */
    export let is_child = false;
    export let font_size = '16px';
    // np. w panelu navbar wartosc to bedzie url
    /* @type {{etykieta: string, wartosc?: string, children?: any[]}[]}  */ 
    export let content = [];
</script>

<div class="dropdown" class:is-child={is_child} style:font-size={font_size}>
  {#if content && content.length > 0}
    <a href="{wartosc}">
      {title}
    </a>
    <div class="dropdown-content">
        {#each content as dropdown_option}
        <div class="dropdown-option">
             {#if dropdown_option.children}
             <div class="dropdown-child">
             <svelte:self title={dropdown_option.etykieta} content={dropdown_option.children} is_child={true} font_size={font_size}/>
             </div>
             {:else}
             <a href="{dropdown_option.wartosc}">
              <div class="no_children">
                {dropdown_option.etykieta}
              </div>
            </a>  
            {/if}  
          </div>
        {/each}
    </div>
    {/if}
</div>

<style>
  a{
    color: inherit;
    text-decoration: none;
  }
.dropdown{
  position: relative;
  padding: 5px;
  padding-right: 8px;
  cursor: default;
}

.no_children{
  padding:5px;
  padding-right: 8px;
  cursor: pointer;
}

.dropdown-content {
  display: none;
  position: absolute;
  /* border: 1px solid rgb(224,224,224); */
  border: 1px solid rgb(0,0,0);
  z-index: 10;
  background-color: white;
  padding-top: 8px;
  padding-bottom: 8px;
  filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, 0.4));
}

.dropdown:hover > .dropdown-content { /* strzałka > sprawia że działa to tylko na dziecko 1 rzędu*/
  display:block;
}

.dropdown-option {
  color: black;
  /* padding: 5px; */
  padding-left: 8px;

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
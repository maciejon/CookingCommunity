<!-- /** title - tytuł dropdownu
* content - tablica opcji dropdownu. etykieta jest wyświetlana a wartość moze być uzywana do czegos innego np. url
*/ -->
<script>
    export let title;
    // np. w panelu navbar wartosc to bedzie url
    /* @type {{etykieta: string, wartosc: string} */ 
    export let content = [];
</script>

<div class="dropdown">
    {title}
    <div class="dropdown-content">
        {#each content as dropdown_option}
          <div class="dropdown-option">
            {dropdown_option.etykieta}
            <br>
          </div>
        {/each}
    </div>
</div> 

<style>
.dropdown-content {
  display: none;
  position: absolute;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown-option {
    margin: 1px;
    border: 1px solid rgb(224,224,224);
}
</style>
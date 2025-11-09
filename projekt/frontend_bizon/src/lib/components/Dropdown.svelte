<script>
    export let dropdown_title;
    /* @type {{etykieta: string, wartosc: string} */
    export let dropdown_content = [];
</script>

<div class="dropdown">
    {dropdown_title}
    <div class="dropdown-content">
        {#each dropdown_content as dropdown_option}
            {dropdown_option}
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
</style>
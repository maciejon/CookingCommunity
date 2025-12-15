<script>
    // Import komponentu Svelte
    import Dropdown from './Dropdown.svelte';
    import LogInPanel from '$lib/components/LogInPanel.svelte';

    // Definicje danych dla każdego dropdownu

const naSkroty = {
    title: 'NA SKRÓTY',
    wartosc: 'na-skroty',
    content: [
        { etykieta: 'Szybkie obiady', wartosc: 'szybkie-obiady' },
        { etykieta: 'Dania w 20 minut', wartosc: 'dania-w-20-minut' },
        {
            etykieta: 'Proste przepisy',
            wartosc: 'proste-przepisy',
            children: [
                { etykieta: 'Sałatki', wartosc: 'salatki' },
                { etykieta: 'Zupy', wartosc: 'zupy' },
                { etykieta: 'Kanapki', wartosc: 'kanapki' }
            ]
        }
    ]
};

const posilki = {
    title: 'POSIŁKI',
    content: [
        { etykieta: 'Śniadania', wartosc: 'sniadania' },
        {
            etykieta: 'Obiady',
            wartosc: 'obiady',
            children: [
                { etykieta: 'Zupy', wartosc: 'zupy' },
                { etykieta: 'Dania główne', wartosc: 'dania-glowne' },
                { etykieta: 'Dodatki', wartosc: 'dodatki' }
            ]
        },
        { etykieta: 'Kolacje', wartosc: 'kolacje' },
        { etykieta: 'Przekąski', wartosc: 'przekaski' }
    ]
};

const skladniki = {
    title: 'SKŁADNIKI',
    content: [
        {
            etykieta: 'Mięso',
            wartosc: 'mieso',
            children: [
                { etykieta: 'Kurczak', wartosc: 'kurczak' },
                { etykieta: 'Wołowina', wartosc: 'wolowina' },
                { etykieta: 'Wieprzowina', wartosc: 'wieprzowina' }
            ]
        },
        { etykieta: 'Warzywa', wartosc: 'warzywa' },
        { etykieta: 'Owoce', wartosc: 'owoce' },
        { etykieta: 'Nabiał', wartosc: 'nabial' }
    ]
};

const naZdrowie = {
    title: 'NA ZDROWIE',
    content: [
        { etykieta: 'Fit przepisy', wartosc: 'fit-przepisy' },
        { etykieta: 'Wegetariańskie', wartosc: 'wegetarianskie' },
        { etykieta: 'Wegańskie', wartosc: 'weganskie' },
        {
            etykieta: 'Bez glutenu',
            wartosc: 'bez-glutenu',
            children: [
                { etykieta: 'Ciasta bezglutenowe', wartosc: 'ciasta-bezglutenowe' },
                { etykieta: 'Chleby bezglutenowe', wartosc: 'chleby-bezglutenowe' }
            ]
        }
    ]
};

const okazje = {
    title: 'OKAZJE',
    content: [
        { etykieta: 'Święta', wartosc: 'swieta' },
        { etykieta: 'Urodziny', wartosc: 'urodziny' },
        { etykieta: 'Grill', wartosc: 'grill' },
        { etykieta: 'Impreza', wartosc: 'impreza' }
    ]
};

const desery = {
    title: 'DESERY',
    content: [
        {
            etykieta: 'Ciasta',
            wartosc: 'ciasta',
            children: [
                { etykieta: 'Serniki', wartosc: 'serniki' },
                { etykieta: 'Czekoladowe', wartosc: 'czekoladowe' },
                { etykieta: 'Owocowe', wartosc: 'owocowe' }
            ]
        },
        { etykieta: 'Lody', wartosc: 'lody' },
        { etykieta: 'Ciasteczka', wartosc: 'ciasteczka' }
    ]
};
</script>
<!-- padding-left: 20px; padding-right: 20px; -->
<header> <!-- nagłówek strony  -->
  <nav> <!--  panel nawigacyjny  -->
    <div class="category-buttons">
      <div class="category-button">
        <Dropdown title={naSkroty.title} wartosc={naSkroty.wartosc} content={naSkroty.content} />
      </div>
      <div class="category-button">
        <Dropdown title={posilki.title} content={posilki.content} />
      </div>
      <div class="category-button">
        <Dropdown title={skladniki.title} content={skladniki.content} />
      </div>
      <div class="category-button">
        <Dropdown title={naZdrowie.title} content={naZdrowie.content} />
      </div>
      <div class="category-button">
        <Dropdown title={okazje.title} content={okazje.content} />
      </div>
      <div class="category-button">
        <Dropdown title={desery.title} content={desery.content} />
      </div>
    </div>
  </nav>

  <div class="second-div">
      <div class="main_logo">
        <a href="http://localhost:5173" >
          <img style="width: 100%" src="/main_logo.png" alt="mam smaka naptaka">
        </a>
      </div>

  <div style="padding-right:6%; width:100%; align-items: center;">
      <form class="search-bar" method="POST">
                <input type="text" name="query" placeholder="Wyszukaj..." class="search-input">
                <button type="submit" class="search-button">
                    <img src="/search_icon.png" alt="Szukaj" class="search-icon">
                </button>
            </form>
  </div>    

    <LogInPanel let:isActive let:toggle>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="log-in-icon" on:click={toggle}>
      <img src="/user_site_icon.png" alt="logowanie" width="20px;">
    </div>
    </LogInPanel>

  </div>
</header>

<style>
  header{
    border-bottom: 1px solid rgb(224,224,224);
    width: 100%;
  }
  nav{
    position:relative;
  }
  .main_logo{
    width: 11%;
    padding: 5px; 
  }
  .category-buttons{
    background-color: black;
    color:white;
    display: flex;
    justify-content: center;
    /* padding-left: 20%;
    padding-right: 20%; */
  }

  @media(min-width:800px){
    .category-button{
      padding-left: 20px; padding-right: 20px;
    }
  }

  .second-div{
    display: flex;
  }
  .search-bar {
    display: flex;
    align-items: center;
    background-color: #e0e0e0; 
    border-radius: 5px;
    padding: 5px;
    width: 38%;
    max-width: 1000px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin: auto;
}

.search-input {
    flex-grow: 1;
    border: none;
    outline: none;
    background: transparent;
    padding: 5px 10px;
    font-size: 16px;
}

.search-button {
    background-color: #D60036;
    border: none;
    padding: 5px;
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease;
}

.search-icon {
    width: 16px;
    height: 16px;
    object-fit: contain;
}

.search-button:hover {
    transform: scale(1.1);
}
.log-in-icon{
  right:0;
  width: 5%;
}
.log-in-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
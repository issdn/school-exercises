<script>
    import { becher } from "./stores.js";

    export let sorteKey = "sorte1";
    export let sorteKey2 = "sorte2";

    let currBecher;
    becher.subscribe(value => {
      currBecher = value;
    });
</script>

<fieldset class="transition-colors duration-[2000ms] border-[3px] border-black p-4 text-xl capitalize dark:border-white">
	<legend class="ml-4 px-1">Dein Becher</legend>
    {#if currBecher[sorteKey].kugel === 0 && currBecher[sorteKey2].kugel === 0}
      <p class="normal-case text-lg">
        Wähle einen oder zwei Geschmäcke, die Anzahl der Kugel und optional einen Zusatz um zu bestellen.
      </p>
    {:else}
      <ul>
        <h1>Kugel:</h1>
        <div class="flex flex-row gap-2 ml-4">
          <li>{currBecher[sorteKey].kugel}</li>
          <li>{currBecher[sorteKey].name}</li>
        </div>
        <div class="flex flex-row gap-2 ml-4">
          <li>{currBecher[sorteKey2].kugel}</li>
          <li>{currBecher[sorteKey2].name}</li>
        </div>
        <h1>Zusatz:</h1>
          <li class="ml-4">{currBecher.zusatz}</li>
        <h1>Preis:</h1>
          <li class="ml-4 bg-fuchsia-400 -rotate-2 px-4 w-fit">{(currBecher.kugelPreis + currBecher.zusatzPreis).toFixed(1)}€</li>
      </ul>
    {/if}
</fieldset>
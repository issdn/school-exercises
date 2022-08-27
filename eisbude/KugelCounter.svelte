<script>
  import { fly } from "svelte/transition";
  import Warning from "./Warning.svelte";
  import { sendToast, becher } from "./stores.js";
  export let sorteKey;
  export let sorteKey2;

  let warningMessage = "";
  let warningVisible;

  const decrement = () => {
    const kugelNow = $becher[sorteKey].kugel;
    if (kugelNow <= 0) {
      return;
    }
    becher.set({
      ...$becher,
      [sorteKey]: { ...$becher[sorteKey], kugel: parseInt([kugelNow]) - 1 },
      kugelPreis: parseFloat($becher.kugelPreis) - 1.0
    });
  };

  const increment = () => {
    const kugelNow = $becher[sorteKey].kugel;
    if (kugelNow >= 6 || kugelNow + $becher[sorteKey2].kugel >= 6) {
      sendToast("Max 6 Kugeln gesamt 😢", 3000);
      return;
    }
    becher.set({
      ...$becher,
      [sorteKey]: { ...$becher[sorteKey], kugel: parseInt([kugelNow]) + 1 },
      kugelPreis: parseFloat($becher.kugelPreis) + 1.0
    });
  };

  const reset = () => {
    becher.set({
      ...$becher,
      [sorteKey]: { ...$becher[sorteKey], kugel: 0 },
      kugelPreis: $becher.kugelPreis - $becher[sorteKey].kugel * 1.0
    });
  };
</script>

<div>
  <div class="flex flex-col-reverse mini:flex-row gap-3 mini:items-end text-xl">
    <div class="flex flex-row gap-3">
      <div on:click={decrement} class="bg-blue-300 py-2 px-4 hover:bg-blue-200 cursor-pointer">
        <i class="fa-solid fa-minus"></i>
      </div>
      <div on:click={increment} class="bg-blue-300 py-2 px-4 hover:bg-blue-200 cursor-pointer">
        <i class="fa-solid fa-plus"></i>
      </div>
    </div>
    <h1 class="text-2xl md:text-[1.8rem] xl:text-[2.15rem]">Kugeln:
    {#key $becher[sorteKey].kugel}
      <span in:fly={{ y: -20 }} class="inline-block">{$becher[sorteKey].kugel}</span>
    {/key}
    </h1>
  </div>
  <p on:click={reset} class="text-neutral-400 w-fit cursor-pointer hover:text-blue-700 dark:hover:text-white">zurücksetzen</p>
</div>
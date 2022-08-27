<script>
  import { slide } from "svelte/transition";
  import { becher } from "./stores.js";
  export let sorte = [
    "vanille",
    "schokolade",
    "erdbeere",
    "chocolate chip",
    "matcha"
  ];
  export let sorteKey;

  let currBecher;
  becher.subscribe(value => {
    currBecher = value;
  });

  let isOpen = false;
</script>

<div on:click={()=>isOpen=!isOpen} class="text-xl flex flex-col gap-y-1 h-fit capitalize relative">
    <div class="flex flex-row gap-x-1 cursor-pointer [&_div]:hover:bg-blue-200">
      <div class="bg-blue-300 w-full flex flex-row py-2 pl-3 cursor-pointer">{currBecher[sorteKey].name}</div>
      <div class="bg-blue-300 px-4 py-2"><i class="fa-solid fa-chevron-down"></i></div>
    </div>
  <div class="relative z-10">
  {#if isOpen}
    <div transition:slide class="absolute w-full">
      <div class:open={isOpen === true} class="hidden">
        {#each sorte as item}
          <div on:click={()=>becher.set({...currBecher, [sorteKey] : {...currBecher[sorteKey], name : item}})} class="bg-blue-300 w-full flex flex-row py-2 pl-3 cursor-pointer hover:bg-blue-200">
            <p>{item}</p>
          </div>
        {/each}
      </div>
    </div>
  {/if}
  </div>
</div>

<style>
  .open {
    display: flex;
    flex-direction: column;
  }
</style>
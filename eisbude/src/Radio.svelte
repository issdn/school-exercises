<script>
 import { becher } from "./stores.js";
 export let name;
 export let preis;

 let currBecher;
 becher.subscribe(value => {
   currBecher = value;
 });
</script>

<div on:click={() => becher.set({...currBecher, zusatz: name, zusatzPreis: name === "kein" ? 0.0 : parseFloat(preis)})} class="flex flex-row gap-2 md:gap-4 items-center text-sm mini:text-lg md:text-2xl">
		<span class="">
			<input class="w-5 h-5 accent-blue-500 dark:accent-fuchsia-500 cursor-pointer" type="radio" id={name} name="zusatz" checked={name==="kein"}>
		</span>
		<div class="flex flex-row w-full justify-between">
			<label class="cursor-pointer" for={name}>{name}</label>
			{#if preis !== null}
				<p>{preis}€</p>
			{/if}
		</div>
</div>
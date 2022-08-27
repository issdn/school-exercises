<script>
	import Radio from "./Radio.svelte";
	export let zusatze = {
	  schokostreusel: "0.5",
	  karamell: "0.7",
	  kirschen: "0.6",
	  schlagsahne: "0.4",
	  kein: null
	};
	// const fetchZusatze = (async () => {
	//   const response = await fetch("https://sveltedeu.free.beeceptor.com/zusatze");
	//   return await response.json();
	// })();
</script>


	<fieldset class="transition-colors duration-[2000ms] border-[3px] border-black p-4 text-xl capitalize dark:border-white">
		<legend class="ml-4 px-1">Zusätze</legend>
		<!-- {#await fetchZusatze}
			<p>Loading...</p>
		{:then zusatze} -->
		<!-- {console.log(JSON.stringify(zusatze))} -->
			{#each Object.entries(zusatze) as [zusatz, preis]}
				<Radio name={zusatz} preis={preis}/>
			{/each}
		<!-- {/await} -->
	</fieldset>

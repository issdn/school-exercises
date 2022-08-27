<script>
	import { toasts, becher, sendToast } from "./stores.js";
	import { fly, fade } from "svelte/transition";
	import axios from "axios";

	import Dropdown from "./Dropdown.svelte";
	import KugelCounter from "./KugelCounter.svelte";
	import Zusatze from "./Zusatze.svelte";
	import Info from "./Info.svelte";
	import InfoForm from "./InfoForm.svelte";
	import Warning from "./Warning.svelte";
	import ToastContainer from "./ToastContainer.svelte";

	const order = () => {
	  if (
	    ($becher.sorte1.name === "eissorte" && $becher.sorte1.kugel > 0) ||
	    ($becher.sorte2.name === "eissorte" && $becher.sorte2.kugel > 0)
	  ) {
	    sendToast(
	      "Bestellen von Kugeln ohne Geschmack ist nicht möglich. Wähle einen Geschmack oder setze die Anzahl der Kugeln zurück.",
	      8000
	    );
	    return;
	  } else {
	    alert(JSON.stringify($becher, null, 4));
	    // axios
	    //   .get("https://sveltedeu.free.beeceptor.com")
	    //   .then(res => alert(JSON.stringify(res.data)));
	  }
	};

	let darkMode = false;
	const toggleDarkMode = () => {
	  darkMode = !darkMode;
	  console.log(darkMode);
	};
</script>

<div class:dark={darkMode} class="h-full w-full">
<main class="transition-colors duration-1000 font-['Roboto_Mono'] font-medium h-full dark:bg-[#1F2937] dark:text-white overflow-auto">
	<div class="p-8 flex flex-col gap-y-4 xl:px-[20vw]">
		<div class="flex flex-row justify-between mb-4 items-center">
			<div class="w-16"/>
			<div class="text-7xl text-[#E879F9] flex justify-center">
				<i class="fa-solid fa-ice-cream -rotate-45"></i>
			</div>
			<div on:click={toggleDarkMode} class:toggledDark={darkMode} class="flex items-center justify-between w-16 h-8 bg-gray-700 cursor-pointer text-yellow-500 rounded-2xl px-2 text-lg after:transition-transform after:duration-500 after:content-[' '] after:absolute after:w-5 after:h-5 after:bg-white after:rounded-xl">
					<i in:fly={{duration:400, delay:200}} class="fa-solid fa-moon"></i>
					<i in:fly={{duration:400, delay:200}} class="fa-solid fa-sun"></i>
			</div>
		</div>
		<div class="flex flex-col gap-y-4 h-full md:flex-row md:flex md:justify-between md:gap-x-36">
			<div class="flex flex-col gap-y-4 md:justify-between md:w-full">
				<div class="flex flex-col gap-y-2">
					<small class="text-white bg-[#E879F9] w-fit px-2 -rotate-2">1 Kugel = 1€</small>
					<Dropdown sorteKey="sorte1"/>
					<KugelCounter sorteKey="sorte1" sorteKey2="sorte2"/>
				</div>
				<div class="flex flex-col gap-y-2">
					<Dropdown sorteKey="sorte2"/>
					<KugelCounter sorteKey="sorte2" sorteKey2="sorte1"/>
				</div>
				<Zusatze/>
			</div>
			<div class="flex flex-col gap-y-4 md:justify-between md:w-full">
				<Info/>
				<InfoForm/>
				<button on:click={order} class="bg-fuchsia-400 py-2 text-xl hover:bg-fuchsia-300 disabled:bg-fuchsia-300 disabled:hover:bg-fuchsia-300 disabled:cursor-not-allowed" disabled={$becher.sorte1.kugel === 0 && $becher.sorte2.kugel === 0}><i class="fa-solid fa-cart-shopping mr-4 text-lg"></i>Bestellen</button>
			</div>
		</div>
	</div>
</main>
<ToastContainer/>
</div>
<style>
	.toggledDark::after {
	  transform: translateX(150%);
	}
</style>
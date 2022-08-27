<script>
 import { toasts } from "./stores.js";
 import Warning from "./Warning.svelte";
</script>

<div class="fixed inset-x-0 inset-y-0 font-['Roboto_Mono'] pointer-events-none flex flex-col items-center justify-end">
		{#each $toasts as toast (toast.id)}
			<Warning index={toast.id} visible={true} message={toast.message}/>
		{/each}
</div>
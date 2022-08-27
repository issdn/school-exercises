<script>
	import { becher } from "./stores.js";
</script>

<div class="h-48">
	<textarea bind:value={$becher.info} class="transition-colors duration-1000 bg-blue-100 dark:bg-gray-700 resize-none w-full h-full p-4 box-border outline-none border-black focus:border-2 dark:border-white" maxlength="256"
	 placeholder="Zusätliche Info" />
	</div>
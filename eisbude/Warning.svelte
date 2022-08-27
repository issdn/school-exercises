<script>
  import { slide } from "svelte/transition";
  import { removeToast } from "./stores.js";
  const sleep = time => new Promise(res => setTimeout(res, time));

  export let index;
  export let message = "";
  export let visible;

  const close = () => {
    visible = false;
    sleep(1000).then(() => removeToast(index));
  };
</script>

{#if visible}
<div transition:slide class="md:w-96 pointer-events-auto mb-4">
  <div class="flex justify-center items-center bg-red-500 p-4 text-white text-sm text-center">
      <p class="w-full">{message}</p>
    <div class="flex justify-end items-center text-3xl">
      <div on:click={close} class="cursor-pointer ml-2 w-fit h-fit rounded-md hover:bg-red-400 px-2">
        <i class="fa-solid fa-xmark"></i>
      </div>
    </div>
  </div>
</div>
{/if}

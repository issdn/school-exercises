import { writable } from "svelte/store";

export const becher = writable({
  sorte1: { name: "eissorte", kugel: 0 },
  sorte2: { name: "eissorte", kugel: 0 },
  zusatz: "kein",
  kugelPreis: 0.0,
  zusatzPreis: 0.0,
  info: ""
});

export const darkMode = writable(false);

const id = () => {
  return Math.random().toString(36).substr(2, 9);
};

export const toasts = writable([]);

export const sendToast = (message, timeout) => {
  const toastId = id();
  toasts.update((state) => [...state, { id: toastId, message }]);
  setTimeout(() => removeToast(toastId), timeout);
};

export const removeToast = (id) => {
  toasts.update((all) => all.filter((t) => t.id !== id));
};

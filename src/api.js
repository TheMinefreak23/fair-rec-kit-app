export const API_URL = import.meta.env.PROD
  ? import.meta.env.VITE_PROD_URL
  : import.meta.env.VITE_DEV_URL

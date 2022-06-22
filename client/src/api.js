/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

export const API_URL = import.meta.env.PROD
  ? import.meta.env.VITE_PROD_URL
  : import.meta.env.VITE_DEV_URL

export const DEV = import.meta.env.DEV

// src/api/http.ts
import axios from 'axios'
export const http = axios.create({
  baseURL: '/api', // passe par le proxy Vite en dev
  timeout: 10000,
})

// src/api/users.ts
import { http } from './http'
export const listUsers  = async () => (await http.get('/users/')).data
export const createUser = async (p: {username:string; firstname:string; email:string; password:string}) =>
  (await http.post('/users/', p)).data

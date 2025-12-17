import { http } from "./http"

export interface AlternativeOut {
  id: string
  description: string
  brand_id?: string | null
  brand_name?: string | null
}

export interface AlternativeCreate {
  description: string
  brand_id?: string | null
}

export interface AlternativeUpdate {
  description?: string
  brand_id?: string | null
}

export const listAlternatives = async () =>
  (await http.get<AlternativeOut[]>("/alternatives/")).data

export const getAlternative = async (id: string) =>
  (await http.get<AlternativeOut>(`/alternatives/${id}`)).data

export const createAlternative = async (p: AlternativeCreate) =>
  (await http.post<AlternativeOut>("/alternatives/", p)).data

export const updateAlternative = async (id: string, p: AlternativeUpdate) =>
  (await http.put<AlternativeOut>(`/alternatives/${id}`, p)).data

export const deleteAlternative = async (id: string) =>
  (await http.delete<{ message: string }>(`/alternatives/${id}`)).data

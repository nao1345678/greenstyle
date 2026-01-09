import { http } from "./http"

export interface BrandOut {
  id: string
  brand_name: string
  logo?: string | null
  website?: string | null
  category_id?: string | null
  price_range?: number | null
  sustainable_materials?: string[] | null
  certifications?: string[] | null
  country_origin?: string | null
  country_production?: string | null
  unsold_management?: string | null
  supply_chain_transparency?: number | null
  global_env_impact?: number | null
  labor_ethics?: number | null
  final_score?: number | null
  short_description?: string | null
  description?: string | null
  planet_badge?: string | null
  labor_badge?: string | null
}

export type BrandCreate = Omit<BrandOut, "id">
export type BrandUpdate = Partial<BrandCreate>

export async function listBrands() {
  const { data } = await http.get<BrandOut[]>("/brands/")
  return data
}

export async function getBrand(id: string) {
  const { data } = await http.get<BrandOut>(`/brands/${id}`)
  return data
}

export async function createBrand(payload: BrandCreate) {
  const { data } = await http.post<BrandOut>("/brands/", payload)
  return data
}

export async function updateBrand(id: string, payload: BrandUpdate) {
  const { data } = await http.put<BrandOut>(`/brands/${id}`, payload)
  return data
}

export async function deleteBrand(id: string) {
  const { data } = await http.delete<{ message: string }>(`/brands/${id}`)
  return data
}

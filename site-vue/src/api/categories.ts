import { http } from "./http"

export interface CategoryOut {
  id: string
  name: string
}
export interface CategoryCreate { name: string }
export interface CategoryUpdate { name?: string }

export const listCategories = async () => (await http.get<CategoryOut[]>("/categories/")).data
export const getCategory    = async (id: string) => (await http.get<CategoryOut>(`/categories/${id}`)).data
export const createCategory = async (p: CategoryCreate) => (await http.post<CategoryOut>("/categories/", p)).data
export const updateCategory = async (id: string, p: CategoryUpdate) => (await http.put<CategoryOut>(`/categories/${id}`, p)).data
export const deleteCategory = async (id: string) => (await http.delete<{message:string}>(`/categories/${id}`)).data

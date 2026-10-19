const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'
export function getToken() { return localStorage.getItem('planora_access') || '' }
export function setTokens(access: string, refresh?: string) {
  localStorage.setItem('planora_access', access)
  if (refresh) localStorage.setItem('planora_refresh', refresh)
}
export function clearTokens() {
  localStorage.removeItem('planora_access')
  localStorage.removeItem('planora_refresh')
}
export async function api<T = any>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers || {})
  if (!(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  if (getToken()) headers.set('Authorization', `Bearer ${getToken()}`)
  const response = await fetch(`${API}${path}`, { ...options, headers })
  if (!response.ok) {
    let message = `Request failed (${response.status})`
    try { const data = await response.json(); message = data.detail || data.non_field_errors?.[0] || JSON.stringify(data) } catch {}
    throw new Error(message)
  }
  if (response.status === 204) return undefined as T
  return response.json()
}

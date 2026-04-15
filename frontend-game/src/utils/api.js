const rawApiUrl = import.meta.env.VITE_API_URL || window.location.origin
const normalizedApiUrl = rawApiUrl.replace(/\/+$/, '')

export const API_URL = normalizedApiUrl

export const buildApiUrl = (path) => {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${API_URL}${normalizedPath}`
}

export const buildWsUrl = (path) => {
  const wsUrl = new URL(API_URL)
  wsUrl.protocol = wsUrl.protocol === 'https:' ? 'wss:' : 'ws:'
  wsUrl.pathname = path.startsWith('/') ? path : `/${path}`
  wsUrl.search = ''
  wsUrl.hash = ''
  return wsUrl.toString()
}

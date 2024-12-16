'use client'

import { useRouter } from 'next/navigation'


export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const router = useRouter()
  let accessToken = router.cookies.get('access_token')?.value

  if (!accessToken) {
    const refreshed = await refreshAccessToken()
    if (!refreshed) {
      throw new Error('Authentication required')
    }
    accessToken = router.cookies.get('access_token')?.value
  }

  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`,
    },
  })

  if (response.status === 401) {
    const refreshed = await refreshAccessToken()
    if (refreshed) {
      return fetchWithAuth(url, options)
    } else {
      throw new Error('Authentication required')
    }
  }

  return response
}

async function refreshAccessToken(): Promise<boolean> {
  const router = useRouter()
  const refreshToken = router.cookies.get('refresh_token')?.value
  if (!refreshToken) {
    return false
  }

  try {
    const response = await fetch('/api/py/refresh-token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    })

    if (response.ok) {
      const { access_token } = await response.json()
      router.cookies.set('access_token', access_token, { maxAge: 60 * 60 }) // 1 hour
      return true
    } else {
      router.cookies.delete('access_token')
      router.cookies.delete('refresh_token')
      return false
    }
  } catch (error) {
    console.error('Error refreshing token:', error)
    return false
  }
}

export function isAuthenticated(): boolean {
  const router = useRouter()
  return !!router.cookies.get('access_token')
}

export function logout() {
  const router = useRouter()
  router.cookies.delete('access_token')
  router.cookies.delete('refresh_token')
}


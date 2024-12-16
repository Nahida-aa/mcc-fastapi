import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const accessToken = request.cookies.get('access_token')
  const refreshToken = request.cookies.get('refresh_token')

  if (!accessToken && refreshToken) {
    // 尝试刷新 token
    try {
      const resp = await fetch('http://your-backend-api/refresh-token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken.value }),
      })

      if (resp.ok) {
        const { access_token } = await resp.json()
        const response = NextResponse.next()
        response.cookies.set('access_token', access_token, { 
          httpOnly: true, 
          secure: process.env.NODE_ENV === 'production',
          maxAge: 60 * 60, // 1 hour
        })
        return response
      }
    } catch (error) {
      console.error('Failed to refresh token:', error)
    }
  }

  if (!accessToken && !request.nextUrl.pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/profile/:path*', '/settings/:path*'],
}


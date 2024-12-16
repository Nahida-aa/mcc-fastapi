import { cookies } from 'next/headers'

async function getUser() {
  const cookieStore = cookies()
  const token = cookieStore.get('access_token')
  
  if (!token) {
    return null
  }

  try {
    const response = await fetch('/api/py/user', {
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })

    if (response.ok) {
      return response.json()
    } else {
      return null
    }
  } catch (error) {
    console.error('Failed to fetch user:', error)
    return null
  }
}

export default async function AuthProvider({ children }: { children: React.ReactNode }) {
  const user = await getUser()

  return (
    <div>
      {user ? (
        <p>Logged in as: {user.username}</p>
      ) : (
        <p>Not logged in</p>
      )}
      {children}
    </div>
  )
}


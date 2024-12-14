'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import AppNavBar from './components/AppNavBar'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const router = useRouter()

  useEffect(() => {
    checkLoginStatus()
  }, [])

  const checkLoginStatus = async () => {
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const response = await fetch('/api/py/user', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (response.ok) {
          const userData = await response.json()
          setIsLoggedIn(true)
          setUsername(userData.username)
        } else {
          // Token is invalid or expired
          localStorage.removeItem('token')
          setIsLoggedIn(false)
        }
      } catch (error) {
        console.error('Error checking login status:', error)
        setIsLoggedIn(false)
      }
    } else {
      setIsLoggedIn(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setIsLoggedIn(false)
    setUsername('')
    router.push('/')
  }

  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-4">Welcome to Minecraft Creative Community</h1>
        {isLoggedIn ? (
          <div>
            <p className="mb-4">Welcome back, {username}!</p>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        ) : (
          <div>
            <p className="mb-4">Please log in to access all features.</p>
            <Link href="/login" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
              Login
            </Link>
          </div>
        )}
      </main>
      <AppNavBar isLoggedIn={isLoggedIn} />
    </div>
  )
}


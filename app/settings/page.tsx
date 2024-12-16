'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function BasicSettings() {
  const [user, setUser] = useState({
    username: '',
    avatar: '',
    email: '',
    phone: '',
    nickname: '',
    age: '',
  })
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  useEffect(() => {
    fetchUserData()
  }, [])

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/py/user', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else {
        alert('Failed to fetch user data')
        router.push('/login')
      }
    } catch (error) {
      console.error('Fetch user data error:', error)
      alert('An error occurred while fetching user data')
      router.push('/login')
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setUser(prevUser => ({
      ...prevUser,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/py/user', {
        method: 'PATCH',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(user),
      })
      if (response.ok) {
        alert('Settings updated successfully')
      } else {
        alert('Failed to update settings')
      }
    } catch (error) {
      console.error('Update settings error:', error)
      alert('An error occurred while updating settings')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="space-y-4">
        <div className="relative">
          <input
            id="username"
            name="username"
            type="text"
            className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            placeholder="用户名"
            value={user.username}
            onChange={handleInputChange}
          />
          <label htmlFor="username" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">用户名</label>
        </div>
        <div className="relative">
          <input
            id="email"
            name="email"
            type="text"
            className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            placeholder="邮箱"
            value={user.email}
            onChange={handleInputChange}
          />
          <label htmlFor="email" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">邮箱</label>
        </div>
        <div className="relative">
          <input
            id="nickname"
            name="nickname"
            type="text"
            className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            placeholder="昵称"
            value={user.nickname}
            onChange={handleInputChange}
          />
          <label htmlFor="nickname" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">昵称</label>
        </div>
        <div className="relative">
          <input
            id="age"
            name="age"
            type="number"
            className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            placeholder="年龄"
            value={user.age}
            onChange={handleInputChange}
          />
          <label htmlFor="age" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">年龄</label>
        </div>
      </div>
      <button type="submit" className="mt-6 bg-blue-500 text-white rounded-md px-4 py-2 disabled:opacity-50" disabled={isLoading}>
        {isLoading ? '更新中...' : '更新基本设置'}
      </button>
    </form>
  )
}


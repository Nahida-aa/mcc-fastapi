// /app/[username]/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'

interface User {
  id: number
  username: string
  avatar: string
  nickname: string
  email: string
  followers_count: number
  following_count: number
  platform_info?: {
    mc_experience: string
    play_reason: string
    server_type: string
    desired_partners: string
    favorite_content: string[]
  }
}

export default function UserProfile() {
  const [user, setUser] = useState<User | null>(null)
  const [isFollowing, setIsFollowing] = useState(false)
  const [isCurrentUser, setIsCurrentUser] = useState(false)
  const { username } = useParams()
  const router = useRouter()

  useEffect(() => {
    fetchUserData()
    checkIfCurrentUser()
  }, [username])

  const fetchUserData = async () => {
    try {
      const response = await fetch(`/api/py/user/${username}`)
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        checkIfFollowing(userData.id)
      } else {
        console.error('Failed to fetch user data')
      }
    } catch (error) {
      console.error('Error fetching user data:', error)
    }
  }

  const checkIfCurrentUser = async () => {
    try {
      const response = await fetch('/api/py/user')
      if (response.ok) {
        const currentUser = await response.json()
        setIsCurrentUser(currentUser.username === username)
      }
    } catch (error) {
      console.error('Error checking current user:', error)
    }
  }

  const checkIfFollowing = async (userId: number) => {
    try {
      const response = await fetch(`/api/py/user/following/${userId}`)
      setIsFollowing(response.ok)
    } catch (error) {
      console.error('Error checking follow status:', error)
    }
  }

  const handleFollow = async () => {
    if (!user) return

    try {
      const response = await fetch(`/api/py/user/follow/${user.id}`, {
        method: isFollowing ? 'DELETE' : 'POST',
      })
      if (response.ok) {
        setIsFollowing(!isFollowing)
        setUser(prevUser => prevUser ? {
          ...prevUser,
          followers_count: isFollowing ? prevUser.followers_count - 1 : prevUser.followers_count + 1
        } : null)
      }
    } catch (error) {
      console.error('Error updating follow status:', error)
    }
  }

  if (!user) {
    return <div className="text-center mt-8">Loading...</div>
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="p-4 sm:p-6 lg:p-8">
          <div className="sm:flex sm:items-center sm:justify-between">
            <div className="sm:flex sm:space-x-5">
              <div className="flex-shrink-0">
                <img className="mx-auto h-20 w-20 rounded-full" src={user.avatar || '/placeholder.svg?height=80&width=80'} alt={user.username} />
              </div>
              <div className="mt-4 text-center sm:mt-0 sm:pt-1 sm:text-left">
                <p className="text-xl font-bold text-gray-900 sm:text-2xl">{user.nickname || user.username}</p>
                <p className="text-sm font-medium text-gray-600">@{user.username}</p>
              </div>
            </div>
            <div className="mt-5 flex justify-center sm:mt-0">
              {!isCurrentUser && (
                <button
                  onClick={handleFollow}
                  className={`px-4 py-2 border rounded-md text-sm font-medium ${
                    isFollowing
                      ? 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
                      : 'border-transparent text-white bg-indigo-600 hover:bg-indigo-700'
                  }`}
                >
                  {isFollowing ? 'Unfollow' : 'Follow'}
                </button>
              )}
              {isCurrentUser && (
                <Link href="/settings" className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                  Edit Profile
                </Link>
              )}
            </div>
          </div>
          <div className="mt-6 grid grid-cols-2 gap-6 text-center">
            <div>
              <p className="text-2xl font-bold text-indigo-600">{user.followers_count}</p>
              <p className="text-sm font-medium text-gray-600">Followers</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-indigo-600">{user.following_count}</p>
              <p className="text-sm font-medium text-gray-600">Following</p>
            </div>
          </div>
          {user.platform_info && (
            <div className="mt-8 border-t border-gray-200 pt-8">
              <h3 className="text-lg font-medium text-gray-900">Platform Info</h3>
              <dl className="mt-4 grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Minecraft Experience</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user.platform_info.mc_experience}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Server Type</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user.platform_info.server_type}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Play Reason</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user.platform_info.play_reason}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Desired Partners</dt>
                  <dd className="mt-1 text-sm text-gray-900">{user.platform_info.desired_partners}</dd>
                </div>
                <div className="sm:col-span-2">
                  <dt className="text-sm font-medium text-gray-500">Favorite Content</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {user.platform_info.favorite_content.join(', ')}
                  </dd>
                </div>
              </dl>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function IdCardSettings() {
  const [idCardInfo, setIdCardInfo] = useState({
    id_card_number: '',
    id_card_holder: '',
    is_real_name: false,
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
        setIdCardInfo(userData.id_card_info)
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
    const { name, value, type, checked } = e.target
    setIdCardInfo(prevInfo => ({
      ...prevInfo,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/py/user/idcard', {
        method: 'PATCH',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(idCardInfo),
      })
      if (response.ok) {
        alert('ID Card info updated successfully')
      } else {
        alert('Failed to update ID Card info')
      }
    } catch (error) {
      console.error('Update ID Card info error:', error)
      alert('An error occurred while updating ID Card info')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="space-y-4">
        <div className="relative">
          <input
            id="idCardNumber"
            name="id_card_number"
            type="text"
            className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            placeholder="身份证号码"
            value={idCardInfo.id_card_number}
            onChange={handleInputChange}
          />
          <label htmlFor="idCardNumber" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">身份证号码</label>
        </div>
        <div className="relative">
          <input
            id="idCardHolder"
            name="id_card_holder"
            type="text"
            className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            placeholder="身份证持有人"
            value={idCardInfo.id_card_holder}
            onChange={handleInputChange}
          />
          <label htmlFor="idCardHolder" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">身份证持有人</label>
        </div>
        <div className="relative">
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              name="is_real_name"
              className="form-checkbox h-5 w-5 text-rose-600"
              checked={idCardInfo.is_real_name}
              onChange={handleInputChange}
            />
            <span className="ml-2 text-gray-700">是否实名认证</span>
          </label>
        </div>
      </div>
      <button type="submit" className="mt-6 bg-blue-500 text-white rounded-md px-4 py-2 disabled:opacity-50" disabled={isLoading}>
        {isLoading ? '更新中...' : '更新身份证信息'}
      </button>
    </form>
  )
}


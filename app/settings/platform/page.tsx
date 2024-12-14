'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function PlatformSettings() {
  const [platformInfo, setPlatformInfo] = useState({
    mc_experience: '',
    play_reason: '',
    server_type: '',
    desired_partners: '',
    favorite_content: [] as string[]
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
        setPlatformInfo(userData.platform_info)
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

  const handleInputChange = (e: React.ChangeEvent<HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setPlatformInfo(prevInfo => ({
      ...prevInfo,
      [name]: value
    }))
  }

  const handleFavoriteContentChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOptions = Array.from(e.target.selectedOptions, option => option.value)
    setPlatformInfo(prevInfo => ({
      ...prevInfo,
      favorite_content: selectedOptions
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/py/user/platform', {
        method: 'PATCH',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(platformInfo),
      })
      if (response.ok) {
        alert('Platform info updated successfully')
      } else {
        alert('Failed to update platform info')
      }
    } catch (error) {
      console.error('Update platform info error:', error)
      alert('An error occurred while updating platform info')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="space-y-4">
        <div className="relative">
          <select
            id="mcExperience"
            name="mc_experience"
            className="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            value={platformInfo.mc_experience}
            onChange={handleInputChange}
          >
            <option value="">选择游戏经验</option>
            <option value="0-1年">0-1年</option>
            <option value="1-3年">1-3年</option>
            <option value="3-5年">3-5年</option>
            <option value="5-8年">5-8年</option>
            <option value="8-12年">8-12年</option>
            <option value="12年以上">12年以上</option>
          </select>
          <label htmlFor="mcExperience" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">Minecraft 游戏经验</label>
        </div>
        <div className="relative">
          <textarea
            id="playReason"
            name="play_reason"
            className="peer placeholder-transparent h-20 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            placeholder="为什么玩 Minecraft"
            value={platformInfo.play_reason}
            onChange={handleInputChange}
          ></textarea>
          <label htmlFor="playReason" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">为什么玩 Minecraft</label>
        </div>
        <div className="relative">
          <select
            id="serverType"
            name="server_type"
            className="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            value={platformInfo.server_type}
            onChange={handleInputChange}
          >
            <option value="">选择服务器类型</option>
            <option value="服务器玩家">服务器玩家</option>
            <option value="公益服">公益服</option>
            <option value="盈利服">盈利服</option>
            <option value="多人竞技服">多人竞技服</option>
            <option value="多人合作服">多人合作服</option>
          </select>
          <label htmlFor="serverType" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">服务器类型</label>
        </div>
        <div className="relative">
          <select
            id="desiredPartners"
            name="desired_partners"
            className="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
            value={platformInfo.desired_partners}
            onChange={handleInputChange}
          >
            <option value="">选择期望的伙伴类型</option>
            <option value="拒绝社交">拒绝社交</option>
            <option value="服务器伙伴">服务器伙伴</option>
            <option value="同好建筑内容的伙伴">同好建筑内容的伙伴</option>
            <option value="同好生存内容的伙伴">同好生存内容的伙伴</option>
            <option value="同好冒险内容的伙伴">同好冒险内容的伙伴</option>
            <option value="同好科技内容的伙伴">同好科技内容的伙伴</option>
          </select>
          <label htmlFor="desiredPartners" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">期望的伙伴类型</label>
        </div>
        <div className="relative">
          <label htmlFor="favorite_content" className="block text-sm font-medium text-gray-700">
            喜爱的内容
          </label>
          <select
            id="favorite_content"
            name="favorite_content"
            multiple
            className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
            value={platformInfo.favorite_content}
            onChange={handleFavoriteContentChange}
          >
            <option value="建筑">建筑</option>
            <option value="红石">红石</option>
            <option value="探险">探险</option>
            <option value="生存">生存</option>
            <option value="PVP">PVP</option>
          </select>
        </div>
      </div>
      <button type="submit" className="mt-6 bg-blue-500 text-white rounded-md px-4 py-2 disabled:opacity-50" disabled={isLoading}>
        {isLoading ? '更新中...' : '更新平台信息'}
      </button>
    </form>
  )
}


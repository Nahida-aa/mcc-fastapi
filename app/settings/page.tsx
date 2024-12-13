'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Settings() {
  const [activeTab, setActiveTab] = useState('basic')
  const [user, setUser] = useState({
    username: '',
    email: '',
    nickname: '',
    age: '',
    platform_info: {
      mc_experience: '',
      play_reason: '',
      server_type: '',
      desired_partners: '',
      favorite_content: []
    },
    id_card_info: {
      id_card_number: '',
      id_card_holder: '',
      is_real_name: false,
    }
  })
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  useEffect(() => {
    // 获取用户数据
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

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target
    setUser(prevUser => {
      if (name.includes('.')) {
        const [section, field] = name.split('.')
        return {
          ...prevUser,
          [section]: {
            ...prevUser[section as keyof typeof prevUser],
            [field]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
          }
        }
      } else {
        return {
          ...prevUser,
          [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
        }
      }
    })
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
        body: JSON.stringify({
          username: user.username,
          email: user.email,
          nickname: user.nickname,
          age: user.age
        }),
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

  const handleIdCardSubmit = async (e: React.FormEvent) => {
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
        body: JSON.stringify(user.id_card_info),
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

  const handlePlatformSubmit = async (e: React.FormEvent) => {
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
        body: JSON.stringify(user.platform_info),
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
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div>
              <h1 className="text-2xl font-semibold">个人设置</h1>
            </div>
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <div className="flex space-x-4">
                  <button
                    className={`px-4 py-2 rounded ${activeTab === 'basic' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                    onClick={() => setActiveTab('basic')}
                  >
                    基本设置
                  </button>
                  <button
                    className={`px-4 py-2 rounded ${activeTab === 'platform' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                    onClick={() => setActiveTab('platform')}
                  >
                    平台信息
                  </button>
                  <button
                    className={`px-4 py-2 rounded ${activeTab === 'idcard' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
                    onClick={() => setActiveTab('idcard')}
                  >
                    身份证设置
                  </button>
                </div>
                {activeTab === 'basic' && (
                  <form onSubmit={handleSubmit}>
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
                    <button type="submit" className="bg-blue-500 text-white rounded-md px-2 py-1 disabled:opacity-50" disabled={isLoading}>
                      {isLoading ? '更新中...' : '更新基本设置'}
                    </button>
                  </form>
                )}
                {activeTab === 'platform' && (
                  <form onSubmit={handlePlatformSubmit}>
                    <div className="relative">
                      <select
                        id="mcExperience"
                        name="platform_info.mc_experience"
                        className="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                        value={user.platform_info.mc_experience}
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
                        name="platform_info.play_reason"
                        className="peer placeholder-transparent h-20 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                        placeholder="为什么玩 Minecraft"
                        value={user.platform_info.play_reason}
                        onChange={handleInputChange}
                      ></textarea>
                      <label htmlFor="playReason" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">为什么玩 Minecraft</label>
                    </div>
                    <div className="relative">
                      <select
                        id="serverType"
                        name="platform_info.server_type"
                        className="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                        value={user.platform_info.server_type}
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
                        name="platform_info.desired_partners"
                        className="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                        value={user.platform_info.desired_partners}
                        onChange={handleInputChange}
                      >
                        <option value="">选择期望的伙伴类型</option>
                        <option value="拒绝社交">拒绝社交</option>
                        <option value="服务器伙伴">服务器伙伴</option>
                        <option value="同好建筑内容的伙伴">同好建筑内容的伙伴</option>
                        <option value="同好生存内容的伙伴">同好生存内容的伙伴</option>
                        <option value="同好冒险内容��伙伴">同好冒险内容的伙伴</option>
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
                        name="platform_info.favorite_content"
                        multiple
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                        value={user.platform_info.favorite_content}
                        onChange={(e) => {
                          const selectedOptions = Array.from(e.target.selectedOptions, option => option.value);
                          setUser(prevUser => ({
                            ...prevUser,
                            platform_info: {
                              ...prevUser.platform_info,
                              favorite_content: selectedOptions
                            }
                          }));
                        }}
                      >
                        <option value="建筑">建筑</option>
                        <option value="红石">红石</option>
                        <option value="探险">探险</option>
                        <option value="生存">生存</option>
                        <option value="PVP">PVP</option>
                      </select>
                    </div>
                    <button type="submit" className="bg-blue-500 text-white rounded-md px-2 py-1 disabled:opacity-50" disabled={isLoading}>
                      {isLoading ? '更新中...' : '更新平台信息'}
                    </button>
                  </form>
                )}
                {activeTab === 'idcard' && (
                  <form onSubmit={handleIdCardSubmit}>
                    <div className="relative">
                      <input
                        id="idCardNumber"
                        name="id_card_info.id_card_number"
                        type="text"
                        className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                        placeholder="身份证号码"
                        value={user.id_card_info.id_card_number}
                        onChange={handleInputChange}
                      />
                      <label htmlFor="idCardNumber" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">身份证号码</label>
                    </div>
                    <div className="relative">
                      <input
                        id="idCardHolder"
                        name="id_card_info.id_card_holder"
                        type="text"
                        className="peer placeholder-transparent h-10 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600"
                        placeholder="身份证持有人"
                        value={user.id_card_info.id_card_holder}
                        onChange={handleInputChange}
                      />
                      <label htmlFor="idCardHolder" className="absolute left-0 -top-3.5 text-gray-600 text-sm peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-440 peer-placeholder-shown:top-2 transition-all peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm">身份证持有人</label>
                    </div>
                    <div className="relative">
                      <label className="inline-flex items-center">
                        <input
                          type="checkbox"
                          name="id_card_info.is_real_name"
                          className="form-checkbox h-5 w-5 text-rose-600"
                          checked={user.id_card_info.is_real_name}
                          onChange={handleInputChange}
                        />
                        <span className="ml-2 text-gray-700">是否实名认证</span>
                      </label>
                    </div>
                    <button type="submit" className="bg-blue-500 text-white rounded-md px-2 py-1 disabled:opacity-50" disabled={isLoading}>
                      {isLoading ? '更新中...' : '更新身份证信息'}
                    </button>
                  </form>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


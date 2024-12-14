import Link from 'next/link'

export default function SettingsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <h1 className="text-2xl font-semibold mb-6">个人设置</h1>
            <div className="flex space-x-4 mb-6">
              <Link href="/settings" className="px-4 py-2 rounded bg-blue-500 text-white">
                基本设置
              </Link>
              <Link href="/settings/platform" className="px-4 py-2 rounded bg-blue-500 text-white">
                平台信息
              </Link>
              <Link href="/settings/idcard" className="px-4 py-2 rounded bg-blue-500 text-white">
                身份证设置
              </Link>
            </div>
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}


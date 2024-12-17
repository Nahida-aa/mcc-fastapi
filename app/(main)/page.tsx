import { HomeHeader } from '@/components/layout/header/home-header'
import React from 'react'
import { server_auth } from '../(auth)/auth';
import { cookies } from 'next/headers';

export default async function AA() {
  const [session, cookieStore] = await Promise.all([server_auth(), cookies()]);
  return (
    <main >
      <HomeHeader user={session?.user} />
      <div className='px-2'>AA</div>
    </main>
  )
}

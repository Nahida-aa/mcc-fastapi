import { HomeHeader } from '@/components/layout/header/home-header'
import React from 'react'
import { server_auth } from '../(auth)/auth';
import { cookies } from 'next/headers';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default async function AA() {
  const [session, cookieStore] = await Promise.all([server_auth(), cookies()]);
  return (
    <main >
      <HomeHeader user={session?.user} />
      <Link href={"/api/py/docs"} className='px-3'>
        <Button>
          去 api 交互文档
        </Button>
      </Link>
    </main>
  )
}

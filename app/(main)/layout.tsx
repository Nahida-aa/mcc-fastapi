import { cookies } from 'next/headers';

import { AppSidebar } from '@/components/app-sidebar';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';

import { server_auth } from '../(auth)/auth';

// export const experimental_ppr = true; // next

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [session, cookieStore] = await Promise.all([server_auth(), cookies()]);
  console.log(`app/(main)/layout.tsx: Layout: session.user: ${JSON.stringify(session?.user)}`);
  const isCollapsed = cookieStore.get('sidebar:state')?.value !== 'true';

  return (
    <SidebarProvider defaultOpen={!isCollapsed} className='h-screen SidebarProvider  '> 
    {/* 模糊背景 */}
      <AppSidebar user={session?.user} />
      <SidebarInset className='h-screen bg-opacity'>{children}</SidebarInset>
    </SidebarProvider>
  );
}

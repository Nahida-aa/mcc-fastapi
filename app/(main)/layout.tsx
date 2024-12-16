// import { cookies } from 'next/headers';

// import { AppSidebar } from '@/components/app-sidebar';
// import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';

// import { auth } from '../(auth)/auth';

// export const experimental_ppr = true;

// export default async function Layout({
//   children,
// }: {
//   children: React.ReactNode;
// }) {
//   const [session, cookieStore] = await Promise.all([auth(), cookies()]);
//   const isCollapsed = cookieStore.get('sidebar:state')?.value !== 'true';

//   return (
//     <SidebarProvider defaultOpen={!isCollapsed} className='h-screen SidebarProvider'>
//       <AppSidebar user={session?.user} />
//       <SidebarInset className='h-screen'>{children}</SidebarInset>
//     </SidebarProvider>
//   );
// }

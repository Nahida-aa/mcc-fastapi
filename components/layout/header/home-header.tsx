'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useWindowSize } from 'usehooks-ts';

// import { ModelSelector } from '@/components/model-selector';
import { SidebarToggle } from '@/components/layout/sidebar/sidebar-toggle';
import { Button } from '@/components/ui/button';
import { BetterTooltip } from '@/components/ui/tooltip';
import { PlusIcon, VercelIcon } from '@/components/icons';
import { useSidebar } from '@/components/ui/sidebar';
import { UserSidebarToggle } from '../sidebar/user-side-toggle';
import { ModeToggle } from '@/components/common/ModeToggle';

export function HomeHeader(
  { user }: { user: UserMeta | undefined }
  // { selectedModelId }: { selectedModelId: string }
) {
  const router = useRouter();
  const { open } = useSidebar();

  const { width: windowWidth } = useWindowSize();
  // const displayUser = user || { email: 'guest@example.com', name: 'Guest', image: null };
  const displayUser = user
  // const user_status = "online" // online, offline, away, 未登录
  let user_status
  if (user) {
    user_status = "online"
  } else {
    user_status = "未登录"
  }
  return (
    <header className="flex sticky  py-1.5 items-center px-2 md:px-2 gap-2 justify-between">
      <div className='flex gap-2 items-center'>
        <UserSidebarToggle user={user} status={user_status} />
        <div>
          <div className="text-xs font-medium">{user?.nickname || user?.name || "Guest"}</div>
          <div className='text-xs text-gray-400'>{user_status}</div>
        </div>
      </div>

      {/* <ModelSelector
        selectedModelId={selectedModelId}
        className="order-1 md:order-2"
      /> */}
      <div className='space-x-1'>
        <ModeToggle />
        {(!open || windowWidth < 768) && (
        <BetterTooltip content="New Server">
          <Button
            variant="outline"
            className="order-2 md:order-1 md:px-2 px-2 ml-auto md:ml-0 size-10 "
            onClick={() => {
              router.push('/');
              router.refresh();
            }}
          >
            <PlusIcon />
            <span className="md:sr-only">New Server</span>
          </Button>
        </BetterTooltip>
      )}
      </div>
    </header>
  );
}

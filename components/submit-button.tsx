'use client';

import { useFormStatus } from 'react-dom';

import { LoaderIcon } from '@/components/icons';

import { Button } from './ui/button';

export function SubmitButton({
  children,
  isLoading,
}: {
  children: React.ReactNode;
  isLoading: boolean;
}) {
  const { pending } = useFormStatus();

  console.log(`pending: ${pending}, isLoading: ${isLoading}`);
  return (
    <Button
      type={pending ? 'button' : 'submit'}
      aria-disabled={pending || isLoading}
      disabled={pending || isLoading}
      className="relative"
    >
      {children}

      {(pending || isLoading) && (
        <span className="animate-spin absolute right-4">
          <LoaderIcon />
        </span>
      )}

      <output aria-live="polite" className="sr-only">
        {pending || isLoading ? 'Loading' : 'Submit form'}
      </output>
    </Button>
  );
}

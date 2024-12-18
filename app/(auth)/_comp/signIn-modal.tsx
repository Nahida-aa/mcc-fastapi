"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { SubmitButton } from "@/components/submit-button";
import {  server_sign_in } from "../actions";
import { useRouter } from "next/navigation";
// import { signIn } from "../auth";

export const sign_in_schema = z.object({
  name: z.string().min(1, "Name is required"),
  password: z.string().min(6, "Password must be at least 6 characters"),
})
export function AignIn_Modal() {
  // const [isMounted, setIsMounted] = useState(false) // 13 版本的 React 有 bug，需要这样处理
  // useEffect(() => {
  //   setIsMounted(true)
  // }, [])

  const router = useRouter();
  
  const form = useForm({
    resolver: zodResolver(sign_in_schema),
    defaultValues: {
      name: '',
      password: '',
    }
  })

  const isLoading = form.formState.isSubmitting
  console.log(`isLoading: ${isLoading}`)
  // const [isSuccessful, setIsSuccessful] = useState(false);

  const onSubmit = async (values: z.infer<typeof sign_in_schema>) => {
    try {
      console.log(`app/(auth)/_comp/signIn-modal.tsx: 开始登录: ${JSON.stringify(values)}`)
      const result = await server_sign_in(values)
      console.log(`app/(auth)/_comp/signIn-modal.tsx: 登录成功: ${JSON.stringify(values)}`)
      router.push('/')
    } catch (error) {
      console.error(error)
    }
  }

  // if (!isMounted) return null // 13 版本的 React 有 bug，需要这样处理
  return (
    <Dialog open>
      <DialogContent 
        className="flex flex-col gap-4 px-4 sm:px-16"
      >
        <DialogHeader>
          <DialogTitle className="text-center">Sign In</DialogTitle>
          <DialogDescription className="text-center">
            Sign in to your account to continue
          </DialogDescription>
        </DialogHeader>
        <Form {...form} >
          <form action="" onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <div className="space-y-4">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel htmlFor="name">Name</FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        id="name"
                        type="text"
                        placeholder="Enter name"
                        required
                        className="bg-muted"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage {...field} />
                  </FormItem>
                )}
              />
              <FormField 
                name="password"
                control={form.control}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel htmlFor="password">Password</FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        id="password"
                        type="password"
                        placeholder="Enter password"
                        required
                        className="bg-muted"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage {...field} />
                  </FormItem>
                )}
              />
            </div>
            <DialogFooter>
              <SubmitButton isLoading={isLoading}> Sign in</SubmitButton>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}

'use server';
import { headers as nextHeaders } from "next/headers"
import { cookies } from 'next/headers'
import { z } from 'zod';

// import { createUser, getUser } from '@/lib/db/queries';

import { createActionURL } from './auth';
import { sign_in_schema } from './_comp/signIn-modal';

const authFormSchema = z.object({
  name: z.string().min(1),
  password: z.string().min(6),
});


export const server_sign_in = async (values: z.infer<typeof sign_in_schema>) => {
  try {
    console.log(`app/(auth)/actions.ts::sign_in 开始登录: `)
    console.log(JSON.stringify(values))
    const headers = new Headers(await nextHeaders())
    const signInURL = createActionURL(
        "signin",
        // @ts-expect-error `x-forwarded-proto` is not nullable, next.js sets it by default
        headers.get("x-forwarded-proto"),
        headers,
        // process.env,
        {basePath: "api/py/auth"}
      )
    // headers.set("Content-Type", "application/x-www-form-urlencoded")
    const snHeaders = { "Content-Type": "application/x-www-form-urlencoded" }
    const body = new URLSearchParams(values)
    // headers.set("Content-Type", "application/json")
    // const body = JSON.stringify(values)
    const resp = await fetch(signInURL,
      {
        method: "POST",
        headers: snHeaders,
        // headers: {
        //   "Content-Type": "application/json",
        // },
        body: body,
      }
    );
    if (resp.ok) {
      const data = await resp.json();
      console.log(`app/(auth)/actions.ts::sign_in 登录成功: ${data}`);

      // 设置 cookies
      const cookieStore = cookies();
      cookieStore.set('access_token', data.access_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        maxAge: 60 * 60, // 1 hour
      });
      cookieStore.set('refresh_token', data.refresh_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        maxAge: 60 * 60 * 24 * 30, // 30 days
      });
      return { 
        access_token: data.access_token, 
        token_type: data.token_type,
        user: data.user }
      // 处理登录成功逻辑
    } else {
      const errorText = await resp.text();
      console.error(`app/(auth)/actions.ts::sign_in 登录失败: ${errorText}`);
    }
    // await signIn('py', {
    //   email: values.name,
    //   password: values.password,
    //   redirectTo: "/",
    //   // redirect: false,
    // },{
    // },{
    //   // basePath: "api/py/auth",
    //   basePath: "api/py",
    // });
  } catch (error) {
    console.error(`app/(auth)/actions.ts::sign_in 登录失败: ${error}`)
  }
}

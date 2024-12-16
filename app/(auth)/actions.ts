// 'use server';

// import { z } from 'zod';

// // import { createUser, getUser } from '@/lib/db/queries';

// import { signIn } from './auth';
// import { sign_in_schema } from './_comp/signIn-modal';

// const authFormSchema = z.object({
//   name: z.string().min(1),
//   password: z.string().min(6),
// });


// export const sign_in = async (values: z.infer<typeof sign_in_schema>) => {
//   try {
//   console.log(`app/(auth)/actions.ts::sign_in 开始登录: `)
//   console.log(JSON.stringify(values))
//   await signIn('py', {
//     email: values.name,
//     password: values.password,
//     redirectTo: "/",
//     // redirect: false,
//   },{
//   },{
//     basePath: "api/py/auth",
//   });
//   console.log(`app/(auth)/actions.ts::sign_in 登录成功: `)
//   } catch (error) {
//     console.error(`app/(auth)/actions.ts::sign_in 登录失败: ${error}`)
//   }
// }


// export interface LoginActionState {
//   status: 'idle' | 'in_progress' | 'success' | 'failed' | 'invalid_data';
// }
// export const login = async (
//   _: LoginActionState,
//   formData: FormData,
// ): Promise<LoginActionState> => {
//   try {
//     const validatedData = authFormSchema.parse({
//       name: formData.get('name'),
//       password: formData.get('password'),
//     });

//     await signIn('mcc', {
//       email: validatedData.name,
//       password: validatedData.password,
//       redirectTo: "/",
//       // redirect: false,
//     });

//     return { status: 'success' };
//   } catch (error) {
//     if (error instanceof z.ZodError) {
//       return { status: 'invalid_data' };
//     }

//     return { status: 'failed' };
//   }
// };

// export interface RegisterActionState {
//   status:
//     | 'idle'
//     | 'in_progress'
//     | 'success'
//     | 'failed'
//     | 'user_exists'
//     | 'invalid_data';
// }

// // export const register = async (
// //   _: RegisterActionState,
// //   formData: FormData,
// // ): Promise<RegisterActionState> => {
// //   try {
// //     const validatedData = authFormSchema.parse({
// //       email: formData.get('email'),
// //       password: formData.get('password'),
// //     });
// //     // 
// //     console.log(`app/(auth)/actions.ts: 开始检测用户是否存在`)
// //     const [user] = await getUser(validatedData.email);
// //     if (user) {
// //       return { status: 'user_exists' } as RegisterActionState;
// //     }
// //     await createUser(validatedData.email, validatedData.password);
// //     await signIn('credentials', {
// //       email: validatedData.email,
// //       password: validatedData.password,
// //       redirect: false,
// //     });

// //     return { status: 'success' };
// //   } catch (error) {
// //     if (error instanceof z.ZodError) {
// //       return { status: 'invalid_data' };
// //     }

// //     return { status: 'failed' };
// //   }
// // };

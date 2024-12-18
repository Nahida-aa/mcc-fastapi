import type { Metadata } from "next";
import "./globals.css";
import { ThemeProvider } from '@/components/providers/theme-provider';
// import AuthProvider from './components/AuthProvider'

export async function generateMetadata() {

  return {
    title: "mcc",
    description: "description",
    keywords: "keywords",
    // manifest: "/api/manifest",
    manifest: "/manifest.json",
    icons: {
      icon: "/favicon.ico",
      shortcut: "/icons/api-192-round.png",
      apple: "/icons/api-192-round.png",
    },
    other: { "baidu-site-verification": process.env.BaiduSiteVerify || "" },
  } satisfies Metadata;
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body 
      className={`antialiased`}
      suppressHydrationWarning
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem={false}
          disableTransitionOnChange
        >
          {/* <AuthProvider> */}
            {children}
          {/* </AuthProvider> */}
        </ThemeProvider>
      </body>
    </html>
  );
}

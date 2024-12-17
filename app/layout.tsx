import "./globals.css";
import localFont from "next/font/local";
import { ThemeProvider } from '@/components/providers/theme-provider';
// import AuthProvider from './components/AuthProvider'
const xiaolaiSans = localFont({
  src: "../public/fonts/XiaolaiMonoSC-Regular.ttf",
  variable: "--font-xiaolai-sans",
  weight: "100 900",
});
const xiaolaiMono = localFont({
  src: "../public/fonts/XiaolaiMonoSC-Regular.ttf",
  variable: "--font-xiaolai-mono",
  weight: "100 900",
});

export const metadata = {
  title: "mcc",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body 
      className={`${xiaolaiSans.variable} ${xiaolaiMono.variable} antialiased`}
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

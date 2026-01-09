import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Allow public routes
  const publicRoutes = ["/auth", "/api", "/mystery-skills-auth.html", "/mystery-skills-flash.html"]
  if (publicRoutes.some((route) => pathname.startsWith(route))) {
    return NextResponse.next()
  }

  // Redirect root to Flash UI page
  if (pathname === "/") {
    return NextResponse.redirect(new URL("/mystery-skills-flash.html", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
}

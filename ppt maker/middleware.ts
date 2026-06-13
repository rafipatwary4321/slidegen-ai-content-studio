import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: { signIn: "/auth/signin" }
});

export const config = {
  matcher: ["/dashboard/history/:path*", "/dashboard/presentations/:path*", "/dashboard/presentation/:path*"]
};
